import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import requests
import urllib3
import json
from lib import utils

urllib3.disable_warnings()

global Output
global Next_Output

proxies = {"http": "http://localhost:8888", "https":"http://localhost:8888"}
verify = "FiddlerRoot.pem"
#########피들러 캡쳐용############

url = "https://news.naver.com/main/main.naver"
header={'Content-Type': 'application/xhtml+xml; charset=utf-8','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
params = {
    'mode':'LSD',
    'mid':'shm',
    'sid1': 100
}

try:
    #result = requests.get(url, headers=header, params=params, proxies=proxies, verify=verify) 피들러용
    result = requests.get(url, headers=header, params=params, verify=False)
    Output = result.text
except Exception as e:
    print("Exception: {}".format(e))

Output = utils.StrGrab(Output, '<div class="cluster_body">', '<div class="cluster_body">', 1)
Output = utils.StrGrab(Output, '<div class="cluster_text">', '<div class="cluster_foot">', 1)

ResultList = list()
subResultList = list()

#헤드라인 제목, 신문사, URL
i = 1
while True:
    aURL = utils.StrGrab(Output, '<a href="', '"', i)
    company = utils.StrGrab(Output, '<div class="cluster_text_press">', '</div>', i)
    HeadLine = utils.StrGrab(Output, 'class="cluster_text_headline nclicks(cls_pol.clsart)">', '</a>', i)
    if aURL == "": break
    subResultList.append(aURL)
    subResultList.append(company)
    subResultList.append(HeadLine)
    ResultList.append(subResultList)
    subResultList = list()
    i = i + 1
    
print(ResultList)

ainput = input("원하는 기사 번호를 입력하세요(0~3): ")

Next_url = ResultList[int(ainput)][0]

result_company = ResultList[int(ainput)][1] #신문사 결과값
result_HeadLine = ResultList[int(ainput)][2] #헤드라인 결과값

Next_param_1 = utils.StrGrab(Next_url, '?', '=', 1)
Next_param_2 = utils.StrGrab(Next_url, '=', '', 1)
Next_url = utils.StrGrab(Next_url, '', '?', 1)

Next_param = {
    Next_param_1 : Next_param_2
}

try:    
    Next_result = requests.get(Next_url, headers=header, params=Next_param, verify=False)
    Next_Output = Next_result.text    

except Exception as e:
    print("Exception: {}".format(e))
    
resul_Name = utils.StrGrab(Next_Output, '<span class="byline_s">', '</span>', 1)
resul_Date = utils.StrGrab(Next_Output, 'data-date-time="', '">', 1)

result_Json = dict(
    신문사 = result_company,
    해드라인 = result_HeadLine,
    기자 = resul_Name,
    기사날짜 = resul_Date
)

print(result_Json)


