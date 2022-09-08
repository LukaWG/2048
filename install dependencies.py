from os import system

def install(module):
    system(f"pip install {module}")

try:
    import pygame
except ImportError:
    install("pygame")
