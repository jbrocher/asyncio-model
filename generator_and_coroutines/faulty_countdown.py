from time import sleep


def count_down_coro():
    n = 5
    while n:
        reset = yield n
        if reset:
            n = reset
        else:
            n -= 1


if __name__ == "__main__":
    count_down = count_down_coro()
    for x in count_down:
        print(x)
        if x == 3:
            count_down.send(5)
        sleep(1)
