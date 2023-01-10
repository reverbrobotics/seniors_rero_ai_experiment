import json

import librosa
import os
import grpc
import rero_grpc.audio_pb2_grpc as audio_grpc
import rero_grpc.audio_pb2 as audio
import rero_grpc.speech_recognition_pb2_grpc as sr_grpc
import rero_grpc.speech_recognition_pb2 as sr
import rero_grpc.nlu_pb2 as nlu
import rero_grpc.nlu_pb2_grpc as nlu_grpc
import rero_grpc.text_to_speech_pb2_grpc as tts_grpc
import rero_grpc.text_to_speech_pb2 as tts
import soundfile as sf
import numpy as np

channel = grpc.insecure_channel("127.0.0.1:50052")
sr_stub = sr_grpc.SpeechRecognitionStub(channel)
audio_stub = audio_grpc.AudioStreamerStub(channel)

src_file = '/media/lukas/data/datasets/seniors_dataset/participant_audio/participant/recording_1668840847955.raw'

def recognize_file(fp):
    audio_list = []

    with open(src_file, 'rb') as read_file:
        bytes = read_file.read(2048)

        while(len(bytes) == 2048):
            audio_obj = audio.Audio()
            audio_obj.sample_rate = 16000
            audio_obj.num_channels = 1
            audio_obj.frames_per_buffer = 1024
            audio_obj.bytes_per_sample = 2
            audio_obj.raw_data = bytes

            audio_list.append(audio_obj)

            bytes = read_file.read(2048)

    sr_result = sr_stub.RecognizeSpeech(iter(audio_list))


    parsed_result = json.loads(sr_result.result)
    text = parsed_result['text']
    return text

text = recognize_file(src_file)
print(text)

channel.close()
