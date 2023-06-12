import pyaudio
import wave
import threading
import tkinter as tk

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


root = tk.Tk()

start_button = tk.Button(root, text="开始说话", command=start_recording)
start_button.pack()

stop_button = tk.Button(root, text="结束说话", command=stop_recording)
stop_button.pack()

root.mainloop()
