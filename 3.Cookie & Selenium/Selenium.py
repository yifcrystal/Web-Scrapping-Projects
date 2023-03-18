#!/usr/bin/env python
# coding: utf-8

# ### Homework 04 - Part II  Yifan (Crystal) CAI

# In[1]:


from bs4 import BeautifulSoup
import requests
import re
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = 'all'
from urllib.request import urlopen
from urllib.request import urlretrieve


# #### Part II
# 1. please get Selenium to work on your system. e., try to code something up in Java or Python that starts a browser of your choice, navigates to google.com, and searches for "askew" as well as "google in 1998" (separate searches!)

# In[1]:


import selenium
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


# In[3]:


driver = webdriver.Chrome(executable_path='/Users/crystal/Desktop/chromedriver_mac64/chromedriver')
driver.implicitly_wait(10)
driver.set_script_timeout(120)
driver.set_page_load_timeout(10)
driver.get("https://google.com")

inp = driver.find_element(By.CSS_SELECTOR,"input[type=text]")
inp.send_keys("askew\n")
time.sleep(5)
driver.quit()


# In[4]:


driver = webdriver.Chrome(executable_path='/Users/crystal/Desktop/chromedriver_mac64/chromedriver')
driver.implicitly_wait(10)
driver.set_script_timeout(120)
driver.set_page_load_timeout(10)
driver.get("https://google.com")

inp = driver.find_element(By.CSS_SELECTOR,"input[type=text]")
inp.send_keys("google in 1998\n")
time.sleep(5)
driver.quit()


# 2. write a script that goes to bestbuy.com, clicks on Deal of the Day, reads how much time is left for the Deal of the Day and prints the remaining time to screen (console), clicks on the Deal of the Day (the actual product), clicks on its reviews, and saves the resulting HTML to your local hard drive as "bestbuy_deal_of_the_day.htm"

# In[6]:


driver = webdriver.Chrome(executable_path='/Users/crystal/Desktop/chromedriver_mac64/chromedriver')
driver.implicitly_wait(30)
driver.set_script_timeout(120)
driver.set_page_load_timeout(100)
driver.get("https://www.bestbuy.com/")

deal_of_the_day = driver.find_element(By.XPATH, "//a[text()='Deal of the Day']")
deal_of_the_day.click()
time.sleep(2)

remaining_hour = driver.find_element(By.XPATH, "//*[@id='countdown']/li[1]/span").text
remaining_min = driver.find_element(By.XPATH, "//*[@id='countdown']/li[3]/span").text
remaining_sec = driver.find_element(By.XPATH, "//*[@id='countdown']/li[5]/span").text
print("Remaining time is", remaining_hour,":",remaining_min,":",remaining_sec)
time.sleep(2)

# Click the Deal of the Day product
driver.find_element(By.CSS_SELECTOR,"#wf-offer-20a2ed61-08c5-4705-b29c-e900b7afdafb-product-title > a").click()
time.sleep(2)

# Click the reviews button
reviews_link = driver.find_element(By.CSS_SELECTOR, "span[class = 'c-reviews order-2']")
reviews_link.click()
time.sleep(2)

# Save the HTML to a local file
folder_path = "/Users/crystal/Desktop/hw04_0212/"
file_name =  f"bestbuy_deal_of_the_day.html"
file_path = folder_path + file_name
try:
    with open(file_path, "w") as file:
        file.write(driver.page_source)
    print(f"{file_name} has been downloaded")
except:
    print(f"Error: {file_name} cannot be downloaded")
    
# Close the webdriver
driver.quit()

