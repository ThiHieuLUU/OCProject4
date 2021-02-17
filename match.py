"""docstring"""

import player


class Match:
    """docstring"""

    def __init__(self, player1=None, score1=None, player2=None, score2=None, ):
        self._match = ([player1, score1], [player2, score2])

#     @property
#     def player1(self):
#         return self._player1
#
#     @player1.setter
#     def player1(self, new_player1):
#         self._player1 = new_player1
#
#     @player1.deleter
#     def player1(self):
#         del self._player1
#
#     @property
#     def score1(self):
#         return self._score1
#
#     @score1.setter
#     def score1(self, new_score1):
#         self._score1 = new_score1
#
#     @score1.deleter
#     def score1(self):
#         del self._score1
#
#     @property
#     def player2(self):
#         return self._player2
#
#     @player2.setter
#     def player2(self, new_player2):
#         self._player2 = new_player2
#
#     @player2.deleter
#     def player2(self):
#         del self._player2
#
#     @property
#     def score2(self):
#         return self._score2
#
#     @score2.setter
#     def score2(self, new_score2):
#         self._score2 = new_score2
#
#     @score2.deleter
#     def score2(self):
#         del self._score2
#
    @property
    def match(self):
        return self._match

    @match.setter
    def match(self, new_match):
        self._match = new_match

    @match.deleter
    def match(self):
        del self._match
#
#     def update_match(self, score1, score2):
#         assert score1 + score2 == 1
#         self._score1 = score1
#         self._score2 = score2
#         # self._match = ([self._player1, self._score1], [self._player2, self._score2])
#         self._match[0][1] = self._score1
#         self._match[1][1] = self._score2
#
# if __name__ == '__main__':
#     player_1 = player.Player(28,"Lucas", "Herve", "27-12-1980", "male", 14)
#     player_2 = player.Player(18,"Luc", "Her", "29-12-1980", "male", 16)
#     m = Match(player_1, 0, player_2, 1)
#     print(m.match)
#     m.update_match(0.5, 0.5)
#     print(m.match)
#     # absurde ? supprimer aussi match ?
#     del m.player1
#     print(m.match)
