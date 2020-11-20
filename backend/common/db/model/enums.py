from enum import Enum


class DrugType(str, Enum):
    HEPARIN = 'HEPARIN'
    INSULIN = 'INSULIN'


class Sex(str, Enum):
    M = 'M'
    F = 'F'
