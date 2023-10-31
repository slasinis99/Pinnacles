from math import factorial
def stirling2(n: int, k: int) -> int:
    s = 0
    for j in range(k+1):
        s += ((-1)**(k-j)*j**n) / (factorial(k-j)*factorial(j))
    return s

def main():
    for k in range(0, 11):
        for n in range(k, 11):
            print(f'S({n}, {k}) = {int(stirling2(n, k))}')
    print(f'S(5, 3) = {int(stirling2(1,2))}')

if __name__ == '__main__':
    main()