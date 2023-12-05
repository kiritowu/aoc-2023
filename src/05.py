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
    """Dictionary that map source to destination based on mapping ranges.
    Source can be streamed(based on id) or batched(based on ranges).
    """

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
    """Extract puzzle attributes from source file"""
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
    """
    The almanac (your puzzle input) lists all of the seeds that need to be planted.
    It also lists what type of soil to use with each kind of seed, what type of
    fertilizer to use with each kind of soil, what type of water to use with each
    kind of fertilizer, and so on. Every type of seed, soil, fertilizer and so on
    is identified with a number, but numbers are reused by each category - that is,
    soil 123 and fertilizer 123 aren't necessarily related to each other.

    For example:

    seeds: 79 14 55 13

    seed-to-soil map:
    50 98 2
    52 50 48

    soil-to-fertilizer map:
    0 15 37
    37 52 2
    39 0 15

    fertilizer-to-water map:
    49 53 8
    0 11 42
    42 0 7
    57 7 4

    water-to-light map:
    88 18 7
    18 25 70

    light-to-temperature map:
    45 77 23
    81 45 19
    68 64 13

    temperature-to-humidity map:
    0 69 1
    1 0 69

    humidity-to-location map:
    60 56 37
    56 93 4

    The almanac starts by listing which seeds need to be planted: seeds 79, 14, 55, and 13.

    The rest of the almanac contains a list of maps which describe how to convert numbers
    from a source category into numbers in a destination category. That is, the section
    that starts with seed-to-soil map: describes how to convert a seed number (the source)
    to a soil number (the destination). This lets the gardener and his team know which soil
    to use with which seeds, which water to use with which fertilizer, and so on.

    Rather than list every source number and its corresponding destination number one by
    one, the maps describe entire ranges of numbers that can be converted. Each line
    within a map contains three numbers: the destination range start, the source range
    start, and the range length.

    Consider again the example seed-to-soil map:

    50 98 2
    52 50 48

    The first line has a destination range start of 50, a source range start of 98, and a
    range length of 2. This line means that the source range starts at 98 and contains two
    values: 98 and 99. The destination range is the same length, but it starts at 50, so
    its two values are 50 and 51. With this information, you know that seed number 98
    corresponds to soil number 50 and that seed number 99 corresponds to soil number 51.

    The second line means that the source range starts at 50 and contains 48 values: 50,
    51, ..., 96, 97. This corresponds to a destination range starting at 52 and also
    containing 48 values: 52, 53, ..., 98, 99. So, seed number 53 corresponds to soil number 55.

    Any source numbers that aren't mapped correspond to the same destination number.
    So, seed number 10 corresponds to soil number 10.

    So, the entire list of seed numbers and their corresponding soil numbers looks like this:

    seed  soil
    0     0
    1     1
    ...   ...
    48    48
    49    49
    50    52
    51    53
    ...   ...
    96    98
    97    99
    98    50
    99    51

    With this map, you can look up the soil number required for each initial seed number:

        Seed number 79 corresponds to soil number 81.
        Seed number 14 corresponds to soil number 14.
        Seed number 55 corresponds to soil number 57.
        Seed number 13 corresponds to soil number 13.

    The gardener and his team want to get started as soon as possible, so they'd like to
    know the closest location that needs a seed. Using these maps, find the lowest location
    number that corresponds to any of the initial seeds. To do this, you'll need to convert
    each seed number through other categories until you can find its corresponding
    location number. In this example, the corresponding types are:

        Seed 79, soil 81, fertilizer 81, water 81, light 74, temperature 78, humidity 78,
        location 82.
        Seed 14, soil 14, fertilizer 53, water 49, light 42, temperature 42, humidity 43,
        location 43.
        Seed 55, soil 57, fertilizer 57, water 53, light 46, temperature 82, humidity 82,
        location 86.
        Seed 13, soil 13, fertilizer 52, water 41, light 34, temperature 34, humidity 35,
        location 35.

    So, the lowest location number in this example is 35.

    What is the lowest location number that corresponds to any of the initial seed numbers?
    """  # noqa: E501
    puzzle = parse_input(lines)
    seeds = puzzle[0]
    for ranges in puzzle[1:]:
        mapper = PuzzleDict(ranges)
        seeds = [mapper[s] for s in seeds]

    return min(seeds)


def part2(lines: List[int]) -> int:
    """Everyone will starve if you only plant such a small number of seeds.
    Re-reading the almanac, it looks like the seeds: line actually describes
    ranges of seed numbers.

    The values on the initial seeds: line come in pairs. Within each pair, the
    first value is the start of the range and the second value is the length
    of the range. So, in the first line of the example above:

    seeds: 79 14 55 13

    This line describes two ranges of seed numbers to be planted in the garden.
    The first range starts with seed number 79 and contains 14 values: 79, 80,
    ..., 91, 92. The second range starts with seed number 55 and contains 13
    values: 55, 56, ..., 66, 67.

    Now, rather than considering four seed numbers, you need to consider a
    total of 27 seed numbers.

    In the above example, the lowest location number can be obtained from seed
    number 82, which corresponds to soil 84, fertilizer 84, water 84, light 77,
    temperature 45, humidity 46, and location 46. So, the lowest location
    number is 46.

    Consider all of the initial seed numbers listed in the ranges on the first
    line of the almanac. What is the lowest location number that corresponds
    to any of the initial seed numbers?
    """
    puzzle = parse_input(lines)
    seeds = puzzle[0]
    seed_ranges = [
        (start, start + length)
        for start, length in zip(seeds[::2], seeds[1::2])
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
