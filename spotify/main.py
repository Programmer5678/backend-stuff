from playwright.sync_api import sync_playwright

def names_to_link(names):
    
    res = []
    
    searches = map( lambda p : p[0] + " " + p[1] + " " + "audio" , names)
    print(searches)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
                                    #   ,viewport={"width": 1200, "height": 100}  # set viewport size
                                    )
        page = context.new_page()
        page.goto("https://youtube.com")
                
        prev_href = ""
        
        for search in searches:
        
            page.fill("input[name='search_query']", search )
            # page.click("button[title='search']", timeout=1000000)
            # page.click(".ytSearchboxComponentSearchButton", timeout=100000)
            # page.click("yt-searchbox[role='search'] button")
            
            s = "xpath=(//yt-searchbox[@role='search']//button)[2]"
            page.wait_for_selector(s)
            page.query_selector(s).click()
            
            s2 = "ytd-video-renderer a#thumbnail"
            # page.wait_for_timeout(10000)
            
            while True: 
                page.wait_for_selector(s2)
                if page.query_selector(s2).get_attribute('href') != prev_href:
                    break
                page.wait_for_timeout(1000)
            
            prev_href = page.query_selector(s2).get_attribute('href')
            res.append( ("https://youtube.com" + prev_href, search) )
            print( "https://youtube.com" + prev_href )
                    
        browser.close()
        
        
    return res
        
    # document.querySelectorAll("[data-testid='tracklist-row']")

