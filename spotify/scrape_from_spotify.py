from playwright.sync_api import sync_playwright
import time

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
        "value" : "AQA9LquN2dRhvicfkQP88S6mQaktKzRIi2VYASS0TKaxOgACNNr6PUAFfaRRQ9YRAgkMLnK6u7PQbdwaz-2SXAdpJnhdHgqupZmRouC_nq-jo7NkHuGJpx54d9frpa3_AtITtNRqQMsMJnimRGqn7dNpsdInpu-J6t4ffKVjGPJVYeE-zh9mH8OnohjEa0tNpyZfKkiZu3Bgy3dqpC0",
        "url" : "https://open.spotify.com"
    }]) #add the session cookie so that no login required
    
    
    
    page = context.new_page()
    
    page.goto("https://open.spotify.com/playlist/05DJiTCdEHbGVCnxOOOtb3?si=OCKJL8jISQ2wuVxtskHwRA&pt=c4cd90515106fe0bd0a9be613f527c38&pi=lGtqPv1MRU20p") # goto the playlist!
    page.wait_for_selector("[data-testid='playlist-tracklist'] [aria-rowindex='2'] [data-encore-id='text']", timeout=10000 ) # wait for the the first text element to load
    
    # print( page.query_selector("[data-testid='playlist-tracklist'] [aria-rowindex='2'] [data-encore-id='text']").inner_text() )
    
    # el = page.query_selector(".main-view- [data-overlayscrollbars-viewport='scrollbarHidden overflowXHidden overflowYScroll']")
    # page.evaluate("document.querySelector('.) ")
    # page.query_selector("[data-testid='playlist-tracklist']").evaluate("el => el.style.backgroundColor = 'red' ")
    # page.query_selector("[data-testid='playlist-tracklist'] [aria-rowindex='2']").evaluate("el => el.style.backgroundColor = 'blue' ")
    
    # page.query_selector("[data-testid='playlist-tracklist']").evaluate("el => el.scrollBy(0, 50)")
    
    
    
    scrollableEl = page.query_selector_all("[data-overlayscrollbars-viewport]")[1]  # this element is used to scorll down to view more songs
    firstRowYPos = page.query_selector(f"[data-testid='playlist-tracklist'] [aria-rowindex='1']").evaluate("el => el.getBoundingClientRect().top") #title row "ttitle , writer etc."
    elNearTopYPos = page.query_selector(".gj5VcIUC9oD2p4BsxzGE").evaluate("el => el.getBoundingClientRect().top")  # this is a header near the top of the scrollable element , so scroll the diff
    scrollableEl.evaluate(f"el => el.scrollBy(0, {firstRowYPos - elNearTopYPos} )") # scroll down based on the difference between the header and first row so first row will 
    #be apporx near the beggining of view. we doing this since after this first scroll-down the firstRowYPos is fixed and can be used as an anchor.
    for i in range(2, 754 + 2): #loop through indecies corresponding to all rows
        desiredRow = page.query_selector_all(f"[data-testid='playlist-tracklist'] [aria-rowindex='{i}'] [data-encore-id='text']") #g

        if len(desiredRow) < 8: #make sure row contains 10 data-encore-id elements(text eleemtns like name songwriter etc. 
            # so row is full) also make sure len(l) != 0 which means we need to load the entire row. so we scroll down to make sure it loads + wait for function 
            
            # print("hi got fucked a little bit but no biggie")
            # r1 = page.query_selector(f"[data-testid='playlist-tracklist'] [aria-rowindex='1']").evaluate("el => el.getBoundingClientRect().top") 
            lastLoadedRowYPos = page.query_selector(f"[data-testid='playlist-tracklist'] [aria-rowindex='{i-1}']").evaluate("el => el.getBoundingClientRect().top") 
            
            print(firstRowYPos, lastLoadedRowYPos )
            scrollableEl.evaluate(f"el => el.scrollBy(0, {lastLoadedRowYPos - firstRowYPos})")   # scroll down based on difference between first row and last laoded row
            #so last loaded row will appear near the top   
            # print( page.query_selector(f"[data-testid='playlist-tracklist'] [aria-rowindex='1']").evaluate("el => el.getBoundingClientRect().top")   ,
            #        page.query_selector(f"[data-testid='playlist-tracklist'] [aria-rowindex='{i-1}']").evaluate("el => el.getBoundingClientRect().top")   )     
            
            # print(f"hopefully {i-1}th is around top...")
    #         page.query_selector_all("[data-overlayscrollbars-viewport]")[1].evaluate("el => el.scrollBy(0, 300)")
            # scrollableEl.evaluate("el => el.scrollBy(0, 250)")
            
            page.wait_for_function(
    f"""() => document.querySelectorAll("[data-testid='playlist-tracklist'] [aria-rowindex='{i}'] [data-encore-id='text']").length >= 8""")
            #wait till the desired row is fully loaded(including all text elements!)
            
            # page.wait_for_selector(f"xpath=(//*[@data-testid='playlist-tracklist']//*[@aria-rowindex='{i}']//*[@data-encore-id='text'])[8]", timeout=1000000 )
            desiredRow = page.query_selector_all(f"[data-testid='playlist-tracklist'] [aria-rowindex='{i}'] [data-encore-id='text']")
            #reset desiredRow. it was previously set before the if statement, but since there was a problem-row not fully loaded set again using same query
        
        print( "LINE: ", desiredRow[0].inner_text(), " and: ", desiredRow[1].inner_text(), desiredRow[3].inner_text()  )

        # do 4 times while there is no selector
        #     scroll
        #     wait 2 seconds
        
        # for iter in range(6):
            
        #     if iter == 5:
        #         raise Exception("FUCK")
            
        #    scrollableEl.evaluate("el => el.scrollBy(0, 250)") 
        #    if page.query_selector(f"xpath=(//*[@data-testid='playlist-tracklist']//*[@aria-rowindex='{i}']//*[@data-encore-id='text'])[8]") :
        #        break
           
            
        # if iter == 5:
        #     error
          
        
        
        
        
    
    # for e in page.query_selector_all("[data-testid='playlist-tracklist'] [aria-rowindex='2'] [data-encore-id='text']") :
    #     e.evaluate("el => el.style.backgroundColor = 'orange' ")
        # print( e.inner_text() )
    
    # page.evaluate("window.scroll({ top: 1000, left: 100, behavior: 'smooth', });")
    
    # print("here2")
    # print("found it!")
    # page.wait_for_timeout(10000)
    
    # page.query_selector("[data-testid='playlist-tracklist'] [aria-rowindex='1'] [data-encore-id='text']" )

    
    # for i in range(1, 755):  # aria-rowindex often starts at 1
    #     selector = f"[data-testid='playlist-tracklist'] [aria-rowindex='f{i}'] [data-encore-id='text']"
        
    #     for attempt in range(30):  # Try scrolling 30 times max
    #         if page.query_selector(selector):
    #             # print(f"Row {i} found")
    #             break
            
    #         page.evaluate("window.scrollBy(0, 300)")
    #         page.wait_for_timeout(300)
            
    #     print( page.query_selector(selector).inner_text() )
    
    
    
    
    print("HERE :)")
            
    page.wait_for_timeout(1000000)
    
    browser.close()
    
# document.querySelectorAll("[data-testid='tracklist-row']")