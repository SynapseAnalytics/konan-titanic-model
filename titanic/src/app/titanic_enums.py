from enum import Enum


class Gender(str, Enum):
    Female = "female"
    Male = "male"


class EmbarkedPorts(str, Enum):
    Cherbourg = 'C'
    Queenstown = 'Q'
    Southampton = 'S'


class TicketClass(int, Enum):
    FirstClass = 1
    SecondClass = 2
    ThirdClass = 3


class Titles(str, Enum):
    Master = "Master"
    Miss = "Miss"
    Mr = "Mr"
    Mrs = "Mrs"
    Other = "Rare"


class SurvivedTypes(str, Enum):
    Yes = 'yes'
    No = 'no'
