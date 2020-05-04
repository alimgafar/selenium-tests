from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait

import pandas as pd

import time as time
from time import sleep

'''
 filename:  scrape_yt.py
 author:    Alim S. Gafar
 authored:  04-26-2020

 This is a practice tool to work with Selenium. I have been working with BeautifulSoup and wanted to learn how to 
 use Selenium to scrape sites rendered with JavaScript. 

 The code written here is to pull and package content from YouTube to be made available for use in other sites. I
 have two use cases in mind. First, to pull videos from different JavaScript-related YouTube channels that I can arrange by
 topic to deliver via email, website, or newsletter. Second, is to do much of the same for Sci-fi and indie filmaker content 
 for Eurodome TV, the Github-hosted website that I started last year with Mike Arbouet.

 The use cases are simply to help me understand what bits of Selenium are important for me to learn. There is much more than
 is used here. More likely, I'll come up with other examples and create separate files to address those cases.

 Modifications: See Github commits for dates and changes.
'''

driver = webdriver.Chrome()
channel_urls = ["https://www.youtube.com/user/MeteorVideos/videos?view=0&sort=dd&flow=grid", "https://www.youtube.com/channel/UC8tgRQ7DOzAbn9L7zDL8mLg/videos?view=0&sort=p&flow=grid",
                "https://www.youtube.com/channel/UCqKS692D_EGX2-0JMYMYcMA/videos?view=0&sort=p&flow=grid"]

playlist_urls = []

video_list = []


def getYTUserVideoList(url):
    print(url)
    driver.get(url)

    videos = driver.find_elements_by_xpath(
        '//*[@id="items"]/ytd-grid-video-renderer')

    for video in videos:
        # need the '.' in the path so it only searches within the pattern
        # and not the whole page
        a_tag = video.find_element_by_xpath('.//*[@id="video-title"]')
        title = a_tag.text
        link = a_tag.get_attribute("href")
        video_id = link.split('=')[-1]
        embed_link = "https://youtube.com/embed/" + video_id
        views = video.find_element_by_xpath(
            './/*[@id="metadata-line"]/span[1]').text
        how_recent = video.find_element_by_xpath(
            '//*[@id="metadata-line"]/span[2]').text
        print(title + '\n' + views + '\t' + how_recent + '\n')

        embed = '<iframe width="560" height="315" src="'
        embed = embed + embed_link + \
            '" frameborder = "0" allow = "accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen > </iframe>'

        video_items = {
            'title': title,
            'views': views,
            'uploaded': how_recent,
            'link': link,
            'embed': embed
        }

        return video_list.append(video_items)


def getYTUserVideoPlaylist(urls):
    print(url)
    driver.get(url)

    videos = driver.find_elements_by_xpath(
        '//*[@id="contents"]/ytd-playlist-video-renderer')

    print(len(videos))

    for video in videos:
        # need the '.' in the path so it only searches within the pattern
        # and not the whole page
        title = video.find_element_by_xpath(
            './/*[@id="video-title"]').text
        author = video.find_element_by_xpath(
            './/*[@id="text"]/a').text
        print(title + '\n' + author + '\n')

        video_items = {
            'title': title,
            'author': author
        }

        video_list.append(video_items)
    df = pd.DataFrame(video_list)
    print(df)


for url in channel_urls:
    getYTUserVideoList(url)

# getYTUserVideoPlaylist(urls[1])

# change default setting to print entire dataframe
pd_defs = pd.get_option("display.max_rows")
pd.set_option("display.max_rows", 500)

df = pd.DataFrame(video_list)
print(df)

# reset dataframe to defaults
pd.set_option("display.max_rows", pd_defs)

sleep(5)
driver.close()

# //*[@id = "contents"]/ytd-playlist-video-list-renderer/[@id = "contents"]/ytd-playlist-video-renderer
