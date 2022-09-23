# =========================================================================== #
# poem reading experiment
# =========================================================================== #
# Copyright(C) 2021 Reverb Robotics Inc.
# Author: Lukas Grasse
# Email:  lukas@reverbrobotics.ca
# =========================================================================== #

from poem_states import PoemStateMachine
from speech_interface import SpeechInterface

with SpeechInterface("0.0.0.0:50052") as speech_interface:
    state_machine = PoemStateMachine(speech_interface, poem_data_csv="data/poem_data.csv", participant_dest_csv="recordings/test_p0.csv")

    print("running poem state machine")
    state_machine.run(None)

