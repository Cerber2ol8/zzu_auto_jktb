# -*- coding:UTF-8 -*-
'''
郑州大学健康状况自动填报脚本
12点钟还没起床的同学必备
'''
 
import urllib
import urllib.request
import urllib.parse
import json
import requests
import re
import schedule
import time
from bs4 import BeautifulSoup
login_url = "https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/login"
#verify_url = "https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/jksb"

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0"
host = "jksb.v.zzu.edu.cn"
session = requests.Session()



def login():
    headers = {'User-Agent':user_agent,
               'Referer':"https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/first0",
               'Host':host}
 
    data = {'uid':'学号',    #学号
            'upw':    '登录密码',   #登录密码
            'smbtn':  '进入健康状况上报平台',
            'hh28':'502'}
    post_data = bytes(urllib.parse.urlencode(data), encoding='utf8')
    r = session.post(login_url, headers=headers,data=post_data)
    r.encoding="utf-8"
    str = r.text
    if  str.find("parent.window.location=") == -1:
        if str.find("密码输入错误") != -1:
            print(str)
            print("登录失败,请检查用户名或密码")
        else:
            print(str)
            print("登录失败")
        exit()
    else:
        print("登录成功！")
        return str



def get_url(html):
    soup=BeautifulSoup(html,'lxml')
    data = soup.find('script')
    pattern = re.compile(r'parent.window.location="(http.*?)"', re.I | re.M)
    script = data.get_text()
    url = pattern.findall(script)
    return url[0]

def get_session(url):
    opid_pattern = re.compile(r'ptopid=(.*?)&', re.I | re.M)
    sid_pattern = re.compile(r'sid=(.*?)$', re.I | re.M)
    sid = sid_pattern.findall(url)[0]
    opid = opid_pattern.findall(url)[0]
    if sid == None:
        print(url)
        print('会话获取失败')
        exit()
    else:
        return sid,opid

def verify(verify_url,opid,sid):

    refer = 'https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/jksb?ptopid='+ opid + '&sid=' + sid
    headers = {'User-Agent':user_agent,
           'Referer':refer,
           'Host':host}
    """
    确认页面需要填写的表单数据
    data = {'day6':    修改首次填报=a     每日填报=b
            'did':     未知变量=1，经测试无需更改
            'men6':    未知变量=a，经测试无需更改
            'sid':     会话id
            'ptopid':  操作id
            }
    """
    data = {'day6': 'b',     
            'did':    '1',
            'men6': 'a',
            'sid':     sid,
            'ptopid':  opid
            }
    post_data = bytes(urllib.parse.urlencode(data), encoding='utf8')
    r = session.post('https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/jksb', headers=headers,data=post_data)
    r.encoding="utf-8"
    str = r.text

    if str.find('填写上报表格') == -1:
        print(str)
        print('填报失败')
        exit()
    else:
        return str


def submit(opid,sid):
    url = 'https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/getsomething?ptopid='+opid+'+&sid=' + sid
    session.get(url)


def report(opid,sid):
    """
    提交页面需要填写的表单数据
    """
    url = 'https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/jksb'
    host = 'jksb.v.zzu.edu.cn'
    headers = {'User-Agent':user_agent,
           'Host':host}
    data = {'myvs_1':   '是',    #1体温是否正常     是/否
            'myvs_2':   '否',    #2是否有咳嗽       是/否
            'myvs_3':   '否',    #3否有乏力症状     是/否
            'myvs_4':   '否',    #4是否有鼻塞     是/否
            'myvsw_1':  '否',    #5是否在郑州       是/否
            'myvsp_1':  'xx',       #6现在居住地       如河南省=41
            'myvsp_3':  'xxxx',     #地市             (身份证地区编码)如河南郑州=4101
            'myvsw_2':  'xxxxxxx',    #详细地址         xxxxxxx
            'myvsw_a1': '否',    #7所在小区(村)是否有确诊    是/否
            'myvsw_a2': '否',    #8共同居住人是否有确诊    是/否
            'myvsp_6':  '否',    #9是否刚从外地返回郑州    是/否
            'myvsp_5':  '正常',  #10是否刚从外地返回郑州    正常
            'myvsw_3':  '否',    #11是否有外出       是/否
            'myvsw_5':  '在家学习', #12在家还在校         在家学习/在学校学习
            'did':      '2',    
            'day6':     'b',    #修改首次填报=a     每日填报=b
            'men6':     'a',    
            'fun3':     '',     
            'ptopid':   opid,   
            'sid':      sid     
            }
    post_data = bytes(urllib.parse.urlencode(data), encoding='utf8')
    r = requests.post(url, headers=headers,data=post_data)
    r.encoding="utf-8"
    str = r.text
    if str.find('感谢你今日上报健康状况') == -1:
        print(str)
        print("填报失败")
    else:
        print('填报成功！')



def main():
    print('登录....')
    str = login()
    verify_url = get_url(str)
    print('获取会话信息....')
    sid, opid = get_session(verify_url)

    print('sid:')
    print(sid)
    print('opid:')
    print(opid)

    submit(opid,sid) #get模拟请求跳转页面
    print('确认页面....')
    str = verify(verify_url,opid,sid)

    report(opid,sid)


if __name__ == '__main__':
    schedule.every().day.at("08:53").do(main)
    while True:
        schedule.run_pending()

        time.sleep(1)
