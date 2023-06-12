import pyaudio
import wave

def play_voice(filename):
    # 打开WAV文件
    wf = wave.open(filename, 'rb')

    # 创建PyAudio对象
    p = pyaudio.PyAudio()

    # 打开音频流
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

    # 播放音频
    while True:
        data = wf.readframes(1024)
        if not data:
            break
        stream.write(data)

    # 关闭音频流和PyAudio对象
    stream.stop_stream()
    stream.close()
    p.terminate()