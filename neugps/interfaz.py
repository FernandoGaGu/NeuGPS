# Module that collects the interfaces used with the programme to interact with the user.
#
# Author: Fernando García Gutiérrez
# Email: fegarc05@ucm.es
#
from .tree import Level
from . import plot

import sys
import os
import pandas as pd
from abc import ABCMeta, abstractmethod


class BaseInterface(object):
    __metaclass__ = ABCMeta

    def __init__(self, name: str):
        self._name = name

    def __repr__(self):
        return f'Interface({self._name})'

    def __str__(self):
        return self.__repr__()

    @abstractmethod
    def getInput(self, **kwargs) -> object:
        raise NotImplementedError

    @abstractmethod
    def error(self, **kwargs) -> object:
        raise NotImplementedError

    @abstractmethod
    def update(self, **kwargs) -> object:
        raise NotImplementedError

    @abstractmethod
    def end(self, **kwargs) -> object:
        raise NotImplementedError


class PromptInterface(BaseInterface):
    COLORS = {
        'purple': '\033[95m',
        'cyan': '\033[96m',
        'blue': '\033[94m',
        'green': '\033[92m',
        'red': '\033[91m',
        'yellow': '\033[93m',
        'END': '\033[0m'
    }

    TITLE = """
 \ \        / / | |                               | |       
  \ \  /\  / /__| | ___ ___  _ __ ___   ___       | |_ ___  
   \ \/  \/ / _ \ |/ __/ _ \| '_ ` _ \ / _ \      | __/ _ \ 
    \  /\  /  __/ | (_| (_) | | | | | |  __/      | || (_) |
     \/  \/ \___|_|\___\___/|_| |_| |_|\___|       \__\___/ 

             /$$   /$$                            /$$$$$$  /$$$$$$$   /$$$$$$ 
            | $$$ | $$                           /$$__  $$| $$__  $$ /$$__  $$
            | $$$$| $$  /$$$$$$  /$$   /$$      | $$  \__/| $$  \ $$| $$  \__/
            | $$ $$ $$ /$$__  $$| $$  | $$      | $$ /$$$$| $$$$$$$/|  $$$$$$ 
            | $$  $$$$| $$$$$$$$| $$  | $$      | $$|_  $$| $$____/  \____  $$
            | $$\  $$$| $$_____/| $$  | $$      | $$  \ $$| $$       /$$  \ $$
            | $$ \  $$|  $$$$$$$|  $$$$$$/      |  $$$$$$/| $$      |  $$$$$$/
            |__/  \__/ \_______/ \______/        \______/ |__/       \______/ 
    """
    HEADER = """
Project supported by the Department of Computer Architecture and Automation, 
Universidad Complutense De Madrid and the Department of Neurology of the Hospital 
Clínico San Carlos.

Authors: Fernando Garcia-Gutierrez, Alfonso Delgado-Alvarez, Cristina Delgado-Alonso, 
Josefa Díaz-Álvarez,  Vanesa Pytel, Maria Valles-Salgado, María Jose Gil, 
Laura Hernández-Lorenzo, Jorge Matías-Guiu, José L. Ayala,  Jordi A. Matias-Guiu.
    """

    NOTES = """
IMPORTANT, this program has been developed as a proof of concept. Neither the 
authors nor the organisations involved  are in any way responsible for any use 
made of this programme or algorithms.
    """

    def __init__(self):
        PromptInterface.clear()
        PromptInterface.print(self.TITLE, 'purple')
        PromptInterface.print(self.HEADER, 'purple')
        PromptInterface.print(self.NOTES, 'yellow')

        super(PromptInterface, self).__init__('Prompt')

    def getInput(self, message) -> str:
        return input(message)

    def update(self, test: Level) -> float:
        assert isinstance(test, Level)
        valid = False
        while not valid:
            user_input = self.getInput('\nEnter the score obtained for the test %s: ' % str(test))
            try:
                user_input = float(user_input)
            except ValueError as ex:
                self.error()

            if isinstance(user_input, float):
                break

        return user_input

    def error(self):
        message = PromptInterface.print(
            '\nIncorrect value entered, do you want to try again? [y/n]: ', 'red', display=False)
        try_again = self.getInput(message).lower()
        if try_again == 'n':
            sys.exit(0)

        return True

    def end(self, probs: pd.DataFrame):
        assert 'Diagnostic' in probs.columns
        assert 'Probability' in probs.columns

        title = 'Model diagnosis: <b>%s</b>' % probs[probs['Probability'] == probs['Probability'].max()]['Diagnostic'].values[0]
        plot.pieChart(probs, 'Diagnostic', 'Probability', title=title)

        return None

    @classmethod
    def print(cls, message: str, color: str, display: bool = True) -> str:
        """
        Displays by console the specified message formatted in the specified colour if possible.
        Parameters
        ----------
        message: str
            Message to be displayed on the screen.
        color: str, default=None
            Colour of the message to be displayed on the screen. To see available colors use:
            help(niconnect.system.COLORS).
        display: bool, defaul=True
            Display the message in the screen.
        """
        if color in cls.COLORS:
            message = '%s%s%s' % (cls.COLORS[color], message, cls.COLORS['END'])
        if display:
            print(message)

        return message

    @classmethod
    def clear(cls):
        if os.name == 'nt':
            _ = os.system('cls')
        else:
            _ = os.system('clear')

