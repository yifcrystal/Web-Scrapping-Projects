#!/usr/bin/env python
# coding: utf-8

# # Homework 07 Yifan(Crystal)CAI

# Write Python or Java code that
# - creates a MongoDB DB called "amazon"
# - reads "reviews_electronics.16.json" and uploads each review as a separate document to the collection "reviews" in the DB "amazon".
# - uses MongoDB's map reduce function to build a new collection "avg_scores" that averages review scores by product ("asin"). Print the first 100 entries of "avg_scores" to screen.
# - uses MongoDB's map reduce function to build a new collection "weighted_avg_scores" that averages review scores by product ("asin"), weighted by the number of votes + 1 (the second number + 1). Print the first 100 entires of "weighted_avg_scores" to screen.
# 
#  
# 
# The format of "reviews_electronics.16.json" is:
# - reviewerID - ID of the reviewer, e.g. A2SUAM1J3GNN3B
# - asin - ID of the product, e.g. 0000013714
# - reviewerName - name of the reviewer
# - helpful - helpfulness rating of the review, e.g. 2/3
# - reviewText - text of the review
# - overall - rating of the product
# - summary - summary of the review
# - unixReviewTime - time of the review
# 
# 
# Please submit one .py, .ipynb, or .java file.

# In[23]:


get_ipython().system('pip install pymongo==4.0')


# In[24]:


import pymongo
import json
from pymongo import MongoClient


# In[25]:


print(pymongo.__version__)


# Creates a MongoDB DB called "amazon" 

# In[26]:


# Connect to MongoDB
username = 'xxx'
password = 'xxx'
db = 'amazon'
connection_string = f'mongodb+srv://{username}:{password}@cluster0.avsc5qq.mongodb.net/{db}?appName=mongosh+1.7.1'
client = MongoClient(connection_string)


# In[3]:


# Database : amazon
amazon = client['amazon']
# Collection : reviews
reviews = amazon['reviews']


# Reads "reviews_electronics.16.json" and uploads each review as a separate document to the collection "reviews" in the DB "amazon".

# In[4]:


# Read Json file
with open("reviews_electronics.16.json","r") as file:
    reviews = file.readlines()


# In[12]:


# len(reviews)
# 324546/5000
# 64*5000
type(reviews)


# In[14]:


# Insert rows into the database by batches of 5000 each
size = 5000
for i in range(0, len(reviews), size):
    batch = reviews[i:i+size]
    parsed_batch = [json.loads(review) for review in batch]
    result = amazon.reviews.insert_many(parsed_batch)
    print(f"Uploaded {len(result.inserted_ids)} reviews. Total uploaded: {i+len(result.inserted_ids)}/{len(reviews)}")


# Use MongoDB's map reduce function to build a new collection "avg_scores" that averages review scores by product ("asin"). Print the first 100 entries of "avg_scores" to screen.

# **Comment:** <br>
# Here I tried to use MapReduce but it's said MapReduce has been deprecated and though I've downgrade my current version of MongoDB it's still not working. So I decided to use aggregate as substitution of MapReduce.

# In[36]:


# # Map reduce function for average review score
# avg_scores = amazon.reviews.mapReduce(
#     "function() {emit(this.asin, this.overall);}",
#     "function(key, values) {return Array.avg(values)}",
#     "avg_scores")


# In[35]:


amazon.reviews.aggregate([
    {"$group": {"_id": "$asin", "avgScore": {"$avg": "$overall"}}},
    {"$out": "avg_scores"}
])


# In[38]:


# Print the first 100 entries of "avg_scores" to screen
cursor = amazon.avg_scores.find().limit(100)
for document in cursor:
    print(document)


# Use MongoDB's map reduce function to build a new collection "weighted_avg_scores" that averages review scores by product ("asin"), weighted by the number of votes + 1 (the second number + 1). Print the first 100 entires of "weighted_avg_scores" to screen.

# In[47]:


pipeline = [
    {"$project": {"_id": 0,"asin": 1,"helpful_votes": {"$arrayElemAt": ["$helpful", 1]},"overall": 1}},
    {"$project": {"asin": 1,
                  "weighted_score": {"$multiply": [{"$add": ["$helpful_votes", 1]}, "$overall"]},
                  "weight": {"$add": ["$helpful_votes", 1]}}},
    {"$group": {"_id": "$asin","weighted_score": {"$sum": "$weighted_score"},"weight": {"$sum": "$weight"}}},
    {"$project": {"asin": "$_id",
                  "weighted_avg_score": {"$divide": ["$weighted_score", "$weight"]},
                  "_id": 0}},
    {"$out": "weighted_avg_scores"}
]

result = amazon.reviews.aggregate(pipeline)


# In[48]:


# Print the first 100 entries of "weighted_avg_scores" to screen
cursor = amazon.weighted_avg_scores.find().limit(100)
for document in cursor:
    print(document)

