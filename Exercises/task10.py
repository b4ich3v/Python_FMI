def find_largest(lst):
    if not lst:
        return None
    largest = lst[0]
    for item in lst:
        if item > largest:
            largest = item
    return largest
