from sys import maxsize

from constants import *

class Node:

    def __init__(self, number) -> None:
        self.__number = number
        self.__cost_red = maxsize - 2 # Not to be confused with '#' cost
        self.__cost_blue = maxsize - 2 # Not to be confused with '#' cost
        self.__color = WHITE_INDICATOR
        self.__neighbors = []

    @property
    def neighbors(self):
        return self.__neighbors

    @property
    def color(self):
        return self.__color

    @property
    def cost_red(self):
        return self.__cost_red

    @property
    def cost_blue(self):
        return self.__cost_blue

    @property
    def number(self):
        return self.__number

    @cost_red.setter
    def cost_red(self, new_cost):
        if new_cost < self.__cost_red:
            self.__cost_red = new_cost

    @cost_blue.setter
    def cost_blue(self, new_cost):
        if new_cost < self.__cost_blue:
            self.__cost_blue = new_cost

    @color.setter
    def color(self, color):
        self.__color = color

    @neighbors.setter
    def neighbors(self, neighbors):
        if len(self.__neighbors) == 0:
            self.__neighbors = neighbors[:]