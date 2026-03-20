def dec_to_bin(cell: int) -> list[int]:
    res = ''
    while cell > 0:
        res = str(cell % 2)+res
        cell //= 2
    while len(res) != 4:
        res = '0'+res
    lst = [int(x) for x in res]
    lst.reverse()
    return lst
