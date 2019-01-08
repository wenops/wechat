from django.shortcuts import render,HttpResponse
import time
import requests
import re
import json
# Create your views here.
CTIME =None
QCODE=None
TIP = 1
def login(request):
    global CTIME
    CTIME = time.time()
    res=requests.get(
        url='https://login.wx.qq.com/jslogin?appid=wx782c26e4c19acffb&fun=new&lang=zh_CN&_=%s' % CTIME
    )
    #print(res.text)
    v=re.findall('uuid = "(.*)";',res.text)
    global QCODE
    QCODE = v[0]
    #print(v[0])
    return render(request,'login.html',{'qcode':QCODE})


def check_login(request):
    global TIP
    ret = {'code':408,'data':None}
    r1=requests.get(
        url='https://login.wx.qq.com/cgi-bin/mmwebwx-bin/login?loginicon=true&uuid=%s&tip=%s&r=-510421028&_=%s' %(QCODE,TIP,CTIME,)
    )
    if 'window.code=408' in r1.text:
        print('无人扫码')
        print(r1.text)
        return HttpResponse(json.dumps(ret))
    elif 'window.code=201' in r1.text:
        ret['code'] = 201
        print(r1.text)
        avatar = re.findall("window.userAvatar = '(.*)';",r1.text)[0]
        print(avatar)
        ret['data']=avatar
        TIP = 0
        return HttpResponse(json.dumps(ret))
    elif 'window.code=200' in r1.text:
        r2=requests.get(
            url='https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxnewloginpage?ticket=AUUOogBJeCyluiGQjhuDWDit@qrticket_0&uuid=gZUxj07Leg==&lang=zh_CN&scan=1546960482&fun=new&version=v2&lang=zh_CN'
        )
        print(r2.text)
        return HttpResponse('....')