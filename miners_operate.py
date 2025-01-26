from datetime import datetime, timezone
from state_machine import curtail, overclock, underclock, normal
import time
import re


ip_pattern = r'^(([1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$'
states = ['overclock', 'normal', 'underclock', 'curtail']


if __name__ == '__main__':
    ips = [s for s in input('Enter ip addresses of miners: ').split()]
    ips[:] = [ip for ip in ips if re.match(ip_pattern, ip)]

    init = int(str(datetime.now(timezone.utc))[11:13]) // 6
    match states[init]:
        case 'curtail':
            state = curtail(ips)
        case 'overclock':
            state = overclock(ips)
        case 'underclock':
            state = underclock(ips)
        case 'normal':
            state = normal(ips)

    time.sleep(6)

    while True:
        curr = int(str(datetime.now(timezone.utc))[11:13]) // 6
        # curr = (init + 1) % 4
        if curr != init:
            match states[init]:
                case 'curtail':
                    state = state.on_event('overclock')
                case 'overclock':
                    state = state.on_event('normal')
                case 'underclock':
                    state = state.on_event('curtail')
                case 'normal':
                    state = state.on_event('underclock')
            init = curr
        else:
            print("Current state: ", state.__repr__())

        time.sleep(6)