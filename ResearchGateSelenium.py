#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 20:17:09 2023

@author: Lumin
"""
#https://github.com/SMSadegh19/ResearchGateCrawler/blob/main/crawler.py

#https://medium.com/@johnpatrickruizborromeo/web-scraping-using-selenium-pandas-and-python-d32fa5bb87e1

#(f"https://www.researchgate.net/search/publication?q={query}&page={page_num}")

from parsel import Selector
from playwright.sync_api import sync_playwright as p
import json
from more_itertools import consecutive_groups
import io
import selenium
from selenium.webdriver import Chrome
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
import time 
from bs4 import BeautifulSoup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import urllib.robotparser
import requests

import csv
import os
import glob

'''https://www.researchgate.net/robots.txt
User-agent: *
Allow: /
Disallow: /cdn-cgi/
Disallow: /connector/
Disallow: /plugins.
Disallow: /firststeps.
Disallow: /publicliterature.PublicLiterature.search.html
Disallow: /lite.publication.PublicationRequestFulltextPromo.requestFulltext.html
Disallow: /amp/authorize
Allow: /signup.SignUp.html
Disallow: /signup.'''

username='lumin.lumin@du.edu'
password = "1q2w!Q@W"
#def researchgateLogin(u,p):  # user / password  run function

driver = webdriver.Chrome('chromedriver')
driver.get("https://www.researchgate.net/login?_sg=NwdtVE70_zdviOxDKwzwMMj7XJBOecrxh3_txMgRe08qjVOr9JhOiTknCb2yzOwWlYRSbgRqKXoikvZlmZXacQ")
time.sleep(3)
uname = driver.find_element(By.NAME, "login") 
uname.send_keys(username)
time.sleep(3)
pword = driver.find_element("id", "input-password") 
pword.send_keys(password)
driver.find_element(By.CSS_SELECTOR, '[type="submit"]').click()

#pullSavedList  
    #profile
driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/header/nav/ul[2]/li[5]/span[2]/div/div/a").click()
    #saved list from profile drop down
driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/header/nav/ul[2]/li[5]/span[2]/div[2]/div/ul/li[2]/a/span/div").click()
time.sleep(2)
    #specify saved list  (not saved AND archived)
driver.find_element(By.XPATH,"/html/body/div[1]/div[3]/div[1]/div/div/div[2]/div[1]/div/div/div/div/div[2]/div/div[1]/div/div[2]/div/nav/div/div/button[2]/div/div").click()
time.sleep(2)   


#pull all saved list URLS:
links=driver.find_elements(By.TAG_NAME,"a")
attrList = []
for i in links:
    attrList.append(i.get_attribute('href')) 
attrFrame = (pd.DataFrame(attrList))
attrFrame=attrFrame.dropna()

contain_values = attrFrame[attrFrame[0].str.contains('researchgate.net/publication/')]

final=pd.concat([contain_values.loc[i].reset_index(drop=True) 
for i in consecutive_groups(contain_values.index)],axis=1)
final.columns=range(len(final.columns))
useURLs = final.tail(1)
useURLs = useURLs.values.flatten().tolist()
time.sleep(2)
print(useURLs)
#def doCiteAbstract(urls):
    #for i in range(len(urls)): #non-functional def at the moment
'''driver.get(useURLs[0])
driver.execute_script('window.open("{}", "_blank");'.format(useURLs[0]))
'''
#one article of saved list
'########################'

article = driver.find_element(By.CLASS_NAME ,"nova-legacy-v-publication-item__meta-left")
article.click()
time.sleep(2)

#more actions dropdown
driver.find_element(By.CSS_SELECTOR, '[aria-label="More actions"]').click()
time.sleep(2)

#citation 
pop = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[1]/div/div/div[1]/div[2]/div/div/div/div[2]/div[2]/div[2]/div/div[3]/span/span/div[1]/div/button[1]/span/div")
pop.click()
time.sleep(1)
#PlainText selextion
plainText = driver.find_element(By.XPATH, "/html/body/div[16]/div/div/div/div/div[1]/div/div[2]/div[3]/label/span[2]")
plainText.click()
time.sleep(1)
#citation and abstract
citAb = driver.find_element(By.XPATH, "/html/body/div[16]/div/div/div/div/div[1]/div/div[3]/div[2]/label/span[1]")
citAb.click()
time.sleep(1)
#download button
dnl = driver.find_element(By.XPATH, "/html/body/div[16]/div/div/div/div/div[2]/div/a/span")
dnl.click()
time.sleep(1)


file_path = '/Users/Lumin/Downloads/*.txt'
rgFile = sorted(glob.iglob(file_path), key=os.path.getctime, reverse=False)



#do the following for both cite and cite with abstract --
#rgFile to function with each article immediate execution
reader = open(rgFile[0],'r')
for row in reader:
    rows = row.split()
citationKeys = ["Author", "Date", "Title", "Publication", "Vol", "Pages", "Abstract"]  
df = pd.DataFrame(columns=citationKeys) 
print(rows) 

#more actions dropdown
driver.find_element(By.CSS_SELECTOR, '[aria-label="More actions"]').click()
time.sleep(2)
#citation 
pop = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[1]/div/div/div[1]/div[2]/div/div/div/div[2]/div[2]/div[2]/div/div[3]/span/span/div[1]/div/button[1]/span/div")
pop.click()
time.sleep(1)
#PlainText selextion
plainText = driver.find_element(By.XPATH, "/html/body/div[16]/div/div/div/div/div[1]/div/div[2]/div[3]/label/span[2]")
plainText.click()
time.sleep(1)
#citation only NO default
citeOnly = driver.find_element(By.XPATH, "/html/body/div[16]/div/div/div/div/div[1]/div/div[3]/div[1]/label/span[2]")
citeOnly.click()
#download button
dnl = driver.find_element(By.XPATH, "/html/body/div[16]/div/div/div/div/div[2]/div/a/span")
dnl.click()
time.sleep(1)

fileCite = '/Users/Lumin/Downloads/*.txt'
citeFile = [sorted(glob.iglob(fileCite), key=os.path.getctime, reverse=False)][0]

reader2 = open(citeFile[0],'r')
for row in reader2:
    rows2 = row.split('.')
print(rows2) 

df.loc[0] = rows2

abSeries = pd.Series(rows)
df["Abstract"] = abSeries
df["username"] = username
df["ArticleURL"] = useURLs[0] # useURLs[i] for multiple aritcles
 

#notes for multiple:
#get next in saved list by init doCiteAbstract(useURLs) -- advance save to csv to csv[i]
#doCiteAbstract(useURLs)

time.sleep(2)
driver.quit()
driver.close()

df.to_csv('/Users/Lumin/Desktop/NLP DataTools1/RGSavedList.csv')
#df["Abstract"].to_csv('/Users/Lumin/Desktop/NLP DataTools1/RGSavedListAbstract1.csv')
#fix repeat values in df order of loadeing cite and cite and abstract:
df["Abstract"][15:].to_csv('/Users/Lumin/Desktop/NLP DataTools1/RGSavedListAbstract1.csv')

#dataframe to sklearn https://stackoverflow.com/questions/74767053/converting-word2vec-output-into-dataframe-for-sklearn



