
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import os


# In[2]:


###1-2. concat the dataset into a dataframe


# In[3]:


import glob

path = r'C:\Users\haoyu\Downloads\spotify_top200_viral50_data' 
all_files = glob.glob(path + "/*.csv")

li = []

for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    li.append(df)

rawdata = pd.concat(li, axis=0, ignore_index=True)


# In[4]:


rawdata


# In[190]:


###3. drop the columns


# In[6]:


rawdata.drop(['Album(s)', 'UPC','Latest Charting Date', 'Spotify Track Link', 'Spotify Artist Link', 'Spotify Album Link', 'Streams','Chart Cycle'],axis=1,inplace = True)


# In[7]:


###4. rename the columns


# In[8]:


rawdata.rename(columns={'Track':'track', 'ISRC':'isrc', 'Spotify Track Ids':'track_id', 'Artist(s)':'artist', 'Spotify Artist Id(s)':'artist_id', 'Spotify Album Ids':'album_id', 'Release Date': 'r_date', 'Record Label' : 'label', 'Country':'country', 'Days on Chart':'days_chart', 'Chart Type':'chart_type', 'Peak Position':'peak_pos', 'Peak Date':'peak_date', 'Latest Position':'latest_pos', 'Position Change':'pos_chg', 'Historical Positions':'hist_pos'}, inplace=True)


# In[9]:


###5. change the dtype


# In[10]:


rawdata['artist'] = rawdata['artist'].astype(str)
rawdata['track'] = rawdata['track'].astype(str)


# In[11]:


###6. fill NA


# In[12]:


rawdata.fillna('UNKNOWN', inplace=True)


# In[13]:


###7. create prev_pos


# In[84]:


rawdata.hist_pos[0].split(",")[-2]


# In[100]:


len(rawdata.hist_pos[0].split(","))


# In[102]:


a = []
for i in range(1750):
    if len(rawdata.hist_pos[i].split(",")) >1:
        a.append(rawdata.hist_pos[i].split(",")[-2])
    else:
        a.append(rawdata.hist_pos[i].split(",")[-1])


# In[104]:


len(a)


# In[48]:


a = [[1,2,30,4],[2,3,50,1]]
rawdata.hist_pos


# In[105]:


rawdata['next_to_last'] = a
rawdata


# In[ ]:


###8. create pos_chg


# In[ ]:


###9. input the off limit data and drop the rows


# In[354]:


path = r'C:\Users\haoyu\Downloads\spreadsheet' 
all_files = glob.glob(path + "/*.xlsx")

li = []

for filename in all_files:
    df = pd.read_excel(filename, index_col=None, header=0)
    li.append(df)

listtodrop = pd.concat(li, axis=0, ignore_index=True)


# In[355]:


listtodrop


# In[356]:


gg = rawdata.artist.str.lower().isin(listtodrop.artist.str.lower())
mask = (gg == False)
katie = rawdata[mask]
katie


# In[357]:


ff = katie.label.str.lower().isin(listtodrop.label.str.lower())
mask1 = (ff == False)
rawdata = katie[mask1]
rawdata


# In[288]:


####10. create a freq column and apply it to dataframe


# In[358]:


rawdata['freq'] = rawdata.groupby('artist')['artist'].transform('count')
rawdata


# In[292]:


###11. rearrange the columns


# In[379]:


newdata = rawdata[['artist', 'track', 'r_date', 'label', 'country','chart_type', 'latest_pos','days_chart', 'freq', 'peak_pos', 'peak_date', 'pos_chg', 'hist_pos',  'track_id', 'artist_id', 'album_id', 'isrc']]
newdata


# In[380]:


newdata['artist_id']


# In[360]:


import requests 


# In[ ]:


###2. I use postman to help me get the access token, if you get a access token, simply copy and paste it after Bearer in headers 


# In[321]:


r=requests.get("https://api.spotify.com/v1/tracks/4y3OI86AEP6PQoDE6olYhO", headers={"Authorization":"Bearer BQBOqQ7WlbR5fTAmcpdws6XTA7mcL8c4faLbLosHaZri3HFJHmo6oNevM0vwNJpNuDFBBozFyFx76YbzOFvmQ7J8AJy8WfSDA2RaJIZkNmFKUvmydSVWblf5b3VAFqIGiwBuCXm6Whc38c9I5rxP-Y7KPKFcHl6HBNraabuVoCntdANXZpI6"})


# In[ ]:


###3. With each track_id, get track_uri, apply it into dateframe


# In[361]:


b = []
for i in newdata['track_id']:
    r=requests.get("https://api.spotify.com/v1/tracks/"+i, headers={"Authorization":"Bearer BQBOqQ7WlbR5fTAmcpdws6XTA7mcL8c4faLbLosHaZri3HFJHmo6oNevM0vwNJpNuDFBBozFyFx76YbzOFvmQ7J8AJy8WfSDA2RaJIZkNmFKUvmydSVWblf5b3VAFqIGiwBuCXm6Whc38c9I5rxP-Y7KPKFcHl6HBNraabuVoCntdANXZpI6"})
    b.append(r.json()['uri'])


# In[362]:


newdata['track_uri'] = b
newdata


# In[ ]:


###3. With each track_id, get popularity score, apply it into dataframe


# In[363]:


c = []
for i in newdata['track_id']:
    r=requests.get("https://api.spotify.com/v1/tracks/"+i, headers={"Authorization":"Bearer BQBOqQ7WlbR5fTAmcpdws6XTA7mcL8c4faLbLosHaZri3HFJHmo6oNevM0vwNJpNuDFBBozFyFx76YbzOFvmQ7J8AJy8WfSDA2RaJIZkNmFKUvmydSVWblf5b3VAFqIGiwBuCXm6Whc38c9I5rxP-Y7KPKFcHl6HBNraabuVoCntdANXZpI6"})
    c.append(r.json()['popularity'])


# In[364]:


newdata['sp'] = c
newdata


# In[ ]:


###3. With each album_id, get release_date, apply it into dataframe


# In[365]:


d = []
for i in newdata['album_id']:
    r=requests.get("https://api.spotify.com/v1/albums/"+i, headers={"Authorization":"Bearer BQBOqQ7WlbR5fTAmcpdws6XTA7mcL8c4faLbLosHaZri3HFJHmo6oNevM0vwNJpNuDFBBozFyFx76YbzOFvmQ7J8AJy8WfSDA2RaJIZkNmFKUvmydSVWblf5b3VAFqIGiwBuCXm6Whc38c9I5rxP-Y7KPKFcHl6HBNraabuVoCntdANXZpI6"})
    d.append(r.json()['release_date'])


# In[366]:


newdata['r_date'] = d
newdata


# In[ ]:


###4. With each album_id, get label, apply it into dataframe


# In[367]:


a = []
for i in newdata['album_id']:
    r=requests.get("https://api.spotify.com/v1/albums/"+i, headers={"Authorization":"Bearer BQBOqQ7WlbR5fTAmcpdws6XTA7mcL8c4faLbLosHaZri3HFJHmo6oNevM0vwNJpNuDFBBozFyFx76YbzOFvmQ7J8AJy8WfSDA2RaJIZkNmFKUvmydSVWblf5b3VAFqIGiwBuCXm6Whc38c9I5rxP-Y7KPKFcHl6HBNraabuVoCntdANXZpI6"})
    a.append(r.json()['label'])


# In[368]:


newdata['label'] = a
newdata


# In[ ]:


###5 I failed to get the artist's popularity score


# In[384]:


e = []
for i in newdata['artist_id']:
    r=requests.get("https://api.spotify.com/v1/artists/"+i, headers={"Authorization":"Bearer BQCsLSiUbTqhWEi7LeIAr952ifjjb_4vL1hXRjMj0x2iyJfu4QyuXE3RXxtK0GTaXZMdL9kz-kuETEo4n8Ew5w1vw5gPOB-Lu9zx85fmED-KYSnXFb7yPbr5hWQGfVYlAGxSntFbqZgI86qyytrOv9o5JAMyQU8SQfi3T7ykSx3I5E3oqPGh"})
    print(r.json())


# In[ ]:


###8. Drop all songs before 2018-06-01


# In[369]:


start_date = '2018-06-01'
mask = (newdata['r_date'] > start_date)
newdata = newdata.loc[mask]
len(newdata)


# In[ ]:


###9. Remove from off_limits excelsheet


# In[370]:


hh = newdata.artist.str.lower().isin(listtodrop.artist.str.lower())
mask = (hh == False)
newdata = newdata[mask]
newdata


# In[371]:


yy = newdata.label.str.lower().isin(listtodrop.label.str.lower())
mask = (yy == False)
newdata = newdata[mask]
len(newdata)


# In[ ]:


###10. sort the dataframe


# In[372]:


newdata.sort_values(by=['latest_pos','days_chart','freq'], ascending = [True,False,False])


# In[ ]:


###11. Select First 20


# In[373]:


newdata = newdata.head(20)
len(newdata)


# In[344]:


###12. Arrange the columns


# In[374]:


newdata.drop(['track_id','album_id','artist_id','isrc'],axis = 1, inplace = True)


# In[375]:


newdata.columns


# In[376]:


newdata = newdata[['artist', 'track', 'r_date', 'label', 'sp','country','chart_type', 'latest_pos','days_chart', 'freq', 'peak_pos', 'peak_date', 'pos_chg', 'hist_pos',  'track_uri' ]]
newdata


# In[ ]:


###13. Export to excel


# In[378]:


newdata.to_excel('Katie final report.xlsx', sheet_name='sheet1', index=False)


# In[ ]:


{
    "snapshot_id": "Myw0M2Y5NmQ4MGRjYTY3Mzk3ZGYyODA0NjRjYTdmYTMzMGE0MmJmYjg4"
}

