from secret import clue

def lucky():

    bits_low = (clue(left_shift=5) >> 5) & 0b111  # bit2, bit1, bit0
    bits_high = clue(right_shift=5) & 0b111  # bit7, bit6, bit5
    bit4 = 1 if clue(bw_or=239) != 239 else 0 # bit4
    bit3 = 1 if clue(bw_and=8) else 0 # bit3

    result = (bits_high << 5) | (bit4 << 4) | (bit3 << 3) | bits_low

    return result
