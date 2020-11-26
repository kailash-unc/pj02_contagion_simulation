"""The model classes maintain the state and logic of the simulation."""

from __future__ import annotations
from typing import List
from random import random
from projects.pj02 import constants
from math import sin, cos, pi, sqrt


__author__ = "730411609"


class Point:
    """A model of a 2-d cartesian coordinate Point."""
    x: float
    y: float

    def __init__(self, x: float, y: float):
        """Construct a point with x, y coordinates."""
        self.x = x
        self.y = y

    def add(self, other: Point) -> Point:
        """Add two Point objects together and return a new Point."""
        x: float = self.x + other.x
        y: float = self.y + other.y
        return Point(x, y)

    def distance(self, other: Point) -> float:
        """Calculates the distance between two points."""
        return sqrt(((other.x - self.x) * (other.x - self.x)) + ((other.y - self.y) * (other.y - self.y)))


class Cell:
    """An individual subject in the simulation."""
    location: Point
    direction: Point
    sickness: int = 0

    def __init__(self, location: Point, direction: Point):
        """Construct a cell with its location and direction."""
        self.location = location
        self.direction = direction

    # Part 1) Define a method named `tick` with no parameters.
    # Its purpose is to reassign the object's location attribute
    # the result of adding the self object's location with its
    # direction. Hint: Look at the add method.
    def tick(self) -> None:
        """Updates the cell state of the simulation by one time step."""
        self.location = self.location.add(self.direction)
        if(self.is_infected()):
            self.sickness += 1
        if(self.sickness > constants.RECOVERY_PERIOD):
            self.immunize()
        
    def color(self) -> str:
        """Return the color representation of a cell."""
        if self.is_vulnerable():
            return "gray"
        if self.is_infected():
            return "crimson"
        if self.is_immune():
            return "cornflower blue"
        return "black"

    def contract_disease(self) -> None:
        """Makes the cell infected."""
        self.sickness = constants.INFECTED

    def is_vulnerable(self) -> bool:
        """Checks if the cell is vulnerable."""
        if self.sickness == constants.VULNERABLE:
            return True
        else:
            return False
    
    def is_infected(self) -> bool:
        """Checks if the cell is infected."""
        if self.sickness >= constants.INFECTED:
            return True
        else:
            return False

    def contact_with(self, other: Cell) -> None:
        """Checks whether a contact will affect a cell."""
        if(self.is_infected() and other.is_vulnerable()):
            other.contract_disease()
        if(self.is_vulnerable() and other.is_infected()):
            self.contract_disease()

    def immunize(self) -> None:
        """Makes the cell immune."""
        self.sickness = constants.IMMUNE
    
    def is_immune(self) -> bool:
        """Checks if the cell is immune."""
        if self.sickness == constants.IMMUNE:
            return True
        else:
            return False
        

class Model:
    """The state of the simulation."""

    population: List[Cell]
    time: int = 0

    def __init__(self, cells: int, speed: float, base_infect: int, base_immune: int = 0):
        """Initialize the cells with random locations and directions."""
        if base_infect + base_immune >= cells or base_infect + base_immune <= 0:
            raise ValueError("__init__() args is not provided with appropriate base_infect/base_immune val")
        self.population = []
        for i in range(0, cells - base_infect - base_immune):
            start_loc = self.random_location()
            start_dir = self.random_direction(speed)
            self.population.append(Cell(start_loc, start_dir))
        for i in range(0, base_infect):
            start_loc = self.random_location()
            start_dir = self.random_direction(speed)
            infected_cell = Cell(start_loc, start_dir)
            infected_cell.contract_disease()
            self.population.append(infected_cell)
        for i in range(0, base_immune):
            start_loc = self.random_location()
            start_dir = self.random_direction(speed)
            immunized_cell = Cell(start_loc, start_dir)
            immunized_cell.immunize()
            self.population.append(immunized_cell)
    
    def tick(self) -> None:
        """Update the state of the simulation by one time step."""
        self.time += 1
        for cell in self.population:
            cell.tick()
            self.enforce_bounds(cell)
        self.check_contacts()

    def random_location(self) -> Point:
        """Generate a random location."""
        start_x = random() * constants.BOUNDS_WIDTH - constants.MAX_X
        start_y = random() * constants.BOUNDS_HEIGHT - constants.MAX_Y
        return Point(start_x, start_y)

    def random_direction(self, speed: float) -> Point:
        """Generate a 'point' used as a directional vector."""
        random_angle = 2.0 * pi * random()
        dir_x = cos(random_angle) * speed
        dir_y = sin(random_angle) * speed
        return Point(dir_x, dir_y)

    def enforce_bounds(self, cell: Cell) -> None:
        """Cause a cell to 'bounce' if it goes out of bounds."""
        if cell.location.x > constants.MAX_X:
            cell.location.x = constants.MAX_X
            cell.direction.x *= -1
        if cell.location.x < constants.MIN_X:
            cell.location.x = constants.MIN_X
            cell.direction.x *= -1
        if cell.location.y > constants.MAX_Y:
            cell.location.y = constants.MAX_Y
            cell.direction.y *= -1
        if cell.location.y < constants.MIN_Y:
            cell.location.y = constants.MIN_Y
            cell.direction.y *= -1
    
    def is_complete(self) -> bool:
        """Method to indicate when the simulation is complete."""
        condition: bool = True
        for cell in self.population:
            condition = condition and (cell.is_immune() or cell.is_vulnerable())
        return condition
    
    def check_contacts(self) -> None:
        """Checks for every cell, whether a contact is made with another."""
        for i in range(0, len(self.population) - 1):
            for j in range(i + 1, len(self.population)):
                if(self.population[i].location.distance(self.population[j].location) < constants.CELL_RADIUS):
                    self.population[i].contact_with(self.population[j])