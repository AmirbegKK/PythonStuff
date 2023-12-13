# Recursive solution for Josephus problem

def josephus(n, k):
    if n == 1:
        return 0
    return (josephus(n - 1, k) + k) % n

n = int(input('Enter 1st number: '))
k = int(input('Enter 2nd number: '))

print(f'Josephus({n}, {k}) is {josephus(n,k)}')
