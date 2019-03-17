#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Declare Dependencies 
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import requests
import os
import pymongo
from flask import Flask
import time


# In[2]:


def scrape(): 

        path={"executable_path":"/usr/local/bin/chromedriver"}


        # In[3]:


        browser = Browser("chrome",**path)


        # In[4]:


        #get_ipython().system('which chromedriver')


        # In[5]:


        # Initialize PyMongo
        conn = 'mongodb://localhost:27017'
        client = pymongo.MongoClient(conn)


        # In[6]:


        db = client.mars_db
        collection = db.items

        Scrape_Results={"mars news": mars_news(),
                        "featured image": featured_image(browser),
                        "Mars Weather": Mars_Weather(),
                        "Mars Facts": Mars_Facts(),
                        "Mars Hemispheres": Mars_Hemi(browser)}

        return Scrape_Results 


def mars_news(): # MARS NEWS
                
        # In[7]:


        url = 'https://mars.nasa.gov/news/'
        response = requests.get(url)
        html = url


        # In[8]:


        headlines_soup = bs(response.text, 'lxml')


        # In[9]:


        headline = headlines_soup.find('div', class_ = 'content_title').text.strip()


        # In[10]:


        #return headline


        # In[11]:


        news = headlines_soup.find('div', class_ = 'rollover_description_inner').text.strip()


        # In[12]:


        return (headline, news)


        # In[13]:


def featured_image(browser):
        featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(featured_image_url)
        time.sleep (2)
        browser.find_by_id("full_image").click()
        time.sleep (2)
        browser.find_link_by_partial_text("more info").click()


        # In[14]:


        #print(browser.html)


        # MARS FEATURED IMAGE

        # In[15]:


        browser.visit(featured_image_url)


        # In[16]:


        html = browser.html
        soup = bs(html, 'lxml')


        # In[17]:


        featured_img_base = "https://www.jpl.nasa.gov"
        featured_img_url_raw = soup.find("div", class_="carousel_items").find("article")["style"]
        featured_img_url = featured_img_url_raw.split("'")[1]
        featured_img_url = featured_img_base + featured_img_url
        return featured_img_url


def Mars_Weather():# MARS WEATHER

        # In[18]:


        #weather on Mars
        url = 'https://twitter.com/marswxreport?lang=en'
        response = requests.get(url)


        # In[19]:


        # create soup
        weather_soup = bs(response.text, 'lxml')


        # In[20]:


        #grab all the tweets
        mars_weather_tweet = weather_soup.find_all('div', class_ = "js-tweet-text-container")


        # In[21]:


        # find the first actual weather tweet (they start with "InSight")
        for tweet in mars_weather_tweet:
                if tweet.text.strip().startswith('InSight'):
                        mars_weather = tweet.text.strip()


        # In[22]:


        return mars_weather


def Mars_Facts(): # MARS FACTS

        # In[23]:


        #visit space-facts/mars
        mars_facts_url = 'https://space-facts.com/mars/'
        

        # In[24]:


        table = pd.read_html(mars_facts_url)
        table[0]
        #set column headers 
        mars_df = table[0]
        mars_df.columns = ["Characteristics", "Profile Facts"]
        return mars_df.to_html()


def Mars_Hemi(browser): # MARS HEMISPHERES

        # In[27]:


        base_hemisphere_url = "https://astrogeology.usgs.gov"
        hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
        browser.visit(hemisphere_url)


        # In[28]:


        html = browser.html
        soup = bs(html, 'lxml')

        # Create empty list for hemisphere urls    
        hemisphere_image_urls = []

        # Retreive all items that contain mars hemispheres information
        links = soup.find_all("div", class_="item")


        # loop through the items previously stored
        for link in links:
                img_dict = {}
                title = link.find("h3").text
                next_link = link.find("div", class_="description").a["href"]
                full_hemisphere = base_hemisphere_url + next_link
                
                browser.visit(full_hemisphere)
                
                
                pic_html = browser.html
                pic_soup = bs(pic_html, 'lxml')
                
                url = pic_soup.find("img", class_="wide-image")["src"]

                img_dict["title"] = title
                img_dict["img_url"] = base_hemisphere_url + url
                
                
                hemisphere_image_urls.append(img_dict)

        return hemisphere_image_urls  

print(scrape())


