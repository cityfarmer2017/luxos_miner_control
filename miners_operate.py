from datetime import datetime, timezone
from state_machine import curtail, overclock, underclock, normal
import time
import re


INTERVAL: int = 6


ip_pattern = r'^(([1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$'
states = ['overclock', 'normal', 'underclock', 'curtail']


class miners_operator:
    """
    this class is for simulating state transition looping on miners.
    """

    def __init__(self, ips: list):
        self.slot = self.__time_slot()
        match states[self.slot]:
            case 'curtail':
                self.state = curtail(ips)
            case 'overclock':
                self.state = overclock(ips)
            case 'underclock':
                self.state = underclock(ips)
            case 'normal':
                self.state = normal(ips)

    def __del__(self):
        self.state.clear()

    @staticmethod
    def __time_slot() -> int:
        return int(str(datetime.now(timezone.utc))[11:13]) // 6

    def state_loop(self) -> None:
        while True:
            curr_slot = self.__time_slot()
            # curr_slot = (self.slot + 1) % 4
            if self.slot != curr_slot:
                match states[self.slot]:
                    case 'curtail':
                        self.state = self.state.on_event('overclock')
                    case 'overclock':
                        self.state = self.state.on_event('normal')
                    case 'underclock':
                        self.state = self.state.on_event('curtail')
                    case 'normal':
                        self.state = self.state.on_event('underclock')
                self.slot = curr_slot
            else:
                print("Current state: ", self.state.__repr__())

            time.sleep(INTERVAL)


if __name__ == '__main__':
    ips = [s for s in input('Enter ip addresses of miners: ').split()]
    ips[:] = [ip for ip in ips if re.match(ip_pattern, ip)]

    try:
        operator = miners_operator(ips)
        time.sleep(INTERVAL)
        operator.state_loop()
    except KeyboardInterrupt:
        del operator