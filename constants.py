#! /usr/bin/venv python3
# coding: utf-8

"""These are some constants used in the project 4."""

# For controller
Y_N = "[y/n]"
Y_RES = ["y"]

TIME_CONTROL_LIST = ["bullet", "blitz", "rapid"]
TIME_CONTROL = "/".join(i for i in TIME_CONTROL_LIST)
DATE_FORMAT = "%d/%m/%Y"
DATE_REQUEST = DATE_FORMAT.lower().replace("%", "")

SCORE_LIST = [0, 0.5, 1]

# For tournament
DEFAULT_NUMBER_OF_ROUNDS = 4
