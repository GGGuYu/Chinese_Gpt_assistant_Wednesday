import time
import threading
import sys

import nls
from play_voice import play_voice
from test_utils import TEST_ACCESS_AKID, TEST_ACCESS_AKKEY,TEST_ACCESS_APPKEY
from nls.token import getToken
import json
URL="wss://nls-gateway.cn-shanghai.aliyuncs.com/ws/v1"
TOKEN=""  #参考https://help.aliyun.com/document_detail/450255.html获取token

class TestSr:
    YuYinTEXT = 'null'
    def __init__(self, tid, test_file, Token , appkey):
        self.__th = threading.Thread(target=self.__test_run)
        self.__id = tid
        self.__test_file = test_file
        self.__token = Token
        self.__appkey = appkey
        
   
    def loadfile(self, filename):
        with open(filename, 'rb') as f:
            self.__data = f.read()
    
    def start(self):
        self.loadfile(self.__test_file)
        self.__th.start()
        self.__th.join()

    def test_on_start(self, message, *args):
        print('test_on_start:{}'.format(message))

    def test_on_error(self, message, *args):
        print('on_error args=>{}'.format(args))

    def test_on_close(self, *args):
        print('on_close: args=>{}'.format(args))

    def test_on_result_chg(self, message, *args):
        print('test_on_chg:{}'.format(message))
        # print("改变啦！！")

    def test_on_completed(self, message, *args):
        parsed_data = json.loads(message)
        result = parsed_data['payload']['result']
        # print(result)
        self.YuYinTEXT = result
        # print(self.YuYinTEXT)

    def __test_run(self):
        # print('thread:{} start..'.format(self.__id))
        
        sr = nls.NlsSpeechRecognizer(
                    token=self.__token,
                    appkey=self.__appkey,
                    # on_start=self.test_on_start,
                    on_result_changed=self.test_on_result_chg,
                    on_completed=self.test_on_completed,
                    # on_error=self.test_on_error,
                    # on_close=self.test_on_close,
                    callback_args=[self.__id]
                )
        # print('{}: session start'.format(self.__id))
        r = sr.start(ex={'format':'pcm', 'hello':123})
           
        self.__slices = zip(*(iter(self.__data),) * 640)
        for i in self.__slices:
            sr.send_audio(bytes(i))
            # time.sleep(0.01)

        r = sr.stop()
        # print('{}: sr stopped:{}'.format(self.__id, r))
        # time.sleep(5)

def multiruntest(num=500):
    for i in range(0, num):
        name = 'thread' + str(i)
        t = TestSr("thread_sr", 'tests/test1.pcm' , TOKEN , TEST_ACCESS_APPKEY)
        t.start()

# info = getToken(TEST_ACCESS_AKID, TEST_ACCESS_AKKEY)
# print("token: " + info)
# TOKEN = info
# nls.enableTrace(True)
# multiruntest(1)
# t = TestSr("thread_sr", 'tests/test1.pcm' , TOKEN , TEST_ACCESS_APPKEY)
# t.start()
# multiruntest(1)
