# -*- coding: UTF-8 -*-
#!/usr/bin/env python3
import requests

def control(config):
    for i in config['userInfo']:
        changesData = getChanges(i)
        # userIndoDic = getUserInfo(i['cookie'])# 为了缩减网络请求所耗的时间，这部分放到了前端
        userIndoDic = {}
        userIndoDic['changesData'] = changesData
        print(userIndoDic)
        print("\n\n")
        return userIndoDic
        
def getPage(pageIndex,userCookie):
    url = "https://bean.m.jd.com/beanDetail/detail.json"
    cookie = {i.split("=")[0]: i.split("=")[1] for i in userCookie.split("; ")}
    data = {"page":pageIndex}
    html = requests.post(url, cookies=cookie, data=data)
    jsonData = html.json()
    return jsonData['jingDetailList']

def getChanges(info):
    userName = info["name"]
    cookie = info["cookie"]
    dataDic = {}
    index = 1#页数
    print("开始统计%s的京豆收益情况"%userName)
    while len(dataDic) <= 7:#近8天的京豆变更记录,取前7天（因为最后一天数值不准确）
        beanData = getPage(index,cookie)
        for i in beanData:
            date = i['date']
            getBeanNum = int(i['amount'])
            if getBeanNum < 0:
                continue
            YMD = date.split(" ")[0][5:]
            if YMD in dataDic:#有则累加京豆
                dataDic[YMD] += getBeanNum
            else:#没有则创建
                dataDic[YMD] = getBeanNum
        index+=1
    dataDic.pop(list(dataDic.keys())[-1])#去除最后一天的结果
    print("近%d天%s的京豆收益情况: "%(len(dataDic),userName),dataDic)
    keys = list(dataDic.keys())
    values = list(dataDic.values())
    # keys.reverse(),values.reverse()#倒序排列
    dataList = [keys,values,len(dataDic)]
    return dataList


#下面信息目前弃用，仅作参考
def getUserInfo(cookie):
    import requests, re,time
    url = 'https://wq.jd.com/user/info/QueryJDUserInfo?sceneid=80027&_=1642224937161&sceneval=2&g_login_type=1&callback=getUserInfoCb&g_ty=ls'
    headers = {'Host': 'wq.jd.com', 'Connection': 'keep-alive',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
               'Accept': '*/*', 'Sec-Fetch-Site': 'same-site', 'Sec-Fetch-Mode': 'no-cors',
               'Referer': 'https://wqs.jd.com/my/jingdou/my.shtml?sceneval=2&jxsid=16422247425862224986&ptag=7155.1.17',
               'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'zh-CN,zh;q=0.9'}
    cookies = {i.split("=")[0]: i.split("=")[1] for i in cookie.split("; ")}
    
    try:
        html = requests.get(url, headers=headers, cookies=cookies)
        htmll = html.text
        userIndoDic = {}
        userIndoDic["headImageUrl"] = re.findall(r'"headImageUrl" : "(.*?)",', htmll, re.I)[0]
        userIndoDic["curPin"] = re.findall(r'"curPin" : "(.*?)",', htmll, re.I)[0]
        userIndoDic["isJTH"] = re.findall(r'"isJTH" : "(.*?)",', htmll, re.I)[0]
        userIndoDic["jdNum"] = re.findall(r'"jdNum" : (.*?),', htmll, re.I)[0]
        userIndoDic["jvalue"] = re.findall(r'"jvalue" : (.*?),', htmll, re.I)[0]
        userIndoDic["levelName"] = re.findall(r'"levelName" : "(.*?)",', htmll, re.I)[0]
        userIndoDic["nickname"] = re.findall(r'"nickname" : "(.*?)",', htmll, re.I)[0]
        userIndoDic["isPlusVip"] = re.findall(r'"isPlusVip" : (.*?),', htmll, re.I)[0]
    except:#错误就重试一次
        html = requests.get(url, headers=headers, cookies=cookies)
        htmll = html.text
        userIndoDic = {}
        userIndoDic["headImageUrl"] = re.findall(r'"headImageUrl" : "(.*?)",', htmll, re.I)[0]
        userIndoDic["curPin"] = re.findall(r'"curPin" : "(.*?)",', htmll, re.I)[0]
        userIndoDic["isJTH"] = re.findall(r'"isJTH" : "(.*?)",', htmll, re.I)[0]
        userIndoDic["jdNum"] = re.findall(r'"jdNum" : (.*?),', htmll, re.I)[0]
        userIndoDic["jvalue"] = re.findall(r'"jvalue" : (.*?),', htmll, re.I)[0]
        userIndoDic["levelName"] = re.findall(r'"levelName" : "(.*?)",', htmll, re.I)[0]
        userIndoDic["nickname"] = re.findall(r'"nickname" : "(.*?)",', htmll, re.I)[0]
        userIndoDic["isPlusVip"] = re.findall(r'"isPlusVip" : (.*?),', htmll, re.I)[0]
    
    return userIndoDic

if __name__ == '__main__':
    pass
