

import requests
from bs4 import BeautifulSoup
import re
import json
import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

# convert parameter to url in order to search the first page.
def make_url_query(makes="",model="",mileage="",transmission=""
                   ,year_min="",year_max="",body_style="",cylinder=""):
    makes=str(makes).lower()
    model=str(model).lower()
    mileage=str(mileage).lower()
    transmission=str(transmission).lower()
    year_min=str(year_min).lower()
    year_max=str(year_max).lower()
    body_style=str(body_style).lower()
    cylinder=str(cylinder).lower()
    homepage = "https://www.cars.com/shopping/results/?&maximum_distance=" \
               "all&mileage_max=&page_size=20&sort=best_match_desc&stock" \
               "_type=used&zip=14000"
    makes_query = "&makes[]="
    mileage_query = "&mileage_max="
    transmission_query = "&transmission_slugs[]="
    year_min_query = "&year_min="
    year_max_query = "&year_max="
    body_style_query = "&body_style_slugs[]="
    cylinder_count_query = "&cylinder_counts[]="
    models_query="&models[]="
    return homepage+makes_query+makes+models_query+makes+"-"+model+mileage_query\
           +mileage+transmission_query+transmission+year_min_query+year_min\
           +year_max_query+year_max+body_style_query+body_style+cylinder_count_query\
           +cylinder


def scrape_url(search_page):
    url=[]
    homepage = search_page
    page = requests.get(homepage, timeout=3)
    soup = BeautifulSoup(page.content, "html.parser")
    possible_url=soup.findAll("script", type="application/ld+json")
    for e in possible_url:
        try:
            a = json.loads(e.text)

            if 'itemListElement' in a:
                for b in a['itemListElement']:
                   if 'url' in b:
                      url.append(b['url'])
        except:
            pass

    price_ls=[]
    price=soup.findAll("span",class_="primary-price")
    for c in price:
        try:
            price_ls.append(c.text)
        except:
            pass
    return url,price_ls
"""

"""
def get_final_information(home_page,page_amount):
    page_query="&page="
    last_page_amount=20
    current_page=1
    result=[]
    while page_amount>=current_page and last_page_amount==20:
        url=home_page+page_query+str(current_page)
        current_page+=1

        (link,price_ls)=scrape_url(url)
        for each in link:
            print("car url processed")
            mileage,price,makes_model_year=get_information(each)
            result.append((mileage,price,makes_model_year))

        last_page_amount=len(price_ls)
    return result
# atrieve further information for a specific car link

def get_information(url):
    homepage = url
    try:
       page = requests.get(homepage, timeout=3)
       soup = BeautifulSoup(page.content, "html.parser")
    except:
        print("a page link error:"+str(url))
        mileage, price, makes_model_year=None,None,None
    try:
        mileage = soup.find("div",class_="listing-mileage").text
    except:
        mileage=None
    try:
        price = soup.find("span",class_="primary-price").text
    except:
        price= None
    try:
       makes_model_year=soup.find("h1",class_="listing-title").text
    except:
        makes_model_year=None
    return mileage,price,makes_model_year

def test():
    # test on search Audi A3 and load 2 pages.
    url = make_url_query(makes="Audi", model="A3")
    info=get_final_information(url, 1)
    print("    mileage        price         year and other information")
    for a in info:
        print(a)


test()













