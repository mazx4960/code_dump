import numpy as np


def gen_el_ma(cur, i):
    n = len(cur)
    if i == n:
        return np.identity(n)
    else:
        new = np.identity(n)
        for j in range(i, n):
            num = cur[j][i - 1]
            pivot = cur[i - 1][i - 1]
            k = -num / pivot
            new[j][i - 1] = k
        cur = new.dot(cur)
        return (gen_el_ma(cur, i + 1)).dot(new)


def solve_sim(arr):
    n = len(arr)
    ans = []
    print(arr)
    for i in range(n - 1, -1, -1):
        total = arr[i][-1]
        target = i
        cur = target + 1
        for j in range(len(ans)):
            total -= ans[j] * arr[i][cur]
            cur += 1
        ans.insert(0, total / arr[i][target])
    return ans


def main():
    # ans is x=2, y=3
    a = np.array([
      [1, 3, 5, 31],
      [2, 4, 6, 40],
      [4, 1, 7, 39]])
    # N = int(input())
    # a = [list(map(int, input().split())) for i in range(N)]

    el_ma = gen_el_ma(a, 1)
    print(el_ma)
    arr = el_ma.dot(a)
    result = solve_sim(arr)
    print(result)


if __name__ == '__main__':
    main()
