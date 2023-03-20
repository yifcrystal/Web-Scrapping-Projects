#!/usr/bin/env python
# coding: utf-8

# ## Individual Project - Yifan(Crystal) CAI

# In[3]:


from bs4 import BeautifulSoup
import requests
import os
import re
import pandas as pd
import numpy as np


# ### 1.2

# #### a). Use the URL identified above and write code that loads eBay's search result page containing sold "amazon gift card". Save the result to file. Give the file the filename "amazon_gift_card_01.htm".

# In[488]:


headers = {"User-Agent": "Mozilla/5.0"}
link = "https://www.ebay.com/sch/i.html?_from=R40&_nkw=amazon+gift+card&LH_Sold=1"
# page = requests.get(link, headers = headers)
# soup = BeautifulSoup(page.text, 'lxml')


# In[489]:


#Set up folder where I hope to download my pages into
folder_path = "/Users/crystal/Desktop/IndividualProject_0202/"
#For loop to go through the list of links to download pages
file_name =  f"amazon_gift_card_01.htm"
file_path = folder_path + file_name

try:
    html = requests.get(link, headers = headers).text
    with open(file_path, "w") as file:
        file.write(html)
    print(f"{file_name} has been downloaded")
except:
    print(f"Error: {file_name} cannot be downloaded")


# #### b). Take your code in (a) and write a loop that will download the first 10 pages of search results. Save each of these pages to "amazon_gift_card_XX.htm" (XX = page number). IMPORTANT: each page request needs to be followed by a 10 second pause.  Please remember, you want your program to mimic your behavior as a human and help you make good purchasing decisions.

# In[490]:


#Set up folder where I hope to download my pages into
folder_path = "/Users/crystal/Desktop/IndividualProject_0202/"
#For loop to go through the first 10 pages to download all of them into htm files.
for i in range(1, 11):
    base_url = "https://www.ebay.com/sch/i.html?_from=R40&_nkw=amazon+gift+card&_sacat=0&LH_TitleDesc=0&LH_Sold=1&rt=nc&_pgn="
    url = base_url + str(i)
    file_name = f"amazon_gift_card_{str(i).zfill(2)}.htm"
    file_path = folder_path + file_name
    
    try:
        html = requests.get(url, timeout=10, headers = headers).text
        with open(file_path, "w") as file:
            file.write(html)
        #Signal me when a file has been successfully downloaded
        print(f"{file_name} has been downloaded")
    except:
        print(f"Error: {file_name} cannot be downloaded")


# #### c). Write code that loops through the pages you downloaded in (b), opens and parses them to a Python or Java xxxxsoup-object.
# #### d). Using your code in (c) and your answer to 1 (g), identify and print to screen the title, price, and shipping price of each item.

# In[491]:


folder_path = "/Users/crystal/Desktop/IndividualProject_0202/"
products_list = []
for i in range(1, 11):
    file_name = f"amazon_gift_card_{str(i).zfill(2)}.htm"
    file_path = folder_path + file_name

    with open(file_path, "r") as file:
        html = file.read()
        soup = BeautifulSoup(html, "lxml")
        items = soup.find_all(attrs = {'class': 's-item__info clearfix'})
        for item in items[1:]:
            try : 
                temp = []
                name = item.find(attrs = {'class': 's-item__title'}).text.replace('New Listing',"")
                #face_price = str(re.findall(r'\$\d+|\d+ Dollars', name)).replace('$','').replace(' Dollars','')
                price = item.find(attrs = {'class': 's-item__price'}).text.strip()
                #price_n = float(price.replace('$',''))
                shipping = item.find(attrs = {'class': 's-item__shipping s-item__logisticsCost'}).text.replace('Free shipping','$0.00').replace('+','').replace(' shipping','')
                temp.append(name)
                temp.append(price)
                temp.append(shipping)
                products_list.append(temp)
                print(f"Product: {temp[0]}" + '\n'
                      f"Price: {temp[1]}" + '\n'
                      f"Shipping Price: {temp[2]}" +'\n')
            except Exception as e : 
                print('\n' + "The item has not shown no shipping information : " + '\n' +
                      f"Product: {name}" + 
                      item.find(attrs = {'class': 's-item__title'}).text.replace('New Listing',"") + '\n' +
                      f"Price: {price}" + 
                      item.find(attrs = {'class': 's-item__price'}).text +'\n')


# #### e). Using RegEx, identify and print to screen gift cards that sold above face value. e., use RegEx to extract the value of a gift card from its title when possible (doesn’t need to work on all titles, > 90% success rate if sufficient). Next compare a gift card’s value to its price + shipping (free shipping should be treated as 0).  If value < price + shipping, then a gift card sells above face value.

# In[492]:


## Compile into DataFrames & Extract values
# This is the dataset of all products together with price, shipping price, face value. 
Products = pd.DataFrame(products_list, columns=['Product','Price','Shipping Price']) 
# Face Price
Products['Face Price'] = Products['Product'].str.extract('(\d+)').astype(float)
# Actual Price
Products['Actual Price'] = Products['Price'].str.extract('(\d+\.\d+)').astype(float)
# Shipping Price
Products['Shipping Price'] = Products['Shipping Price'].str.extract('(\d+\.\d+)').astype(float)
# Total Price
Products['Total Price'] = Products['Actual Price'] + Products['Shipping Price']
Products.head()


# In[504]:


# This is the dataset of the products that has face value < price + shipping price
Over_priced = Products[Products['Face Price'] < Products['Total Price']]
Over_priced.to_csv('Over_priced.txt', sep='\t', index=False)
Over_priced.head()


# #### f). What fraction of Amazon gift cards sells above face value? Why do you think this is the case?

# In[484]:


Over_priced_fraction = round(len(Over_priced)/len(Products)*100,2)
print(f"The fraction of Amazon gift cards sells above face value is {Over_priced_fraction}%")


# #### Comment: 
# I think from the point of view of supply and demand, Amazon gift cards can sell above face value because that it's convenient to make purchase from Amazon using Amazon gift cards; additionally, some people may buy gift cards at a discount and resell them for a profit. 

# ### 2.2 

# #### a). Following the steps we discussed in class and write code that automatically logs into the website https://www.fctables.com/

# In[ ]:


# Write code that automatically logs into the website#
url = 'https://www.fctables.com'
values = {'login_action': 1,
          'login_username': 'cyf08050716',
          'login_password': 'wyz0522',
          'user_remeber': 1,
          'submit':1}
res = requests.get(url, data=values)


# #### b). Verify that you have successfully logged in:  use the cookies you received during log in and write code to access https://www.fctables.com/tipster/my_bets/ . Check whether the word “Wolfsburg” appears on the page.  Don’t look for your username to confirm that you are logged in (it won’t work) and use this page’s content instead.

# In[13]:


# Use the cookies you received during log in and write code to access
session_requests = requests.session()
URL = 'https://www.fctables.com/tipster/my_bets/'
cookies = session_requests.cookies.get_dict()
page = session_requests.get(URL, cookies = cookies)
soup = BeautifulSoup(page.content, 'html.parser')

if "Wolfsburg" in soup.text:
    print("The word 'Wolfsburg' was found on the website.")
else:
    print("The word 'Wolfsburg' was not found on the website.")

