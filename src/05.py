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


class PuzzleDict(defaultdict):
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
        """Return element if x in range, else return identity"""
        key = self.smallest_key(x)
        dest, length = self.source_map[key]
        if key < x < (key + length):
            # return computed destination id
            return dest + (x - key)
        else:
            # if x is not in range, return identity
            return x

    def parse_range(
        self, seed_ranges: List[Tuple[int, int]]
    ) -> List[Tuple[int, int]]:  # [(start, end), ...]
        """Given a list of seed ranges, return a list of mapped seed ranges"""
        mapped_seed_ranges = []
        while seed_ranges:
            seed_start, seed_end = seed_ranges.pop()

            for source, (dest, length) in self.source_map.items():
                # split the ranges
                ovlp_start = max(seed_start, source)
                ovlp_end = min(seed_end, source + length)

                if ovlp_start < ovlp_end:
                    mapped_seed_ranges.append(
                        (ovlp_start - source + dest, ovlp_end - source + dest)
                    )

                    if seed_start < ovlp_start:
                        seed_ranges.append((seed_start, ovlp_start))
                    if ovlp_end < seed_end:
                        seed_ranges.append((ovlp_end, seed_end))
                    break
            else:
                mapped_seed_ranges.append((seed_start, seed_end))

        return mapped_seed_ranges


def parse_input(lines: List[str]) -> PUZZLE:
    seeds = list(map(int, lines[0].split("seeds: ")[-1].split()))
    ranges = defaultdict(list)

    for line in lines[2:]:
        if not line:
            continue
        elif line.endswith("map:"):
            key = line.split("map:")[0].strip()
        else:
            ranges[key].append(tuple(map(int, line.split())))

    return PUZZLE(seeds, *ranges.values())


def part1(lines: List[str]) -> int:
    puzzle = parse_input(lines)
    seeds = puzzle[0]
    for ranges in puzzle[1:]:
        mapper = PuzzleDict(ranges)
        seeds = [mapper[s] for s in seeds]

    return min(seeds)


def part2(lines: List[int]) -> int:
    puzzle = parse_input(lines)
    seeds = puzzle[0]
    seed_ranges = [
        (start, start + length) for start, length in zip(seeds[::2], seeds[1::2])
    ]

    for ranges in puzzle[1:]:
        mapper = PuzzleDict(ranges)
        seed_ranges = mapper.parse_range(seed_ranges)

    print(seed_ranges)
    return min([seed[0] for seed in seed_ranges])


if __name__ == "__main__":
    data = get_data(year=2023, day=5).splitlines()
    print(part1(data))
    print(part2(data))
