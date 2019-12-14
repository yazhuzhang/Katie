
# coding: utf-8

# In[3]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# In[4]:


HelpDesk = pd.read_csv("/Yazhu/Uconn/5894/Assignments/HelpDesk.csv")
HelpDesk.head()


# In[5]:


HelpDesk.dtypes


# In[6]:


obj_df = HelpDesk.copy()
obj_df.head()


# In[7]:


obj_df["RequestorSeniority"] = obj_df["RequestorSeniority"].astype('category')
obj_df["FiledAgainst"] = obj_df["FiledAgainst"].astype('category')
obj_df["TicketType"] = obj_df["TicketType"].astype('category')
obj_df["Severity"] = obj_df["Severity"].astype('category')
obj_df["Priority"] = obj_df["Priority"].astype('category')
obj_df["Satisfaction"] = obj_df["Satisfaction"].astype('category')
obj_df.dtypes


# In[8]:


obj_df["RequestorSeniority"] = obj_df["RequestorSeniority"].cat.codes
obj_df["FiledAgainst"] = obj_df["FiledAgainst"].cat.codes
obj_df["TicketType"] = obj_df["TicketType"].cat.codes
obj_df["Severity"] = obj_df["Severity"].cat.codes
obj_df["Priority"] = obj_df["Priority"].cat.codes
obj_df["Satisfaction"] = obj_df["Satisfaction"].cat.codes
obj_df.head()


# In[9]:


X = obj_df[['RequestorSeniority', 'ITOwner', 'FiledAgainst', 'TicketType','Severity','Priority','daysOpen']]
y = obj_df['Satisfaction']


# In[10]:


#Hold-out validation
from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=123)


# In[18]:


#KNN Model
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
#making the instance
model = KNeighborsClassifier(n_jobs=-1)
#Hyper Parameters Set
n = list(range(1,50))
params = {'n_neighbors': n}
#Making models with hyper parameters sets
model1 = GridSearchCV(model, param_grid=params, n_jobs=1)
#Learning
model1.fit(X_train,y_train)
#The best hyper parameters set
print("Best Hyper Parameters:\n",model1.best_params_)
#Prediction
prediction=model1.predict(X_test)
#importing the metrics module
from sklearn import metrics
#evaluation(Accuracy)
print("Accuracy:",metrics.accuracy_score(prediction,y_test))
#evaluation(Confusion Metrix)
print("Confusion Metrix:\n",metrics.confusion_matrix(prediction,y_test))
#Best K =47 and the accuracy of KNN Model is 0.3442, not a good fit model for the data

