from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
                                  ,accept_downloads = True
                                #   ,viewport={"width": 1200, "height": 100}  # set viewport size
                                  )
    page = context.new_page()
    page.goto("https://ytmp3.la/")
    
    
    songs = [ ("https://www.youtube.com/watch?v=VG3JsmOmDqw&pp=ygUsY2FudCBob2xkIHVzIG1hY2tlbG1vcmUgYW5kIHJ5YW4gbGV3aXMgYXVkaW8%3D" , "booby") ,
              ("https://www.youtube.com/watch?v=MV_3Dpw-BRY&pp=ygUSbmlnaHRjYWxsIGthdmluc2t5" , "kavinsky") ,
              ("https://www.youtube.com/watch?v=-DSVDcw6iW8&pp=ygULYSByZWFsIGhlcm8%3D", "realhero")
             ]
    
    for song in songs: 
    
        page.locator("input#v").fill( song[0] )            
        page.locator("button[type='submit']").click()        
        page.wait_for_function(" document.querySelectorAll('button').length == 3 ") # make sure we have 3 buttons before we select based on button order
        
        
        page.evaluate("""
    () => {
        window.open = function(url, target, features) {
            console.log('hi');
        };
    }
    """)
        
        with page.expect_download() as download_info:
            page.query_selector("button").click()
        print("outside:)")
        print( download_info.value, download_info.value.save_as(f"results/{song[1]}.mp3") )
        
        
        page.get_by_text("Next").click()
        
    page.wait_for_timeout(1000000)
    
    browser.close()
    
    
    
    
    
    
# document.querySelectorAll("[data-testid='tracklist-row']")