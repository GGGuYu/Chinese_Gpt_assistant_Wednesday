import time
import threading
import sys
from nls.token import getToken
import nls
from play_voice import play_voice
from test_utils import TEST_ACCESS_AKID, TEST_ACCESS_AKKEY,TEST_ACCESS_APPKEY
URL="wss://nls-gateway.cn-shanghai.aliyuncs.com/ws/v1"
TOKEN=""  #参考https://help.aliyun.com/document_detail/450255.html获取token





TEXT='我是一个笨猪哦'

class TestTts:
    def __init__(self, tid, test_file , Token , appkey):
        self.__th = threading.Thread(target=self.__test_run)
        self.__id = tid
        self.__test_file = test_file
        self.__token = Token
        self.__appkey = appkey
   
    def start(self, text):
        self.__text = text + "~~"
        self.__f = open(self.__test_file, "wb")
        self.__th.start()
        self.__th.join()
    
    def test_on_metainfo(self, message, *args):
        print("on_metainfo message=>{}".format(message))  

    def test_on_error(self, message, *args):
        print("on_error args=>{}".format(args))

    def test_on_close(self, *args):
        print("on_close: args=>{}".format(args))
        try:
            self.__f.close()
        except Exception as e:
            print("close file failed since:", e)

    def test_on_data(self, data, *args):
        try:
            self.__f.write(data)
        except Exception as e:
            print("write data failed:", e)

    def test_on_completed(self, message, *args):
        print("on_completed:args=>{} message=>{}".format(args, message))


    def __test_run(self):
        print("thread:{} start..".format(self.__id))
        # print("进来之后的Token:" + TOKEN)
        tts = nls.NlsSpeechSynthesizer(
                    token=self.__token,
                    appkey=self.__appkey,
                    # on_metainfo=self.test_on_metainfo,
                    on_data=self.test_on_data,
                    on_completed=self.test_on_completed,
                    # on_error=self.test_on_error,
                    # on_close=self.test_on_close,
                    callback_args=[self.__id]
                )

        # while True:
        #     print("{}: session start".format(self.__id))
        #     r = tts.start(self.__text, voice="ailun", ex={'enable_subtitle':True})
        #     print("{}: tts done with result:{}".format(self.__id, r))
        #     time.sleep(5)
        # print("{}: session start".format(self.__id))
        r = tts.start(self.__text, voice="ruoxi",aformat="wav"
                      ,volume=100,speech_rate=110,pitch_rate=-1)
        # print("{}: tts done with result:{}".format(self.__id, r))
        # time.sleep(5)
        
def multiruntest(num=500):
    for i in range(0, num):
        name = "thread" + str(i)
        t = TestTts(name, "tests/test_tts.pcm")
        t.start(TEXT)
        
# info = getToken(TEST_ACCESS_AKID, TEST_ACCESS_AKKEY)
# print("token: " + info)
# TOKEN = info
# nls.enableTrace(True)
# # multiruntest(1)
# name = "thread_1"
# t = TestTts(name , "tests/test_tts.wav" , TOKEN , TEST_ACCESS_APPKEY)
# t.start(TEXT)


