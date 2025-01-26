from datetime import datetime, timezone
from state_machine import curtail, overclock, underclock, normal
import time
import re


INTERVAL: int = 6


ip_pattern = r'^(([1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$'
states = ['overclock', 'normal', 'underclock', 'curtail']


class miners_operator:
    """
    this class is for simulating operations on miners.
    """

    def __init__(self, ips: list):
        self.stage = int(str(datetime.now(timezone.utc))[11:13]) // 6
        match states[self.stage]:
            case 'curtail':
                self.state = curtail(ips)
            case 'overclock':
                self.state = overclock(ips)
            case 'underclock':
                self.state = underclock(ips)
            case 'normal':
                self.state = normal(ips)

    def __del__(self):
        # print("__del__ called!")
        self.state.clear()

    def state_loop(self) -> None:
        while True:
            curr_stage = int(str(datetime.now(timezone.utc))[11:13]) // 6
            # curr_stage = (self.stage + 1) % 4
            if self.stage != curr_stage:
                match states[self.stage]:
                    case 'curtail':
                        self.state = self.state.on_event('overclock')
                    case 'overclock':
                        self.state = self.state.on_event('normal')
                    case 'underclock':
                        self.state = self.state.on_event('curtail')
                    case 'normal':
                        self.state = self.state.on_event('underclock')
                self.stage = curr_stage
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
        # print("Ctrl-C pressed!")
        del operator