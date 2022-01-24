# author: Handong Chen

import json

from nlp_process import *
from scraper_car_search import *
from functools import reduce
import re
#make_url_query(makes="",model="",mileage="",transmission="",year_min="",year_max="",body_style="",cylinder="")

def extracting(dict,key):
    try:
        return list(dict[key])[0]
    except:
        return""

def distance(obj1,obj2):
    distance=0
    for index in range(len(obj1)):
            distance+=( obj1[index]-int(re.sub('\D', "", obj2[index])))**2

    return distance**0.5

def candidate_validation(ls):
    try:
        #print(ls)
        hypothesis=ls[:10]
    except:
        print("can't have enough hypothesis")
        return

    hypothesis=list(map(lambda x:int(re.sub('\D', "", x[1])),hypothesis))
    print(hypothesis)
    hypothesis.sort()
    hypothesis=hypothesis[len(ls)//2-2:len(ls)//2+2]
    print(hypothesis)
    price=reduce(lambda x,y:x+y,hypothesis)
    return price/len(hypothesis)

if __name__ == "__main__":
    with open("input.json", 'r') as f:
        inputs = json.load(f)
    input_string = "I am looking to buy my automatic transmission 2017 " \
                   "Chevrolet Silverado. The lease is coming to an end " \
                   "next month. The car current has 22k miles. I mentioned " \
                   "this to my dealer and he said that I can only buy it " \
                   "after they (the dealer Honda) bought it first and then " \
                   "they financed it to me. He made it sound like after he " \
                   "buys my lease, he is going to increase the price and " \
                   "charge me more than my residual buyout price in the " \
                   "financing. Is this something that happens when buying a " \
                   "lease car? The dealer buys it first and then charges more " \
                   "than your residual to finance? I guess that the residual " \
                   "is only related to a full buyout at end of lease?"

    price_label = 25000
    input=process(input_string)
    print(extracting(input,'make'))
    url=make_url_query(makes=extracting(input,'make'),model=extracting(input,'model'),
                       body_style=extracting(input,'body_style'),
                       year_min=extracting(input,'year'),year_max=extracting(input,'year'))
    info=get_final_information(url, 1)

    info=list(map(lambda x:list(x),info))
    for each in range(len(info)):

         info[each].append(distance([extracting(input,'mileage')],info[each]))
    info.sort(key=lambda x:x[3])
    print(candidate_validation(info))
    print((price_label-candidate_validation(info))/price_label)



