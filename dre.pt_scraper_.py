import requests
from bs4 import BeautifulSoup
import pandas as pd
import re



def item_dict (a_listing):
    listing_dict = {}
    
    listing_dict['Url'] = a_listing.a['href']
    listing_dict['Title'] = a_listing.a.text.strip()

    author= a_listing.find('div',{"class":"author"})
    listing_dict['Author'] = author.text.strip()

    summary= a_listing.find('div',{"class":"summary"})
    listing_dict['Summary'] = summary.text.strip()
    
    return listing_dict




headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Referer': 'https://dre.pt/web/guest/home/-/dre/calendar/normal/II',
    'Accept-Language': 'en-US,en;q=0.9',
}


master_listing = []

for i in range(1,5):
    #print('Getting page' + str(i))

    params = (
        
        ('serie', 'II^'),
        ('at', 'c^'),
        ('parte_filter', '41'),
        ('number', str(i)),
    )

    response = requests.get('https://dre.pt/web/guest/home/-/dre/144452178/details/maximized', headers=headers, params=params )


    # response = requests.get('https://dre.pt/web/guest/home/-/dre/144452178/details/maximized?serie=II^&at=c^&parte_filter=41', headers=headers, cookies=cookies)

    html = response.text
    soup = BeautifulSoup(html,'html.parser')


    listing = soup.find_all("ul")[6]
    post = listing.find_all("li")


    for a_listing in post:
        post = item_dict(a_listing)
        master_listing.append(post)


#output dataframe-csv

df = pd.DataFrame(master_listing)
df.to_csv('dre_final_trial.csv',index = False)

