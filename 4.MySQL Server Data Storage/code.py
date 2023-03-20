#!/usr/bin/env python
# coding: utf-8

# # Homework 05 Yifan (Crystal) CAI

# In[1]:


import mysql.connector
import warnings
import requests
import json
import codecs
from bs4 import BeautifulSoup
import pprint
from datetime import datetime
import time


# 1. Go to https://api.github.com and familiarize yourself with the API.

# 2. Go to https://api.github.com/repos/apache/hadoop/contributors . This is the Apache Hadoop Github Repo's contributors’ endpoint. Extract the JSON corresponding to the first 100 contributors from this API. (Hint: the API request is a GET request and the variable name that handles the items per page is "per_page").  Write Java or Python code that does all this.

# In[5]:


### personal identification code
headers = {'Authorization' : 'token ' + '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'}
response = requests.get('https://api.github.com/repos/apache/hadoop/contributors', headers = headers, params={'per_page': 100})
contributors_json = json.loads(response.content)
# len(contributors_json)
pprint.pprint(contributors_json)


# 3. For each of the 100 contributors extracted in (2), write code that accesses their user information and extracts "login", "id", "location", "email", "hireable", "bio", "twitter_username", "public_repos", "public_gists", "followers", "following", "created_at" (and print those to screen)

# In[6]:


for contributor in contributors_json:
    user_url = contributor['url']
    user_response = requests.get(user_url, headers = headers)
    user_json = user_response.json()

    login = user_json['login']
    user_id = user_json['id']
    location = user_json['location']
    email = user_json['email']
    hireable = user_json['hireable']
    bio = user_json['bio']
    twitter_username = user_json['twitter_username']
    public_repos = user_json['public_repos']
    public_gists = user_json['public_gists']
    followers = user_json['followers']
    following = user_json['following']
    created_at = user_json['created_at']

    print(f"Login: {login}")
    print(f"ID: {user_id}")
    print(f"Location: {location}")
    print(f"Email: {email}")
    print(f"Hireable: {hireable}")
    print(f"Bio: {bio}")
    print(f"Twitter Username: {twitter_username}")
    print(f"Public Repos: {public_repos}")
    print(f"Public Gists: {public_gists}")
    print(f"Followers: {followers}")
    print(f"Following: {following}")
    print(f"Created At: {created_at}")
    print()


# 4. Write code that creates an SQL database + table, and stores all the information obtained in (3) in it.  Please be cautious of the data type you choose for each collumn and briefly justify your decisions.  What do you choose as Primary Key and why?

# **Answer :** <br>
# I choose user_id as primary key as this is the field that each user has unique value; I set those columns with numbers and strings to be of type "VARCHAR" and those columns with only numbers to be of type "INT". 

# In[7]:


## Create a new database to create table into

# Connect to MySQL server
conn = mysql.connector.connect(host='localhost',user='root',password='wyz710522')
# Create a cursor to execute SQL queries
cursor = conn.cursor()
# Create a new database if not exist
SQL_DB = "github"
query_Database = "CREATE DATABASE IF NOT EXISTS " + SQL_DB
cursor.execute(query_Database)


# In[8]:


## Create Table in the database 

# Connect to MySQL server
conn = mysql.connector.connect(host='localhost',user='root',password='wyz710522')
# Create a cursor to execute SQL queries
cursor = conn.cursor()
# Create a new table if not exist to include all the columns needed
SQL_TABLE_CONTRIBUTORS = "Contributors"
SQL_TABLE_CONTRIBUTORS_DEF = "(" +         "login VARCHAR(300) NOT NULL," +         "user_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY," +         "location VARCHAR(300)," +         "email VARCHAR(300)," +         "hireable INT," +         "bio VARCHAR(300)," +         "twitter_username VARCHAR(300)," +         "public_repos INT," +         "public_gists INT," +         "followers INT," +         "following INT," +         "created_at VARCHAR(300)" +         ")"
query_Table = "CREATE TABLE IF NOT EXISTS " + SQL_DB + "." + SQL_TABLE_CONTRIBUTORS + " " + SQL_TABLE_CONTRIBUTORS_DEF + ";";
cursor.execute(query_Table)


# In[9]:


## Fetch all the content of the table
headers = {'Authorization' : 'token ' + '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'}
url = 'https://api.github.com/repos/apache/hadoop/contributors'
response = requests.get(url,headers = headers, params={'per_page': 100})
contributors_json = response.json()
        
logins = []
user_ids = []
locations = []
emails = []
hireables = []
bios = []
twitter_usernames = []
public_reposs = []
public_gistss  = []
followerss = []
followings = []
created_ats = []
        
for contributor in contributors_json:
    user_url = contributor['url']
    user_response = requests.get(user_url, headers = headers)
    user_json = user_response.json()
    login = user_json['login']
    logins.append(login)
    user_id = user_json['id']
    user_ids.append(user_id)
    location = user_json['location']
    locations.append(location)
    email = user_json['email']
    emails.append(email)
    hireable = user_json['hireable']
    hireables.append(hireable)
    bio = user_json['bio']
    bios.append(bio)
    twitter_username = user_json['twitter_username']
    twitter_usernames.append(twitter_username)
    public_repos = user_json['public_repos']
    public_reposs.append(public_repos)
    public_gists = user_json['public_gists']
    public_gistss.append(public_gists)
    followers = user_json['followers']
    followerss.append(followers)
    following = user_json['following']
    followings.append(following)
    created_at = user_json['created_at']
    created_ats.append(created_at)


# In[10]:


## Insert all the values into the table created 

# Connect to MySQL server
conn = mysql.connector.connect(host='localhost',user='root',database = "github",password='wyz710522')
# Create a cursor to execute SQL queries
cursor = conn.cursor()
# Insert the fetched values into the table 
query_Insert = f"INSERT INTO {SQL_TABLE_CONTRIBUTORS} (login, user_id, location, email, hireable, bio, twitter_username, public_repos, public_gists, followers, following, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
values = []
for i in range(len(logins)) :
    row = (logins[i], user_ids[i], locations[i], emails[i], hireables[i], bios[i], twitter_usernames[i], 
           public_reposs[i], public_gistss[i], followerss[i], followings[i], created_ats[i])
    values.append(row)
cursor.executemany(query_Insert, values)

# Commit changes to the database
conn.commit()
# Close connection
conn.close()


# 5. Optimize your code in (4) to allow for quick look-ups of "login", "location", and "hireable".  What choices do you make and why?

# **Optmized code by indexing the three columns**

# In[11]:


## Create another Table using the method of Indexd columns in the database 

# Connect to MySQL server
conn = mysql.connector.connect(host='localhost',user='root',database = 'github',password='wyz710522')
# Create a cursor to execute SQL queries
cursor = conn.cursor()
# Create a new table if not exist to include all the columns needed
SQL_TABLE_CONTRIBUTORS_NEW = "Contributors_New"
SQL_TABLE_CONTRIBUTORS_NEW_DEF = "(" +         "login VARCHAR(300)," +         "user_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY," +         "location VARCHAR(300)," +         "email VARCHAR(300)," +         "hireable INT," +         "bio VARCHAR(300)," +         "twitter_username VARCHAR(300)," +         "public_repos INT," +         "public_gists INT," +         "followers INT," +         "following INT," +         "INDEX (login)," +         "INDEX (location)," +         "INDEX (hireable)," +         "created_at VARCHAR(300)" +         ")"
query_Table = "CREATE TABLE IF NOT EXISTS " + SQL_DB + "." + SQL_TABLE_CONTRIBUTORS_NEW + " " + SQL_TABLE_CONTRIBUTORS_NEW_DEF + ";";
cursor.execute(query_Table)


# In[12]:


## Fetch all the content of the table
token = 12345 #(here will needs to be your own token)
headers = {'Authorization' : 'token ' + token}
url = 'https://api.github.com/repos/apache/hadoop/contributors'
response = requests.get(url,headers = headers, params={'per_page': 100})
contributors_json = response.json()
        
logins = []
user_ids = []
locations = []
emails = []
hireables = []
bios = []
twitter_usernames = []
public_reposs = []
public_gistss  = []
followerss = []
followings = []
created_ats = []
        
for contributor in contributors_json:
    user_url = contributor['url']
    user_response = requests.get(user_url, headers = headers)
    user_json = user_response.json()
    login = user_json['login']
    logins.append(login)
    user_id = user_json['id']
    user_ids.append(user_id)
    location = user_json['location']
    locations.append(location)
    email = user_json['email']
    emails.append(email)
    hireable = user_json['hireable']
    hireables.append(hireable)
    bio = user_json['bio']
    bios.append(bio)
    twitter_username = user_json['twitter_username']
    twitter_usernames.append(twitter_username)
    public_repos = user_json['public_repos']
    public_reposs.append(public_repos)
    public_gists = user_json['public_gists']
    public_gistss.append(public_gists)
    followers = user_json['followers']
    followerss.append(followers)
    following = user_json['following']
    followings.append(following)
    created_at = user_json['created_at']
    created_ats.append(created_at)


# In[13]:


## Insert all the values into the table created 

# Connect to MySQL server
conn = mysql.connector.connect(host='localhost',user='root',database = "github",password='wyz710522')
# Create a cursor to execute SQL queries
cursor = conn.cursor()
# Insert the fetched values into the table 
query_Insert = f"INSERT INTO {SQL_TABLE_CONTRIBUTORS_NEW} (login, user_id, location, email, hireable, bio, twitter_username, public_repos, public_gists, followers, following, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
values = []
for i in range(len(logins)) :
    row = (logins[i], user_ids[i], locations[i], emails[i], hireables[i], bios[i], twitter_usernames[i], 
           public_reposs[i], public_gistss[i], followerss[i], followings[i], created_ats[i])
    values.append(row)
cursor.executemany(query_Insert, values)

# Commit changes to the database
conn.commit()
# Close connection
conn.close()


# **Check the difference of speed of running**

# In[27]:


# Previous Method
conn = mysql.connector.connect(host='localhost',user='root',database = "github",password='wyz710522')
start = time.time()
cursor = conn.cursor()
cursor.execute("SELECT login , user_id , location FROM Contributors WHERE location in ('San Francisco','Tokyo','Seattle')")
result = cursor.fetchall()
end = time.time()
# The time of executing 
execution_time = end - start
print("Previous Method's Execution Time is {}".format(execution_time))


# In[28]:


# After we indexed the columns
conn = mysql.connector.connect(host='localhost',user='root',database = "github",password='wyz710522')
start_new = time.time()
cursor = conn.cursor()
cursor.execute("SELECT login , user_id , location FROM Contributors_New WHERE location in ('San Francisco','Tokyo','Seattle')")
result = cursor.fetchall()
end_new = time.time()
# The time of executing 
execution_time_new = end_new - start_new
print("Current Method's Execution Time is {}".format(execution_time_new))


# In[29]:


# % Increase of Speed
per_speed_increase = round(((execution_time - execution_time_new) / execution_time)*100,2)
print("The speed has been increased by {}% after we indexed the columns".format(per_speed_increase))

