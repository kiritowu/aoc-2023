from typing import List

from aocd import get_data


def part1(lines: List[str]):
    """
    You will get a fixed amount of time during which your boat has to travel
    as far as it can, and you win if your boat goes the farthest.

    As part of signing up, you get a sheet of paper (your puzzle input) that
    lists the time allowed for each race and also the best distance ever
    recorded in that race. To guarantee you win the grand prize, you need to
    make sure you go farther in each race than the current record holder.

    The organizer brings you over to the area where the boat races are held.
    The boats are much smaller than you expected - they're actually toy
    boats, each with a big button on top. Holding down the button
    charges the boat, and releasing the button allows the boat to move.
    Boats move faster if their button was held longer, but time spent holding
    the button counts against the total race time. You can only hold the
    button at the start of the race, and boats don't move until the button
    is released.

    For example:

    Time:      7  15   30
    Distance:  9  40  200

    This document describes three races:

        The first race lasts 7 milliseconds. The record distance in this race
        is 9 millimeters.
        The second race lasts 15 milliseconds. The record distance in this
        race is 40 millimeters.
        The third race lasts 30 milliseconds. The record distance in this
        race is 200 millimeters.

    Your toy boat has a starting speed of zero millimeters per millisecond.
    For each whole millisecond you spend at the beginning of the race holding
    down the button, the boat's speed increases by one millimeter per
    millisecond.

    Since the current record for this race is 9 millimeters, there are
    actually 4 different ways you could win: you could hold the button
    for 2, 3, 4, or 5 milliseconds at the start of the race.

    In the second race, you could hold the button for at least 4
    milliseconds and at most 11 milliseconds and beat the record, a total
    of 8 different ways to win.

    In the third race, you could hold the button for at least 11 milliseconds
    and no more than 19 milliseconds and still beat the record, a total of 9
    ways you could win.

    To see how much margin of error you have, determine the number of ways
    you can beat the record in each race; in this example, if you multiply
    these values together, you get 288 (4 * 8 * 9).

    Determine the number of ways you could beat the record in each race.
    What do you get if you multiply these numbers together?
    """
    times = list(map(int, lines[0].split("Time: ")[-1].split()))
    distance = list(map(int, lines[1].split("Distance: ")[-1].split()))

    acc = 1
    for t, d in zip(times, distance):
        acc *= sum([1 if i * (t - i) > d else 0 for i in range(1, t)])

    return acc


def part2(lines: List[str]) -> int:
    """
    As the race is about to start, you realize the piece of paper with race
    times and record distances you got earlier actually just has very bad
    kerning. There's really only one race - ignore the spaces between the
    numbers on each line.

    So, the example from before:

    Time:      7  15   30
    Distance:  9  40  200

    ...now instead means this:

    Time:      71530
    Distance:  940200

    Now, you have to figure out how many ways there are to win this
    single race. In this example, the race lasts for 71530 milliseconds
    and the record distance you need to beat is 940200 millimeters.
    You could hold the button anywhere from 14 to 71516 milliseconds
    and beat the record, a total of 71503 ways!

    How many ways can you beat the record in this one much longer race?
    """
    t = int("".join(lines[0].split("Time: ")[-1].split()))
    d = int("".join(lines[1].split("Distance: ")[-1].split()))
    total = sum([1 if i * (t - i) > d else 0 for i in range(1, t)])
    return total


if __name__ == "__main__":
    data = get_data(year=2023, day=6).splitlines()

    print(part1(data))
    print(part2(data))
