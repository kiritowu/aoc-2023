from typing import Tuple, List
from collections import defaultdict, namedtuple

from aocd import get_data


PUZZLE = namedtuple(
    "Puzzle",
    [
        "seeds",
        "seedtosoil",
        "soiltofertilizer",
        "fertilizertowater",
        "watertolight",
        "lighttotemperature",
        "temperaturetohumidity",
        "humiditytolocation",
    ],
)


class PuzzleMap(defaultdict):
    def __init__(self, ranges: Tuple[int, int, int], *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.source_map = dict(
            sorted({r[1]: (r[0], r[2]) for r in ranges}.items())
        )  # source: (dest, length)

    def smallest_key(self, x: int) -> int:
        """Return smallest key that is bigger than x
        from source_map keys using binary search."""
        left, right = 0, len(self.source_map.keys()) - 1
        source_keys = list(self.source_map.keys())
        smallest = source_keys[0]
        while left <= right:
            mid = (left + right) // 2
            if source_keys[mid] < x:
                smallest = source_keys[mid]
                left = mid + 1
            else:
                right = mid - 1
        return smallest

    def __getitem__(self, x):
        key = self.smallest_key(x)
        dest, length = self.source_map[key]
        if key < x < (key + length):
            # return computed destination id
            return dest + (x - key)
        else:
            # if x is not in range, return identity
            return x


def parse_input(lines: List[str]) -> PUZZLE:
    seeds = list(map(int, lines[0].split("seeds: ")[-1].split()))
    ranges = defaultdict(list)

    for line in lines[2:]:
        if not line:
            continue
        elif line.endswith("map:"):
            id = line.split("map:")[0].strip()
        else:
            ranges[id].append(tuple(map(int, line.split())))

    return PUZZLE(seeds, *ranges.values())


def part1(lines: List[str]) -> int:
    puzzle = parse_input(lines)
    seeds = puzzle[0]
    for ranges in puzzle[1:]:
        mapper = PuzzleMap(ranges)
        seeds = [mapper[s] for s in seeds]

    return min(seeds)


def part2(lines: List[int]) -> int:
    puzzle = parse_input(lines)
    seed_ranges = puzzle[0]
    seeds = []
    for i in range(len(seed_ranges) // 2):
        # out of memory
        for j in range(seed_ranges[i], seed_ranges[i] + seed_ranges[i + 1]):
            seeds.append(j)

    for ranges in puzzle[1:]:
        mapper = PuzzleMap(ranges)
        seeds = [mapper[s] for s in seeds]

    return min(seeds)


if __name__ == "__main__":
    data = get_data(year=2023, day=5)
    print(part1(data.splitlines()))
    print(part2(data.splitlines()))
