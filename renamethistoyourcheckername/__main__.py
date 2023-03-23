import asyncio
import os
import checker
from checker_base import cli
import logging


async def main_menu():
    cli.clear()
    resp = cli.query_option('Main Menu', ['Start'])
    if resp == 1:
        cli.clear()
        await checker.GeoGuesserChecker().start()

def make_directories(directories: list[str]):
    for directory in directories:
        try:
            os.mkdir(directory)
        except FileExistsError:
            pass

def make_files(files: list[str]):
    for new_file in files:
        with open(new_file, 'a'):
            pass


async def main():
    make_directories(['input', 'output', 'logs'])
    make_files(['input/proxies.txt', 'input/lines.txt'])

    logging.basicConfig(filename='logs/log.txt')


    while True:
        await main_menu()

setattr(asyncio.sslproto._SSLProtocolTransport, "_start_tls_compatible", True)

# uvloop only supported on *nix
# if os.name == "win32":
asyncio.run(main())
# else:
#     import uvloop
#     if sys.version_info >= (3, 11):
#         with asyncio.Runner(loop_factory=uvloop.new_event_loop) as runner:
#             runner.run(main())
#     else:
#         uvloop.install()
#         asyncio.run(main())
