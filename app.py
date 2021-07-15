import requests
from bs4 import BeautifulSoup
import json
import os
import pandas as pd
import time
import random

columns=['標題', '觀看數', '留言數','作者給分','平均分數','評分人數', '文章內容','發文時間','連結']
data=[]

keywords = ['台北美食']
for keyword in keywords:
    print(f'---------{keyword}職位---------')
    
    for i in range(3):
        r=i+1
        url='https://www.pixnet.net/mainpage/api/tags/%E5%8F%B0%E5%8C%97%E7%BE%8E%E9%A3%9F/feeds?page={}&per_page=5&filter=articles&sort=latest&refer=https%3A%2F%2Fwww.pixnet.net%2Fblog%2Farticles%2Fcategory%2F26'.format(r)
        
        params={'page':r,'per_page':'5','filter':'articles','sort':'latest','refer':'https://www.pixnet.net/blog/articles/category/26'}
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
        ss=requests.session()
        try:
            res =ss.get(url=url , headers=headers , params=params)
        except IndexError as e:
            break
        js=json.loads(res.text)
        for n in range(0,5):
            title=js['data']['feeds'][n]['title']
            reach=js['data']['feeds'][n]['hit']
            reply=js['data']['feeds'][n]['reply_count']
            memcerr=js['data']['feeds'][n]['poi']['member_rating']
            avgr=js['data']['feeds'][n]['poi']['rating']['avg']
            countr=js['data']['feeds'][n]['poi']['rating']['count']
            avt=js['data']['feeds'][n]['avatar'].split('/')[4]
            artc=js['data']['feeds'][n]['link'].split('-')[0].split('/')[-1]
            link=js['data']['feeds'][0]['link']
            urlc='https://emma.pixnet.cc/blog/articles/{}?user={}&limit=5&format=json&_=1624680317272'.format(artc,avt)
            headersc = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'}
            resc = requests.get(url=urlc , headers=headersc )
            jsc=json.loads(resc.text)
            ajc=jsc['article']['body']
            artsoupc = BeautifulSoup(ajc,'html.parser')
            t = time.localtime(int(jsc['article']['public_at']))
            a=time.asctime(t)
            
            rdata=[title,reach,reply,memcerr,avgr,countr,artsoupc.text,a,link]
            data.append(rdata)
        
        time.sleep(random.randint(1,10))
        
df =pd.DataFrame(data=data,columns=columns)
df          
     
        
