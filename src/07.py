from typing import List
from collections import Counter

from aocd import get_data


def strength(hand_hex: List[str], with_joker: bool = False) -> int:
    """Calculate strength of a hand based on the
    Camel Card rules:

    6xxxx - Five of a kind (e.g. 11111)
    5xxxx - Four of a kind (e.g. 11112)
    4xxxx - Full House (e.g. 11122)
    3xxxx - Three of a kind (e.g. 11123)
    2xxxx - Two pair (e.g. 11223)
    1xxxx - One pair (e.g. 11234)
    0xxxx - High card (e.g. 12345)

    Where xxxx represent the relative strength of each card in base-16
    A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, 2.
    """
    hand_counter = Counter(hand_hex)
    joker_freq = 0
    if with_joker and "0" in hand_counter:
        # Find frequency of Joker and Max card
        joker_freq = hand_counter.pop("0")
        max_freq = max(hand_counter.values()) if hand_counter else 0

        # Replace Joker with max card in hand
        for key, freq in hand_counter.items():
            if freq == max_freq:
                hand_counter[key] += joker_freq
                break
        else:
            # In the case of all 5 cards are Joker
            hand_counter["0"] = joker_freq

        # Ensure max_freq is maximum
        max_freq += joker_freq
    else:
        max_freq = max(hand_counter.values())

    s = "".join(hand_hex)

    # Five of a kind
    if len(hand_counter) == 1:
        s = "6" + s
    elif len(hand_counter) == 2:
        # Four of a kind
        if max_freq == 4:
            s = "5" + s
        # Full House
        else:
            s = "4" + s
    elif max_freq == 3:
        # Three of a kind
        s = "3" + s
    elif max_freq == 2:
        if len(list(filter(lambda x: x == 2, hand_counter.values()))) == 2:
            # Two pair
            s = "2" + s
        else:
            # One pair
            s = "1" + s

    return int(s, 16)


def part1(lines: List[str]) -> int:
    """
    In Camel Cards, you get a list of hands, and your goal is to order them
    based on the strength of each hand. A hand consists of five cards labeled
    one of A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, or 2. The relative strength
    of each card follows this order, where A is the highest and 2 is the
    lowest.

    Every hand is exactly one type. From strongest to weakest, they are listed
    in `strength` function.

    If two hands have the same type, a second ordering rule takes effect.
    Start by comparing the first card in each hand. If these cards are
    different, the hand with the stronger first card is considered stronger.
    If the first card in each hand have the same label, however, then move on
    to considering the second card in each hand. If they differ, the hand with
    the higher second card wins; otherwise, continue with the third card in
    each hand, then the fourth, then the fifth.

    So, 33332 and 2AAAA are both four of a kind hands, but 33332 is stronger
    because its first card is stronger. Similarly, 77888 and 77788 are both a
    full house, but 77888 is stronger because its third card is stronger (and
    both hands have the same first and second card).

    To play Camel Cards, you are given a list of hands and their corresponding
    bid (your puzzle input). For example:

    32T3K 765
    T55J5 684
    KK677 28
    KTJJT 220
    QQQJA 483

    This example shows five hands; each hand is followed by its bid amount.
    Each hand wins an amount equal to its bid multiplied by its rank, where
    the weakest hand gets rank 1, the second-weakest hand gets rank 2, and so
    on up to the strongest hand. Because there are five hands in this example,
    the strongest hand will have rank 5 and its bid will be multiplied by 5.

    So, the first step is to put the hands in order of strength:

        32T3K is the only one pair and the other hands are all a stronger type,
        so it gets rank 1.
        KK677 and KTJJT are both two pair. Their first cards both have the
        same label, but the second card of KK677 is stronger (K vs T), so
        KTJJT gets rank 2 and KK677 gets rank 3.
        T55J5 and QQQJA are both three of a kind. QQQJA has a stronger first
        card, so it gets rank 5 and T55J5 gets rank 4.

    Now, you can determine the total winnings of this set of hands by adding
    up the result of multiplying each hand's bid with its rank (765 * 1 + 220
    * 2 + 28 * 3 + 684 * 4 + 483 * 5). So the total winnings in this example
    are 6440.

    Find the rank of every hand in your set. What are the total winnings?
    """
    cards = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
    card2hex = {k: hex(i).replace("0x", "") for i, k in enumerate(cards[::-1])}

    hands = [line.split(" ") for line in lines]
    hands.sort(key=lambda x: strength(list(map(lambda x: card2hex[x], x[0]))))
    total = 0
    for rank, (_, bid) in enumerate(hands, start=1):
        total += rank * int(bid)

    return total


def part2(lines: List[str]) -> int:
    """
    To make things a little more interesting, the Elf introduces one
    additional rule. Now, J cards are jokers - wildcards that can act like
    whatever card would make the hand the strongest type possible.

    To balance this, J cards are now the weakest individual cards, weaker
    even than 2. The other cards stay in the same order: A, K, Q, T, 9, 8,
    7, 6, 5, 4, 3, 2, J.

    J cards can pretend to be whatever card is best for the purpose of
    determining hand type; for example, QJJQ2 is now considered four
    of a kind. However, for the purpose of breaking ties between two hands
    of the same type, J is always treated as J, not the card it's pretending
    to be: JKKK2 is weaker than QQQQ2 because J is weaker than Q.

    Using the new joker rule, find the rank of every hand in your set. What
    are the new total winnings?
    """
    cards = [
        "A",
        "K",
        "Q",
        "T",
        "9",
        "8",
        "7",
        "6",
        "5",
        "4",
        "3",
        "2",
        "J",
    ]
    card2hex = {k: hex(i).replace("0x", "") for i, k in enumerate(cards[::-1])}

    hands = [line.split(" ") for line in lines]
    hands.sort(
        key=lambda x: strength(
            list(map(lambda x: card2hex[x], x[0])), with_joker=True
        )
    )
    total = 0
    for rank, (_, bid) in enumerate(hands, start=1):
        total += rank * int(bid)

    return total


if __name__ == "__main__":
    data = get_data(year=2023, day=7).splitlines()
    print(part1(data))
    print(part2(data))
