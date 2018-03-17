from bs4 import BeautifulSoup
import requests
import time
import re
import os


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'Cookie': '***'
}
pattern = re.compile('\"pin_id\":(\w+)')


def get_picID(item, pages):
    picids = []
    for i in range(1, pages+1):
        url = 'http://huaban.com/search/?q={}&page={}'.format(item, i)
        web_data = requests.get(url, headers=headers)
        soup = BeautifulSoup(web_data.text, 'lxml')
        # 使用extend可以追加元素，而不是append的将整个列表放入大列表中
        picids.extend(pattern.findall(str(soup)))
        time.sleep(1)
    print('共有{}个结果'.format(len(picids)))
    return picids


def get_pic(picID, addr):
    os.makedirs(addr+'/pic/')
    for i in picID:
        url = 'http://huaban.com/pins/{}/'.format(i)
        # print(url)
        pattern2 = re.compile('\"pin_id\":{}([\s\S]*?)(\"width\")'.format(i))
        pattern3 = re.compile('\"key\":\"([\s\S]*?)\"')
        pattern4 = re.compile('\"type\":\"image/(\w*?)\"')
        web_data = requests.get(url, headers=headers)
        soup = BeautifulSoup(web_data.text, 'lxml')
        imgurl1 = pattern2.findall(str(soup))
        imgurl2 = pattern3.findall(str(imgurl1))
        imgTYPE = pattern4.findall(str(imgurl1))
        if imgTYPE[0] == 'jpeg':
            end = 'jpg'
        else:
            end = imgTYPE[0]
        trueURL = 'http://img.hb.aicdn.com/'+imgurl2[0]  # +'.{}'.format(end)
        with open(addr+'/pic/'+imgurl2[0]+'.{}'.format(end), 'wb') as f:
            f.write(requests.get(trueURL).content)
        time.sleep(1)


get_pic(get_picID('car+wheel', 10), 'F:/save')

'''
url = 'http://huaban.com/pins/125991242/'
#print(url)
web_data = requests.get(url, headers=headers)
soup = BeautifulSoup(web_data.text, 'lxml')
#print(soup)
imgurl1 = pattern2.findall(str(soup))
imgurl2 = pattern3.findall(str(imgurl1))
trueURL = imgurl2[0]
#img = imgurl.get('src')
print(trueURL)
'''
