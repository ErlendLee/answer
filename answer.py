# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from PIL import ImageGrab,Image
from aip import AipOcr
import requests
headers = {
"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36",
}
APP_ID = '??????' #你的百度云appid
API_KEY = '????????'  #你调用百度云接口的apikey
SECRET_KEY = '???????' #百度云SECRET_KEY
client = AipOcr(APP_ID,API_KEY,SECRET_KEY)
""" 读取图片 """
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()
""" 如果有可选参数 """
options = {}
options["language_type"] = "CHN_ENG"
options["detect_direction"] = "true"
options["detect_language"] = "true"
options["probability"] = "true"
back = {'0':'A',
        '1':'B',
        '2':'C',
        '3':'D'}
action = ''
while action != 'over':  
    answers = []
    answers_count = []
    bbox = (40, 260, 320, 640)
    img = ImageGrab.grab(bbox)
    img.save('jietu1.jpg')
    base_img = Image.open('jietu1.jpg')
    box1 = (0,92,21,120)
    box2 = (264,92,279,120) #截图区域
    tmp_img = Image.open('tietu.jpg')
    region = tmp_img
    region1 = region.resize((box1[2]-box1[0],box1[3]-box1[1]))
    base_img.paste(region1,box1)
    region2 = region.resize((box2[2]-box2[0],box2[3]-box2[1]))
    base_img.paste(region2,box2)
    base_img.save('jietu.jpg')
    image = get_file_content('jietu.jpg')
    """ 调用通用文字识别, 图片参数为本地图片 """
    text = client.basicGeneral(image)
    howmany = len(text['words_result'])
    i = 0
    title = ''
    while i <= howmany-5:
        title = title + str(text['words_result'][i]['words']).replace(' ','')
        i += 1
    print('题目：',title)
    while i < howmany :
        answers.append(text['words_result'][i]['words'])
        i += 1
    res = requests.get('https://www.baidu.com/s?wd='+title,headers=headers)
    result = res.text.encode(res.encoding).decode('utf-8')
    j = 0
    while j <= 3:
        answers_count.append(result.count(answers[j]))
        j += 1
    k = 0
    while k <= 3:
        print(back[str(k)],'-',answers[k],'-',answers_count[k])
        k += 1
    if answers_count.count(max(answers_count)) == 1:
        print('推荐答案是：',back[str(answers_count.index(max(answers_count)))])
    else:
        print('无推荐答案')
    action = input()
