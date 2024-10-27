def calculate_final_vector(coords, hexes):
    x = coords[0]
    y = coords[1]

    for current in hexes:
        current = current.lower()
        if current == "ffffff":
            continue
        elif current == "000000":
            break
        elif current == "c0ffc0" or current == "c00000":
            x -= 1
        elif current == "00c000" or current == "ffc0c0":
            x += 1
        elif current == "c0c000" or current == "c0c0ff":
            y += 1
        elif current == "ffffc0" or current == "0000c0":
            y -= 1
        else:
            print("Nishto")
    return (x, y)
