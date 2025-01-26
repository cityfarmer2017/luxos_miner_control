from utility import send_request


class state(object):
    """
    This is a state base class which simulate a state machine and provides some utility methods.
    """

    def __init__(self, ips):
        self.ips = ips
        print('Current state: ', str(self))
        # send_request('login', '1.1.1.1')
        print(ips)
        self.__process_states()

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
            data = send_request('login', ip)
            if not data:
                exit(1)
            
            match str(self):
                case 'curtail':
                    send_request('curtail', data['token'], 'active')
                case 'overclock':
                    send_request('curtail', data['token'], 'sleep')
                    send_request('profileset', data['token'], 'overclock')
                case 'underclock':
                    send_request('profileset', data['token'], 'underclock')
                case 'normal':
                    send_request('profileset', data['token'], 'normal')


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