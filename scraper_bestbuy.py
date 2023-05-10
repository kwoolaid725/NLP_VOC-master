import pandas as pd
from requests_html import HTMLSession
import json, os
from bs4 import BeautifulSoup


# HTMLSession for status from 403 to 200
s = HTMLSession()
url = 'https://www.bestbuy.com/site/reviews/dyson-v15-detect-cordless-vacuum-yellow-nickel/6451330?variant=A&skuId=6451330' \
      '&page='
product_name='Dyson V15 Detect'
# json = soup.find_all('script', type='application/ld+json')

def getdata(url):
    r = s.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup


soup = getdata(url)

count = 1
results =[]
while True:
    soup = getdata(url + str(count))
    page = soup.find('ul', {'class': 'pagination ugc body-copy-lg'})
    lastPage = page.find('li', {'class': 'page next disabled'})
    reviews = soup.select('.review-item')

    for review in reviews:
        data = review.find('script', type='application/ld+json')
        x = json.loads(data.string)
        rating = (x['reviewRating']['ratingValue'])
        date = review.find('time')['title']
        author = (x['author']['name'])
        title = (x['name'])
        body = (x['reviewBody'])

        result = {
            'RETAILER': 'bestbuy',
            'PRODUCT': product_name,
            'RATING': rating,
            'POST_DATE': date,
            'REVIEWER_NAME': author,
            'TITLE': title,
            'CONTENT': body
        }
        results.append(result)
        print('Page: '+ str(count))
        print(len(results))
    if not lastPage:
        count = count + 1
    else:
        break

df = pd.DataFrame(results)


# df.to_csv(f'E:/2022\Database_and_Programming\Web Scraping and Sentiment Analysis\Raw Data\{product_name}.csv', mode='a',
#           index=False, header=not os.path.exists(f'E:/2022\Database_and_Programming\Web Scraping and Sentiment Analysis\Raw Data\{product_name}.csv'),
#           encoding='utf-8-sig')
df.to_csv('C:/Users/aiden2.kim/Desktop/Python-Projects/NLP_VOC-master/raw data/CordlessVacs_5.10.23.csv', index=False, encoding='utf-8-sig',
          mode='a', header=not os.path.exists('C:/Users/aiden2.kim/Desktop/Python-Projects/NLP_VOC-master/raw data/CordlessVacs_5.10.23.csv'))

#** later figure out how to change author type to string






