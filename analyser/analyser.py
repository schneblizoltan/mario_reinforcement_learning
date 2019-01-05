""" Analyser module """

import numpy as np
from scipy.stats import linregress,pearsonr

class Analyser(object):
    """This class represents the methods wich are analysing the performance of a RF agent"""

    WIN = 3265                                                              # At this distance the agent completed level 1
    TRAIN_EPISODE_NR = 14000                                                # For this many episodes we won't be calculating the winrate

    def pearson_r(self, file1, file2):
        """ Returns the pearson r parameter for two statistic file"""
        
        mdist = self._file_to_array(file1)
        mreward = self._file_to_array(file2, type=np.float32)

        return np.corrcoef(mdist, mreward)[0, 1]

    def _file_to_array(self, file, type=int):
        """ Returns an array of type "type" built from the content of a file."""

        mlist = []
        for line in open(file):
            mlist.append(line)
        return np.asarray(mlist, dtype=type)

    def win_percentage(self, file):

        won_games = 0
        all_games = 0
        all_games2 = 0

        for line in open(file):
            if all_games2 >= Analyser.TRAIN_EPISODE_NR:
                if int(line) >= Analyser.WIN:
                    won_games += 1
                all_games += 1
            all_games2 += 1
        return (won_games / all_games) * 100
    