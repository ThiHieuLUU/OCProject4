"""docstring"""


class Match:
    """docstring"""

    def __init__(self, player1=None, score1=None, player2=None, score2=None, ):
        self._match = ([player1, score1], [player2, score2])

    @property
    def match(self):
        return self._match

    @match.setter
    def match(self, new_match):
        self._match = new_match

    @match.deleter
    def match(self):
        del self._match
