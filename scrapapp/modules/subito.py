import os, requests, csv, json, sys, time
from bs4 import BeautifulSoup
import time
from datetime import datetime
import logging

import django
django.setup()

from scrapapp.models import Subito

# curr_dir = os.pacth.dirname(__file__)

def fetch_site(site_url):
    html = requests.get(site_url, headers={'User-Agent': 'Mozilla/5.0'}).text
    time.sleep(4)
    return BeautifulSoup(html, 'html.parser')

def get_item_detail(item_url):
    """
    * Fetch detail result of item with the item url
    * return (user_id, title, description, price, location, images)
    """
    detail = fetch_site(item_url)

    item_user_info = detail.select_one('[class*="index-module_rounded_user_badge__"]')
    item_user_info = item_user_info['href'] if item_user_info else ''

    try:
        item_user_id = '000'
        if item_user_info:
            item_user_info = item_user_info.split('/', 2)
            if len(item_user_info) == 3:
                item_user_id = item_user_info[2]

        item_title = detail.select_one('[class*="AdInfo_ad-info__title__"]')
        item_title = item_title.text if item_title else ''

        item_description = detail.select_one('[class*="AdDescription_description__"]')
        item_description = item_description.text if item_description else ''

        item_location = detail.select_one('[class*="AdInfo_ad-info__location__"]')
        item_location = item_location.text if item_location else ''

        item_price = detail.select_one('[class*="AdInfo_ad-info__price__"]')
        item_price = item_price.text if item_price else ''

        img_tags = detail.select('figure.carousel-cell > img')
        item_imgs = [tag['src'] for tag in img_tags] if img_tags else []

        return item_user_id, item_title, item_description, item_price, item_location, item_imgs
    except:
        return '000', '', '', '', '', ''
  
def trim_both(st):
    return st[1:len(st) - 1]

def get_total_page_number(soup):
    """ Return total page number based on pagination container """
    total_pages = soup.select('.pagination-container > .unselected-page')
    last_page = total_pages[len(total_pages) - 1]
    last_page = last_page.select_one('a')['href']
    ind = last_page.index('?o=')
    last_page = last_page[ind+3:len(last_page)]
    return last_page

# requestsz
def subitoProc(post_data=None):
    if not post_data: return

    # Get user selected values
    remote_city = post_data.get('remote_city', '')
    remote_category = post_data.get('remote_category', '')
    select_city = post_data.get('select_city', '')
    select_category = post_data.get('select_category', '')

    select_city = trim_both(select_city).split(':')
    country_id = int(trim_both(select_city[0]))
    state_id = int(trim_both(select_city[1]))
    city_id = int(trim_both(select_city[2]))
    city_url = trim_both(select_city[3])

    select_category = trim_both(select_category).split(':')
    section_id = int(trim_both(select_category[0]))
    category = int(trim_both(select_category[1]))
    category_url = trim_both(select_category[2])

    # Proc
    base_url = remote_city + remote_category
    soup = fetch_site(base_url)
    items = soup.select('[class*="SmallCard-module_link__"]')

    total_page_num = get_total_page_number(soup)

    for page in range(int(total_page_num)):
        t_url = base_url + "/?o=%s" % (page + 1)

        print('\nTarget Site URL: ', t_url)

        soup = fetch_site(t_url)
        items = soup.select('[class*="SmallCard-module_link__"]')

        if not items or items.length == 0:
            items = soup.select('[class*="BigCard-module_link__"]')

        for item in items:
            print(' - ', item['href'])

            user_id, title, description, price, location, images = get_item_detail(item['href'])
            if title == '': continue

            subito = Subito.objects.filter(Title=title)
            if len(subito) != 0: continue

            # Save DB
            subito = Subito(
                UserID = user_id,           # default 100
                Title = title,        
                Description = description,  
                Images = ','.join(img for img in images),       
                Mobile = 'XXX',             # IF
                Age = 0,                    # IF
                Price = price,              # IF
                Location = location,        # IF
                CountryID = country_id,     # Given
                StateID = state_id,         # Given
                CityID = city_id,           # Given
                CityURL = city_url,         # Given
                Section = section_id,       # Given
                Category = category,        # Given
                CategoryURL = category_url, # Given
                Scrap = 2,                  # Default
                Status = 1,                 # Default
                # StartDate': ''     # Today
            )

            subito.save()

        # break