def odd_iter():
    """
    构造一个从3开始的奇数序列
    :return:
    """
    n = 1
    while True:
        n = n + 2
        yield n


def not_divisible(n):
    """
    筛选函数,判断某数能否整除n
    :param n:
    :return:
    """
    return lambda x: x % n > 0


def primes():
    """
    生成素数序列
    :return:
    """
    yield 2
    # 初始序列
    it = odd_iter()
    while True:
        # 返回序列的第一个数
        n = next(it)
        yield n
        # 更新序列
        it = filter(not_divisible(n), it)


if __name__ == '__main__':
    for n in primes():
        if n < 100:
            print(n)
        else:
            break
    print("ok")
