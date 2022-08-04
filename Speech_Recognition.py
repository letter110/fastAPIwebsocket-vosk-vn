from vosk import Model, KaldiRecognizer
import pyaudio
import librosa
model = Model('D:/Project/thuc_tap_he/vosk/vn')
recognizer = KaldiRecognizer(model, 16000)

############################
# test micro
############################
# cap = pyaudio.PyAudio()
# stream = cap.open(format=pyaudio.paInt16, channels=1,
#                   rate=16000, input=True, frames_per_buffer=8192)
# stream.start_stream()
# print('started')
# while(True):
#     data = stream.read(4096*3)
#     if len(data) == 0:
#         break
#     if recognizer.AcceptWaveform(data):
#         print(recognizer.Result())


