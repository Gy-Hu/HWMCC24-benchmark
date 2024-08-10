# assume( len(a) >= 1 and len(b) >= 1 and a[0] == b[0])
def last_same_element(a: list, b: list):
    len_a = len(a)
    len_b = len(b)
    same = a[0]
    if(len_a<=len_b):
        len_min = len_a
    else:
        len_min = len_b
    for idx in range(len_min):
        if(a[idx] == b[idx]):
            same = a[idx]

    return same



print(last_same_element([1, 2], [1, 3]))  # 1
print(last_same_element([1, 2], [1, 2, 4]))  # 2
print(last_same_element([1, 2, 5], [1, 2]))  # 2
print(last_same_element([1, 2, 5], [1, 2, 4]))  # 2
