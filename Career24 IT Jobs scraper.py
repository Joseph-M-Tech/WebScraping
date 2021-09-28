#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import re
import pandas as pd


# In[2]:


def jobs_func(job_result):
    job_dict = {}
    
    #job_dict['img_url'] = job_result.img["src"]
    job_title = job_result.find("span",{"class":"schema"})
    job_link_title = job_result.find("a")
    job_town = job_result.find("p")
    job_contract = job_result.find("span",{"class":"pull-left"})
    #job_detail = job_result.find("div",{"class":"span8 job_search_content job_search_summary"})
    job_employer = job_result.find("div",{"class":"posted"})
    job_closing = job_result.find("p",{"class":"daysleft"})

    job_dict['job_link'] = job_link_title['href']
    job_dict['job_title'] = job_title.text.strip()

    job_dict['town'] = job_town.text.strip()
    job_dict['employment_terms'] = job_contract.text.strip()
    #job_dict['details'] = job_detail.text.strip()
    job_dict['employer'] = job_employer.text.strip()
    job_dict['closing_days'] = job_closing.text.strip()
    
    return job_dict


# In[3]:




headers = {
    'authority': 'www.careers24.com',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'x-requested-with': 'XMLHttpRequest',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    'content-type': 'application/json; charset=UTF-8',
    'origin': 'https://www.careers24.com',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.careers24.com/jobs/se-it/?sort=dateposted^&page=1',
    'accept-language': 'en-US,en;q=0.9',
}

master_jobs = []
for i in range(1,200):
   # print('getting page' + str(i))
    params = (
        ('page', str(i))
    )
    

    data = '^{^\\^vacancyimpressions^\\^:^[^{^\\^ImpressionSourceId^\\^:1,^\\^VacancyId^\\^:1685943^},^{^\\^ImpressionSourceId^\\^:1,^\\^VacancyId^\\^:1685926^},^{^\\^ImpressionSourceId^\\^:1,^\\^VacancyId^\\^:1685919^},^{^\\^ImpressionSourceId^\\^:1,^\\^VacancyId^\\^:1685918^},^{^\\^ImpressionSourceId^\\^:1,^\\^VacancyId^\\^:1685905^},^{^\\^ImpressionSourceId^\\^:1,^\\^VacancyId^\\^:1685904^},^{^\\^ImpressionSourceId^\\^:1,^\\^VacancyId^\\^:1685889^},^{^\\^ImpressionSourceId^\\^:1,^\\^VacancyId^\\^:1685883^},^{^\\^ImpressionSourceId^\\^:1,^\\^VacancyId^\\^:1685835^},^{^\\^ImpressionSourceId^\\^:1,^\\^VacancyId^\\^:1685833^}^]^}'

    response = requests.post('https://www.careers24.com/jobs/se-it/?sort=dateposted&ref=sbj', headers=headers, data=data)
    html = response.text
    soup = BeautifulSoup(html,'html.parser')
    job_list = soup.find_all("div",{"class":"row job_search_wrapper"})


    for job_result in job_list:
        job_list = jobs_func(job_result)
        master_jobs.append(job_list)


# In[4]:


len(master_jobs)


# In[ ]:





# In[5]:


df = pd.DataFrame(master_jobs)


# In[6]:


#Output a csv file
df.to_csv('finalSa_jobs_output.csv',index = False)





