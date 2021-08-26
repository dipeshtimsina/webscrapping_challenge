#!/usr/bin/env python
# coding: utf-8

# In[1]:


# dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd 


# In[2]:


# pip install splinter


# In[ ]:


# splinter setup
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[4]:


# redplanetscience.com 
url = "https://redplanetscience.com/"
browser.visit(url)
time.sleep(1)


# In[5]:


#page to soup
html = browser.html
soup = bs(html, "html.parser")


# In[6]:


#latest news title
news_title = soup.find('div', class_='content_title').text
# news_title


# In[7]:


#latest paragraph of news 
news_p = soup.find('div', class_='article_teaser_body').text
# news_p


# In[8]:


#image site 
jpl_url = "https://spaceimages-mars.com/"
browser.visit(jpl_url)
time.sleep(1)


# In[9]:


# page into soup
html = browser.html
soup = bs(html, "html.parser")


# In[10]:


#navigation with splinter and have url be a variable
relative_image_path = soup.find_all('img')[1]["src"]
featured_image_url = jpl_url + relative_image_path
# featured_image_url


# In[11]:


# galaxyfacts
mars_url = "https://galaxyfacts-mars.com/"
tables = pd.read_html(mars_url)
tables


# In[12]:


type(tables) #what form the data is in


# In[13]:


#index normalization
facts_df = tables[0]
#no earth allowed
facts_df = facts_df.drop(columns=[2])
#new names
facts_df = facts_df.rename(columns={0: "Mars Profile", 1: "Measurements"})

# Display DataFrame
facts_df


# In[14]:


facts_df = facts_df.drop([0])
facts_df


# In[15]:


#conversion to string for HTML
mars_facts = facts_df.to_html()
mars_facts.replace('\n', '')
# print(mars_facts)
# mars_facts


# In[16]:


#visit mars hemi
mars_hem_url = "https://marshemispheres.com/"
browser.visit(mars_hem_url)
time.sleep(1)
#to soup
html = browser.html
soup = bs(html, "html.parser")


# In[17]:


# link up then extract
links = browser.find_by_css('a.product-item img')
mars_items = soup.find_all('div', class_='item')


# In[19]:


#create a dictionary with the hemi-url
hem_img_urls=[]
#loop through mars items 
for item in mars_items:
    #for errors 
    try:
        # take the titles then the url
        hem = item.find('div',class_='description')
        hem_title=hem.h3.text
        hem_url = hem.a['href']
        browser.visit(mars_hem_url + hem_url)
        
        # extrat links for the images 
        html=browser.html
        soup=bs(html,'html.parser')
        img_src=soup.find('li').a['href']
        if (hem_title and img_src):
            print('-'*25)
            print(hem_title)
            print(mars_hem_url+img_src)
            #dict for the urls 
        hem_dict={
            'title': hem_title,
            'image_url': img_src
        }
        hem_img_urls.append(hem_dict)
    except Exception as e:
        print(e)


# In[20]:


#complete dict for all the data
mars_dict={
    'hem_title': hem_title,
    'hem_image_url': img_src,
    'news_title': news_title,
    'news_p': news_p,
    'featured_img': featured_image_url,
    'mars_facts': mars_facts
    
}

