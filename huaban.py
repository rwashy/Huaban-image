from bs4 import BeautifulSoup
import requests
import time
import re
import os


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'Cookie': 'wP_v=070f54489b21dDX0BPx4Z9TxLsoqFhTWztCuRRTWjxprPOUfLaw6QtIdoZwrQhI0; sid=HAa511uCiydxwy15np8VqISjg8s.yX1H38nJlxDq83OHdmuy%2FBcJ%2FppNnNFMYZjiVU9O6pY; _f=iVBORw0KGgoAAAANSUhEUgAAADIAAAAUCAYAAADPym6aAAABJElEQVRYR%2B1VOxYCIQwMF7KzsvFGXmW9kY2VnQfxCvgCRmfzCD9lnz53myWQAJOZBEfeeyIi7xz%2FyEXzZRPFhYbPc3hHXO6I6TbFixmfEyByeQQSxu6BcAXSkIGMazMjuBcz8pQcq44o0Iuyyc1p38C62kNsOdeSZDOQlLRQ80uOMalDgWCGMfsW2B5%2FATMUyGh2uhgptV9Ly6l5nNOa1%2F6zmjTqkH2aGEk2jY72%2B5k%2BNd9lBfLMh8GIP11iK95vw8uv7RQr4oNxOfbQ%2F7g5Z4meveyt0uKDEIiMLRC4jrG1%2FjkwKxCRE2e5lF30leyXYvQ628MZKV3q64HUFvnPAMkVuSWlEouLSiuV6dp2WtPBrPZ7uO5I18tbXWvEC27t%2BTcv%2Bx0JuJAoUm2L%2FQAAAABJRU5ErkJggg%3D%3D%2CWin32.1920.1080.24; _uab_collina=151791848165608576485496; _ga=GA1.2.192691287.1517918482; uid=10593'
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
