from api_request import send


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
            send('logout', ip)
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
            data = send('login', ip)
            if not data:
                exit(1)
            
            match str(self):
                case 'curtail':
                    resp = send('curtail', data['token'], 'active')
                case 'overclock':
                    resp = send('curtail', data['token'], 'sleep')
                    if resp:
                        print(f"{ip}'s " + resp['message'])
                    resp = send('profileset', data['token'], 'overclock')
                case 'underclock':
                    resp = send('profileset', data['token'], 'underclock')
                case 'normal':
                    resp = send('profileset', data['token'], 'normal')
    
            if resp:
                print(f"{ip}'s " + resp['message'])


class curtail(state):
    """
    The state which indicates that the miner should be curtailed
    """

    def on_event(self, event):
        if event == 'overclock':
            return overclock(self.ips)
        
        return self


class overclock(state):
    """
    The state which indicates that the miner should be overclocked
    """

    def on_event(self, event):
        if event == 'normal':
            return normal(self.ips)
        
        return self


class underclock(state):
    """
    The state which indicates that the miner should be underclocked
    """

    def on_event(self, event):
        if event == 'curtail':
            return curtail(self.ips)
        
        return self


class normal(state):
    """
    The state which indicates that the miner should be overclocked
    """

    def on_event(self, event):
        if event == 'underclock':
            return underclock(self.ips)
        
        return self