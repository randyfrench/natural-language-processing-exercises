#import libraries
import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import os
from time import strftime

############ Function to get Codeup Blogs

def get_front_page_links():
    """
    Short function to hit the codeup blog landing page and return a list of all the urls to further blog posts on the
    page.
    """
    response = requests.get("https://codeup.com/blog/", headers={"user-agent": "Codeup DS Germain"})
    soup = BeautifulSoup(response.text)
    links = [link.attrs["href"] for link in soup.select(".more-link")]
    return links

def parse_codeup_blog_article(url):
    "Given a blog article url, extract the relevant information and return it as a dictionary."
    response = requests.get(url, headers={"user-agent": "Codeup DS Germain"})
    soup = BeautifulSoup(response.text)
    return {
        "title": soup.select_one(".entry-title").text,
        "published": soup.select_one(".published").text,
        "content": soup.select_one(".et_pb_post_content").text.strip(),
    }


def get_blog_articles():
    "Returns a dataframe where each row is a blog post from the codeup blog landing page."
    links = get_front_page_links()
    df = pd.DataFrame([parse_codeup_blog_article(link) for link in links])
    return df



today = strftime('%Y-%m-%d')
get_blog_articles().to_json(f'codeup_blog_{today}.json')


####### Function to get News Articles

def parse_news_card(card):
    'Given a news card object, returns a dictionary of the relevant information.'
    card_title = card.select_one('.news-card-title')
    output = {}
    output['title'] = card_title.find('a').text.strip()
    output['published'] = card_title.select_one('.time').attrs['content']
    output['author'] = card_title.select_one('.author').text
    output['content'] = card.select_one('.news-card-content').div.text.strip()
    return output


def parse_inshorts_page(url):
    '''Given a url, returns a dataframe where each row is a news article from the url.
    Infers the category from the last section of the url.'''
    category = url.split('/')[-1]
    response = requests.get(url, headers={'user-agent': 'Codeup DS Germain'})
    soup = BeautifulSoup(response.text)
    cards = soup.select('.news-card')
    df = pd.DataFrame([parse_news_card(card) for card in cards])
    df['category'] = category
    return df

def get_inshorts_articles():
    '''
    Returns a dataframe of news articles from the business, sports, technology, and entertainment sections of
    inshorts.
    '''
    url = 'https://inshorts.com/en/read/{}'
    categories = ['business', 'sports', 'technology', 'entertainment']
    df = pd.concat([parse_inshorts_page(url.format(cat)) for cat in categories])
    df = df.reset_index(drop=True)
    return df


today = strftime('%Y-%m-%d')
get_inshorts_articles().to_json(f'inshorts-{today}.json')