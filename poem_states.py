import csv
import os
from functools import partial
from time import sleep
import time

from speech_interface import SpeechInterfaceStateMachine

class PoemStateMachine(SpeechInterfaceStateMachine):
    def __init__(self, speech_interface, poem_data_csv, participant_dest_csv):
        super().__init__(speech_interface)

        self.poem_data = self.parse_poem_csv(poem_data_csv)
        self.load_poem_states()
        self.participant_dest_csv = participant_dest_csv
        self.participant_rows = [['poem_line', 'ttsend', 'sttend', 'stim_text', 'recognized_text']]
        self.time_start = -1

    def read_intro(self, text, args):
        self.speech_interface.TTS(text)
        sleep(0.5)
        return ("confirm", None)

    def confirm(self, text, title_state, args):
        self.speech_interface.TTS(text)

        res = self.speech_interface.getRawSRResult()

        if res is not None and ("yes" in res or "yup" in res or "yeah" in res):
            return (title_state, None)

        return ("confirm", None)

    def title(self, text, line_state, args):
        self.speech_interface.TTS(text)
        sleep(1)
        return line_state, None

    def poem_line(self, text, states, args):
        self.speech_interface.TTS(text)
        sleep(0.5)
        tts_end = time.time() * 1000
        return("line_record", (text, tts_end, states))

    def line_record(self, args):
        text, tts_end, states = args
        current_line_state, next_line_state = states

        res = self.speech_interface.getRawSRResult()
        sttend = time.time() * 1000

        self.participant_rows.append([current_line_state, tts_end, sttend, text, res])

        return(next_line_state, None)

    def conclusion(self, text, args):
        self.speech_interface.TTS(text)
        return("write_data", None)

    def write_data(self, args):
        self.write_participant_csv()
        return("end_state", None)

    def parse_poem_csv(self, csv_path):
        poem_data = {}

        poem_data['poems'] = []

        with open(csv_path, 'r') as rf:
            reader = csv.reader(rf)

            next(reader)

            for row in reader:
                if row[0] == "intro":
                    poem_data['intro'] = row[1]

                elif row[0] == "confirmation":
                    poem_data['confirm'] = row[1]

                elif row[0] == 'title':
                    poem_data['poems'].append({})
                    poem_data['poems'][-1]['title'] = row[1]
                    poem_data['poems'][-1]['lines'] = []

                elif row[0] == 'line':
                    poem_data['poems'][-1]['lines'].append(row[1])

                elif row[0] == 'conclusion':
                    poem_data['conclusion'] = row[1]


        return poem_data

    def load_poem_states(self):
        # add line record
        self.add_state("line_record", self.line_record)

        # add start
        self.add_state("start", partial(self.read_intro, self.poem_data['intro']))

        # add confirm
        self.add_state("confirm", partial(self.confirm, self.poem_data['confirm'], "title_1"))

        # loop through poems
        for i, poem in enumerate(self.poem_data['poems']):
            #add poem title
            self.add_state(f"title_{i + 1}",
                                    partial(self.title, poem['title'], f"poem_{i + 1}_line_1"))

            # add lines of poem
            for j, line in enumerate(poem['lines']):
                current_state = f"poem_{i + 1}_line_{j + 1}"

                #add intermediate poems
                if j != len(poem['lines']) - 1:
                    self.add_state(current_state, partial(self.poem_line, line, (current_state, f"poem_{i + 1}_line_{j + 2}")))

                #add final line of poem, advance to either next title or conclusion of poem experiment
                else:
                    if i != len(self.poem_data['poems']) - 1:
                        self.add_state(current_state, partial(self.poem_line, line, (current_state, f"title_{i + 2}")))
                    else:
                        self.add_state(current_state, partial(self.poem_line, line, (current_state, f"conclusion")))

        self.add_state("conclusion", partial(self.conclusion, self.poem_data['conclusion']))

        self.add_state("write_data", self.write_data)
        self.add_state("end_state", None, end_state=True)
        self.set_start("start")

    def write_participant_csv(self):
        dest_dir = '/'.join(self.participant_dest_csv.split('/')[:-1])

        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)

        with open(self.participant_dest_csv, 'w') as wf:
            writer = csv.writer(wf)

            writer.writerows(self.participant_rows)