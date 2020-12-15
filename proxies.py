def get_proxies():
    """
    *** only need to run check_proxies() ***
    Script to obtain list of proxies, obtained from
    https://medium.com/datadriveninvestor/how-to-not-get-caught-while-web-scraping-88097b383ab8
    Returns a list of proxies
    """

    from bs4 import BeautifulSoup as soup
    import requests

    proxy_web_site = 'https://free-proxy-list.net/'
    response = requests.get(proxy_web_site)
    page_html = response.text
    page_soup = soup(page_html, "html.parser")
    containers = page_soup.find_all("div", {"class": "table-responsive"})[0]
    ip_index = [8*k for k in range(80)]
    proxies = set()

    for i in ip_index:
        ip = containers.find_all("td")[i].text
        port = containers.find_all("td")[i+1].text
        https = containers.find_all("td")[i+6].text
        print("\nip address : {}".format(ip))
        print("port : {}".format(port))
        print("https : {}".format(https))
    
        if https == 'yes':
            proxy = ip + ':' + port
            proxies.add(proxy)
                
    return proxies

def check_proxies():
    """
    Works in tandem with get_proxies() to check for working proxies; 
    Script to obtain list of proxies, obtained from
    https://medium.com/datadriveninvestor/how-to-not-get-caught-while-web-scraping-88097b383ab8
    Returns a list of verified proxies
    """
    working_proxies = set()
    proxy_list = get_proxies()            
    test_url = 'https://httpbin.org/ip'    
    for i in proxy_list:
        print("\nTrying to connect with proxy: {}".format(i))
        try:
            response = requests.get(test_url, proxies_list={"http": i, "https": i}, timeout = 5)
            print(response.json())
            print("This proxy is added to the list. Have a lovely day!")
            working_proxies.add(i)
            
        except:
            print("Skipping. Connnection error")

    return working_proxies