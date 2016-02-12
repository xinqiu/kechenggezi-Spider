# coding=utf-8

import random
import requests

def main():
    url = 'http://kechenggezi.com/campus_stars?page=1&cur_time=1455265064747' #cur_time后面的值可以修改
    user_agent = 'Mozilla/5.0 (iPhone;CPU iPhone OS 9_2_1 like Mac OS X) AppleWebKit/601.1.46(KHTML, like Gecko)Mobile/13D15 ClassBox/7.3 ClassBox/7.3 ClassBox/7.3'
    cookies = {
        'Hm_lpvt_31589adaafcdee0269f5b28ec8ac344c':'1455265065',
        'Hm_lvt_31589adaafcdee0269f5b28ec8ac344c':'1455253763,1455254740,1455256199,1455264343',
        '_zg':'%7B%22uuid%22%3A%20%221500db06c20404-005d4025a-68391f6f-3d10d-1500db06c2194f%22%2C%22sid%22%3A%201455262803.041%2C%22updated%22%3A%201455265064.764%2C%22info%22%3A%201455253762809%2C%22cuid%22%3A%20%22fbb65b1f-7c34-43d9-860a-ef8ba61fbd37%22%7D',
        'from_gezi':'true',
        'token':'XXXXXXXXXXXXXXXXXX', #此处填写你的设备token
        '_kecheng_session':'BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJTY4MDk1YzUyZGM4MzljMTI2NDA3ZTIxYmEwZTFiZTRhBjsAVEkiDHVzZXJfaWQGOwBGaQPNEZ4%3D--3f25c9aaf3b0fe73009d80f4dd2c628541c0bd7c',
        'responseTimeline':'294'
    }

    headers = {'User-Agent': user_agent,
               'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Language': 'zh-cn',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Content-Type':'application/json',
               'X-Requested-With': 'XMLHttpRequest'
    }

    r = requests.get(url, cookies=cookies,headers=headers)
    data = r.json()

    tpages = data['total_pages']
    count = 0

    for i in range(tpages):
        url = 'http://kechenggezi.com/campus_stars?page=' + str(i + 1) +'&cur_time=145526506' + str(int(random.random() * 10000) % 10000).ljust(4,'0')
        r = requests.get(url, cookies=cookies,headers=headers)
        data = r.json()
        p = data['campus_stars']
        for i in range(len(p)):
            print p[i]['name'], p[i]['favor_count']

            #以下代码为保存图片
            count += 1
            conn = requests.get(p[i]['avatar_url'], cookies=cookies,headers=headers)
            name = str(i) +'.jpg'
            f = open(r'/path/to/save/'+ name,'wb')  #填写保存位置
            f.write(conn.content)
            f.close()
            nc = u"%d\t%s\t%s\n" %(count, p[i]['name'], str(p[i]['favor_count']))
            fc = open(r'/path/to/save/list.txt','a') #填写保存位置
            fc.write(nc.encode('utf-8'))
            fc.close()

if __name__ == '__main__':
    main()
