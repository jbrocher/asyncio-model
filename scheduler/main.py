from socket import SO_REUSEADDR, SOL_SOCKET, socket
from scheduler.future import AcceptSocket, ReadSocket, Sleep
from scheduler.scheduler import Scheduler


async def sleep(n: int):
    return await Sleep(n)


async def read(conn):
    return await ReadSocket(conn)


async def accept(sock):
    return await AcceptSocket(sock)


async def echo(sock):
    while True:
        data = await read(sock)
        if not data:
            sock.close()

        print(f"received {data}")
        # assume non-blocking
        sock.send(data)


async def echo_server(scheduler: Scheduler, port: int):
    print("creating socket...")
    sock = socket()
    sock.bind(("localhost", port))

    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.listen(100)
    sock.setblocking(False)
    print("socket created waiting for connection")
    while True:
        conn = await accept(sock)
        # Schedule new concurrent connection
        scheduler.create_task(echo(conn))


if __name__ == "__main__":
    scheduler = Scheduler()
    scheduler.create_task(echo_server(scheduler, 1235))
    scheduler.run_forever()
