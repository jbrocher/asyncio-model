from time import sleep


def fibonnaci_generator():
    n_1 = 0
    n_2 = 1
    while True:
        n = n_1 + n_2
        yield n

        n_2 = n_1
        n_1 = n


if __name__ == "__main__":
    generator = fibonnaci_generator()
    for x in generator:
        print(x)
        sleep(1)
