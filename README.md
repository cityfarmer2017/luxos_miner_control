# luxos_challenge
This is a project developed to the entry challenge of Luxos.

Please follow the steps listed below to run / test the code:

1. Start a Python3 virual environment in current directory.

    **python3 -m venv venv**

    **source venv/bin/activate**

2. Install modules / packages that will be used in the script.

    **pip install flask requests**

3. Start the ***app.py*** (refer to the README of that project for more information).

    **cd luxos_server**

    **python3 app.py**

4. Run ***miners_operate.py*** in a different shell, which is the entry of the application.

    - Run in normal mode, in which the miner state will transition every 6 hours.

        **python3 miners_operate.py**

    - Run in debug mode, in which the miner state will transition every 6 seconds.

        **python3 miners_operate.py --debug**

5. The code is now running as a state machine of a endless loop, you need to press ***ctrl-c*** to stop it.

Some extra information:

The script will first ask for your input the IPv4 addresses of miners, so please enter space seperated IPv4 strings,
and the invalid IPv4 string will be filtered out automaticly, please keep this in mind in case of your surprize.

This script is using UTC time to determine the miners' operating mode, so please don't be surprised if it's not
consistent to your expectation based on your local time.

BTW, I thinks there is a issue in api.py, that a minser's state and profile storage should also be cleared when it
gets logged out.