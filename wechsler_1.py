# =========================================================================== #
# Wechsler 1 experiment
# =========================================================================== #
# Copyright(C) 2021 Reverb Robotics Inc.
# Author: Lukas Grasse
# Email:  lukas@reverbrobotics.ca
# =========================================================================== #

from wechsler_states import Wechsler1StateMachine
from speech_interface import SpeechInterface
import argparse

parser = argparse.ArgumentParser(description="Wechsler 1 Experiment")
parser.add_argument('--grpc_host', default="0.0.0.0:50052", help="gRPC rero_core address (default 0.0.0.0:50052)")
parser.add_argument('--dataset_csv', default="data/wechsler_1_data.csv", help="path to dataset to run participant on (default data/wechsler_1_data.csv)")
parser.add_argument('--logging_csv', default="recordings/test.csv", help="path to write participant data to (default recordings/test_w1.csv)")
ARGS = parser.parse_args()

with SpeechInterface(ARGS.grpc_host) as speech_interface:
    state_machine = Wechsler1StateMachine(speech_interface, wechsler_data_csv=ARGS.dataset_csv, participant_dest_csv=ARGS.logging_csv)

    print("running wechsler 1 state machine")
    state_machine.run(None)

