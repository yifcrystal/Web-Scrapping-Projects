#!/usr/bin/env python
# coding: utf-8

# # Homework 02 
# 
# ### Q1 : 
# - Use your browser's development tools to find a unique way to access its list price and its current price. What do you choose? Please remember, you can choose multiple selectors to get where you want to be. E.g., you may choose to select "span.class1 p.class2" to select the "p" of class "class2" inside of the "span" of class "class1".
# - Store the prices to strings.
# - Use Python's (or Java's) regex (!!) functionality to convert the prices to "1234.56" (no dollar sign, comma, just a "." separator for cents). Print both, the list price and the current price to screen / terminal.

# In[408]:


from bs4 import BeautifulSoup
import requests
import re
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = 'all'


# In[123]:


headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"}
url= "https://www.tigerdirect.com/applications/SearchTools/item-details.asp?EdpNo=1501390"
page = requests.get(url, headers = headers)
# Create a beautifulsoup object 
soup = BeautifulSoup(page.text, 'lxml')


# In[252]:


#List price 
list_prices = soup.select("span del")
for i in list_prices:
    print('List price is',i.text)
#store price to string  
ListPrice = i.text


# In[260]:


#Current price 
current_prices = soup.select("div.pdp-price p.final-price span.sr-only")
for i in current_prices:
    print("Current Price is", i.text.replace('\n', '').replace('\r', '').replace("          ", " ").replace('and','.').replace('cents','').replace(" . ",'.'))
    
#store price to string  
CurrentPrice = i.text.replace('\n', '').replace('\r', '').replace("          ", " ").replace('and','.').replace('cents','').replace(" . ",'.')


# In[261]:


print(re.sub("[$,]", "", ListPrice))
print(re.sub("[$,]", "", CurrentPrice))


# ### Q2. 
# - Loads "https://www.usnews.com/" "finds" its current "Top Stories" (do not hard-code it's URL!) (You may use your browser's dev tools to find a functioning way to access all the "Top Stories" and then implement the access to them in your code.)
# - Read + print the URL of the _second_ current top story to the screen (terminal). Load that page 
# - Read + print the header as well as the first 3 sentences of the main body to the screen
#     - Example: the current _second_ "Top Stories" is "Trump Org Gets Max Fine for Tax Fraud" I want your code to load "https://www.usnews.com/", then read all the "Top Stories" (currently "Biden Invited to Address Congress", "Trump Org Gets Max Fine for Tax Fraud", ...), get the URL that the second top story links to ("https://www.usnews.com/news/national-news/articles/2023-01-13/trump-organization-sentenced-to-pay-1-6-million-for-tax-fraud"; this information is stored in the "href" property of the tag "a", i.e., '<a href="https://...">...</a>', store the link to a string + print it to screen, then load the content of the string and read + print the header as well as the first 3 sentences)

# In[349]:


url_01= "https://www.usnews.com"
page_01 = requests.get(url_01, headers = headers)
# Create a beautifulsoup object 
soup_01 = BeautifulSoup(page_01.text, 'lxml')


# #### Get the headline of the second "Top Stories" 

# In[394]:


#method 01
temp = soup_01.find_all('h3', 
                        class_ = 'Heading-sc-1w5xk2o-0 ContentBox__StoryHeading-sc-1egb8dt-3 MRvpF fqJuKa story-headline')[2]
#method 02
temp = soup_01.find_all('h3', 
                       attrs = {'class': 'Heading-sc-1w5xk2o-0 ContentBox__StoryHeading-sc-1egb8dt-3 MRvpF fqJuKa story-headline'})[2]

headline = temp.text
headline


# #### Get the link of the second "Top Stories" 

# In[396]:


link = soup_01.find_all('h3',class_ = 'Heading-sc-1w5xk2o-0 ContentBox__StoryHeading-sc-1egb8dt-3 MRvpF fqJuKa story-headline')[2].a.get('href')
link


# #### Get the first 3 sentences of the second "Top Stories" 

# In[397]:


url_02= link
page_02 = requests.get(url_02, headers = headers)
# Create a beautifulsoup object 
soup_02 = BeautifulSoup(page_02.text, 'lxml')

soup_02


# In[410]:


p1 = soup_02.find_all('div', class_ = 'Raw-slyvem-0 bCYKCn')[0].p.text
p2 = soup_02.find_all('div', class_ = 'Raw-slyvem-0 bCYKCn')[1].p.text
p3 = soup_02.find_all('div', class_ = 'Raw-slyvem-0 bCYKCn')[2].p.text
p1
p2
p3

