n = 150
c_avail = [1, 5,10, 25]

def change(n, coins_available, coins_so_far):
    if sum(coins_so_far) == n:
        yield coins_so_far
    elif sum(coins_so_far) > n:
        pass
    elif coins_so_far == []:
        pass
    else:
        for c in change(n, coins_available[:], coins_so_far + [coins_available[0]]):
            yield c
        for c in change(n, coins_available[1:], coins_so_far):
            yield c


print [x for x in change(n, c_avail, [])]