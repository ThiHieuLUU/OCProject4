#! /usr/bin/venv python3
# coding: utf-8

"""There are some exceptions which will be met in the process of checking players, rounds, matches, etc."""


class RoundIndexError(Exception):
    pass


class EmptyListError(Exception):
    pass
