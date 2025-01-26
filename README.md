# luxos_challenge
This is a project developed to the entry challenge of Luxos.

Please follow the steps listed below to run / test the code:

1. Start a Python3 virual environment in current directory.

    **python3 -m venv venv**

    **source venv/bin/activate**

2. Install modules / packages that will be used in the script.

    **pip install flask requests**

3. Start the app.py (refer to the README of that project for more information).

4. Run ***miners_operate.py***, which is the entry of the application.

    **python3 miners_operate.py**

Hint:

    this script is using UTC time to determine the miners' operating mode, so please don't be surprised if it's not
    consistent to your expectation based on your local time. And based on the time stage within a day, the miners' state
    will change every 6 hours, so if you are not tolerant with the long period between state transition, you can comment
    out the line #37 in ***miners_operate.py***, and uncomment the line following, this action will give you state
    transition every 6 seconds.