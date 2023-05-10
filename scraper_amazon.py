import time, os
import re
import pandas as pd
import regex
import requests
from bs4 import BeautifulSoup


HEADERS = ({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
    'Accept-Language': 'en-US, en;q=0.5'
})


# 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
# "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"



def getdata(url):
    payload = {'api_key': '0a53d12b168b28c41638451a545f7495', 'url': url, 'keep_headers': 'true'}

    for i in range(5):
        r = requests.get('http://api.scraperapi.com', params=payload, headers=HEADERS, timeout=60)
        print("status code received:", r.status_code)
        if r.status_code != 200:
            # saving response to file for debugging purpose.
            continue
        else:
            soup = BeautifulSoup(r.text, 'html.parser')
            return soup



results = []

url = 'https://www.amazon.com/Dyson-Detect-Cordless-Vacuum-Yellow/product-reviews/B0979R48CX/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews'
product_name = 'Dyson V15 Detect'
def get_reviews(soup):
    # reviews = soup.find_all('div', {'data-hook': 'review'})

    regex = re.compile('.*customer_review-.*')
    for review in soup.find_all('div', {'id': regex}):
        result = {
        'RETAILER': 'amazon',
        'PRODUCT': product_name,
        'RATING': round(float(review.find('i', {'data-hook': 'review-star-rating'}).text.replace('out of 5 stars', '').strip())),
        'POST_DATE': review.find('span', {'data-hook': 'review-date'}).text.replace('Reviewed in the United States on', '').strip(),
        'REVIEWER_NAME': review.find('div', {'class': 'a-profile-content'}).text.strip(),
        'TITLE': review.find('a', {'data-hook': 'review-title'}).text.strip(),
        'CONTENT': review.find('span', {'data-hook': 'review-body'}).text.strip(),
        # 'SIZE_STYLE': review.find('a', {'data-hook': 'format-strip'}).text.replace('Style:', ' / Style:').strip()

        }
        # print(result)
        results.append(result)


for x in range(1, 999):
    soup = getdata(f'{url}&pageNumber={x}')
    print(f'Page: {x}')
    get_reviews(soup)
    print(len(results))

    if not soup.find('li', {'class': 'a-disabled a-last'}):
        pass
    else:
        break

df = pd.DataFrame(results)
df.to_csv('C:/Users/aiden2.kim/Desktop/Python-Projects/NLP_VOC-master/raw data/CordlessVacs_5.10.23.csv', index=False, encoding='utf-8-sig',
          mode='a', header=not os.path.exists('C:/Users/aiden2.kim/Desktop/Python-Projects/NLP_VOC-master/raw data/CordlessVacs_5.10.23.csv'))


# df.to_excel('amazon_reviews.xlsx', index=False)




