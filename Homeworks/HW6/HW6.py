from abc import ABC, abstractmethod

from enum import Enum
from collections import Counter
from typing import Iterable, Tuple, List

# 4-bit compressed representation
hashed_unicode_symbols = {
    "♣": 1 << 0,  # 0001
    "♦": 1 << 1,  # 0010
    "♥": 1 << 2,  # 0100
    "♠": 1 << 3,  # 1000
}


class Suit(Enum):
    CLUBS = "♣"
    DIAMONDS = "♦"
    HEARTS = "♥"
    SPADES = "♠"
    WILD = "W" # 0000

    @property
    def symbol(self) -> str:
        return self.value

    @property
    def compressed(self) -> int:
        """4-bit store manipulation"""
        if self is Suit.WILD:
            return 0
        return hashed_unicode_symbols[self.value]

    @staticmethod
    def from_compressed(mask: int) -> "Suit":
        """Decompressing logic"""
        if mask == 0:
            return Suit.WILD
        for sym, bit in hashed_unicode_symbols.items():
            if bit == mask:
                for suit in Suit:
                    if suit.value == sym:
                        return suit
        raise ValueError(f"Invalid compressed suit: {mask}")


# Таблица 1: Ранг -> стойност в чипове
RANK_VALUES = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 10,
    "Q": 10,
    "K": 10,
    "A": 11,
}

# Rank ordering index (used for sort_key / Deck)
RANK_INDEX = {rank: i for i, rank in enumerate(RANK_VALUES.keys())}


class AbstractCard(ABC):
    __slots__ = ("_rank", "_suit")

    def __init__(self, rank: str, suit: Suit) -> None:
        if rank not in RANK_VALUES:
            raise ValueError(f"Invalid rank: {rank}")
        if not isinstance(suit, Suit):
            raise TypeError("suit must be an instance of Suit")

        self._rank = rank
        self._suit = suit

    @property
    def rank(self) -> str:
        return self._rank

    @property
    def suit(self) -> Suit:
        return self._suit

    @property
    @abstractmethod
    def chips(self) -> int:
        raise NotImplementedError

    @property
    def sort_key(self) -> Tuple[int, int]:
        """Unified sorting key: (rank index, compressed suit code) or (rank_index, 0bxxxx)"""
        return (RANK_INDEX[self.rank], self.suit.compressed)

    def __str__(self) -> str:
        return f"{self._rank}{self._suit.symbol}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.rank!r}, {self.suit!r})"


class Card(AbstractCard):
    """Normal card"""

    @property
    def chips(self) -> int:
        return RANK_VALUES[self.rank]


class SilverCard(AbstractCard):
    """Silver card"""

    @property
    def chips(self) -> int:
        return RANK_VALUES[self.rank] * 2

    def __str__(self) -> str:
        return f"Silver {self.rank}{self.suit.symbol}"


class GoldCard(AbstractCard):
    """Golden card"""

    @property
    def chips(self) -> int:
        return RANK_VALUES[self.rank] * 4

    def __str__(self) -> str:
        return f"Gold {self.rank}{self.suit.symbol}"


class WildCard(AbstractCard):
    """Wild card"""

    def __init__(self, rank: str) -> None:
        super().__init__(rank, Suit.WILD)

    @property
    def chips(self) -> int:
        return RANK_VALUES[self.rank]

    def __str__(self) -> str:
        return f"Wild {self.rank}{self.suit.symbol}"


class JokerAction(ABC):
    @abstractmethod
    def apply(self, chips: int, mult: int) -> Tuple[int, int]:
        raise NotImplementedError


class JokerActionIdentity(JokerAction):
    def apply(self, chips: int, mult: int) -> Tuple[int, int]:
        return chips, mult


class JokerActionAddChips(JokerAction):
    def __init__(self, delta: int) -> None:
        self.delta = int(delta)

    def apply(self, chips: int, mult: int) -> Tuple[int, int]:
        return chips + self.delta, mult


class JokerActionMultiplyMult(JokerAction):
    def __init__(self, factor: int) -> None:
        self.factor = int(factor)

    def apply(self, chips: int, mult: int) -> Tuple[int, int]:
        return chips, mult * self.factor


class JokerActionAddToMult(JokerAction):
    def __init__(self, delta: int) -> None:
        self.delta = int(delta)

    def apply(self, chips: int, mult: int) -> Tuple[int, int]:
        return chips, mult + self.delta


class JokerActionComposite(JokerAction):
    """Centralized logic which allows us to combine different kinds of provided actions"""

    def __init__(self, actions: Iterable[JokerAction]) -> None:
        self._actions = list(actions)

    def apply(self, chips: int, mult: int) -> Tuple[int, int]:
        for action in self._actions:
            chips, mult = action.apply(chips, mult)
        return chips, mult


class Joker:
    """Joker implementation (tuple of chips, multi factor and action logic)"""

    __slots__ = ("_chips", "_mult", "_action")

    def __init__(self, chips: int, mult: int, action: JokerAction | None = None) -> None:
        self._chips = int(chips)
        self._mult = int(mult)

        if action is None:
            action = JokerActionIdentity()

        if not isinstance(action, JokerAction):
            raise TypeError("action must be an instance of JokerAction")

        self._action = action

    @property
    def chips(self) -> int:
        return self._chips

    @property
    def mult(self) -> int:
        return self._mult

    @property
    def action(self) -> JokerAction:
        return self._action

    def __str__(self) -> str:
        return (
            f"Joker(chips={self.chips}, mult={self.mult}, "
            f"action={self.action.__class__.__name__})"
        )

    def __repr__(self) -> str:
        return f"Joker({self.chips}, {self.mult}, action={self.action})"


class Hand:
    """Hand implementation (container of cards, list)"""

    __slots__ = ("_cards",)

    def __init__(self, cards: Iterable[AbstractCard]) -> None:
        cards = list(cards)
        if len(cards) != 5:
            raise ValueError("Hand must contain exactly 5 cards.")
        self._cards = tuple(cards)

    @property
    def cards(self) -> Tuple[AbstractCard, ...]:
        return self._cards

    def __iter__(self):
        return iter(self._cards)

    def __len__(self) -> int:
        return 5

    def __str__(self) -> str:
        return "Hand[" + ", ".join(str(c) for c in self._cards) + "]"

    def __repr__(self) -> str:
        return f"Hand({self._cards!r})"


class CardFactory:
    """CardFactory implementation (string parser, String -> Card object)"""

    @staticmethod
    def _parse_rank_and_suit(token: str) -> Tuple[str, Suit]:
        token = token.strip()
        if len(token) < 2:
            raise ValueError(f"Invalid card notation: {token!r}")
        suit_char = token[-1]
        rank_part = token[:-1]
        if suit_char not in hashed_unicode_symbols:
            raise ValueError(f"Unknown suit symbol: {suit_char!r}")
        if rank_part not in RANK_VALUES:
            raise ValueError(f"Unknown rank: {rank_part!r}")
        for suit in Suit:
            if suit.value == suit_char:
                return rank_part, suit
        raise ValueError(f"Cannot map suit symbol: {suit_char!r}")

    @classmethod
    def from_string(cls, s: str) -> AbstractCard:
        s = s.strip()
        lower = s.lower()

        if lower.startswith("silver "):
            core = s[7:].strip()
            rank, suit = cls._parse_rank_and_suit(core)
            return SilverCard(rank, suit)

        if lower.startswith("gold "):
            core = s[5:].strip()
            rank, suit = cls._parse_rank_and_suit(core)
            return GoldCard(rank, suit)

        if lower.startswith("wild "):
            core = s[5:].strip()
            parts = core.split()
            if not parts:
                raise ValueError(f"Invalid Wild notation: {s!r}")
            rank = parts[0]
            if rank not in RANK_VALUES:
                raise ValueError(f"Unknown rank for Wild: {rank!r}")
            return WildCard(rank)

        # Normal card
        rank, suit = cls._parse_rank_and_suit(s)
        return Card(rank, suit)

    @classmethod
    def from_strings(cls, items: Iterable[str]) -> List[AbstractCard]:
        return [cls.from_string(s) for s in items]


class ScoreManager:
    """Centralized management/monitoring for card's score"""

    @staticmethod
    def _calculate_rank_bonus(cards: List[AbstractCard]) -> int:
        rank_counts = Counter(c.rank for c in cards)
        return sum(count for count in rank_counts.values() if count >= 2)

    @staticmethod
    def _calculate_suit_bonus(cards: List[AbstractCard]) -> int:
        suit_counts = Counter(c.suit for c in cards if c.suit is not Suit.WILD)
        wild_count = sum(1 for c in cards if c.suit is Suit.WILD)

        bonus = 0
        for suit in (Suit.CLUBS, Suit.DIAMONDS, Suit.HEARTS, Suit.SPADES):
            count = suit_counts.get(suit, 0) + wild_count
            if count >= 2:
                bonus += count
        return bonus

    @classmethod
    def score(cls, cards: Iterable[AbstractCard], jokers: Iterable[Joker]) -> int:
        cards = list(cards)
        jokers = list(jokers)

        if len(cards) != 5:
            return 0

        chips = sum(c.chips for c in cards) + sum(j.chips for j in jokers)
        mult = 1 + sum(j.mult for j in jokers)

        mult += cls._calculate_rank_bonus(cards)
        mult += cls._calculate_suit_bonus(cards)

        for j in jokers:
            chips, mult = j.action.apply(chips, mult)

        return int(chips * mult)

    @classmethod
    def score_hand(cls, hand: Hand, jokers: Iterable[Joker]) -> int:
        return cls.score(hand.cards, jokers)


if __name__ == "__main__":
    # Example 1, expected 200
    c1 = Card("A", Suit.CLUBS)
    c2 = Card("K", Suit.HEARTS)
    c3 = Card("K", Suit.SPADES)
    c4 = Card("7", Suit.DIAMONDS)
    c5 = Card("2", Suit.DIAMONDS)
    hand1 = Hand([c1, c2, c3, c4, c5])
    print("Example 1:", ScoreManager.score(hand1, []))

    # Example 2, expected 4484
    c1 = Card("A", Suit.CLUBS)
    c2 = SilverCard("K", Suit.DIAMONDS)
    c3 = GoldCard("K", Suit.HEARTS)
    c4 = WildCard("A")
    c5 = Card("A", Suit.SPADES)
    j1 = Joker(5, 2)
    j2 = Joker(10,3,JokerActionComposite([JokerActionAddChips(10), JokerActionMultiplyMult(2)]))
    hand2 = Hand([c1, c2, c3, c4, c5])
    print("Example 2:", ScoreManager.score(hand2, [j1, j2]))

    # Example 3, expected 1387 and 1606
    c1 = Card("A", Suit.HEARTS)
    c2 = Card("K", Suit.HEARTS)
    c3 = Card("Q", Suit.HEARTS)
    c4 = Card("J", Suit.HEARTS)
    c5 = Card("10", Suit.HEARTS)
    hand3 = Hand([c1, c2, c3, c4, c5])
    j1 = Joker(1, 1, JokerActionComposite([JokerActionAddChips(10), JokerActionMultiplyMult(2)]))
    j2 = Joker(1, 1, JokerActionComposite([JokerActionAddChips(10), JokerActionAddToMult(3)]))
    print("Example 3 (j1, j2):", ScoreManager.score_hand(hand3, [j1, j2]))  
    print("Example 3 (j2, j1):", ScoreManager.score_hand(hand3, [j2, j1]))  
