#!/usr/bin/env python
# coding: utf-8

# # Homework 06 Yifan(Crystal)CAI

# ### Connect MongoDB to JupyterNotebook

# In[1]:


get_ipython().system('pip install pymongo')


# In[2]:


import pymongo
from pymongo import MongoClient


# In[3]:


username = 'xxx'
password = 'xxx'
database = 'samples_pokemon'
connection_string = f'mongodb+srv://{username}:{password}@cluster0.avsc5qq.mongodb.net/{database}?appName=mongosh+1.7.1'
client = MongoClient(connection_string)


# 1. Please write code to query and print to screen all Pokémon character “name”s (and “_id” but not the entire document) with candy_count >= month + day of your birthday  (e.g., my birthday is 2/12 and I query candy_count >= 14 as 2+12 = 14).  

# In[4]:


# Database : sample_pokemon
pokemon = client['samples_pokemon']

# Collection : sample_pokemon
pokemon_data = pokemon['samples_pokemon']

# Query : My birthday is at 07/16, so  candy_count >= 23
query01 = {'candy_count': {'$gte': 23}}

# Retrieve requested data
for pokemon in pokemon_data.find(query01, {"name": 1,'_id':1}):
    print(pokemon)


# 2. Please write code to query and print to screen all Pokémon character “name”s (and “_id” but not the entire document) with num = month or num = day of your birthday  (e.g., my birthday is 2/12 and I have to query num = 2 or num = 12). 

# In[5]:


# Query
query02 = {"$or": [{"num": '007'}, {"num": '016'}]}

# Retrieve requested data
for pokemon in pokemon_data.find(query02, {"name": 1,'_id':1}):
    print(pokemon) 


# 3. Please write code to query and print to screen all Crunchbase company “name”s (and “_id” but not the entire document) that have “text” in their “tag_list”.  

# In[41]:


# Database : crunchbase
crunchbase = client['crunchbase']

# Collection : crunchbase
crunchbase_data = crunchbase['crunchbase_database']

# Query
query03 = ({"tag_list" : {'$regex' : "\w*\\btext\\b"}})

# Retrieve requested data
for cb in crunchbase_data.find(query03, {"name": 1,'_id':1, 'tag_list':1}):
    print(cb) 


# 4. Please write code to query and print to screen all Crunchbase company “name”s and “twitter_username” (and “_id” but not the entire document) that (i) were founded between 2000 and 2010 (including 2000 and 2010), or (ii) email address is ending in “@gmail.com”. 

# In[46]:


# Query
query04 = {"$or": [{"founded_year": {'$gte': 2000, '$lte': 2010}}, 
                   {"email_address": {'$regex' : ".+@gmail.com"}}]}

# Retrieve requested data
for cb in crunchbase_data.find(query04, {"name": 1,"twitter_username":1,'_id':1, 'founded_year' :1,"email_address":1 }):
    print(cb) 

