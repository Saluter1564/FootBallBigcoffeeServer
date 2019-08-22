import logging
import os
import sys
import django
from datetime import datetime
import json
from django.db.models import Q
from django.forms.models import model_to_dict
sys.path.append(os.path.abspath('..'))  # 将项目路径添加到系统搜寻路径当中
os.environ['DJANGO_SETTINGS_MODULE'] = 'newsapi.settings'  # 设置项目的配置文件
django.setup()
import time,json,requests
from article import models
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ttyingqiu():
    """初始化数据
        headers：headers数据
        toy_list_dict：玩法映射表
        time_Difference:当前时间6天的差值"""
    def __init__(self):
        self.headers = {'Content-Type': 'application/json; charset=UTF-8',
                        'Accept-Charset': 'UTF-8, ISO-8859-1',
                        'Cookie': 'JSESSIONID=9F9A4F13C6124CD8E1EC1FA7B3BB37FD.c219',
                        'deviceUuid': '21610e74de2ed5d1',
                        'jcobToken': '',
                        'Accept': 'application/json,text/html',
                        'sessionLoginCookie': 'dc184baf-b35a-1054-9ea7-8838fce0101e',
                        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.0; EVA-AL00 Build/HUAWEIEVA-AL00)',
                        'Host': 'tt.ttyingqiu.com',
                        'Connection': 'Keep-Alive',
                        'Accept-Encoding': 'gzip',
                        'Content-Length': '141',
                   }
        self.toy_list_dict = {'rq_rq3_checked': '让球胜',
                    'rq_rq1_checked': '让球平',
                    'rq_rq0_checked': '让球负',
                    'sf_sf3_checked': '胜',
                    'sf_sf1_checked': '平',
                    'sf_sf0_checked': '负',
                    'jc_yz_hjspl_checked': '亚盘主受让',
                    'jc_yz_wjspl_checked': '亚盘客受让',
                    'bd_yz_hjspl_checked': '主让',
                    'bd_yz_wjspl_checked': '客让',
                    'spf_sf3_checked': '胜',
                    'spf_sf1_checked': '平',
                    'spf_sf0_checked': '负'
                    }
        self.time_Difference=int(time.time()*1000)-6*24*60*60*1000

    """获取排行榜，进入数据库
            1、清除当前排行榜
            2、更新数据"""
    def rankings_list(self):
        url='https://tt.ttyingqiu.com/api/query/interpretation/list/1?agentId=2335083&platform=android&appVersion=5.7.1'
        data={
            "raceStatus":'0',
            "amountMode":'1',
            "publishType":'0',
            "improvStatus":["1","2"],
            "notWinRefund":'false',
            "ownBuyAmount":'false',
            "sortType":'10',
            "raceType":'0'
        }
        value=requests.post(url=url,headers=self.headers,json=data).text
        value=json.loads(value)
        print(value)


        return value

    """获取首页相关数据"""

    def home_data(self):
        url = 'https://tt.ttyingqiu.com/api/new/home?platform=android&appVersion=6.1.0&agentId=2335083&needTab=true'
        data={'agentId':'2335083',
              'platform':'android',
              'appVersion':'5.7.1'

        }
        cookies={'JSESSIONID':'9F9A4F13C6124CD8E1EC1FA7B3BB37FD.c219'}
        headers = {
            'Accept-Charset': 'UTF-8, ISO-8859-1',
            'Cookie': 'JSESSIONID=9F9A4F13C6124CD8E1EC1FA7B3BB37FD.c219',
            'deviceUuid': '21610e74de2ed5d1',
            'cobToken': '',
            'Accept': 'application/json,text/html',
            'sessionLoginCookie': 'dc184baf-b35a-1054-9ea7-8838fce0101e',
            'User-Agent':'Dalvik/2.1.0 (Linux; U; Android 7.0; EVA-AL00 Build/HUAWEIEVA-AL00)',
            'Host': 'tt.ttyingqiu.com',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip'
        }
        value = requests.get(url=url, headers=headers,cookies=cookies).text
        print(value)
        return value
    def sport_data(self):
        url='http://sport.ttyingqiu.com/sportdata/f?agentId=2335083&platform=android&appVersion=6.1.0'
        headers={'Content-Type': 'application/json; charset=UTF-8',
                'ccept-Charset': 'UTF-8, ISO-8859-1',
                'Cookie': '',
                'deviceUuid': '21610e74de2ed5d1',
                'jcobToken': '',
                'Accept': 'application/json,text/html',
                'sessionLoginCookie': 'dc184baf-b35a-1054-9ea7-8838fce0101e',
                'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.0; EVA-AL00 Build/HUAWEIEVA-AL00)',
                'Host': 'sport.ttyingqiu.com',
                'Connection': 'Keep-Alive',
                'Accept-Encoding': 'gzip',
                'Content-Length': '138',
                }
        json={"timestamp":int(time.time()*100),
              "verifyStr":"",
              "simple":1,
              "apiName":"getMatchListByDate",
              "date":"2019-08-09",
              "game":0,
              "pageNo":1,
              "pageSize":20
              }
        value=requests.post(url=url,headers=headers,json=json).text
        print(value)
        return value

class sportdata_api():
    def __init__(self):
        self.url='http://sport.ttyingqiu.com/sportdata/f?agentId=2335083&platform=android&appVersion=6.1.0'
        self.headers={'Content-Type': 'application/json; charset=UTF-8',
                'Accept-Charset': 'UTF-8, ISO-8859-1',
                'Cookie':'',
                'deviceUuid': '21610e74de2ed5d1',
                'jcobToken':'',
                'Accept': 'application/json,text/html',
                'sessionLoginCookie': 'dc184baf-b35a-1054-9ea7-8838fce0101e',
                'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.0; EVA-AL00 Build/HUAWEIEVA-AL00)',
                'Host': 'sport.ttyingqiu.com',
                'Connection': 'Keep-Alive',
                'Accept-Encoding': 'gzip',
                'Content-Length': '93'
                }
        self.timestamp=int(time.time()*1000)

    def post_data(self):
        value=requests.post(url=self.url,headers=self.headers,json={"timestamp":1565316168247,"verifyStr":"","apiName":"getMatchPointRank","leagueMatchId":2964377}).text
        print(value)

    def post_tt(self):
        url = 'http://sport.ttyingqiu.com/sportdata/f?agentId=2335083&platform=android&appVersion=6.1.0'
        data = {
            "timestamp": str(int(time.time() * 1000)),
            "verifyStr": "",
            "simple": str(1),
            "apiName": "getMatchListByDate",
            "game": str(0),
            "pageNo": str(1),
            "pageSize": str(20)
        }
        headers = {
        }
        data1={"timestamp":str(int(time.time() * 1000)),
               "verifyStr":"",
               "apiName":"getTeamBoutExploits",
               "matchId":3052469,
               "number":10}
        data=requests.post(url=url,json=data1)
        print(data.text)
if __name__ == "__main__":
    # data=ttyingqiu()
    # #print(time.time())
    # # data.rankings_list()
    # # data.home_data()
    # data.sport_data()
    # value=sportdata_api()
    # print(value.post_tt())
    # print(time.time())
    # print(value.post_data())
    print(requests.post(url='http://127.0.0.1:3000/getTeamBoutExploits').text)