from typing import List
from collections import defaultdict

from aocd import get_data


def part1(lines: List[str]):
    """
    The engineer explains that an engine part seems to be missing from the
    engine, but nobody can figure out which one. If you can add up all the
    part numbers in the engine schematic, it should be easy to work out which
    part is missing.

    The engine schematic (your puzzle input) consists of a visual
    representation of the engine. There are lots of numbers and symbols you
    don't really understand, but apparently any number adjacent to a symbol,
    even diagonally, is a "part number" and should be included in your sum.
    (Periods (.) do not count as a symbol.)

    Here is an example engine schematic:

    467..114..
    ...*......
    ..35..633.
    ......#...
    617*......
    .....+.58.
    ..592.....
    ......755.
    ...$.*....
    .664.598..

    In this schematic, two numbers are not part numbers because they are not
    adjacent to a symbol: 114 (top right) and 58 (middle right). Every other
    number is adjacent to a symbol and so is a part number; their sum is 4361.

    Of course, the actual engine schematic is much larger.
    What is the sum of all of the part numbers in the engine schematic?
    """
    # Find number then check for any symbol its perimeter
    symbols = set(["+", "-", "*", "/", "$", "#", "@", "&", "%", "^", "!", "~", "="])
    result = []
    for i, line in enumerate(lines):
        num = ""
        for j, char in enumerate(line):
            if char.isdigit():
                num += char
                if j != len(line) - 1:
                    # Check if next char is digit if not last char in the line
                    continue
            if num:
                # Search for symbol accross the perimeter
                left_idx = max(j - len(num) - 1, 0)
                right_idx = min(j + 1, len(line))
                # Check top
                if i > 0 and len(set(lines[i - 1][left_idx:right_idx]) & symbols) > 0:
                    result.append(int(num))
                # Check bottom
                elif (
                    i < len(lines) - 1
                    and len(set(lines[i + 1][left_idx:right_idx]) & symbols) > 0
                ):
                    result.append(int(num))
                # Check left and right
                elif (
                    lines[i][left_idx] in symbols or lines[i][right_idx - 1] in symbols
                ):
                    result.append(int(num))
            num = ""
        # Check top and bottom
    return sum(result)


def part2(lines):
    """
    The missing part wasn't the only issue - one of the gears in the engine is
    wrong. A gear is any * symbol that is adjacent to exactly two part numbers.
    Its gear ratio is the result of multiplying those two numbers together.

    This time, you need to find the gear ratio of every gear and add them all
    up so that the engineer can figure out which gear needs to be replaced.

    Consider the same engine schematic again:

    467..114..
    ...*......
    ..35..633.
    ......#...
    617*......
    .....+.58.
    ..592.....
    ......755.
    ...$.*....
    .664.598..

    In this schematic, there are two gears. The first is in the top left; it
    has part numbers 467 and 35, so its gear ratio is 16345. The second gear
    is in the lower right; its gear ratio is 451490. (The * adjacent to 617 is
    not a gear because it is only adjacent to one part number.) Adding up all
    of the gear ratios produces 467835.

    What is the sum of all of the gear ratios in your engine schematic?
    """
    # Find number then check for any symbol its perimeter
    symbol = "*"
    result = []
    # Store coordinates of asterisk and its adjacent numbers
    asterisk_coords = defaultdict(list)
    for i, line in enumerate(lines):
        num = ""
        for j, char in enumerate(line):
            if char.isdigit():
                num += char
                if j != len(line) - 1:
                    # Check if next char is digit if not last char in the line
                    continue
            if num:
                # Search for symbol accross the perimeter
                left_idx = max(j - len(num) - 1, 0)
                right_idx = min(j + 1, len(line))
                # Check top
                if i > 0 and symbol in lines[i - 1][left_idx:right_idx]:
                    asterisk_coords[(i - 1, lines[i - 1].index("*", left_idx))].append(
                        int(num)
                    )
                # Check bottom
                elif i < len(lines) - 1 and symbol in lines[i + 1][left_idx:right_idx]:
                    asterisk_coords[(i + 1, lines[i + 1].index("*", left_idx))].append(
                        int(num)
                    )
                # Check left and right
                elif lines[i][left_idx] == symbol:
                    asterisk_coords[(i, left_idx)].append(int(num))
                elif lines[i][right_idx - 1] == symbol:
                    asterisk_coords[(i, right_idx - 1)].append(int(num))
            num = ""
        # Check top and bottom

    # For each gear, check if it has two adjacent numbers and calculate ratio
    for nums in asterisk_coords.values():
        if len(nums) == 2:
            result.append(nums[0] * nums[1])
    return sum(result)


if __name__ == "__main__":
    data = get_data(year=2023, day=3).splitlines()
    print(part1(data))
    print(part2(data))
