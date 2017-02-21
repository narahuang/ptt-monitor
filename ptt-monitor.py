#!/usr/bin/python3
# 
# Simple script to monitor PTT boards
# Usage: ptt-monitor.py [board_name] [page_count]


import requests
from bs4 import BeautifulSoup
import urllib.parse
import sys

NOT_EXIST = BeautifulSoup('<a>本文已被刪除</a>', 'lxml').a

def get_posts_on_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    posts = list()
    for article in soup.find_all('div', 'r-ent'):
        meta = article.find('div', 'title').find('a') or NOT_EXIST
        posts.append({
            'title': meta.getText().strip(),
            'link': meta.get('href'),
            'push': article.find('div', 'nrec').getText(),
            'date': article.find('div', 'date').getText(),
            'author': article.find('div', 'author').getText(),
        })

    next_link = soup.find('div', 'btn-group-paging').find_all('a', 'btn')[1].get('href')

    return posts, next_link


def get_pages(num):
    page_url = INDEX
    all_posts = list()
    for i in range(num):
        posts, link = get_posts_on_page(page_url)
        all_posts += posts
        page_url = urllib.parse.urljoin(INDEX, link)
    return all_posts

def get_postlinks(num):
    links = list()
    for post in get_pages(num):
        links.append( urllib.parse.urljoin(INDEX, post['link'])  )
    return links

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: {0} [board_name] [page_count]".format(sys.argv[0]))
    else:
        INDEX = "https://www.ptt.cc/bbs/"+sys.argv[1]+"/index.html"
        page = int(sys.argv[2])

    #print(get_postlinks(page))
    url_prefix='https://www.ptt.cc'
    for post in get_pages(page):
        url = url_prefix+str(post['link'])
        print(post['push'], post['title'], post['date'], post['author'], url)


