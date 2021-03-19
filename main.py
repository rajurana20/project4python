import requests
from bs4 import BeautifulSoup
import pandas as pd

def extract(page):
  headers ={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'}
  url =f"https://www.indeed.com/jobs?q=data+engineer&l=Virginia&start={page}"
  r=requests.get(url,headers)
  soup=BeautifulSoup(r.content,'html.parser')
  return soup

def transform(soup):
  divs=soup.find_all('div',class_='jobsearch-SerpJobCard')
  for item in divs:
    title = item.find('a').text.strip()
    try:
      location=item.find('div',class_='location').text.strip()
    except:
      location=''
    try:
      review=item.find('span',class_='ratingsContent').text.strip()
    except:
      review=''
    try:
      page_url=f"https://www.indeed.com{item.find('a')['href']}"
    except:
      page_url=''
    company=item.find('span',class_='company').text.strip()
    job_description=item.find('div', class_='summary').text.strip().replace('\n','')

    job={
      'title':title,
      'location':location,
      'company':company,
      'job_description':job_description,
      'review':review,
      'page_url':page_url
    }
    joblist.append(job)
  return

joblist=[]

for i in range(0,40,10):
  print(f'Getting page, {i}')
  c=extract(0)
  transform(c)

df=pd.DataFrame(joblist)
print(df.head())
df.to_csv('jobs.csv')
