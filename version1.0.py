#!/usr/bin/env python 
# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
import os

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/94.0.4606.71 Safari/537.36',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
                     '*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
           'Upgrade-Insecure-Requests': '1'}


def save_file(url, path):
    response = requests.get(url, headers=headers)
    with open(path, 'wb') as file:
        file.write(response.content)
        file.flush()


def get_website(url):
    site = requests.get(url, headers=headers)
    content = site.text

    soup = BeautifulSoup(content, 'lxml')
    divs = soup.find_all(class_='gdtm')
    title = soup.h1.get_text()
    page = 0
    i = 0

    for div in divs:
        pic_url = div.a.get('href')
        page = page + 1

        print('Saving file ' + title + str(page) + '.jpg')

        # noinspection PyBroadException
        try:
            save_file(get_pic_url(pic_url), 'D:/comic/' + title + '/' + title + '_' + str(page) + '.jpg')
        except:
            print('Can not download ' + title + str(page) + '.jpg')
        else:
            print('Succeed')
            i = i + 1
    print('Finished downloading ' + str(page) + ' files,' + str(i) + ' of them are successful')
    menu()


def get_pic_url(url):
    site = requests.get(url, headers=headers)
    content = site.text
    soup = BeautifulSoup(content, 'lxml')
    imgs = soup.find_all(id='img')
    for img in imgs:
        pic_src = img['src']
        return pic_src


def menu():
    url = input('Please enter the url:')
    if url.find('https://e-hentai.org/g/') != -1:
        print('--OK,getting information--')
        # noinspection PyBroadException
        try:
            site = requests.get(url, headers=headers)
            content = site.text
            soup = BeautifulSoup(content, 'lxml')
            divs = soup.find_all(class_='gdtm')
            title = str(soup.h1.get_text())
            page = len(divs)

        except:
            print('Wrong! Please try again!!!')
            menu()
        else:
            print('The comic name is ' + title + ' , it has ' + str(page) + ' page,start downloading!!!')
            if os.path.exists('D:/comic/' + title):
                pass
            else:
                os.makedirs('D:/comic/' + title)

            get_website(url)

    else:
        print('Oh, it is not an e-hentai comic url, please enter again!')
        menu()


if __name__ == "__main__":
    menu()
