import pandas as pd
from requests_html import HTMLSession
import time
import json, os
from bs4 import BeautifulSoup


# HTMLSession for status from 403 to 200
s = HTMLSession()
url = 'https://www.homedepot.com/p/reviews/LG-CordZero-All-in-One-Cordless-Stick-Vacuum-Cleaner-A939KBGS/319148737/'
product_name='LG A939KBGS'


def getdata(url):
    r = s.get(url)
    time.sleep(1)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup


soup = getdata(url)
count = 1

post_dates = []
results = []

while True:
    soup = getdata(url + str(count))
    data = soup.find_all('div', {'class': 'review_item'})
    for da in data:
        author = da.select_one('div > div >  div:nth-child(2) > div > div > div.review-content__no-padding.col__12-12 > button').text
        title = da.select_one('div > div > div:nth-child(2) > div > div > span').text
        date = da.select_one('div > div > div > div > span').text

        date_result = {
            'REVIEWER_NAME': author,
            'TITLE': title,
            'POST_DATE': date
        }
        post_dates.append(date_result)

    json_data = [
        json.loads(x.string) for x in soup.find_all('script',type='application/ld+json')
    ]
    reviews = json_data[0]['review']
    for review in reviews:
        rating = (review['reviewRating']['ratingValue'])
        author = (review['author']['name'])
        title = (review['headline'])
        body = (review['reviewBody'])

        result = {
            'RETAILER': 'homedepot',
            'PRODUCT': product_name,
            'RATING': rating,
            'REVIEWER_NAME': author,
            'TITLE': title,
            'CONTENT': body
        }

        results.append(result)
    if data:
        count = count + 1
        print(count)
    else:
        break

pd.set_option('display.max_columns', None)
df1 = pd.DataFrame(post_dates)
df2 = pd.DataFrame(results)   #Use for Star Rating Counts

# Dropping Unnecessary Rows
df_with_reviews = df2[~df2.CONTENT.str.contains('Rating provided by a verified purchaser', na=False)]
df_with_reviews.dropna(subset = ['CONTENT'], inplace=True)

df = df_with_reviews.merge(df1, how='inner', on=['REVIEWER_NAME','TITLE'])
column_move = df.pop('POST_DATE')
df.insert(3,'POST_DATE', column_move)

df_rating = df2['RATING']

# df.to_csv(f'E:/2022\Database_and_Programming\Web Scraping and Sentiment Analysis\Raw Data/{product_name}.csv', mode='a',
#           index=False, header=not os.path.exists(f'E:/2022\Database_and_Programming\Web Scraping and Sentiment Analysis\Raw Data/{product_name}.csv'), encoding='utf-8-sig')
df_rating.to_csv(f'C:/Users/aiden2.kim/Desktop/Python-Projects/NLP_VOC-master/raw data/{product_name}_Ratings.csv', encoding='utf-8-sig')

df.to_csv('C:/Users/aiden2.kim/Desktop/Python-Projects/NLP_VOC-master/raw data/CordlessVacs_5.10.23.csv', index=False, encoding='utf-8-sig',
          mode='a', header=not os.path.exists('C:/Users/aiden2.kim/Desktop/Python-Projects/NLP_VOC-master/raw data/CordlessVacs_5.10.23.csv'))