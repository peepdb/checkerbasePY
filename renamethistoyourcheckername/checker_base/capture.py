import asyncio
from dataclasses import dataclass, field

@dataclass
class CaptureBase:
    line_count: int
    checked: int = 0
    valid: int = 0
    retries: int = 0
    duplicates: int = 0
    cpm: int = 0
    checked_ids: list = field(default_factory=list) #append a unique id to check for duplicates

    @property
    def remaining(self):
        return self.line_count - (self.checked - self.retries)

    async def monitor_cpm(self):
        while True:
            old_checked = self.checked
            await asyncio.sleep(1)
            new_checked = self.checked
            self.cpm = (new_checked - old_checked) * 60
            self.output()
    