#!/usr/bin/env python
# coding: utf-8

# ### Homework 04 - Part I  Yifan (Crystal) CAI

# In[1]:


from bs4 import BeautifulSoup
import requests
import re
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = 'all'
from urllib.request import urlopen
from urllib.request import urlretrieve


# #### Part I
# Write code in Java or Python (full source code not markup) that logs into Planespotters.net and verifies that it is logged in my navigating to https://www.planespotters.net/member/profile and checking that your username is displayed on the page.  (The task at hand requires at least 2 page-requests.  I have solved it with 3 page-requests but have not tried if less page requests work as well.)  Specifically, your code should do the following:

# 1. Access https://www.planespotters.net/user/login using a standard GET request. Read and store the cookies received in the response.  In addition, parse the response and read (and store to a string variable) the value of the hidden input field that will (most likely) be required in the login process.

# In[2]:


url = "https://www.planespotters.net/user/login"
# Send a GET request to the URL
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0'
headers = {"user-agent": user_agent} 
response = requests.get(url, headers = headers)
# Store the cookies received in the response
cookies = response.cookies.get_dict()
print(cookies)
# Parse the response and find the hidden input field
soup = BeautifulSoup(response.text, 'html.parser')
# Store the hidden field value to a string variable
hidden_field = soup.find("input", type="hidden")["name"]
hidden_field
csrf = soup.find("input", id="csrf")["value"]
csrf


# 2. Make a post request using the cookies from (1) as well as all required name-value-pairs (including your username and passwords).

# In[3]:


# # Use the name-value-pairs to log in
session_requests = requests.session()
url = 'https://www.planespotters.net/user/login'
values = {#"referer" : 'https://www.planespotters.net/user/login',
          "username" : "crystal0805",
          "password" : "wyz710522",
          "csrf" : str(csrf)}
res = session_requests.post(url, 
                    data = values, 
                    cookies = cookies, 
                    headers = {"User-Agent":
                               'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.56'})
if res.status_code == 200 :
    print("Successfully logged in")
else:
    print("Failed to log in")


# 3. Get the cookies from the response of the post request and add them to your cookies from (1).

# In[4]:


# Get the new cookie
cookies_new = session_requests.cookies.get_dict()
cookies_new


# In[5]:


# Update the new cookie to the current cookie 
cookies.update(cookies_new)
print(cookies)


# 4. Verifies that you are logged in by accessing the profile page https://www.planespotters.net/member/profile with the saved cookies.

# In[6]:


session_requests = requests.session()
u = 'https://www.planespotters.net/member/profile'
v = {"username" : "crystal0805",
     "password" : "wyz710522",
     "csrf" : str(csrf)}
r = session_requests.post(u, data = v, cookies = cookies, headers = headers)
if r.status_code == 200 :
    print("Successfully logged in")
else:
    print("Failed to log in")


# 5. Then, print out the following at the end:
# - The entire Jsoup/BeautifulSoup document of your profile page.
# - All (combined) cookies from (3).
# - A boolean value to show your username is contained in the document in part (5)(a).

# In[7]:


#The entire Jsoup/BeautifulSoup document of your profile page.
profile_page = BeautifulSoup(r.content , "html.parser")
print(profile_page)


# In[8]:


# All (combined) cookies from (3).
print(cookies)


# In[9]:


#A boolean value to show your username is contained in the document in part (5)(a).
if 'crystal0805' in r.text:
    True
else:
    False

