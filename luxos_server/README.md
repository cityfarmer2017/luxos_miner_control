# LuxOS Miner Control Application Challenge

You're tasked with developing a control application for managing the operation of a fleet of miners. The miner can operate in different modes based on the time of day. Your application should interact with an API that provides endpoints to control the mining fleet operation.

## Requirements

- Develop an application (preferrably in Python but any coding language is acceptable) that interfaces with the provided API.
- The application should schedule different miner modes based on the time of day, as follows:
  - From 00:00 to 06:00, the miner should be overclocked.
  - From 06:00 to 12:00, the miner should operate in normal mode.
  - From 12:00 to 18:00, the miner should be underclocked.
  - From 18:00 to midnight, the miner should be curtailed.
- The application should be able to control several miners at the same time while keeping state of its actions.

## Bonus Points

- Test your application thoroughly to ensure that it behaves as expected under different scenarios.
- Document your code and provide clear instructions on how to run and test the application.

## Additional Notes

- You can assume that the Miner Control API provides endpoints for setting the miner's operation mode (overclock, normal, underclock, curtail) and requires authentication using a token.
- Write a README.md file that explains how to run the application and any other relevant information.

## Evaluation Criteria:

- Correctness and completeness of the solution.
- Robustness of error handling and edge case handling.
- Clarity and organization of the code.
- Quality and thoroughness of testing.
- Effectiveness of documentation and instructions.

## API Help

1. Login

```
curl -X POST -H "Content-Type: application/json" -d '{"miner_ip": ""}' http://localhost:5000/api/login
```

Params:

- ip: IP address of the miner

2. Logout

```
curl -X POST -H "Content-Type: application/json" -d '{"miner_ip": ""}' http://localhost:5000/api/logout
```

Params:

- ip: IP address of the miner

3. Curtail

```
curl -X POST -H "Content-Type: application/json" -d '{"token": "token", "mode": ""}' http://localhost:5000/api/curtail
```

Params

- token as retrieved from login
- mode: sleep or active

4. Profileset

```
curl -X POST -H "Content-Type: application/json" -d '{"token": "", "profile": ""}' http://localhost:5000/api/profileset
```

Params

- token as retrieved from login
- profile: underclock, overclock, normal
