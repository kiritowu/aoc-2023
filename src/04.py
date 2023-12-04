from typing import List

def part1(lines: List[str]):
    total = 0
    for line in lines:
        game_id, numbers = line.split(": ")
        win_nums, draw_nums = map(lambda x: set(map(int, x.split())),numbers.split(" | "))
        score = 2 ** max(len(win_nums & draw_nums)-1,0)
        total += score
    return total


if __name__ == "__main__":
    with open("../inputs/04.txt", "r") as f:
        inputs = f.read().splitlines()
    print(part1(inputs))
