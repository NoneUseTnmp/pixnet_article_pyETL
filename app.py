import requests
from bs4 import BeautifulSoup
import json
import os
import pandas as pd
import time
import random
from fake_useragent import UserAgent as ua
from random import choice
vvls=['18.235.220.172',
 '20.94.229.106',
 '35.172.135.29',
 '77.247.126.158',
 '143.198.239.216',
 '92.204.129.161',
 '162.243.167.58',
 '167.172.132.136',
 '132.145.137.26',
 '3.136.37.78',
 '205.185.118.53',
 '103.83.37.11',
 '52.25.159.130',
 '12.218.209.130',
 '24.172.82.94',
 '159.203.188.130',
 '52.251.88.114',
 '172.245.92.238',
 '165.227.80.176',
 '51.81.82.175',
 '165.227.71.60',
 '198.255.161.102',
 '157.230.95.4',
 '162.243.168.215',
 '216.236.198.30',
 '209.126.13.170',
 '50.16.33.219']
columns=['標題', '觀看數', '留言數','作者給分','平均分數','評分人數', '文章內容','發文時間','連結']
data=[]
mis_pag=[]
error=0
none_page=0
fulldata=0
thrt=0
keywords = ['台北美食']

r=324

url0='https://www.pixnet.net/tags/%E5%8F%B0%E5%8C%97%E7%BE%8E%E9%A3%9F'
ua0=ua().random      
#params={'page':r,'per_page':'5','filter':'articles','sort':'latest','refer':'https://www.pixnet.net/blog/articles/category/26'}
headers0 = {'User-Agent':"".format(ua0)}
ss=requests.session()
res0= ss.get(url0, headers=headers0)


for keyword in keywords:
    print(f'---------{keyword}職位---------')
    
    while True:
        
        ua1=ua().random
        url='https://www.pixnet.net/mainpage/api/tags/%E5%8F%B0%E5%8C%97%E7%BE%8E%E9%A3%9F/feeds?page={}&per_page=5&filter=articles&sort=latest&refer=https%3A%2F%2Fwww.pixnet.net%2Fblog%2Farticles%2Fcategory%2F26'.format(r)
        a_=choice(vvls)
        #print(a_)
        proxies1 = { 'http': 'http://' + a_ }
        parameters={'page':r,'per_page':'5','filter':'articles','sort':'latest','refer':'https://www.pixnet.net/blog/articles/category/26'}
        headers = {'User-Agent':"".format(ua1)}
        #ss=requests.session()
        try:
            res =ss.get(url=url , headers=headers ,proxies=proxies1)
        except IndexError as e:
            break
        js=json.loads(res.text)
        
        if len(js['data']['feeds']) !=0:
            for n in range(0,5):
                title=js['data']['feeds'][n]['title']
                reach=js['data']['feeds'][n]['hit']
                reply=js['data']['feeds'][n]['reply_count']
                if len(js['data']['feeds'][n]['poi']) !=0 :                
                    memcerr=js['data']['feeds'][n]['poi']['member_rating']
                    avgr=js['data']['feeds'][n]['poi']['rating']['avg']
                    countr=js['data']['feeds'][n]['poi']['rating']['count']
                else:
                    memcerr=None
                    avgr=None
                    countr=None


                avt=js['data']['feeds'][n]['avatar'].split('/')[4]
                if js['data']['feeds'][n]['link'] is not None :
                    artc=js['data']['feeds'][n]['link'].split('-')[0].split('/')[-1]
                    link=js['data']['feeds'][n]['link']
                    rere=random.randint(1,9999)
                    ua2=ua().random
                    b_=choice(vvls)
                    #print(b_)
                    proxies2 = { 'http': 'http://' + b_ }
                    urlc='https://emma.pixnet.cc/blog/articles/{}?user={}&limit=5&format=json&_=162468031{}'.format(artc,avt,rere)
                    headersc = {'User-Agent':ua2}
                    #Parameters={'utm_source':'PIXNET','utm_medium':'Hashtag_article'}
                    resc = requests.get(url=urlc , headers=headersc,proxies=proxies2)
                    jsc=json.loads(resc.text)
                    if jsc['error'] !=1:

                        ajc=jsc['article']['body']
                        artsoupc = BeautifulSoup(ajc,'html.parser')
                        t = time.localtime(int(jsc['article']['public_at']))
                        a=time.asctime(t)

                        rdata=[title,reach,reply,memcerr,avgr,countr,artsoupc.text,a,link]
                        data.append(rdata)
                        fulldata+=1
                        
                        print('.')
                        r_t=random.randint(1,3)
                        time.sleep(r_t)
                    elif jsc['error'] ==1:
                        
                        print('Exceed Anonymous Rate Limit')
                        break
                    
                    else:
                        print('else')
                        error+=1
                        
                        
                
                    
                    

            print('{}'.format(r))
            r+=1
            if r==362:
                
                print('done')
                break

        else:
            mis_pag.append(js['data']['page'])
            break
        
        #print("page{} break {} s".format(r,r_t))
        #thrt=thrt+r_t
        
print('total_break_time: {}s'.format(thrt))
print("no_article:{}".format(error))
print("none_page:{}".format(none_page))
print("missing_page:{}".format(mis_pag))
print("fulldata:{}".format(fulldata))
df =pd.DataFrame(data=data,columns=columns)
df          
    
        
