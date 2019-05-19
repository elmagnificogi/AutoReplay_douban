import random
import re
#from apscheduler.schedulers.blocking import BlockingScheduler
from lxml import html
import requests
from PIL import Image
import os,sys

def main():
    db_urls = [
        'https://www.douban.com/group/topic/141037106/',
        'https://www.douban.com/group/topic/141008050/',
        'https://www.douban.com/group/topic/141006630/',
        'https://www.douban.com/group/topic/141005669/',
        'https://www.douban.com/group/topic/141004111/',
        'https://www.douban.com/group/topic/141003329/',
        'https://www.douban.com/group/topic/141002674/'
        ]


    db_url = "https://www.douban.com/group/topic/141002674/"
    Cookie = 'bid=b16kx11APXM; ll="118282"; douban-fav-remind=1; douban-profile-remind=1; ct=y; _ga=GA1.2.2116562073.1558235896; _gid=GA1.2.1026987747.1558254879; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1558265006%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3D57aywD0Q6WTnl7XKbIHuE8zWE5epzov3Jk7LtVUL7clOAGuZmUBS-a-MNTzYiTmfD2AoTT8mx1my6hYutqi9ia%26wd%3D%26eqid%3Dbfe569310000a652000000065ce0caec%22%5D; ps=y; ap_v=0,6.0; dbcl2="164776595:eNdVT94l/C8"; ck=OLvw; _pk_id.100001.8cb4=cc09238f4c125f7c.1558235895.5.1558275428.1558256275.; _pk_ses.100001.8cb4=*; push_noty_num=0; push_doumail_num=0; __utma=30149280.2116562073.1558235896.1558251801.1558265006.5; __utmb=30149280.500.9.1558267190533; __utmc=30149280; __utmz=30149280.1558235896.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=30149280.16477'
    replay_comment = "up"

    headers = {
        "Host": "www.douban.com",
        "Referer": "https://www.douban.com/group/topic/141037106/?start=0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
        "Cookie":'bid=UFYUzuCXrzU; douban-fav-remind=1; _pk_ses.100001.8cb4=*; ap_v=0,6.0; dbcl2="164776595:mQULF8+uzlA"; ck=YaK5; _pk_id.100001.8cb4=7f6412afdff3f2a2.1558270168.1.1558270179.1558270168.; push_noty_num=0; push_doumail_num=0; __utma=30149280.1650496989.1558270179.1558270179.1558270179.1; __utmc=30149280; __utmz=30149280.1558270179.1.1.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/passport/login; __utmt=1; __utmv=30149280.16477; __utmb=30149280.6.6.1558270179'

    }
    params = {
        "ck": "YaK5",
        "rv_comment": "up",
    }

    headers['Referer'] = db_url + '?start=0'
    headers['Cookie'] = Cookie
    #print(headers['Referer'])

    ck_index = Cookie.find('ck=')
    #print(ck)
    ck_str = Cookie[ck_index+3:ck_index+7]
    #print(ck_str)

    params['ck'] = ck_str
    params['rv_comment'] = replay_comment

    db_url_rpl = db_url +'/add_comment'
    print(db_url_rpl)


    # get captcha
    response = requests.post(db_url,headers=headers, data=params,verify=False).content.decode()
    selector = html.fromstring(response)
    captcha_image = selector.xpath("//img[@id=\"captcha_image\"]/@src")
    if(captcha_image):
        print(captcha_image)
        captcha_id = selector.xpath("//input[@name=\"captcha-id\"]/@value")
        print(captcha_id)

        captcha_name = re.findall("id=(.*?):",captcha_image[0])   #findall返回的是一个列表
        filename = "douban_%s.jpg" % (str(captcha_name[0]))
        print("文件名为："+filename)
        #创建文件名
        with open(filename, 'wb') as f:
        #以二进制写入的模式在本地构建新文件
            header = {
                'User-Agent': '"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",'
                ,'Referer': captcha_image[0]}
            f.write(requests.get(captcha_image[0],headers=header).content)
            print("%s下载完成" % filename)
        print(os.path.dirname(os.path.realpath(__file__))+ r'\\' + filename)
        img=Image.open(os.path.dirname(os.path.realpath(__file__)) +r'\\' +filename)
        img.show()
        captcha_veryfy = input("输入验证码:").replace('\n', '').replace('\n', '')
        # urllib.request.urlretrieve(requests.get(i,headers=header), "%s%s%s.jpg" % (dir, image_title, num))

    else:
        # 发起请求请求
        requests.post(db_url_rpl, headers=headers, data=params, verify=False)
        #input


    #res = requests.post(db_url_rpl,headers=headers, data=params)
    #print(res)
    input

    

if __name__ == '__main__':
    main()