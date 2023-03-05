#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 20:17:09 2023

@author: Lumin
"""

from more_itertools import consecutive_groups
from selenium import webdriver
from selenium.webdriver.common.by import By
import time 
import pandas as pd
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
#print(useURLs)
#safety measure of saving URLs without NAs, not toally necessary
urlDF = pd.DataFrame(useURLs)
isNAN = urlDF[urlDF[0].isna()] #returns row number of NAN, let's user know if a link didn't download. 
urlDF = urlDF.dropna(0)
urlDF = urlDF.reset_index(drop=True)
urlDF.to_csv('/Users/Lumin/Desktop/NLP DataTools1/RGSavedListURL.csv')
print(urlDF)




##################
#the reliable part has come to an end
##################

#the following code will go from url to url, but the pathways/selectors/locators are not the same from document to document

'''
#def getInfo(urlDF):
    #for i in range(len(urlDF)):
        
      
articleURL = urlDF.loc[1, 0]
driver.get(articleURL)

#more actions dropdown
driver.find_element(By.CSS_SELECTOR, '[aria-label="More actions"]').click()
time.sleep(2)

#citation 
pop = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/div[1]/div/div/div[1]/div[2]/div/div/div/div[2]/div[2]/div[2]/div/div[3]/span/span/div[1]/div/button[1]/span/div")
pop.click()
time.sleep(1)

#PlainText selection      
plainText = driver.find_element(By.XPATH , "/html/body/div[36]/div/div/div/div/div[1]/div/div[2]/div[3]/label/span[1]")
time.sleep(1)
plainText.click()
time.sleep(2)

#citation only
citeOnly = driver.find_element(By.XPATH , '/html/body/div[36]/div/div/div/div/div[1]/div/div[3]/div[1]/label/span[1]')
time.sleep(1)
citeOnly.click()
time.sleep(1)

#download cite button
dnl = driver.find_element(By.XPATH , '/html/body/div[36]/div/div/div/div/div[2]/div/a/span')
time.sleep(1)
dnl.click()
time.sleep(1)
  
file_path = '/Users/Lumin/Downloads/*.txt'
rgFile = sorted(glob.iglob(file_path), key=os.path.getctime, reverse=False)

reader = open(rgFile[0],'r')
for row in reader:
    rows = row.split('.')  
citeDF = pd.DataFrame(rows)
citeDF=citeDF.T
pd.set_option('display.max_columns', None)
citeDF.to_csv("/Users/Lumin/Desktop/NLP DataTools1/citeDF.csv")
'''   

##########################
#citeByURL = getInfo(urlDF) 
##########################


#for i in range(len(useURLs)):
    #query = useURLs[i]
'''
query = urlDF.loc[2,0]
pageN = 1
driver.get("https://www.researchgate.net/search")
time.sleep(2)  
find = driver.find_element(By.NAME , "query") 
time.sleep(2)
find.send_keys(query)
driver.find_element(By.PARTIAL_LINK_TEXT , 'search.Search.html?ev=nav').click()
    
  
driver.find_elements(By.XPATH ,"/html/body/div[1]/div[3]/div[1]/div/div/div[2]/div[1]/div/div/div/div/div[1]/div/div/div/div/div/div/div[1]/div/div/div/div[2]/div/div[1]/div/div[1]/a/span").click()
'''

'''
query = urlDF.loc[i,0]
googDriver = webdriver.Chrome('chromedriver')
googDriver.get("https://www.google.com/")
find = googDriver.find_element(By.NAME , "q") 
time.sleep(2)
find.send_keys(query)
googDriver.find_element(By.ID , "gbqfbb").click()
'''



fullText = '/Users/Lumin/Downloads/*.pdf'
rgPDF = sorted(glob.iglob(file_path), key=os.path.getctime, reverse=False)

pdfDF0 = pd.read_csv(rgPDF[0])
pdfDF1 = pd.read_csv(rgPDF[1])

time.sleep(2)
driver.quit()
driver.close()





