from collections import deque
import asyncio
from datetime import datetime
import os
from . import cli
from abc import ABC, abstractmethod
import logging
from dataclasses import dataclass
import aiohttp

@dataclass
class ProxyManager:
    proxies: list
    _index: int = 0

    @property
    def count(self):
        return len(self.proxies)

    def get(self):
        if not self.count:
            return None

        self._index = (self._index + 1)%self.count

        return self.proxies[self._index]
    
    def ban(self, proxy: str):
        self.proxies.remove(proxy)

class CheckerBase(ABC): 
    def __init__(self, lines_path: str = 'input/lines.txt', proxies_path: str = 'input/proxies.txt'):
        self.lines =        deque(self._load_file(lines_path))
        self.queue =        asyncio.Queue()
        self.proxy =        ProxyManager(self._load_file(proxies_path))
        self._file_locker = asyncio.Lock()
        self._date =        datetime.now().strftime("%Y-%m-%d %H;%M;%S")

        self._make_output_folder()

    @abstractmethod
    async def check(self):
        pass

    def _make_output_folder(self):
        path = f"output/{self._date}/"

        os.makedirs(os.path.dirname(path), exist_ok=True)
    
    def _load_file(self, path: str) -> list:
        try:
            with open(path) as f:
                data = f.read().splitlines()
                
                return list(filter(lambda line: line is not None, data))
        except FileNotFoundError:
            return None

    async def write_hit(self, file_name: str, hit, capture:list = None):
        output_string = hit

        if capture:
            formatted_capture = ['']
            for element in capture:
                formatted_capture.append(str(element))
            output_string += ' | '.join(formatted_capture)

        async with self._file_locker:
            with open(f"output/{self._date}/{file_name}.txt", "a") as f:
                f.write(output_string + '\n')

    async def _worker(self):
        while True:
            line = await self.queue.get()
            try:
                await self.check(line, self.proxy.get())
            
            except aiohttp.ClientConnectionError:
                self.capture.retries += 1
                await self.queue.put(line)

            except Exception as e:
                logging.error(f'Error processing line: {line} {e}')
                self.capture.retries += 1

                await self.queue.put(line)

            self.queue.task_done()


                
    async def start(self):
        cli.print_title()

        if not self.lines:
            cli.pretty_input('Input folder is empty. Press enter to return')
            return
        
        if self.proxy.count:
            resp = cli.query_option(f'{self.proxy.count} {"proxies" if self.proxy.count > 1  else "proxy"} loaded. Would you like to enable proxies?', ['Enable', 'Disable'])

            if resp == 2:
                self.proxy._proxies.clear()

        cpm_monitor = asyncio.create_task(self.capture.monitor_cpm())

        threads = int(cli.pretty_input('Input number of threads [1-3 proxyless, max 100]'))

        consumers = [asyncio.create_task(self._worker()) for _ in range(threads)]

        for line in self.lines:
            await self.queue.put(line)

        await self.queue.join()

        for consumer in consumers:
            consumer.cancel()


        self.capture.output()
        print()
        cli.pretty_input('Done checking. Press enter to return')
