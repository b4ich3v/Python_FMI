class Tone:
    TONES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

    def __init__(self, input_name):
        if input_name not in self.TONES:
            raise ValueError("Invalid tone name")
        self.name_of_tone = input_name

    def __str__(self):
        return self.name_of_tone

    def __hash__(self):  # this time i didn't use it
        return hash(self.name_of_tone)

    def __eq__(self, other):
        return isinstance(other, Tone) and self.name_of_tone == other.name_of_tone

    def __add__(self, other):
        if isinstance(other, Tone):
            return self._calculate_tone(other, "+")
        elif isinstance(other, Interval):
            return self._calculate_interval(other, "+")
        raise TypeError("Invalid operation")

    def __sub__(self, other):
        if isinstance(other, Tone):
            return self._calculate_tone(other, "-")
        elif isinstance(other, Interval):
            return self._calculate_interval(other, "-")
        raise TypeError("Invalid operation")

    def get_index(self):
        return Tone.TONES.index(self.name_of_tone)

    def _calculate_tone(self, other, symbol):
        if symbol == "+":
            return Chord(self, other)
        elif symbol == "-":
            distance = (self.TONES.index(self.name_of_tone) -
                        self.TONES.index(other.name_of_tone)) % 12
            return Interval(distance)
        else:
            raise ValueError("Invalid symbol")

    def _calculate_interval(self, other, symbol):
        if symbol == "+":
            index = (self.TONES.index(self.name_of_tone) + other.semitones) % 12
            return Tone(self.TONES[index])
        elif symbol == "-":
            index = (self.TONES.index(self.name_of_tone) - other.semitones) % 12
            return Tone(self.TONES[index])
        else:
            raise ValueError("Invalid symbol")


class Interval:
    INTERVAL_NAMES = [
        "octave", "minor 2nd", "major 2nd", "minor 3rd",
        "major 3rd", "perfect 4th", "diminished 5th",
        "perfect 5th", "minor 6th", "major 6th",
        "minor 7th", "major 7th"
    ]

    def __init__(self, number):
        if isinstance(number, int):
            self.semitones = number % 12
        else:
            raise TypeError("Invalid input")

    def __str__(self):
        return self.INTERVAL_NAMES[self.semitones]

    def __add__(self, other):
        if isinstance(other, Interval):
            return Interval(self.semitones + other.semitones)
        raise TypeError("Invalid operation")

    def __neg__(self):
        return Interval(-self.semitones)


class Chord:
    def __init__(self, root, *tones):
        if not isinstance(root, Tone):
            raise ValueError("Root must be a Tone instance")

        for tone in tones:
            if not isinstance(tone, Tone):
                raise ValueError("All tones must be Tone instances")

        unique_tones = [root]
        for tone in tones:
            if tone not in unique_tones: #using __eq__
                unique_tones.append(tone)

        if len(unique_tones) < 2:
            raise TypeError("Cannot have a chord made of only 1 unique tone")

        self.root = root
        self.tones = unique_tones

    def __str__(self):
        root_index = Tone.TONES.index(self.root.name_of_tone)
        other_tones = [tone for tone in self.tones if tone != self.root]
        sorted_tones = sorted(
            other_tones,
            key=lambda tone: (Tone.TONES.index(tone.name_of_tone) - root_index) % 12
        )
        sorted_tones.insert(0, self.root)
        return "-".join(str(tone) for tone in sorted_tones)

    def __add__(self, other):
        if isinstance(other, Tone):
            return self._add_tone(other)
        elif isinstance(other, Chord):
            return self._add_chord(other)
        raise TypeError("Invalid operation")

    def __sub__(self, other):
        if isinstance(other, Tone):
            if other not in self.tones:  # using __eq__
                raise TypeError(f"Cannot remove tone {other} from chord {self}")
            new_tones = [tone for tone in self.tones if tone != other]
            if len(set(new_tones)) < 2:
                raise TypeError("Cannot have a chord made of only 1 unique tone")
            return Chord(*new_tones)
        raise TypeError("Invalid operation")

    def _validate_distance_to_root(self, target):
        root_index = self.root.get_index()
        for tone in self.tones:
            distance = (tone.get_index() - root_index) % 12
            if distance == target:
                return True
        return False

    def is_minor(self):
        return self._validate_distance_to_root(3)

    def is_major(self):
        return self._validate_distance_to_root(4)

    def is_power_chord(self):
        return not self.is_minor() and not self.is_major()

    def _add_tone(self, other):
        if other not in self.tones:  # using __eq__
            new_tones = list(self.tones)
            new_tones.append(other)
            return Chord(*new_tones)
        else:
            return self

    def _add_chord(self, other):
        new_tones = list(self.tones)
        for tone in other.tones:
            if tone not in self.tones:  # using __eq__
                new_tones.append(tone)
        return Chord(*new_tones)

    def transposed(self, input_interval):
        if not isinstance(input_interval, Interval):
            raise ValueError("Interval must be an instance of Interval")

        transposed_tones = [tone + input_interval for tone in self.tones]
        return Chord(*transposed_tones)
