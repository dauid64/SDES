def permutation_10(key):
    key_permutated = ''
    table = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
    for i in table:
        key_permutated += key[i - 1]
    return key_permutated

def shift_left(split_key):
    split_key = split_key[1:] + split_key[0]
    return split_key

def permutation_8(key):
    key_permutated = ''
    table = [6, 3, 7, 4, 8, 5, 10, 9]
    for i in table:
        key_permutated += key[i - 1]
    return key_permutated

def generate_keys(key):
    key_permutated = permutation_10(key)

    left = shift_left(key_permutated[:5])
    right = shift_left(key_permutated[5:])


    key1 = permutation_8(left + right)

    left = shift_left(shift_left(left))
    right = shift_left(shift_left(right))

    key2 = permutation_8(left + right)

    return key1, key2



