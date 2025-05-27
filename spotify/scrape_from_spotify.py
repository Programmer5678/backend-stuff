from playwright.sync_api import sync_playwright, expect
import time


from dotenv import load_dotenv
import os

def get_session_cookie():
    load_dotenv()
    return os.getenv("SPOTIFY_SESSION")


def scrape_from_spotify():
    
    # playlist_length = 754
    # playlist_length = 50
    playlist_link = "https://open.spotify.com/playlist/2UZk7JjJnbTut1w8fqs3JL"
    
    res = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False,
                                    args=[
        "--disable-background-networking",
        "--disable-background-timer-throttling",
        "--disable-backgrounding-occluded-windows",
        "--disable-client-side-phishing-detection",
        "--disable-default-apps",
        "--disable-popup-blocking"
    ])
        context = browser.new_context(user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
                                    #   ,viewport={"width": 1200, "height": 100}  # set viewport size
                                    )
        context.add_cookies([{
            "name" : "sp_dc",
            "value" : get_session_cookie(),
            "url" : "https://open.spotify.com"
        }]) #add the session cookie so that no login required
        
        
        
        page = context.new_page()
        
        page.goto(playlist_link) # goto the playlist!
        
        # page.wait_for_timeout(10000000)
        # page.locator("[data-testid='playlist-page'] >:nth-child(1) >:nth-child(1) >:nth-child(2) >:nth-child(4) ").evaluate("el => el.style.backgroundColor = 'orange' ")
        

        playlist_length = page.wait_for_function(
    r"""() => {
        const q = document.querySelector("[data-testid='playlist-page'] >:nth-child(1) ");
        
        if (!q) return false;

        const descendants = q.querySelectorAll("*");
        for (let i = 0; i < descendants.length; i++) {
            const text = descendants[i].innerText;
            if (/^\d+\s*songs$/.test(text)) {
                return parseInt(text);
            }
        }

        return false;
    }""").json_value()
        
        print(playlist_length)
                
        page.wait_for_selector("[data-testid='playlist-tracklist'] [aria-rowindex='2'] [data-encore-id='text']", timeout=10000 ) # wait for the the first text element to load        
        
        print( page.query_selector("[data-testid='playlist-tracklist'] [aria-rowindex='2'] [data-encore-id='text']").inner_text() )
        
        els = page.locator("[data-overlayscrollbars-viewport]")
        expect(els).to_have_count(3)
        scrollableEl = els.nth(1)  # this element is used to scorll down to view more songs
    
        firstRowYPos = page.locator(f"[data-testid='playlist-tracklist'] [aria-rowindex='1']").evaluate("el => el.getBoundingClientRect().top") #title row "ttitle , writer etc."
        elNearTopYPos = page.locator(".gj5VcIUC9oD2p4BsxzGE").evaluate("el => el.getBoundingClientRect().top")  # this is a header near the top of the scrollable element , so scroll the diff
        scrollableEl.evaluate(f"el => el.scrollBy(0, {firstRowYPos - elNearTopYPos} )") # scroll down based on the difference between the header and first row so first row will 
        #be apporx near the beggining of view. we doing this since after this first scroll-down the firstRowYPos is fixed and can be used as an anchor.
        
        
        # print( page.query_selector("[data-testid='playlist-tracklist'] [aria-rowindex='2'] [data-encore-id='text']").inner_text(),
        #        len(page.query_selector_all("[data-testid='playlist-tracklist'] [aria-rowindex='2'] [data-encore-id='text']") ))
        
        # print( page.query_selector("[data-testid='playlist-tracklist'] [aria-rowindex='8'] [href^='/track']").inner_text() )
        # print( page.query_selector("[data-testid='playlist-tracklist'] [aria-rowindex='8'] [href^='/artist/']").inner_text() )
            
        page.wait_for_function(f"""() => 
            document.querySelector("[data-testid='playlist-tracklist'] [aria-rowindex='{2}'] [href^='/track/']").innerText.length > 0 &&
            document.querySelector("[data-testid='playlist-tracklist'] [aria-rowindex='{2}'] [href^='/artist/']").innerText.length > 0
            """)
        
        
        for i in range(2, playlist_length + 2): #loop through indecies corresponding to all rows
            
            
            repeating_s = f"""() => 
            document.querySelector("[data-testid='playlist-tracklist'] [aria-rowindex='{i}'] [href^='/track/']")?.innerText?.length > 0 &&
            document.querySelector("[data-testid='playlist-tracklist'] [aria-rowindex='{i}'] [href^='/artist/']")?.innerText?.length > 0
            """
            
            rowExists = page.evaluate( repeating_s )
            # print("exists ? " , rowExists)

            if not rowExists : #make sure row contains 10 data-encore-id elements(text eleemtns like name songwriter etc. 
                # so row is full) also make sure len(l) != 0 which means we need to load the entire row. so we scroll down to make sure it loads + wait for function 
                
                lastLoadedRowYPos = page.query_selector(f"[data-testid='playlist-tracklist'] [aria-rowindex='{i-1}']").evaluate("el => el.getBoundingClientRect().top") 
                
                print(firstRowYPos, lastLoadedRowYPos, i-1 )
                scrollableEl.evaluate(f"el => el.scrollBy(0, {lastLoadedRowYPos - firstRowYPos})")   # scroll down based on difference between first row and last laoded row
                #so last loaded row will appear near the top   
      
                
                page.wait_for_function(repeating_s)
                print( "here" )
                #wait till the desired row is fully loaded(including all text elements!)
                
                # page.wait_for_selector(f"xpath=(//*[@data-testid='playlist-tracklist']//*[@aria-rowindex='{i}']//*[@data-encore-id='text'])[8]", timeout=1000000 )
            
            res.append( ( page.query_selector(f"[data-testid='playlist-tracklist'] [aria-rowindex='{i}'] [href^='/track/']").inner_text() , 
            page.query_selector(f"[data-testid='playlist-tracklist'] [aria-rowindex='{i}'] [href^='/artist/']").inner_text() ) )
                        
            print( page.query_selector(f"[data-testid='playlist-tracklist'] [aria-rowindex='{i}'] [href^='/track/']").inner_text() , 
            page.query_selector(f"[data-testid='playlist-tracklist'] [aria-rowindex='{i}'] [href^='/artist/']").inner_text() ) 
    
        # print("HERE :)")
                
        # page.wait_for_timeout(1000000)
        
        browser.close()
     
    return res   
    # document.querySelectorAll("[data-testid='tracklist-row']")
    
