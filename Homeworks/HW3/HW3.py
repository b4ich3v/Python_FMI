class Tone:
    TONES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

    def __init__(self, input_name):
        if input_name not in self.TONES:
            raise ValueError("Invalid tone name")
        self.name_of_tone = input_name

    def __str__(self):
        return self.name_of_tone

    def __hash__(self):
        return hash(self.name_of_tone)

    def __eq__(self, other):
        return isinstance(other, Tone) and self.name_of_tone == other.name_of_tone

    def get_index(self):
        return Tone.TONES.index(self.name_of_tone)

    def __add__(self, other):
        if isinstance(other, Tone):
            return Chord(self, other)
        elif isinstance(other, Interval):
            index = (self.TONES.index(self.name_of_tone) + other.semitones) % 12
            return Tone(self.TONES[index])
        raise TypeError("Invalid operation")

    def __sub__(self, other):
        if isinstance(other, Tone):
            distance = (self.TONES.index(self.name_of_tone) - self.TONES.index(other.name_of_tone)) % 12
            return Interval(distance)
        elif isinstance(other, Interval):
            index = (self.TONES.index(self.name_of_tone) - other.semitones) % 12
            return Tone(self.TONES[index])
        raise TypeError("Invalid operation")


class Interval:
    interval_names = {
        0: "octave", 1: "minor 2nd", 2: "major 2nd", 3: "minor 3rd",
        4: "major 3rd", 5: "perfect 4th", 6: "diminished 5th",
        7: "perfect 5th", 8: "minor 6th", 9: "major 6th", 10: "minor 7th", 11: "major 7th"
    }

    def __init__(self, number):
        if type(number) is int:
            self.semitones = number % 12
        else:
            raise TypeError("Negative interval number")

    def __str__(self):
        return self.interval_names[self.semitones]

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

        unique_tones = [root] + list(tones)

        if len(set(unique_tones)) < 2: #using __eq__ from Tone
            raise TypeError("Cannot have a chord made of only 1 unique tone")

        self.root = root
        self.tones = unique_tones

    def __str__(self):
        other_tones = [tone for tone in self.tones if tone != self.root]
        sorted_tones = sorted(other_tones, key=lambda tone: Tone.TONES.index(tone.name_of_tone))
        sorted_tones.insert(0, self.root)

        return "-".join(str(tone) for tone in sorted_tones)

    def is_minor(self):
        root_index = self.root.get_index()

        for tone in self.tones:
            distance = (tone.get_index() - root_index) % 12
            if distance == 3:
                return True
        return False

    def is_major(self):
        root_index = self.root.get_index()

        for tone in self.tones:
            distance = (tone.get_index() - root_index) % 12
            if distance == 4:
                return True
        return False

    def is_power_chord(self):
        return not self.is_minor() and not self.is_major()

    def __add__(self, other):
        if isinstance(other, Tone):
            new_tones = list(self.tones)
            if other not in new_tones: #using __eq__ from Tone
                new_tones.append(other)
            return Chord(*new_tones)
        elif isinstance(other, Chord):
            new_tones = list(self.tones)
            for tone in other.tones:
                if tone not in new_tones: #using __eq__ from Tone
                    new_tones.append(tone)
            return Chord(*new_tones)
        raise TypeError("Invalid operation")

    def __sub__(self, other):
        if isinstance(other, Tone):
            if other not in self.tones:
                raise TypeError(f"Cannot remove tone {other} from chord {self}")

            new_tones = [tone for tone in self.tones if tone != other]
            if len(set(new_tones)) < 2:
                raise TypeError("Cannot have a chord made of only 1 unique tone")

            return Chord(self.root, *new_tones)
        raise TypeError("Invalid operation")

    def transposed(self, input_interval):
        if not isinstance(input_interval, Interval):
            raise ValueError("Interval must be an instance of Interval")

        transposed_tones = {tone + input_interval for tone in self.tones} #using __hash__ from Tone
        return Chord(*transposed_tones)
