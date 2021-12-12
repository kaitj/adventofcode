import utils


class Octopus:
    """Octopus energy"""

    def __init__(self, energy: int, x_pos: int, y_pos: int, grid):
        self.x = x_pos
        self.y = y_pos
        self.energy = energy
        self.last_flash = -1
        self.grid = grid

    def neighbours(self):
        neighbours = [
            self.grid.get_octo(self.x - 1, self.y - 1),
            self.grid.get_octo(self.x, self.y - 1),
            self.grid.get_octo(self.x + 1, self.y - 1),
            self.grid.get_octo(self.x - 1, self.y),
            self.grid.get_octo(self.x, self.y),
            self.grid.get_octo(self.x + 1, self.y),
            self.grid.get_octo(self.x - 1, self.y + 1),
            self.grid.get_octo(self.x, self.y + 1),
            self.grid.get_octo(self.x + 1, self.y + 1),
        ]

        for neighbour in neighbours:
            yield neighbour

    def inc_energy(self):
        if self.energy == 9:
            self.flash(self.grid)
        if self.last_flash == self.grid.step:
            pass
        else:
            self.energy += 1

    def flash(self, grid):
        if self.last_flash != grid.step:
            self.energy = 0
            self.last_flash = grid.step
            grid.num_flashes += 1
            for neighbour in self.neighbours():
                if neighbour:
                    neighbour.inc_energy()


class OctopusGrid:
    """List containing energies of octopuses"""

    def __init__(self, data: list[int]):
        self.grid = {}
        self.step = 0
        self.num_flashes = 0
        for ypos, line in enumerate(data):
            for xpos, energy in enumerate(line):
                octopus = Octopus(energy, xpos, ypos, self)
                self.grid[(xpos, ypos)] = octopus
        self.size = len(self.grid)

    def get_octo(self, xpos, ypos):
        return self.grid.get((xpos, ypos), None)

    def next_step(self):
        for octo in self.grid.values():
            octo.inc_energy()
        self.step += 1


def puzzle1(data: list[int], steps: int = 10):
    octo_grid = OctopusGrid(data)
    for _ in range(steps):
        octo_grid.next_step()

    return octo_grid.num_flashes


def puzzle2(data: list[int]):
    octo_grid = OctopusGrid(data)
    current_flashes = octo_grid.num_flashes

    while True:
        octo_grid.next_step()
        if octo_grid.num_flashes == current_flashes + octo_grid.size:
            return octo_grid.step
        current_flashes = octo_grid.num_flashes


if __name__ == "__main__":
    in_fpath = input("Enter path containing octopus energy grid: ")
    in_data = utils.parse_lines(in_fpath, int)

    # Puzzle 1
    print(f"The total number of flashes is {puzzle1(in_data, 100)}")

    # Puzzle 2
    print(f"The step when all octopuses flash is: {puzzle2(in_data)}")
