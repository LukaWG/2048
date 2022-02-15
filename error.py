"""
Module for handling custom errors
"""

class Base(Exception):
    def __init__(self, str):
        super().__init__(str)

class Dir_Not_Definied(Base):
    def __init__(self, str):
        super().__init__(str)