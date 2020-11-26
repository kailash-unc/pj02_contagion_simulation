"""Module created to chart the infection and immunization curves of a simulation.

Hypothesis: If infected is only 0.2% of the population in a dense population, 
more than half of the population is going to be infected before becoming immune.

Under a dense population of 500 people, only one person was selected to be infected.
Even though this was only 0.2% of the population, the infected cell count reached, a strickingly high, 
greater than 90% of the population. I was amazed how quickly the infection spread throught the people.
Another interesting thing was that immune cells only started emerging after reaching peak infection.
"""


import argparse
from projects.pj02.model import Model
import matplotlib.pyplot as plt
from typing import List


def main() -> None:
    """Entry point to create a chart."""
    parser = argparse.ArgumentParser()
    parser.add_argument("cell_count")
    parser.add_argument("base_infected")
    parser.add_argument("base_immune")
    args = parser.parse_args()
    model = Model(int(args.cell_count), 5.0, int(args.base_infected), int(args.base_immune))
    ticks: List[int] = [0]
    infected: List[int] = [int(args.base_infected)]
    immune: List[int] = [int(args.base_immune)]

    counter: int = 0
    while(not model.is_complete()):
        total_infected: int = 0
        total_immune: int = 0
        model.tick()
        counter += 1
        ticks.append(counter)
        for cell in model.population:
            if(cell.is_infected()):
                total_infected += 1
            if(cell.is_immune()):
                total_immune += 1
        infected.append(total_infected)
        immune.append(total_immune)
 
    plt.title("Immunity and Infection Over Time")
    plt.plot(ticks, infected, color = "crimson", label = "Infected Cells")
    plt.plot(ticks, immune, color = "CornflowerBlue", label = "Immune Cells")
    plt.xlabel("Time Ticks")
    plt.ylabel("Number of Cells")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()