import csv
import os.path
import re
import threading
import tkinter
from tkinter import INSERT, END
from pydub import AudioSegment, effects
from pydub.playback import play
src_folder = "/media/lukas/data/datasets/seniors_dataset/participant_audio_transcripts_checked"

def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)

def convert_text(txt):
    return re.sub(r'\W+', '', txt.replace(' ', '_')).replace('_', ' ').lower()

for file in os.listdir(src_folder):

    audio_path = "/media/lukas/data/datasets/seniors_dataset/participant_audio_wav/"

    src_csv = f"{src_folder}/{file}"
    dst_csv = f"{src_folder}_digits/{file}"

    if os.path.exists(dst_csv):
        continue

    print("processing ", file)
    print(dst_csv)

    window = tkinter.Tk()

    input_rows = []

    with open(src_csv, 'r') as rf:
        reader = csv.reader(rf)
        header = next(reader)

        for row in reader:
            input_rows.append(row)

    process_ind = 0

    window.title(f"Transcript Checker {process_ind}/{len(input_rows)}")

    output_rows = [header]

    def play_audio():
        print("playing")
        global process_ind
        global input_rows
        sound= AudioSegment.from_wav(os.path.join(audio_path, input_rows[process_ind][0], input_rows[process_ind][1]))
        normsound = effects.normalize(sound)
        t = threading.Thread(target=play, args=(normsound,))
        t.start()

    def handle_next():
        global process_ind
        global text_box
        global output_rows
        global window

        if process_ind == len(input_rows)-1:
            fixed_text = text_box.get("1.0", END)
            output_rows.append(input_rows[process_ind])
            output_rows[-1][2] = convert_text(fixed_text.strip())
            print("done")
            window.destroy()
        else:
            fixed_text = text_box.get("1.0",END)
            output_rows.append(input_rows[process_ind])
            output_rows[-1][2] = convert_text(fixed_text.strip())
            process_ind += 1

            while not (has_numbers(input_rows[process_ind][2]) or input_rows[process_ind][2] == "") and process_ind < len(input_rows)-2 and "7" not in input_rows[process_ind][0]:
                fixed_text = input_rows[process_ind][2]
                output_rows.append(input_rows[process_ind])
                output_rows[-1][2] = convert_text(fixed_text.strip())

                process_ind += 1

            window.title(f"Transcript Checker {process_ind}/{len(input_rows)}")
            text_box.delete('1.0', END)
            text_box.insert("1.0", input_rows[process_ind][2])

    play_button = tkinter.Button(window, text="Play", command=play_audio)

    play_button.pack()

    text_box = tkinter.Text(window)
    text_box.insert(tkinter.INSERT, input_rows[process_ind][2])
    text_box.pack()

    next_button = tkinter.Button(window, text="Next", command=handle_next)
    next_button.pack()

    tkinter.mainloop()

    with open(dst_csv, 'w') as wf:
        writer = csv.writer(wf)
        writer.writerows(output_rows)