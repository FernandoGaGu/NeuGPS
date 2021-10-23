# Module that includes the classes necessary to implement the logic of classification algorithms based on
# decision trees.
#
# Author: Fernando García Gutiérrez
# Email: fegarc05@ucm.es
#
import os
import pandas as pd
from copy import deepcopy


class Level(object):
    def __init__(self, test: str = None, cutoff: float or int = None, left_level=None, right_level=None):
        assert isinstance(test, str)
        assert isinstance(cutoff, float) or isinstance(cutoff, int)
        assert isinstance(left_level, type(self)) or left_level is None
        assert isinstance(right_level, type(self)) or right_level is None

        self._test = test
        self._cutoff = cutoff
        self._next_levels = [left_level, right_level]

    def __repr__(self):
        return self._test

    def __str__(self):
        return self.__repr__()

    def __call__(self, scalar: int or float, data: pd.DataFrame) -> tuple:
        assert self._test in data.columns
        assert isinstance(scalar, int) or isinstance(scalar, float)

        if scalar <= self._cutoff:
            new_data = data[data[self._test] <= self._cutoff]
            return self._next_levels[0], new_data
        else:
            new_data = data[data[self._test] > self._cutoff]
            return self._next_levels[1], new_data


class Tree(object):
    def __init__(self, data: pd.DataFrame or str, diagnosis_col: str, initial_level: Level):
        if isinstance(data, str):
            assert os.path.exists(data), 'Path to %s not found' % data
            try:
                data = pd.read_csv(data, index_col=0)
            except Exception:
                try:
                    data = pd.read_parquet(data)
                except Exception as ex:
                    raise Exception('Error during data loading. Corrupted file %s' % data)

        assert isinstance(initial_level, Level)
        assert isinstance(diagnosis_col, str)
        assert isinstance(data, pd.DataFrame)
        assert str(initial_level) in data.columns
        assert diagnosis_col in data.columns

        self._initial_level = initial_level
        self._current_level = initial_level
        self._initial_data = data
        self._current_data = data.copy()
        self._diagnosis_col = diagnosis_col

    def __repr__(self):
        return f'Tree({str(self._current_level)})'

    @property
    def current_level(self) -> Level:
        return self._current_level

    @property
    def initial_level(self) -> Level:
        return self._initial_level

    def updateLevel(self, scalar: float):
        if self._current_level is None:
            return self

        self_copy = deepcopy(self)
        self_copy._current_level, self_copy._current_data = self_copy._current_level(scalar, self_copy._current_data)

        return self_copy

    def restartLevel(self):
        self_copy = deepcopy(self)
        self_copy._current_level = self_copy._initial_level
        self_copy._current_data = self_copy._initial_data

        return self_copy

    def getCurrentProbabilities(self) -> pd.DataFrame:
        probabilities = pd.DataFrame(
            (self._current_data[self._diagnosis_col].value_counts() / self._current_data.shape[0])).reset_index()
        probabilities.columns = ['Diagnostic', 'Probability']

        return probabilities
