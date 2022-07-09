#!/usr/bin/env python
# coding: utf-8

# In[33]:


import requests
from bs4 import BeautifulSoup

def get_topics_page():
    # TODO - add comments
    topic_url = 'https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=100&start=000&ref_=adv_next'
    response=requests.get(topic_url)
    # check successfull response
    if response.status_code != 200:
        raise Exception(f'Failed to load page {topic_url}')
    # Parse using BeautifulSoup
    doc = BeautifulSoup(response.text, 'html.parser')
    return doc


# In[34]:


doc=get_topics_page()


# In[35]:


def get_movie_titles(doc):
    
    selection_class="lister-item-header"
    movie_title_tags=doc.find_all('h3',{'class':selection_class})
    movie_titles=[]

    for tag in movie_title_tags:
        title = tag.find('a').text
        movie_titles.append(title)
        
        
    return movie_titles


# In[37]:


titles = get_movie_titles(doc)


# In[38]:


titles[:5]


# In[39]:


def get_movie_year(doc):
    year_selector = "lister-item-year text-muted unbold"           
    movie_year_tags=doc.find_all('span',{'class':year_selector})
    movie_year_tagss=[]
    for tag in movie_year_tags:
        movie_year_tagss.append(tag.get_text().strip()[1:5])
    return movie_year_tagss


# In[40]:


years = get_movie_year(doc)


# In[41]:


years[:5]


# In[42]:


def get_movie_url(doc):
    url_selector="lister-item-header"           
    movie_url_tags=doc.find_all('h3',{'class':url_selector})
    movie_url_tagss=[]
    base_url = 'https://www.imdb.com/'
    for tag in movie_url_tags:
        movie_url_tagss.append('https://www.imdb.com/' + tag.find('a')['href'])
    return movie_url_tagss


# In[43]:


urls = get_movie_url(doc)


# In[44]:


urls[:5]


# In[45]:


def get_movie_rating(doc):
    rating_selector="inline-block ratings-imdb-rating"            
    movie_rating_tags=doc.find_all('div',{'class':rating_selector})
    movie_rating_tagss=[]
    for tag in movie_rating_tags:
        movie_rating_tagss.append(tag.get_text().strip())
    return movie_rating_tagss


# In[46]:


ratings = get_movie_rating(doc)


# In[47]:


ratings[:5]


# In[48]:


def get_movie_duration(doc):
    
    selection_class="runtime"
    movie_duration_tags=doc.find_all('span',{'class':selection_class})
    movie_duration=[]

    for tag in movie_duration_tags:
        duration = tag.text[:-4]
        movie_duration.append(duration)
        
        
    return movie_duration


# In[49]:


durations = get_movie_duration(doc)


# In[50]:


durations[:5]


# def get_movie_genre(doc):
#     select_class="genre"
#     movie_genre_tags=doc.find_all('span',{'class':select_class})
#     movie_genre=[]
# 
#     for tag in movie_genre_tags:
#         genre = tag.text[:-4]
#         movie_genre.append(tag.get_text().strip())
#         
#         
#     return movie_genre
#     

# genres = get_movie_genre(doc)

# genres[:5]

# In[98]:


def get_movie_certificate(doc):
    selects_class="certificate"
    movie_certificate_tags=doc.find_all('span',{'class':selects_class})
    movie_certificate=[]

    for tag in movie_certificate_tags:
        certificate = tag.text[:-4]
        movie_certificate.append(tag.get_text().strip())
        
        
    return movie_certificate


# In[99]:


certificates = get_movie_certificate(doc)


# In[100]:


certificates[:5]


# In[101]:


import pandas as pd


# In[127]:


def all_pages():
# Let's we create a dictionary to store data of all movies
    movies_dict={
        'title':[],
    
        'duration':[],
        'rating':[],
        'year':[],
      
        'url':[]
    }
  # We have to scrap more than one page so we want urls of all pages with the help of loop we can get all urls
    for i in range(1,2000,100):
       
        try:
            url = 'https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=100&start='+str(i)+'&ref_=adv_next'
            response = requests.get(url)
        except:
            break
        
        if response.status_code != 200:
            break
           
    # Parse using BeautifulSoup
        doc = BeautifulSoup(response.text, 'html.parser')
        titles = get_movie_titles(doc)
        urls = get_movie_url(doc)
        
        ratings = get_movie_rating(doc)
        durations = get_movie_duration(doc)
        years = get_movie_year(doc)
        
    
        
    # We are adding every movie data to dictionary
        for i in range(len(titles)):
            movies_dict['title'].append(titles[i])
          
            movies_dict['duration'].append(durations[i])
            movies_dict['rating'].append(ratings[i])
            movies_dict['year'].append(years[i])
            
            movies_dict['url'].append(urls[i])
        
    return pd.DataFrame(movies_dict)


# In[128]:


movies_dict={
    'title':titles,
    'duration':durations,
    'rating':ratings,
    'year':years,
    'url':urls
}


# In[129]:


df = pd.DataFrame(movies_dict)


# In[130]:


df.head()


# In[131]:


movies = all_pages()


# In[132]:


movies.to_csv('movies.csv',index=None)


# In[ ]:




