# =========================================================================== #
# Digits experiment
# =========================================================================== #
# Copyright(C) 2021 Reverb Robotics Inc.
# Author: Lukas Grasse
# Email:  lukas@reverbrobotics.ca
# =========================================================================== #

from digit_states import  DigitMachine
from speech_interface import SpeechInterface
import argparse

parser = argparse.ArgumentParser(description="Digits Experiment")
parser.add_argument('--grpc_host', default="10.42.0.242:50052", help="gRPC rero_core address (default 0.0.0.0:50052)")
parser.add_argument('--dataset_csv', default="data/digits_data.csv", help="path to dataset to run participant on (default data/digits_data.csv)")
parser.add_argument('--logging_csv', default="recordings/test_digits.csv", help="path to write participant data to (default recordings/test_digits.csv)")
ARGS = parser.parse_args()

with SpeechInterface(ARGS.grpc_host) as speech_interface:
    state_machine = DigitMachine(speech_interface, digit_data_csv=ARGS.dataset_csv, participant_dest_csv=ARGS.logging_csv)

    print("running digit state machine")
    state_machine.run(None)

