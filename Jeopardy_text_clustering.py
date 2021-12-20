#!/usr/bin/env python
# coding: utf-8

# OBJECTIVES: 
# 1. Frequency of subjects over the years
# 2. Breakdown of question value by subject and analyze question complexity by question value
# 3. Description of patterns in Final Jeopardy questions
#  
# *THIS CODE IS BUILDING THE MODEL ON THE Q, A, and C*
#  
# NOTES / UPDATES:
# - Mark's original csv had dollar signs in the values column, mine did not so if yours does you will have to ask Mark for the code to remove the dollar signs
# - This code removes jpegs, html, and targetblanks
# - I applied the cleansing function to the Category column and renamed it 'C' (didn't do this previously and the clustering technique may not have captured Category as accurately since punctuation was not removed and it was not all lowercase)
# - High value is specified as anything greater than 800, there is no reasoning. If someone prefers a different cutoff to determine what is a high value, we can absolutely change it
# - This does not include Mark's summary stats for each cluster

# In[2]:


import pandas as pd
import seaborn as sns
import nltk
from pandasql import sqldf
from pandas import DataFrame
from sentiment_module import sentiment
from afinn import Afinn
afinn = Afinn(language='en')


# In[3]:


#Read in CSV
jep = pd.read_csv("file:///C:/Users/sehoc/OneDrive/Desktop/Fall%202/Text%20Analysis/Data/jeopardy.csv")


# In[4]:



#Make Question and Answer a string 
import string
jep["Answer"] = jep[" Answer"].astype(str) #Also got rid of the space before Answer
jep["Question"] = jep[" Question"].astype(str) #Also got rid of the space before Question

#Make value a string
jep["Value"] = jep[" Value"].astype(str) #Also got rid of the space before Value


# In[5]:


#Function to get rid of punctuation and make it all lowercase
def cleansing(x):
    x = x.lower() #Make it lowercase
    x = "".join((char for char in x if char not in string.punctuation)) #Remove punctuation
    return x

#Apply function
jep["A"] = jep["Answer"].apply(cleansing)
jep["Q"] = jep["Question"].apply(cleansing)
jep["C"] = jep[" Category"].apply(cleansing)


# In[6]:


#Pull out just the year and month to evaluate trend over time
jep['Year'] = pd.DatetimeIndex(jep[" Air Date"]).year
jep['Month'] = pd.DatetimeIndex(jep[" Air Date"]).month


# In[7]:


#Drop uneccessary columns
jep = jep.drop("Show Number", axis=1)
jep = jep.drop(" Air Date", axis=1)
jep = jep.drop(" Question", axis=1)
jep = jep.drop(" Answer", axis=1)
jep = jep.drop("Question", axis=1)
jep = jep.drop("Answer", axis=1)


# In[8]:


#Some more cleaning and renaming columns to get rid of the extra space
jep["Category"] = jep[" Category"]
jep["Round"] = jep[" Round"]
jep = jep.drop(" Value", axis=1)
jep = jep.drop(" Category", axis=1)
jep = jep.drop(" Round", axis=1)


# In[9]:


#Get rid of values that are 'None' and make them 0
#This is for visualization purposes and so when we make def highvalue it does not have any errors
mask = (jep.Value == 'None')
jep.Value = jep.Value.mask(mask,'0')

#Make Value an integer
jep.Value = jep.Value.astype(int)


# In[10]:



#Calculate sentiment based on the affin score
jep["Answer_Sentiment"] = jep["A"].apply(afinn.score) #This creates a column called "Answer_Sentiment" which is the sentiment present in the "A" column
jep["Question_Sentiment"] = jep["Q"].apply(afinn.score) #This creates a column called "Question_Sentiment" which is the sentiment present in the "Q" column
jep["Total_Sentiment"] = jep[['Answer_Sentiment', 'Question_Sentiment']].sum(axis=1) #This adds up the sentiment scores (sentiment is evaluated on a word by word basis) for Q and A so we can see the total sentiment for that observation 


# In[11]:


#remove JPEG from dataset
filt = []
for i in range(len(jep)):
    if ((jep["Q"][i].find('jpg') != -1) or (jep["Q"][i].find('href') != -1) or (jep["Q"][i].find('targetblank') != -1)):
        filt.append(i)
jep = jep.drop(index = filt)
jep = jep.reset_index()
jep = jep.drop("index", axis=1)


# In[12]:


#Lets analyze high value vs low value Jeopardy questions

def highvalue(row):
    value = 0 #Initializes it so every observation is 0
    if row['Value'] > 800: #Looks at the Value column and if the Value is > 800, then the observation is 1, if it isn't it remains 0 because we initialized it at 0
        value = 1
    return value #This is what tells us what the function did

jep['If_High_Value'] = jep.apply(highvalue, axis =1) #Creates a column "If_High_Value", then applies the highvalue function to jep and axis=1 tells the function to look at the first axis and use the column that is called "Value" which is specified by 'if row["Value"]' in the function 


# In[13]:


#This concatenates A, Q, and Category to make one long string and puts it in the "Con_Text" column
jep["Con_Text"] = jep['A'].map(str) + ' ' + jep['Q'].map(str) + ' ' + jep['C'].map(str)


# In[14]:


from sklearn.cluster import MiniBatchKMeans
from sklearn.feature_extraction.text import TfidfVectorizer


# In[15]:


random_state = 0 #This is like a seed, so it makes analzying as a team easier / more coherent (I think)
n_topics = 25 #This is to say how many clusters we want, I'm going to do 25 since we are going to recategorize anyways

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

vec = TfidfVectorizer(max_features=5000, stop_words="english", max_df=0.95, min_df=2) #This removes stop words and preps the data to be clustered 
features = vec.fit_transform(jep.Con_Text) #This finds the features for the model we are building

from sklearn.decomposition import NMF
cls = NMF(n_components=n_topics, random_state=random_state) #Tells it how many topics and the seed aka random_state
cls.fit(features) #Fit the features found from above


# In[16]:


#Generate list of unique words found by the vectorizer
feature_names = vec.get_feature_names()


# In[17]:


#This is a description of each cluster
#The output is sorted so that the words with the highest scores are returned in descending order aka the first words are more influential / descriptive about the cluster compared to the last word for that cluster
n_top_words = 15 #Change this number to see more words 

for i, topic_vec in enumerate(cls.components_):
    print(i, end=' ')
    for fid in topic_vec.argsort()[-1:-n_top_words-1:-1]:
        print(feature_names[fid], end=' ')
    print()
    
#This is what will be copy and pasted into a Google Sheets so we can assign latent factors


# In[ ]:


print ("\nUnique values :  \n", jep.nunique())


# In[18]:


#Apply the clustering function to the Q and A columns
qx = cls.transform(vec.transform(jep.Q)).argsort(axis=1)[:,-1]
ax = cls.transform(vec.transform(jep.A)).argsort(axis=1)[:,-1]
x = cls.transform(vec.transform(jep.C)).argsort(axis=1)[:,-1]

jep["ReAnswer"] = ax #Create a column that shows what cluster just the Answer is in
jep["ReQuestion"] = qx #Create a column that shows what cluster just the Question is in
jep["ReCategory"] = x #Create a column that shows what cluster just the Category is in


# In[19]:


#Apply the function to the concatenated column (same as above but to the concatenated text column)
conx = cls.transform(vec.transform(jep.Con_Text)).argsort(axis=1)[:,-1]
jep["ReCon_Text"] = conx


# In[20]:


#This output is based on a clustering model built on Q, A and C
jep.to_csv(r'C:\Users\sehoc\OneDrive\Desktop\jep_output_QAC.csv')


# In[ ]:




