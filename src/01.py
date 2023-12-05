from typing import List

from aocd import get_data


def part1(lines: List[str]) -> int:
    """
    The newly-improved calibration document consists of lines of text;
    each line originally contained a specific calibration value that
    the Elves now need to recover. On each line, the calibration value
    can be found by combining the first digit and the last digit
    (in that order) to form a single two-digit number.

    For example:

    1abc2
    pqr3stu8vwx
    a1b2c3d4e5f
    treb7uchet

    In this example, the calibration values of these four lines are
    12, 38, 15, and 77. Adding these together produces 142.

    Consider your entire calibration document.
    What is the sum of all of the calibration values?
    """
    total = 0
    for line in lines:
        # Two-Pointer to find the digits
        l, r = 0, len(line) - 1
        while l <= r:
            if not line[l].isdigit():
                l += 1
            elif not line[r].isdigit():
                r -= 1
            else:
                total += int(line[l] + line[r])
                break
    return total


def part2(lines: List[str]) -> int:
    """
    Your calculation isn't quite right. It looks like some of the digits are
    actually spelled out with letters: one, two, three, four, five, six, seven,
    eight, and nine also count as valid "digits".

    Equipped with this new information, you now need to find the real first
    and last digit on each line. For example:

    two1nine
    eightwothree
    abcone2threexyz
    xtwone3four
    4nineeightseven2
    zoneight234
    7pqrstsixteen

    In this example, the calibration values are 29, 83, 13, 24, 42, 14, and
    76. Adding these together produces 281.

    What is the sum of all of the calibration values?
    """
    # Seach and replace the words with the numbers
    # Instead of replacing directly to digit, a fuzzy replacement is used
    # to avoid replacing the digits that are part of other digits
    str2num = {
        "one": "o1ne",
        "two": "t2wo",
        "three": "th3ree",
        "four": "f4our",
        "five": "f5ive",
        "six": "s6ix",
        "seven": "se7ven",
        "eight": "eig8ht",
        "nine": "ni9ne",
        "zero": "ze0ro",
    }
    results = []
    for line in lines:
        for word, num in str2num.items():
            line = line.replace(word, num)
        results.append(line)
    return part1(results)


if __name__ == "__main__":
    data = get_data(year=2023, day=1).splitlines()
    print(part1(data))
    print(part2(data))
