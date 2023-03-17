#!/usr/bin/env python
# coding: utf-8

# ### Homework 02 

# In[1]:


from bs4 import BeautifulSoup
import requests
import re
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = 'all'
from urllib.request import urlopen
from urllib.request import urlretrieve


# #### a). Use the URL identified above and write code that loads the first page with 40 items per page of “B&N Top 100”.

# In[2]:


headers = {"User-Agent": "Mozilla/5.0"}
url= "https://www.barnesandnoble.com/b/books/_/N-1fZ29Z8q8?Nrpp=40&page=1"
page = requests.get(url, headers = headers)
# Create a beautifulsoup object 
soup = BeautifulSoup(page.text, 'lxml')


# #### b). Take your code in (a) and create a list of each book’s product page URL. This list should be of length 40.

# In[3]:


base_url = "https://www.barnesandnoble.com"
items = soup.find_all('h3',class_ = 'product-info-title')
links = []
for i in items:
    links.append(base_url + i.a.get('href'))
print(links)
#Check the length of the list of links
len(links) 


# #### c). Write a loop that downloads each product page of the top 40 books in “B&N Top 100”. e., save each of these pages to your computer using a meaningful filename (e.g., "bn_top100_01.htm"). IMPORTANT: Each page request needs to be followed by at least a 5 second pause!  Remember, you want your program to mimic your behavior as a human and help you make good purchasing decisions.

# In[7]:


#Set up folder where I hope to download my pages into
folder_path = "/Users/crystal/Desktop/assign02_0128/"
#For loop to go through the list of links to download pages
for i in range(1, 41):
    link = links[i-1]
    file_name = f"Top{str(i).zfill(2)}.html"
    file_path = folder_path + file_name
    
    try:
        html = requests.get(link, timeout=20,headers = headers).text
        with open(file_path, "w") as file:
            file.write(html)
        #Signal me when a file has been successfully downloaded
        print(f"{file_name} has been downloaded")
    except:
        print(f"Error: {file_name} cannot be downloaded")


# #### d). Write a separate piece of code that loops through the pages you downloaded in (c), opens and parses them into a Python or Java xxxxsoup-object. Next, access the “Overview” section of the page and print the first 100 characters of the overview text to screen.

# In[14]:




