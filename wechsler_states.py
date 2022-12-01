import csv
import os
from functools import partial
from time import sleep
import time

from speech_interface import SpeechInterfaceStateMachine
from util import check_string_confirm


class Wechsler1StateMachine(SpeechInterfaceStateMachine):
    def __init__(self, speech_interface, wechsler_data_csv, participant_dest_csv):
        super().__init__(speech_interface)

        self.participant_dest_csv = participant_dest_csv
        self.participant_rows = [['story_id', 'responseline', 'ttsend', 'sttend', 'recognized_text']]
        self.time_start = -1
        self.story_count = 0
        self.total_stories = 0
        self.response_count = 0
        self.story_texts = []

        self.intro_count = 0
        self.intro_texts = []

        self.response_prompts = []

        self.wechsler_data = self.parse_wechsler_1_csv(wechsler_data_csv)
        self.load_wechsler_1_states()

    def read_intro(self, args):
        self.speech_interface.setVocab("")
        self.speech_interface.TTS(self.intro_texts[self.intro_count])

        return ("confirm", None)


    def confirm(self, text, args):
        self.speech_interface.TTS(text.split('/')[0])

        res = self.speech_interface.getRawSRResult()

        if res is not None and check_string_confirm(res):
            self.intro_count += 1

            self.speech_interface.TTS(text.split('/')[1])

            res = self.speech_interface.getRawSRResult()

            while res is None or not check_string_confirm(res):
                res = self.speech_interface.getRawSRResult()

            return ("story", None)


        return ("intro", None)

    def story(self, args):
        self.speech_interface.TTS("OK, I will begin the story in a moment.")
        story_txt = self.story_texts[self.story_count]
        # story_txts = story_txt.split('.')
        #
        # for txt in story_txts:
        #     self.speech_interface.TTS(txt+'.')

        self.speech_interface.TTS(story_txt)
        sleep(0.5)

        self.response_count = 0
        self.story_count += 1

        return ("response_prompt", None)


    def response_prompt(self, args):
        if self.response_count == 0:
            self.speech_interface.TTS(self.response_prompts[0])
        else:
            self.speech_interface.TTS(self.response_prompts[1])

        sleep(0.5)

        tts_end = time.time() * 1000
        return ("response_record", tts_end)


    def response_record(self, tts_end):
        res = self.speech_interface.getRawSRResult()
        sttend = time.time() * 1000

        self.participant_rows.append([self.story_count-1, self.response_count, tts_end, sttend, res])
        self.response_count += 1

        print("response: ", res)

        if res is not None and not (res == "" or res == "huh"):
            return ("response_record", tts_end)

        return("done_confirmation", None)

    def done_confirmation(self, text, args):
        self.speech_interface.TTS(text)

        res = self.speech_interface.getRawSRResult()

        if res is not None and not check_string_confirm(res):
            if self.story_count < len(self.story_texts):
                return ("intro", None)

            else:
                return("conclusion", None)

        return ("response_prompt", None)


    def conclusion(self, text, args):
        self.speech_interface.TTS(text)
        return("write_data", None)

    def write_data(self, args):
        self.write_participant_csv()
        return("end_state", None)


    def parse_wechsler_1_csv(self, csv_path):
        wechsler_data = {}

        with open(csv_path, 'r') as rf:
            reader = csv.reader(rf)

            for row in reader:
                if row[0] == 'intro':
                    self.intro_texts.append(row[1])

                elif row[0] == 'confirmation':
                    wechsler_data['confirmation'] = row[1]

                elif row[0] == 'done_confirmation':
                    wechsler_data['done_confirmation'] = row[1]

                elif row[0] == 'story':
                    self.story_texts.append(row[1])

                elif row[0] == 'response_prompt':
                    self.response_prompts.append(row[1])

                elif row[0] == 'conclusion':
                    wechsler_data['conclusion'] = row[1]


        return wechsler_data

    def load_wechsler_1_states(self):
        self.add_state("intro", self.read_intro)

        self.add_state("confirm", partial(self.confirm, self.wechsler_data['confirmation']))

        self.add_state("story", self.story)

        self.add_state("response_prompt", self.response_prompt)

        self.add_state("response_record", self.response_record)

        self.add_state("done_confirmation", partial(self.done_confirmation, self.wechsler_data['done_confirmation']))

        self.add_state("conclusion", partial(self.conclusion, self.wechsler_data['conclusion']))

        self.add_state("write_data", self.write_data)
        self.add_state("end_state", None, end_state=True)
        self.set_start("intro")

    def write_participant_csv(self):
        dest_dir = '/'.join(self.participant_dest_csv.split('/')[:-1])

        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        with open(self.participant_dest_csv, 'w') as wf:
            writer = csv.writer(wf)

            writer.writerows(self.participant_rows)


class Wechsler2StateMachine(SpeechInterfaceStateMachine):
    def __init__(self, speech_interface, wechsler_data_csv, participant_dest_csv):
        super().__init__(speech_interface)

        self.participant_dest_csv = participant_dest_csv
        self.participant_rows = [['story_id', 'response_count', 'question', 'ttsend', 'sttend', 'recognized_text']]
        self.time_start = -1

        self.intro_texts = []
        self.hint_texts = []
        self.prompt_texts = []
        self.recognition_prompt_texts = []

        self.intro_count = 0
        self.hint_count = 0
        self.prompt_count = 0
        self.response_count = 0
        self.questions = {}
        self.question_count = 0
        self.recognition_prompt_count = 0

        self.parse_wechsler_2_csv(wechsler_data_csv)
        self.load_wechsler_2_states()

    def read_intro(self, args):
        self.speech_interface.setVocab("")
        if self.intro_count >= len(self.intro_texts):
            return ("conclusion", None)

        self.speech_interface.TTS(self.intro_texts[self.intro_count])
        self.intro_count += 1
        #sleep(0.5)

        res = self.speech_interface.getRawSRResult()

        if res is not None and check_string_confirm(res):
            return ("hint", None)

        return ("prompt", None)


    def hint(self, args):
        self.speech_interface.TTS(self.hint_texts[self.intro_count-1])
        sleep(0.5)

        return ("prompt", None)


    def prompt(self, args):

        if args is not None and args:
            self.speech_interface.TTS("Tell me everything else you can remember.")
        else:
            self.speech_interface.TTS(self.prompt_texts[self.prompt_count])
            self.prompt_count += 1

            self.response_count = 0

        sleep(0.5)

        tts_end = time.time() * 1000

        return ("response_record", tts_end)


    def response_record(self, tts_end):
        res = self.speech_interface.getRawSRResult()
        sttend = time.time() * 1000

        self.participant_rows.append([self.prompt_count-1, self.response_count, -1, tts_end, sttend, res])
        self.response_count += 1

        print("response: ", res)

        if res is not None and not (res == "" or res == "huh"):
            return ("response_record", tts_end)

        return("done_confirmation", None)

    def recognition_prompt(self, args):
        self.speech_interface.TTS(self.recognition_prompt_texts[self.recognition_prompt_count])
        self.recognition_prompt_count += 1
        self.question_count = 0

        sleep(0.5)

        return ("question", None)

    def done_confirmation(self, args):
        self.speech_interface.TTS(self.done_confirmation_text)

        res = self.speech_interface.getRawSRResult()

        if res is not None and check_string_confirm(res):
            return ("prompt", True)

        return ("recognition_prompt", None)

    def question(self, args):
        self.speech_interface.TTS(self.questions[self.recognition_prompt_count][self.question_count])

        tts_end = time.time() * 1000
        return ("question_response", tts_end)

    def question_response(self, tts_end):
        res = self.speech_interface.getRawSRResult()
        sttend = time.time() * 1000

        self.question_count += 1

        self.participant_rows.append([self.recognition_prompt_count, -1, self.question_count, tts_end, sttend, res])

        if self.question_count < len(self.questions[self.recognition_prompt_count]):
            return ("question", None)

        return ("intro", None)


    def conclusion(self, args):
        self.speech_interface.TTS(self.conclusion_text)
        return("write_data", None)

    def write_data(self, args):
        self.write_participant_csv()
        return("end_state", None)


    def parse_wechsler_2_csv(self, csv_path):

        with open(csv_path, 'r') as rf:
            reader = csv.reader(rf)

            for row in reader:
                if row[0] == 'intro':
                    self.intro_texts.append(row[1])

                elif row[0] == 'hint':
                    self.hint_texts.append(row[1])

                elif row[0] == 'prompt':
                    self.prompt_texts.append(row[1])

                elif row[0] == 'recognition_prompt':
                    self.recognition_prompt_texts.append(row[1])
                    self.questions[len(self.recognition_prompt_texts)] = []

                elif row[0] == 'question':
                    self.questions[len(self.recognition_prompt_texts)].append(row[1])

                elif row[0] == 'done_confirmation':
                    self.done_confirmation_text = row[1]

                elif row[0] == 'conclusion':
                    self.conclusion_text = row[1]


    def load_wechsler_2_states(self):
        self.add_state("intro", self.read_intro)
        self.add_state("hint", self.hint)
        self.add_state("prompt", self.prompt)
        self.add_state("response_record", self.response_record)
        self.add_state("done_confirmation", self.done_confirmation)
        self.add_state("recognition_prompt", self.recognition_prompt)
        self.add_state("question", self.question)
        self.add_state("question_response", self.question_response)
        self.add_state("conclusion", self.conclusion)

        self.add_state("write_data", self.write_data)
        self.add_state("end_state", None, end_state=True)
        self.set_start("intro")

    def write_participant_csv(self):
        dest_dir = '/'.join(self.participant_dest_csv.split('/')[:-1])

        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        with open(self.participant_dest_csv, 'w') as wf:
            writer = csv.writer(wf)

            writer.writerows(self.participant_rows)
