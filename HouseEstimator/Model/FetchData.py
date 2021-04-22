import re
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time



page = 250
while page < 500:
    df = pd.DataFrame(columns=['link', 'location', 'area', 'room', 'year', 'price'])
    page += 1
    r = requests.get('https://shabesh.com/search/خرید-فروش/آپارتمان/تهران/' + str(page))
    print(r)
    soup = BeautifulSoup(r.text, 'html.parser')
    elements = soup.find_all('div', attrs={'class': 'list_announceListMode__3NDlF'})
    for element in elements:
        try:
            link = element.find('a')
            link = 'https://shabesh.com'+link.get('href')
            price_loc_info = element.find_all('span', attrs={'class': 'list_infoItem__3FLZC'})
            price = price_loc_info[0].get_text(strip=True)
            price = re.sub(r'\,', '', price)
            price = int(re.findall(r'\d+', price)[0])
            location = price_loc_info[1].text
            location = re.sub(r'تهران', '', location)
            location = re.sub(r' ،', '', location)
            els = element.find('div', attrs={'class': 'list_infoItem__3FLZC'})
            els = els.text.split()
            area = els[0]
            room = re.sub(r'متر', '', els[1])
            year = re.sub(r'خواب', '', els[2])
            row_data = {'link': link, 'location': location, 'area': area, 'room': room, 'year': year, 'price': price}
            print(row_data)
            df = df.append(row_data, ignore_index=True)
        except:
            pass
    print(page)
    if page % 10 == 0:
        time.sleep(60)
    df.to_csv('Data.csv', mode='a', header=False,index=False)