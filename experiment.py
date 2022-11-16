# =========================================================================== #
# full experiment
# =========================================================================== #
# Copyright(C) 2021 Reverb Robotics Inc.
# Author: Lukas Grasse
# Email:  lukas@reverbrobotics.ca
# =========================================================================== #
import os
from digit_states import DigitMachine
from poem_states import PoemStateMachine
from wechsler_states import Wechsler1StateMachine, Wechsler2StateMachine
from speech_interface import SpeechInterface
import argparse

parser = argparse.ArgumentParser(description="Full Experiment")
parser.add_argument('--grpc_host', default="10.42.0.242:50052", help="gRPC rero_core address (default 0.0.0.0:50052)")
parser.add_argument('--wechsler_1_dataset_csv', default="data/wechsler_1_data.csv", help="path to dataset to run participant on (default data/wechsler_1_data.csv)")
parser.add_argument('--poem_dataset_csv', default="data/poem_data.csv", help="path to dataset to run participant on (default data/poem_data.csv)")
parser.add_argument('--wechsler_2_dataset_csv', default="data/wechsler_2_data.csv", help="path to dataset to run participant on (default data/wechsler_2_data.csv)")
parser.add_argument('--digits_dataset_csv', default="data/digits_data.csv", help="path to dataset to run participant on (default data/digits_data.csv)")
parser.add_argument('--logging_dir', default="recordings/test_p1", help="path to write participant data to (default recordings/test_p1)")
ARGS = parser.parse_args()

if not os.path.exists(ARGS.logging_dir):
    os.makedirs(ARGS.logging_dir)

wechsler_1_logging_path = os.path.join(ARGS.logging_dir, "wechsler_1_results.csv")

# wechsler 1
with SpeechInterface(ARGS.grpc_host) as speech_interface:
    state_machine = Wechsler1StateMachine(speech_interface, wechsler_data_csv=ARGS.wechsler_1_dataset_csv, participant_dest_csv=wechsler_1_logging_path)

    print("running wechsler 1 state machine")
    state_machine.run(None)


#poem
poem_logging_path = os.path.join(ARGS.logging_dir, "poem_results.csv")

with SpeechInterface(ARGS.grpc_host) as speech_interface:
    state_machine = PoemStateMachine(speech_interface, poem_data_csv=ARGS.poem_dataset_csv, participant_dest_csv=poem_logging_path)

    print("running poem state machine")
    state_machine.run(None)

#digits
digits_logging_path = os.path.join(ARGS.logging_dir, "digits.csv")

with SpeechInterface(ARGS.grpc_host) as speech_interface:
    state_machine = DigitMachine(speech_interface, digit_data_csv=ARGS.digits_dataset_csv, participant_dest_csv=digits_logging_path)

    print("running digit state machine")
    state_machine.run(None)

#wechsler 2
wechsler_2_logging_path = os.path.join(ARGS.logging_dir, "wechsler_2.csv")

with SpeechInterface(ARGS.grpc_host) as speech_interface:
    state_machine = Wechsler2StateMachine(speech_interface, wechsler_data_csv=ARGS.wechsler_2_dataset_csv, participant_dest_csv=wechsler_2_logging_path)

    print("running wechsler 2 state machine")
    state_machine.run(None)
