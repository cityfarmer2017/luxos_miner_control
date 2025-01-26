import api_request


class state(object):
    """
    This is a state base class which will be inherited by sub-classes to simulate a state machine,
    and provides some utility methods.
    """

    def __init__(self, ips: list):
        self.ips = ips
        self.__process_states()

    def clear(self):
        for ip in self.ips:
            api_request.send('logout', ip)
        self.ips.clear()

    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        return self.__class__.__name__
    
    def on_event(self, event):
        """
        Handle events that are delegated to this state.
        """
        pass

    def __process_states(self) -> None:
        for ip in self.ips:
            data = api_request.send('login', ip)
            if not data:
                print(f'longin failed for {ip}!!!')
                exit(1)

            print(f"Miner {ip} is operating in {str(self)} mode:")

            match str(self):
                case 'curtail':
                    resp = api_request.send('curtail', data['token'], 'active')
                case 'overclock':
                    resp = api_request.send('curtail', data['token'], 'sleep')
                    if resp:
                        print('\t' + resp['message'])
                    resp = api_request.send('profileset', data['token'], 'overclock')
                case 'underclock':
                    resp = api_request.send('profileset', data['token'], 'underclock')
                case 'normal':
                    resp = api_request.send('profileset', data['token'], 'normal')
    
            if resp:
                print('\t' + resp['message'])


class curtail(state):
    """
    The state which indicates that the miner should be curtailed
    """

    def on_event(self, event):
        return overclock(self.ips) if event == 'overclock' else self


class overclock(state):
    """
    The state which indicates that the miner should be overclocked
    """

    def on_event(self, event):
        return normal(self.ips) if event == 'normal' else self


class underclock(state):
    """
    The state which indicates that the miner should be underclocked
    """

    def on_event(self, event):
        return curtail(self.ips) if event == 'curtail' else self


class normal(state):
    """
    The state which indicates that the miner should be overclocked
    """

    def on_event(self, event):
        return underclock(self.ips) if event == 'underclock' else self