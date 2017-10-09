
# coding: utf-8

# In[28]:

#import packages 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import requests
from scipy.stats import norm
from sklearn.preprocessing import StandardScaler
from scipy import stats
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings('ignore')
get_ipython().magic('matplotlib inline')


# In[29]:

credits = pd.read_csv("C:/Users/Darran_K/Documents/Dataquest Practicals/TMDB_5000/tmdb_5000_credits.csv")
movies = pd.read_csv("C:/Users/Darran_K/Documents/Dataquest Practicals/TMDB_5000/tmdb_5000_movies.csv")
del credits['title']


# In[30]:

df = pd.concat([movies, credits], axis=1)
priint(df.head)
newCols = ['id','title','release_date','vote_average','vote_count',
           'budget','revenue','genres','keywords','cast','crew','tagline', 'runtime', 'production_companies', 
           'production_countries', 'status']
df = df[newCols]
#print(df.head())


# In[31]:

#df.plot.scatter("budget", "revenue")


# In[32]:

#change budget and revenue into millions for easier reading
df["budget"] = df["budget"]/ 1000000
df["revenue"] = df["revenue"]/ 1000000


# In[33]:

#remove all rows that contain a 0 / keep all that do not have a 0
df = df[(df != 0).all(1)]


# In[34]:

df["RoI"] = df["revenue"]/df["budget"]


# In[35]:

df= df.reset_index()
#print(df.iloc[df["RoI"].idxmax(),:])


# In[36]:

#print(df["release_date"].max())


# In[37]:

def find_year(date):
    splits = date.split("-")
    return splits[0]


# In[38]:

#df.groupby("release_date").RoI.max()
df["release_year"] = df["release_date"].apply(find_year)


# In[39]:

#extract release year from dates
x = df.groupby("release_year").RoI.max()
df.groupby("release_year").RoI.idxmax()
#3077
#2522
# Remove films that appear to be outliers. revenue/budget score is not close to any other film
outliers = [3077, 2522]
df.drop(df.index[outliers], inplace=True)


# In[54]:

print(df.iloc[3077,:])


# In[40]:

#plot some graphs
#3223
#3218
#3215
#plt.plot(df.groupby("release_year").RoI.max())
plt.plot(df.groupby("release_year").RoI.mean())
plt.show()
plt.plot(df.groupby("release_year").revenue.max())
plt.plot(df.groupby("release_year").revenue.mean())
plt.show()
plt.plot(df.groupby("release_year").budget.max())
plt.plot(df.groupby("release_year").budget.mean())
plt.show()


# Findings:
#     1. From the graphs we can see that the movie business started gaining interest in the early 1960's. this corresponds with a lot of the "classics" in films being released, such as psycho, The pink panther, breakfast at tiffanys and 2001: a space odyssey, many of which are still watched to this day
#     2. The amount of revenue garnered from movies has be exponentially increasing. This may be due to the increase in money invested in the idustry through larger budgets than before. Although, the average budget and revenue earnt has only been steadily increasing. The max budgets line shows that certain films are getting a much larger than average budget. These could be the blockbusters from large studios.
#     3. however from the average return on investment, we can see other than a few big years; the average return for investors has not increased much.
#     4. Further investigation into inflation should be undertaken

# Web scrape Attempt of https://inflationdata.com/Inflation/Inflation_Rate/HistoricalInflation.aspx

# In[41]:

response = requests.get("https://inflationdata.com/Inflation/Inflation_Rate/HistoricalInflation.aspx")
content = response.content


# In[42]:

parser = BeautifulSoup(content, 'html.parser')
table = parser.table


# In[43]:

row = parser.find_all("tr")
row = row[2:-3]


# In[44]:

print(df["release_year"].min())
years = []
averageIn = []
for i in row:
    yearIn = i.text[0:5]
    inflationMonths = i.text.split(" %")
    inflationMonths = float(inflationMonths[-2])
    years.append(yearIn)
    averageIn.append(inflationMonths)
print(averageIn)
print(years)


# In[45]:

df["release_year"] = pd.to_numeric(df["release_year"])


# In[46]:

def inflationCalc(index):
    year = index
    x = 100
    num = 2016 - year 
    for i in range(num, -1, -1):
        x = (x * ((100 +averageIn[i])/100))
    return (x/100)


# In[ ]:




# In[47]:

df["inflation_rate"] = df["release_year"].apply(inflationCalc)


# In[48]:

df["bugIn"] = df["budget"] * df["inflation_rate"]
df["revIn"] = df["revenue"] * df["inflation_rate"]


# In[49]:

df["RoI_In"] = (df["revIn"]/df["bugIn"])
plt.plot(df.groupby("release_year").RoI_In.mean())
plt.show()
#plt.plot(df.groupby("release_year").revenue.max())
plt.plot(df.groupby("release_year").revenue.mean())
plt.plot(df.groupby("release_year").revIn.mean())
plt.title("Revenue")
plt.show()
#plt.plot(df.groupby("release_year").budget.max())
plt.plot(df.groupby("release_year").budget.mean())
plt.plot(df.groupby("release_year").bugIn.max())
plt.title("Budget")
plt.show()
sns.lmplot(x="bugIn", y="revIn", data=df,  x_estimator=np.mean)
#sns.lmplot(x="release_year", y="RoI_In", data=df, x_estimator=np.mean)


# Findings 2:
#     1. After accounting for inflation, we can see that the average revenue earnt has not increased dramatically.
#     2. However the average budget has increased.

# In[50]:

print(df["RoI_In"].idxmax())
print(df.iloc[3171,:])


# In[51]:

print(df["revIn"].idxmax())
print(df.iloc[2880,:])


# In[62]:


df.boxplot(["budget"], return_type="dict")
plt.plot()


# In[242]:

df = df[df["bugIn"] <=160.9]
df = df2[df2["bugIn"] >1]
print(len(df2))
print(212/len(df))


# In[108]:

#pd.options.display.float_format = "{:.1f}".format
df.describe()
f, ax = plt.subplots(figsize=(7, 7))
ax.set(xscale="log")
sns.regplot(y="revIn", x="bugIn", data=df2)


# In[101]:

df["bugIn"].min()


# In[111]:

sns.regplot(x="runtime", y="RoI_In", data=df2)


# Question: Do longer films result in a higher revenue?
# Answer: No, using Return of Investment, the average is the same, however lower budget films tend to be shorter and less risky, this means if a shorter film succeeds it can provide a large ROI

# In[133]:

sns.barplot(x="release_year", y="runtime", data=df2, estimator=np.mean)
plt.xticks(rotation = 45)


# Question: has the average film length increased over the past 100 years?
# Answer: On average no, in actual fact, films seems to have a standard length now, whereas in the past the average length og a film varied, year on year. 

# In[134]:

df.head()


# In[227]:

df["genres"]= df["genres"].apply(ast.literal_eval)
df["keywords"]= df["keywords"].apply(ast.literal_eval)


# In[225]:

import ast
genre = {}
keyword = {}
genre = df["genres"].apply(strToDict)
genre = comboDict(genre)
keyword = df["keywords"].apply(strToDict)
keyword = comboDict(keyword)


# In[240]:

df["keywords"] = df["keywords"].apply(stripToNums)
df["genres"] = df["genres"].apply(stripToNums)


# In[241]:

df.head()


# In[222]:

def strToDict(string):
    dict = {}
    #string = ast.literal_eval(string)
    #print(string)
    for i in string:
        print(i)
        idNo = i["id"]
        name = i["name"]
        dict[idNo] = name
    return dict


# In[185]:

def comboDict(list):
    dict = {}
    for i in list:
        dict.update(i)
    return dict


# In[234]:

def stripToNums(list):
    codes = []
    for i in list:
        code = i["id"]
        codes.append(code)
    return codes


# In[243]:




# In[ ]:



