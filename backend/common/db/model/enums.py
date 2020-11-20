from enum import Enum


class DrugType(Enum, str):
    HEPARIN = 'HEPARIN'
    INSULIN = 'INSULIN'


class Sex(Enum, str):
    M = 'M'
    F = 'F'
