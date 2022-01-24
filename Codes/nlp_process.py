# author: Yujie Zhao

import json
import nltk
import re

from pprint import pprint


# Load all the makes from the maeks.json file.
def load_makes():
    with open("makes.json", 'r') as f:
        makes_list = json.load(f)
    result = set()
    for each_make in makes_list:
        result.add(each_make.lower())
    return result


MAKES_LIST = load_makes()


# pprint(MAKES_LIST)

# load all the makes and models
def load_make_models():
    with open("model_keyword.json", 'r') as f:
        make_models = json.load(f)
    result = {}
    for make in make_models:
        models = make_models[make]
        lower_models = []
        for each_model in models:
            lower_models.append(each_model.lower())
        result[make.lower()] = set(lower_models)
    return result


MAKE_MODELS = load_make_models()


# pprint(MAKE_MODELS)

# Load all the body styles from the body_style.json file.
def load_body_styles():
    with open("body_styles.json", 'r') as f:
        body_styles = json.load(f)
    result = set()
    for each_body_style in body_styles:
        result.add(each_body_style.lower())
    return result


BODY_STYLE_LIST = load_body_styles()


# pprint(BODY_STYLE_LIST)

# Load all the body styles from the body_style.json file.
def load_transmissions():
    with open("transmissions.json", 'r') as f:
        transmissions = json.load(f)
    result = set()
    for each_transmission in transmissions:
        result.add(each_transmission.lower())
    return result


TRANSMISSIONS_LIST = load_transmissions()
# pprint(TRANSMISSIONS_LIST)

REPLACE_PATTERNS = [
    (r'won\'t', 'will not'),
    (r'can\'t', 'can not'),
    (r'i\'m', 'i am'),
    (r'(\w+)\'ll', '\g<1> will'),
    (r'(\w+)n\'t', '\g<1> not'),
    (r'(\w+)\'ve', '\g<1> have'),
    (r'(\w+)\'s', '\g<1> is'),
    (r'(\w+)\'re', '\g<1> are'),
    # convert 100k to 100000
    (r'(\d+)[kK]', '\g<1>000'),
    # conver $100 to 100 dollars
    (r'\$(\d+)', '\g<1> dollars')
]


def short_form_replace(text):
    for (pattern, replacement) in REPLACE_PATTERNS:
        text = re.sub(pattern, replacement, text)
    return text


# print(short_form_replace('100k'))
# print(short_form_replace('100K'))
# print(short_form_replace('$100'))
# print(short_form_replace('$10k'))

def process(query):
    # process only lower case strings
    query = query.lower()
    # process short forms like I'll
    query = short_form_replace(query)
    # generate words
    words = nltk.tokenize.word_tokenize(query)
    bigrams = nltk.bigrams(words)
    biwords = []
    for bigram in bigrams:
        biwords.append(bigram[0] + ' ' + bigram[1])
    trigrams = nltk.trigrams(words)
    triwords = []
    for trigram in trigrams:
        triwords.append(trigram[0] + ' ' + trigram[1] + ' '
                        + trigram[2])
    fourgrams = nltk.ngrams(words, 4)
    fourwords = []
    for fourgram in fourgrams:
        fourwords.append(fourgram[0] + ' ' + fourgram[1] + ' '
                         + fourgram[2] + ' ' + fourgram[3])

    found_makes = set()
    for a_word in words:
        if a_word in MAKES_LIST:
            found_makes.add(a_word)
    for a_biword in biwords:
        if a_biword in MAKES_LIST:
            found_makes.add(a_biword)
    # pprint(found_makes)

    found_models = set()
    for make in MAKE_MODELS:
        models = MAKE_MODELS[make]
        for a_word in words:
            if a_word in models:
                found_models.add(a_word)
        for a_biword in biwords:
            if a_biword in models:
                found_models.add(a_biword)
        for a_triword in triwords:
            if a_triword in models:
                found_models.add(a_triword)
        for a_fourword in fourwords:
            if a_fourword in models:
                found_models.add(a_fourword)
    # pprint(found_models)

    found_body_styles = set()
    for a_word in words:
        if a_word in BODY_STYLE_LIST:
            found_body_styles.add(a_word)
    for a_biword in BODY_STYLE_LIST:
        if a_biword in MAKES_LIST:
            found_body_styles.add(a_biword)
    # pprint(found_body_styles)

    found_transmissions = set()
    for a_word in words:
        if a_word in TRANSMISSIONS_LIST:
            found_transmissions.add(a_word)
    # pprint(found_transmissions)

    found_years = set()
    for a_word in words:
        if a_word.isnumeric():
            num = int(a_word)
            if num > 1960 and num < 2025:
                found_years.add(num)
    # pprint(found_years)

    found_mileages = set()
    for a_word in words:
        if a_word.isnumeric():
            num = int(a_word)
            if num > 5000:
                found_mileages.add(num)
    # pprint(found_mileages)

    return {'make': found_makes, 'model': found_models, 'body_style': found_body_styles,
            'transmission': found_transmissions, 'year': found_years, 'mileage': found_mileages}


if __name__ == '__main__':
    input_string = "I am looking to buy my automatic transmission 2019 Honda Civic Sedan lease. The lease is coming to an end next month. The car current has 20k miles. I mentioned this to my dealer and he said that I can only buy it after they (the dealer Honda) bought it first and then they financed it to me. He made it sound like after he buys my lease, he is going to increase the price and charge me more than my residual buyout price in the financing. Is this something that happens when buying a lease car? The dealer buys it first and then charges more than your residual to finance? I guess that the residual is only related to a full buyout at end of lease?"
    print(process(input_string))
