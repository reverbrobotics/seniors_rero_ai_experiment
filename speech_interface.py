import json
import grpc
import rero_grpc.audio_pb2_grpc as audio_grpc
import rero_grpc.audio_pb2 as audio
import rero_grpc.speech_recognition_pb2_grpc as sr_grpc
import rero_grpc.speech_recognition_pb2 as sr
import rero_grpc.nlu_pb2 as nlu
import rero_grpc.nlu_pb2_grpc as nlu_grpc
import rero_grpc.text_to_speech_pb2_grpc as tts_grpc
import rero_grpc.text_to_speech_pb2 as tts

class SpeechInterface:
    def __init__(self, host):
        self.channel = grpc.insecure_channel(host)

        #audio stub
        self.audio_stub = audio_grpc.AudioStreamerStub(self.channel)

        #speech recognition stub
        self.sr_stub = sr_grpc.SpeechRecognitionStub(self.channel)

        #nlu stub
        self.nlu_stub = nlu_grpc.NLUStub(self.channel)

        #tts stub
        self.tts_stub = tts_grpc.TextToSpeechStub(self.channel)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.channel.close()

    def setVocab(self, vocab):
        vocab_request = sr.Vocab()
        vocab_request.vocab = vocab
        self.sr_stub.SetVocab(vocab_request)

    def getRawSRResult(self):
        # create audio request object
        request = audio.StreamRequest()

        # set audio params
        request.sample_rate = 16000
        request.num_channels = 1
        request.format = "paInt16"
        request.frames_per_buffer = 1024
        request.bytes_per_sample = 2

        #get speech recognition result synchronously (call sr_stub.RecognizeSpeech.future for asynchronous object)
        audio_stream = self.audio_stub.GetStream(request)
        sr_result = self.sr_stub.RecognizeSpeech(audio_stream)

        #parse json result
        parsed_result = json.loads(sr_result.result)

        return parsed_result['text']

    def getSRNLUResult(self):
        # create audio request object
        request = audio.StreamRequest()

        # set audio params
        request.sample_rate = 16000
        request.num_channels = 1
        request.format = "paInt16"
        request.frames_per_buffer = 1024
        request.bytes_per_sample = 2

        #get speech recognition result synchronously (call sr_stub.RecognizeSpeech.future for asynchronous object)
        audio_stream = self.audio_stub.GetStream(request)

        sr_result = self.sr_stub.RecognizeSpeech(audio_stream)

        for audio in audio_stream:
            print(audio)

        #parse json result
        parsed_result = json.loads(sr_result.result)

        nlu_request = nlu.NLURequest()
        nlu_request.request = parsed_result['text']

        nlu_result = self.nlu_stub.GetSpeechIntent(nlu_request)

        return nlu_result

    def TTS(self, text):
        tts_request = tts.TTSRequest(text=text)
        self.tts_stub.TTS(tts_request)


class SpeechInterfaceStateMachine:
    def __init__(self, speech_interface):
        self.handlers = {}
        self.startState = None
        self.endStates = []
        self.speech_interface = speech_interface

    def add_state(self, name, handler, end_state=0):
        name = name.upper()
        self.handlers[name] = handler
        if end_state:
            self.endStates.append(name)

    def set_start(self, name):
        self.startState = name.upper()

    def run(self, cargo):
        try:
            handler = self.handlers[self.startState]
        except:
            raise RuntimeError("must call .set_start() before .run()")
        if not self.endStates:
            raise RuntimeError("at least one state must be an end_state")

        while True:
            (newState, cargo) = handler(cargo)
            if newState.upper() in self.endStates:
                print("reached ", newState)
                break
            else:
                handler = self.handlers[newState.upper()]