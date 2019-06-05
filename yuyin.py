from pyaudio import PyAudio,paInt16
import time 
from urllib.request import urlopen,Request
import json

def play_audio(data):
    pa = PyAudio()  #设备实例化
    equip = pa.open(
         format=paInt16,
         channels=1,
         rate=16000,
         output=True,
    )#打开设备，并且支持输出
    equip.write(data)#
    equip.stop_stream()
    equip.close()
    pa.terminate()#关闭设备实例
def record_audio():
    pa = PyAudio()
    equip = pa.open(
         format=paInt16,
         channels=1,
         rate=16000,
         input=True,
         frames_per_buffer=1024,
    )
    data = []
    times = 0
    start = time.time()
    while times < 50:
        data.append(equip.read(1024))
        times += 1
    end = time.time()
    print('[TALK] %.2f' % (end - start))
    data = b''.join(data)
    equip.close()
    pa.terminate()#关闭设备实例
    return data
def baidu_token():
    Secret = 'OtDjqLYWsYK09s4DmcCNG0lrTDqj25If'
    API = 'uvQP8Opq0WrzBrU66TpZCvPN'
    grant_type = 'client_credentials'
    url = 'https://openapi.baidu.com/oauth/2.0/token?grant_type=%s&client_id=%s&client_secret=%s'
    response = json.loads(urlopen(url % (grant_type,API,Secret)).read().decode())
    result = response['access_token']
    return result
    
def baidu_api(data):
    url = 'http://vop.baidu.com/server_api'
    data_len = len(data)
    access_token = baidu_token()
    post_data = json.dumps({
        "format":"wav",
        "rate":16000,
        "channel":1,
        "cuid":" 00-50-56-C0-00-08",
        "token":access_token,
        "len":data_len,
    }).encode()
    headers = {'Content-Type':'application/json'}
    res = Request(url,headers=headers,data=post_data)
    ress = json.loads(urlopen(res).read().decode())
    return ress
def main():
    data = record_audio()
    rs = baidu_api(data)
    print(rs)

if __name__ == '__main__':
    main()
   
