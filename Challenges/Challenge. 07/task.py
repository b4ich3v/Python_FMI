from secret import clue

def lucky():

    bits_low = (clue(left_shift=5) >> 5) & 0b111  # bit2, bit1, bit0
    bits_high = clue(right_shift=5) & 0b111  # bit7, bit6, bit5
    bit_middle = (1 << 0b1) if clue(bw_or=239) != 239 else 0 # bit4
    bit_middle = (bit_middle | 0b1) if clue(bw_and=8) else bit_middle # bit4, bit3

    result = (bits_high << 5) | (bit_middle << 3) | bits_low

    return result
