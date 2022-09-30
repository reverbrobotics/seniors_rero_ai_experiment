import csv
import os
from functools import partial
from time import sleep
import time
import re

from speech_interface import SpeechInterfaceStateMachine

class DigitMachine(SpeechInterfaceStateMachine):
    def __init__(self, speech_interface, digit_data_csv, participant_dest_csv):
        super().__init__(speech_interface)

        self.participant_dest_csv = participant_dest_csv
        self.participant_rows = [['task', 'ttsend', 'sttend', 'task_digits', 'response_digits']]
        self.time_start = -1

        self.reverse_digits = []
        self.sequence_digits = []

        self.reverse_digits_count = 0
        self.sequence_digits_count = 0

        self.reverse_digits_task = True
        self.fail_count = 0

        self.intro_texts = []
        self.intro_count = 0

        self.confirm_text = None
        self.conclusion_text = None

        self.digits = {'zero':0, 'one':1, 'two':2, 'three':3, 'four':4, 'five':5, 'six':6, 'seven':7, 'eight':8, 'nine':9}

        self.parse_digits_csv(digit_data_csv)
        self.load_digit_states()

    def read_intro(self, args):
        self.speech_interface.TTS(self.intro_texts[self.intro_count])
        self.intro_count += 1

        sleep(0.25)
        return ("confirm", None)

    def confirm(self, args):
        self.speech_interface.TTS(self.confirm_text)

        res = self.speech_interface.getRawSRResult()
        self.fail_count = 0

        if res is not None and "yes" in res:
            if self.intro_count == 1:
                return ("read_backward_digits", None)
            else:
                self.reverse_digits_task = False
                return("read_sequence_digits", None)


        return ("confirm", None)

    def read_backwards_digits(self, args):
        self.speech_interface.TTS(self.reverse_digits[self.reverse_digits_count])
        self.reverse_digits_count += 1

        tts_end = time.time() * 1000

        return ("reverse_digits_record", tts_end)



    def reverse_digits_record(self, tts_end):
        digit_text = self.reverse_digits[self.reverse_digits_count-1]
        digits = self.parse_digits_from_text(digit_text)

        res = self.speech_interface.getRawSRResult()
        sttend = time.time() * 1000

        res_digits = self.parse_digits_from_text(res)
        print(digit_text)
        print(digits)
        print(res_digits)
        print(" ")

        self.participant_rows.append(["reverse", tts_end, sttend, digits, res_digits])

        check = self.check_reverse_digits(digits, res_digits)

        if not check:
            self.fail_count += 1

        if self.fail_count >= 2:
            return ("intro", None)

        return ("read_backward_digits", None)

    def read_sequence_digits(self, args):
        self.speech_interface.TTS(self.sequence_digits[self.sequence_digits_count])
        self.sequence_digits_count += 1

        tts_end = time.time() * 1000

        return ("sequence_digits_record", tts_end)

    def sequence_digits_record(self, tts_end):
        digits = self.parse_digits_from_text(self.sequence_digits[self.sequence_digits_count - 1])

        res = self.speech_interface.getRawSRResult()
        sttend = time.time() * 1000

        res_digits = self.parse_digits_from_text(res)

        print(digits)
        print(res_digits)
        print(" ")

        self.participant_rows.append(["sequence", tts_end, sttend, digits, res_digits])

        check = self.check_sequence_digits(digits, res_digits)

        if not check:
            self.fail_count += 1

        if self.fail_count >= 2:
            return ("conclusion", None)

        return ("read_sequence_digits", None)

    def conclusion(self, args):
        self.speech_interface.TTS(self.conclusion_text)
        return("write_data", None)

    def write_data(self, args):
        self.write_participant_csv()
        return("end_state", None)

    def parse_digits_csv(self, csv_path):
        with open(csv_path, 'r') as rf:
            reader = csv.reader(rf)

            next(reader)

            for row in reader:
                if row[0] == 'intro':
                    self.intro_texts.append(row[1])

                elif row[0] == 'confirmation':
                    self.confirm_text = row[1]

                elif row[0] == 'backward_digits':
                    self.reverse_digits.append(row[1])

                elif row[0] == 'sequence_digits':
                    self.sequence_digits.append(row[1])

                elif row[0] == 'conclusion':
                    self.conclusion_text = row[1]


    def load_digit_states(self):
        self.add_state("intro", self.read_intro)
        self.add_state("confirm", self.confirm)

        self.add_state("read_backward_digits", self.read_backwards_digits)
        self.add_state("reverse_digits_record", self.reverse_digits_record)
        self.add_state("read_sequence_digits", self.read_sequence_digits)
        self.add_state("sequence_digits_record", self.sequence_digits_record)

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

    def parse_digits_from_text(self, text):
        text = text.replace(',', '')
        digit_list = text.split(' ')

        parsed_digits = []
        for digit in digit_list:
            if digit not in self.digits:
                continue

            parsed_digits.append(self.digits[digit])

        return parsed_digits


    def check_reverse_digits(self, ref_digits, digits):
        if len(ref_digits) != len(digits):
            return False

        digits.reverse()

        for i in range(len(ref_digits)):
            if ref_digits[i] != digits[i]:
                return False

        return True

    def check_sequence_digits(self, ref_digits, digits):
        if len(ref_digits) != len(digits):
            return False

        ref_digits.sort()

        for i in range(len(ref_digits)):
            if ref_digits[i] != digits[i]:
                return False

        return True
