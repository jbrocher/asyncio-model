from time import sleep


def fibonnaci_generator():
    n_1 = 0
    n_2 = 1
    while True:
        n = n_1 + n_2
        yield n
        sleep(1)

        n_2 = n_1
        n_1 = n


def filter_even():
    while True:
        x = yield
        if x > 200:
            return x
        if x % 2 == 0:
            print(x)


if __name__ == "__main__":
    filter = filter_even()
    generator = fibonnaci_generator()
    filter.send(None)
    for x in generator:
        filter.send(x)
