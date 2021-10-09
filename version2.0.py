#!/usr/bin/env python 
# -*- coding:utf-8 -*-

import requests
import os
import re
import time
from bs4 import BeautifulSoup


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/94.0.4606.71 Safari/537.36',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
                     '*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
           'Upgrade-Insecure-Requests': '1',
           'DNT': '1'}
root_dir = 'D:/comic/'
overwrite = False
replace_char = '_'
conn_delay = 5
read_delay = 30
max_retry = 2
ip_list = []


def save_file(url, path):
    response = requests.get(url, headers=headers,
                            timeout=(conn_delay, read_delay))
    with open(path, 'wb') as file:
        file.write(response.content)
        file.flush()


def get_pic_url(url):
    site = requests.get(url, headers=headers)
    content = site.text
    soup = BeautifulSoup(content, 'lxml')
    imgs = soup.find_all(id="img")
    for img in imgs:
        pic_src = img['src']
        return pic_src


def get_pic_list(url):
    site = requests.get(url, headers=headers)
    content = site.text
    soup = BeautifulSoup(content, 'lxml')
    divs = soup.find_all(class_='gdtm')
    img_count = len(divs)

    print('||共 %d 张图片，开始下载...' % img_count)
    title = re.sub(r'[\\/:*?"<>|\r\n]', replace_char, soup.h1.get_text())
    img_num = 0
    i = 0

    for div in divs:
        pic_url = div.a.get('href')
        pic_alt = div.a.img.get('alt')
        pic_name = pic_url.rpartition('/')[2].rpartition('-')[0] + '-' + pic_alt
        img_num = img_num + 1
        print('>> Saving: ' + pic_name + '.jpg')
        pic_path = '%s%s/%s.jpg' % (root_dir, title, pic_name)
        # noinspection PyBroadException
        try:
            if not overwrite and os.path.exists(pic_path) and os.path.isfile(pic_path):
                print('Already Exists <<')
            else:
                save_file(get_pic_url(pic_url), pic_path)
        except Exception as e:
            print(e)
            if max_retry < 1:
                print('Failed<<')
            time.sleep(1)
            for ri in range(0, max_retry):
                # noinspection PyBroadException
                try:
                    print('>> Retry times ' + str(ri + 1) + ':')
                    save_file(get_pic_url(pic_url), pic_path)
                except Exception as e_2:
                    print(e_2)
                    if ri == max_retry - 1:
                        print('Failed <<')
                    time.sleep(1)
                else:
                    print('Succeed <<')
                    i = i + 1
                    break
        else:
            print('Succeed <<')
            i = i + 1

    print('||本页共下载 %d 个文件，其中 %d 个成功。' % (img_num, i))
    return [img_num, i]


def get_gallery(url):
    if url.find('https://e-hentai.org/g/') != -1:
        url = url.partition('?p')[0]
        print('== 正在获取内容... ==')
        # noinspection PyBroadException
        try:
            site = requests.get(url, headers=headers)
            content = site.text
            soup = BeautifulSoup(content, 'lxml')
            pages = soup.find(class_='ptt').find_all('a')
            page_count = int(pages[len(pages)-2].get_text())
            title = str(soup.h1.get_text())
            title_2 = str(soup.find(id='gj').get_text())
            print('||[漫画名] 《%s》\n||[日文名] 《%s》\n||共 %d 页' %
                  (title, title_2, page_count))
            title = re.sub(r'[\\/:*?"<>|\r\n]', replace_char,
                           title)
            if not os.path.exists(root_dir + title):
                os.mkdir(root_dir + title)
        except Exception as e:
            print(e)
            print('== 未知错误！已停止解析。 ==')
        else:
            total_file = 0
            succeed_file = 0
            for page_num in range(0, page_count):
                print('||当前第 %d 页' % (page_num + 1))
                target_url = url
                if page_num != 0:
                    target_url = url + '?p=' + str(page_num)
                return_args = get_pic_list(target_url)
                total_file += return_args[0]
                succeed_file += return_args[1]
            print('== 《%s》下载完成！共 %d 个文件，其中 %d 个成功！==' %
                  (title, total_file, succeed_file))
    else:
        print('<错误:"' + url + '" 不是一个有效的eh漫画目录页面的地址。>\n')


def main():
    urls = []
    url = input('<请输入链接(输入空白内容结束)>:\n')
    while url != "":
        urls.append(url)
        url = input('== 已输入链接列表 ==\n' + str(urls) + '\n<请输入链接(输入空白内容结束):>\n')
    print('== 输入结束 ==')
    if len(urls) > 0:
        for item in urls:
            get_gallery(item)
        main()
    else:
        print('== 结束运行 ==')


if __name__ == "__main__":
    main()
