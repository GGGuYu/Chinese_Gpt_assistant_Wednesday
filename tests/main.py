import asyncio
import websockets
import pyaudio
import wave
import threading
import nls
from play_voice import play_voice
from test_utils import TEST_ACCESS_AKID, TEST_ACCESS_AKKEY,TEST_ACCESS_APPKEY
from nls.token import getToken
from databaseHelper import DatabaseHelper
from openbrower import open_browser
from APIforWednesday import create_word_file,read_txt_file,read_word_file,open_website,play_music

# 全局变量，用于保存当前正在播放的音乐文件名
current_playing = None

# 存储所有连接的客户端
clients = set()
URL="wss://nls-gateway.cn-shanghai.aliyuncs.com/ws/v1"
TOKEN=""  #参考https://help.aliyun.com/document_detail/450255.html获取token

from test_sr import TestSr 
from test_tts import TestTts

info = getToken(TEST_ACCESS_AKID, TEST_ACCESS_AKKEY)
print("token: " + info)
TOKEN = info
nls.enableTrace(True)
databaseHelper = DatabaseHelper()


FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024

frames = []

class AudioRecorder:
    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.is_recording = False

    def start_recording(self):
        frames.clear()
        self.stream = self.audio.open(format=FORMAT, channels=CHANNELS,
                                      rate=RATE, input=True,
                                      frames_per_buffer=CHUNK)
        self.is_recording = True

        t = threading.Thread(target=self.record)
        t.start()

    def stop_recording(self):
        self.is_recording = False

    def record(self):
        global frames
        while self.is_recording:
            data = self.stream.read(CHUNK, exception_on_overflow=False)
            frames.append(data)

    def save_recording(self, filename):
        wf = wave.open(filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(self.audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()


recorder = AudioRecorder()


def start_recording():
    recorder.start_recording()

def stop_recording():
    recorder.stop_recording()
    recorder.save_recording("tests/output.pcm")

def wake_up_3():
    memolist = databaseHelper.get_memos()
    memoString = ''
    mcnt = 0
    for m in memolist:
        mcnt += 1
        pre = '记忆' + str(mcnt) + ':'
        memoString += pre + m + ';'
    print(memoString)
    if memoString != '':
        memoString += '以上是你与当前用户交流的几段之前的对话，这些可能能够帮助你与用户更好的交流。'
    strings = [
        "在接下来的对话中，你将扮演一位名为星期三的私人助理，必须保证严格遵守以下规则:",
        "#规则1: 你的主要目的是与用户闲聊,因此回复尽量活泼简短.",
        "#规则2: 你的回复必须控制在120字符以内, 尽量简短.",
        "#规则3: 你的名字叫做星期三,不能告诉用户你是AI语言模型.",
        "并且星期三可以通过回复的文字中添加一些格式化指令去帮助用户做一些现实中的事情,下面列举一些星期三可以使用的格式化指令,在[]中的为格式化指令.",
        "格式化指令_1:[create_word_file(content, filename)]:这个格式化指令用于创建一个word文档,其中content和filename",
        "是需要星期三填写的parameter,content是文档内容,filename是保存的文件名;",
        "example for 格式化指令_1: {用户说:\"写一篇word文档内容是你的自我介绍,文件名是profile\" 星期三回复:\"[create_word_file('我是星期三，一个您的私人助理。', 'profile.docx')],已为您完成word,请检查。\".",
        "example for 格式化指令_1: {用户说:\"帮我写一篇主题是战争的文章,放在word中,文件名是war\" 星期三回复:\"[create_word_file('关于战争,我认为... ...', 'war.docx')],已为您完成word,请检查。\".",
        "格式化指令_2:[read_file(filename)]:这个格式化指令用于帮助星期三读取一个txt或word文件,其中filename",
        "是需要星期三填写的parameter,filename是目标的文件名,回复这个指令之后,星期三会得到系统程序对这个文档内容的回复;",
        "example for 格式化指令_2: {用户说:\"请你查看test文件,它是一个txt后缀文件,查看后总结一下内容给我。\" 星期三回复:\"[read_file('test.txt')],正在查阅text.txt,等待系统返回\",然后星期三结束输入等待回复}.",
        "example for 格式化指令_2: {用户说:\"请你查看work文件,它是一个docx后缀文件,查看后总结一下内容给我。\" 星期三回复:\"[read_file('work.docx')],正在查阅work.docx,等待系统返回\",然后星期三结束输入等待回复}.",
        "格式化指令_3:[open_website(url)]:这个格式化指令用于在浏览器中打开网址为url的网站",
        "url是需要星期三填写的parameter,url是网站网址;",
        "example for 格式化指令_3: {用户说:\"打开哔哩哔哩\" 星期三回复:\"[open_website('https://www.bilibili.com/')],已为您打开哔哩哔哩网站,请检查。\".",
        "example for 格式化指令_3: {用户说:\"帮我打开youtube\" 星期三回复:\"[open_website('https://www.youtube.com/')],已为您打开YouTube网站,请检查。\".",
        # "格式化指令_4:[play_music(musicname)]:这个格式化指令用于播放名称为musicname.mp3的音乐",
        # "musicname是需要星期三填写的parameter,musicname是音乐名;",
        # "example for 格式化指令_4: {用户说:\"放一首一路向北\" 星期三回复:\"[play_music('一路向北.mp3')],已为您播放一路向北,请享用。\".",
        # "example for 格式化指令_4: {用户说:\"播放音乐,歌名是夜曲\" 星期三回复:\"[play_music('夜曲.mp3')],已为您播放夜曲,请享用。\".",
        "格式化指令_4:[open_music_site()]:这个格式化指令用于帮助用户打开音乐网站,这个指令不需要参数,系统会直接打开音乐网站",
        "example for 格式化指令_4: {用户说:\"打开音乐\" 星期三回复:\"[open_music_site()],已为您打开音乐播放网站,请享用。\".",
        "example for 格式化指令_4: {用户说:\"我要听点歌\" 星期三回复:\"[open_music_site()],已为您打开音乐播放网站,请享用。\".",
        "通过以上格式化指令的example可以看出,格式化指令和python中的函数类似,星期三通过在回复中添加这些[]括号中的格式化指令,",
        "其他程序会帮助星期三实现格式化指令对应的功能,所以你只需要在回复中添加对应任务的格式化指令,就可以真实的帮助到用户完成任务。",
        "但是只有在上文明确出现过的格式化指令才是星期三可以使用的,",
        "这在下句话之后我们将开启全新的对话。",
        "你不用对上面的话做出任何回复，",
        "请合理地在回复中添加格式化指令语句实现用户的需求(若用户提出需求),并必须严格遵守你的规则,更好的扮演星期三和用户交流,现在你将回复：",
        "\"欢迎回来亲爱的先生,这里是星期三。\"。之后等待用户回复。"
    ]
    strings.insert(0 , memoString)
    result = "".join(strings)
    return result

async def receive(websocket, path):
    # 添加新的客户端到集合中
    clients.add(websocket)
    print('有新的客户端连接')
    LOCKED = False
    FRIST = True
    SystemLocked = False
    try:
        async for message in websocket:
            # 接收到消息时处理
            print(f'接收到客户端发来的消息：{message}')
            memo = message
            if LOCKED:
                databaseHelper.add_memo(memo)
                message = "遵命，我将会彻底的记住这次愉快的对话。"
                LOCKED = False
            
            if FRIST and message != "连接开始！":
                message = "欢迎回来亲爱的先生,这里是星期三。"
                FRIST = False

            if message != "连接开始！":
                # 在新线程中播放语音
                # 装载语音文件
                tts = TestTts("thread_tts" , "tests/test_tts.wav" , TOKEN , TEST_ACCESS_APPKEY)
                tts.start(message)
                t2 = threading.Thread(target=play_voice, args=("tests/test_tts.wav",))
                t2.start()




        #这里开始主要是在判断有没有星期三自行决定要执行的指令
            ind_word = message.find("create_word_file")
            ind_txt_read = message.find("read_file")
            ind_open_web = message.find("open_website")
            ind_play_music = message.find("play_music")
            ind_open_music_site = message.find("open_music_site()")
            txtresult = ""
            #如果检测到wordapi
            if ind_word != -1:
                param = message[ind_word+16:]
                pre1 , rear1 , pre2 , rear2 = -1 , -1 , -1 ,-1
                cnt = 0
                index = 0
                for i in param:
                    index += 1
                    if i == '\'':
                        cnt += 1
                        if cnt == 1:
                            pre1 = index
                        elif cnt == 2:
                            rear1 = index
                        elif cnt == 3:
                            pre2 = index
                        elif cnt == 4:
                            rear2 = index
                if pre1 != -1 and pre2 != -1 and rear1 != -1 and rear2 != -1:
                    #拿出参数
                    content = param[pre1:rear1-1]
                    filename = param[pre2:rear2-1]
                    create_word_file(content , filename)

            #如果检测到阅读word或者txtAPI
            if ind_txt_read != -1:
                param = message[ind_word+9:]
                pre1 , rear1  = -1 , -1 
                cnt = 0
                index = 0
                for i in param:
                    index += 1
                    if i == '\'':
                        cnt += 1
                        if cnt == 1:
                            pre1 = index
                        elif cnt == 2:
                            rear1 = index
                if pre1 != -1 and rear1 != -1:
                    #拿出参数
                    filename = param[pre1:rear1-1]
                    if filename[-1] == 'x':
                        txtresult = read_word_file(filename)
                    elif filename[-1] == 't':
                        txtresult = read_txt_file(filename)
                    txtresult = "这是一条系统回复,以下是" + filename+ "的内容:" + txtresult
                    SystemLocked = True

            #如果检测到打开网站api
            if ind_open_web != -1:
                param = message[ind_word+12:]
                pre1 , rear1 = -1 , -1
                cnt = 0
                index = 0
                for i in param:
                    index += 1
                    if i == '\'':
                        cnt += 1
                        if cnt == 1:
                            pre1 = index
                        elif cnt == 2:
                            rear1 = index
                if pre1 != -1 and rear1 != -1:
                    #拿出参数
                    url = param[pre1:rear1-1]
                    tw = threading.Thread(target=open_website, args=(url,))
                    tw.start()

            #如果检测到打开音乐api
            if ind_open_music_site != -1:
                url = 'https://tool.liumingye.cn/music/#/search/M/song/一路向北'
                tw = threading.Thread(target=open_website, args=(url,))
                tw.start()

            #如果检测到播放音乐API
            if ind_play_music != -1:
                param = message[ind_word+10:]
                pre1 , rear1 = -1 , -1
                cnt = 0
                index = 0
                for i in param:
                    index += 1
                    if i == '\'':
                        cnt += 1
                        if cnt == 1:
                            pre1 = index
                        elif cnt == 2:
                            rear1 = index
                if pre1 != -1 and rear1 != -1:
                    #拿出参数
                    musicname = param[pre1:rear1-1]
                    play_music(musicname)

            #判断指令结束





            inputs = "" #用户输入
            result = "" #待发送信息
            cnt = 0 #状态判别器
            if FRIST:
                result = wake_up_3()
            elif SystemLocked:
                result = txtresult
                SystemLocked = False
            else:
                print("正在等待输入，")
                print("输入1开始录音，")
                print("输入2停止录音,")
                print("输入3保存长期记忆,")
                print("输入4重新唤醒星期三")
                while True:
                    inputs = input() 
                    if inputs == '1':
                        cnt += 1
                        if cnt == 1:
                            start_recording() #新开一个线程去搞
                        else:
                            print("正在录制，结束请按2")
                    if inputs == '2':
                        stop_recording()
                        t = TestSr("thread_sr", 'tests/output.pcm' , TOKEN ,TEST_ACCESS_APPKEY)
                        t.start()
                        # 将识别结果作为消息发送到聊天界面
                        print("识别结果： "  + t.YuYinTEXT)
                        result = t.YuYinTEXT
                        break
                    if inputs == '3' and cnt != 1:
                        result = '请对这次的对话中的重要内容做一个不超过100字的总结'
                        LOCKED = True #添加记忆锁
                        break
                    if inputs == '4' and cnt != 1:
                        result = wake_up_3()
                        LOCKED = False
                        FRIST = True
                        SystemLocked = False
                        break
                    if inputs != '1' and inputs != '2' and inputs != '3' and inputs != '4':
                        if cnt == 1:
                            stop_recording()
                            cnt = 0
            #将消息发送给所有已连接的客户端（除了当前客户端）
            await websocket.send(result)

    except websockets.exceptions.ConnectionClosed:
        print('客户端断开连接')

    finally:
        # 移除已断开连接的客户端
        clients.remove(websocket)

async def send(message):
    # 向所有已连接的客户端发送消息
    for client in clients:
        if client.open:
            await client.send(message)

async def start_server():
    async with websockets.serve(receive, "localhost", 8888):
        print("WebSocket 服务器已启动")
        await asyncio.Future()  # 阻止停止

if __name__ == "__main__":
    # t3 = threading.Thread(target=open_browser)
    # t3.start()
    #以上两行自动打开浏览器的代码并不支持BAI，只能使用备用网站
    asyncio.run(start_server())