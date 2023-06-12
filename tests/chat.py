import tkinter as tk
import requests
import json
import pyaudio
import wave
import threading
import time
import sys
import nls
from play_voice import play_voice
from test_utils import TEST_ACCESS_AKID, TEST_ACCESS_AKKEY,TEST_ACCESS_APPKEY
from nls.token import getToken


URL="wss://nls-gateway.cn-shanghai.aliyuncs.com/ws/v1"
TOKEN=""  #参考https://help.aliyun.com/document_detail/450255.html获取token

from test_sr import TestSr 
from test_tts import TestTts

info = getToken(TEST_ACCESS_AKID, TEST_ACCESS_AKKEY)
print("token: " + info)
TOKEN = info
nls.enableTrace(True)


FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024

frames = []

class ChatView:
    def __init__(self, master):
        self.messages = []
        self.api_endpoint = "https://api.openai.com/v1/chat/completions"
        self.api_key = "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" # Replace with your actual API key
        self.model = "gpt-3.5-turbo"
        self.temperature = 0.7
        
        self.master = master
        self.master.title("星期三")
        
        # chat messages frame
        self.chat_messages_frame = tk.Frame(self.master)
        self.chat_messages_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        self.chat_messages_scrollbar = tk.Scrollbar(self.chat_messages_frame)
        self.chat_messages_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.chat_messages_text = tk.Text(self.chat_messages_frame, wrap=tk.WORD, yscrollcommand=self.chat_messages_scrollbar.set)
        self.chat_messages_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.chat_messages_scrollbar.config(command=self.chat_messages_text.yview)
        
        # chat input frame
        self.chat_input_frame = tk.Frame(self.master)
        self.chat_input_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.chat_input_entry = tk.Entry(self.chat_input_frame)
        self.chat_input_entry.pack(side=tk.LEFT, padx=5, pady=5, expand=True, fill=tk.X)
        
        self.chat_input_button = tk.Button(self.chat_input_frame, text="Send", command=self.send_message)
        self.chat_input_button.pack(side=tk.RIGHT, padx=5, pady=5)

        # Bind enter key to send message
        self.bind_enter_key()

    def bind_enter_key(self):
        self.master.bind('<Return>', lambda event: self.chat_input_button.invoke())

    def send_message(self):
        user_message = self.chat_input_entry.get().strip()
        if user_message == "":
            return
        
        message = {
            "id": str(len(self.messages)),
            "role": "user",
            "content": user_message,
        }
        self.messages.append(message)
        self.chat_messages_text.insert(tk.END, f"\nYou: {message['content']}")
        
        self.chat_input_entry.delete(0, tk.END)
        
        send_messages = []
        for m in self.messages:
            send_messages.append({"role": m['role'], "content": m['content']})

        print("send_messages : ")
        print(send_messages)
        try:
            response = requests.post(self.api_endpoint, headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            }, data=json.dumps({
                "model": self.model,
                "messages": send_messages,
                "temperature": self.temperature,
            }))
            
            send_messages.clear()
            data = response.json()
            bot_message = data["choices"][0]['message']['content'].strip()
            # 装载语音文件
            tts = TestTts("thread_tts" , "tests/test_tts.wav" , TOKEN , TEST_ACCESS_APPKEY)
            tts.start(bot_message)
            bot_message_obj = {
                "id": str(len(self.messages)),
                "role": "bot",
                "content": bot_message,
            }
            self.messages.append(bot_message_obj)
            self.chat_messages_text.insert(tk.END, f"\nBot: {bot_message_obj['content']}")
            # 在新线程中播放语音
            t2 = threading.Thread(target=play_voice, args=("tests/test_tts.wav",))
            t2.start()
        except Exception as e:
            print(f"Error while sending message: {e}")


class AudioRecorder:
    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.is_recording = False

    def start_recording(self):
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

root = tk.Tk()

chat_view = ChatView(root)



def start_recording():
    recorder.start_recording()

def stop_recording():
    recorder.stop_recording()
    recorder.save_recording("tests/output.pcm")
    t = TestSr("thread_sr", 'tests/output.pcm' , TOKEN ,TEST_ACCESS_APPKEY)
    t.start()
    # 将识别结果作为消息发送到聊天界面
    chat_view.chat_input_entry.insert(0, t.YuYinTEXT)
    # print("检查: " + t.YuYinTEXT)
    chat_view.send_message()
    chat_view.chat_input_entry.delete(0, 'end')
    
start_button = tk.Button(root, text="开始说话", command=start_recording)
start_button.pack()

stop_button = tk.Button(root, text="结束说话", command=stop_recording)
stop_button.pack()

root.mainloop()

