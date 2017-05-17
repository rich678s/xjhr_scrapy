#!/usr/bin/python3.6
# -*- coding: utf-8 -*-  
import requests,os,random,time,urllib
from bs4 import BeautifulSoup


class xjHr():
    def __init__(self):
        self.user_agent_list = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"            
        ]
        
    def request(self,url):
        UA = random.choice(self.user_agent_list)
        headers = {'headers':UA}
        response = requests.get(url,headers=headers)  
        return response        
    
    def getPageNo(self,htmlSource):
        soup = BeautifulSoup(htmlSource,'lxml')
        #如果a个数等于0，本页无数据,如果a个数等于1，只需遍历本页，如果a大于2（只可能是3），一页一页遍历
        a_list = soup.find('div',class_='seaPage').find_all('a')
        a_len = len(a_list)
        max_page = 1
        if(a_len > 2):
            max_page = soup.find('div',class_='seaPage').find_all('a')[-2].get_text()
        elif(a_len == 1):
            max_page = 2
        return int(max_page)
    
    def mkdir(self,path):
        path = path.strip()
        isExists = os.path.exists(path)
        if not isExists:
            os.makedirs(path)
            os.chdir(path)
            return True
        else:
            os.chdir(path)
            print('目录已经存在，切换至此目录')
            return False
        
    def getPersonNo(self,url,page_num,savePath,isMustPhoto):
        response = self.request(url)
        htmlSource = response.text
        max_page = 0
        if(page_num == 0):
            max_page = self.getPageNo(htmlSource)
        else:
            #如果max_page大于用户的设定则按照用户页数取，如果max_page小于用户设定页数取全部
            sysPage_num = self.getPageNo(htmlSource)            
            if(sysPage_num >= page_num):            
                max_page = int(page_num)
            else:
                max_page = sysPage_num
        self.mkdir(savePath)
        for page in range(1,max_page+1):
            page_url = url+'&PageNo='+str(page)
            response = self.request(page_url)
            serialSoup = BeautifulSoup(response.text,'lxml')
            personList = serialSoup.find('div',class_='seaList').find_all('div',class_='seaLists')
            for person_html in personList:
                time.sleep(4)
                file_name = person_html.find('li',class_='seaList12').get_text()+'_'+person_html.find('li',class_='seaList14').get_text()+'_'+person_html.find('li',class_='seaList16').get_text()+'_'+person_html.find('li',class_='seaList18').get_text()
                personNo =person_html.find('li',class_='seaList10').find('input')['value']
                personHasPhoto =person_html.find('li',class_='seaList11').find('img')['alt']
                if isMustPhoto:
                    if personHasPhoto == '已上传照片':
                        self.down_resume(personNo, file_name)
                else:
                    self.down_resume(personNo, file_name)
              
                
    def down_resume(self,personNo,file_name): 
        print('开始下载'+file_name+'文档')
        doc = self.request('http://www.xjhr.com/uploadfiles/Person/Resume/JL'+personNo+'.doc')
        with open(file_name.replace('/','+').replace('\\','+').replace('//','+')+'.doc','ab') as f:
            f.write(doc.content)
            
    def customization(self,degree=0,age=0,workyears=0,sex=0,jobProperty=0,publishDate=0,orderId=0,workPlace='',key='',jobType=0,page_num=0,savePath=r'D:\xjhr',isMustPhoto=False):
        key = urllib.parse.quote(key.encode('gb2312'))
        url = 'http://www.xjhr.com/jianli/Search.aspx?JobType='+str(jobType)+'&WorkPlace='+str(workPlace)+'&JobProperty='+str(jobProperty)+'&Age='+str(age)+'&Degree='+str(degree)+'&WorkYears='+str(workyears)+'&Sex='+str(sex)+'&Key='+key+'&Orderid='+str(orderId)+'&Styleid=1&PublishDate='+str(publishDate)
        self.getPersonNo(url,page_num,savePath,isMustPhoto)
#网站参数
#Degree（学历）：0（不限），10（初中），20（高中），30（中技），40（中专），50（大专），60（本科），70（硕士），80（博士）
#Age(年龄):0（不限），1（16-20），2（21-25），3（26-30），4（31-35），5（36-40），6（41-50），7（51-60），8（25岁以上），9（30岁以上），10（35岁以上）
#WorkYears（工作年限）：0（不限），102（在校学生），101（应届生），1（1年以上），2（2年以上），3（3年以上），5（5年以上），8（8年以上），10（10年以上）     
#Sex(性别)：0（不限），1（男），2（女）
#JobProperty（职业性质）：0（不限），1（全职），2（兼职），3（临时），4（实习）
#PublishDate（更新时间）：0（不限），1（1天内），2（2天内），3（3天内），7（7天内），15（15天内），30（30天内），60（60天内），90（90天内），180（180天内），365（365天内）
#Orderid（排序类型）：0（更新时间），1（发布时间），2（热度）
#WorkPlace(当前所在地):太多，请至网站获取，可空
#Key(关键字):自由填写，可空
#JobType（岗位类别）:太多，请至网站获取，默认0不限

#自定义参数
#page_num（获取页数）：默认为0即获取到的最大页数
#isMustPhoto（是否必须照片）：默认false，如果true，则只下载有照片的
#savePath(保存路径):参数形式为r'E:\rc'，其中r不可缺少
if __name__ == '__main__':
	a = xjHr()
	a.customization(sex=2,age=2,isMustPhoto=True,publishDate=60)
        
       
