"""
Module for handling custom errors
(Experimental)
"""

class Base(Exception):
    '''
    Base class for all exceptions
    '''
    def __init__(self, str):
        super().__init__(str)

class Dir_Not_Definied(Base):
    def __init__(self, str):
        super().__init__(str)