# Receipt Processor

A web service that processes receipts and calculates reward points based on specified rules

## Features

### Special Features

- Modular codebase: I understand it's a simple coding challenge, but I still made the code organized into several modules, for the sake of maintainability in a production environment
- Input Validation: Implemented input validation to ensure the quality of receipt inputs. I validated the following:
  - input regex must follow api.yml
  - no duplicated receipts
  - all entries must be present in the receipts, and there cannot be more entries present
  - date must be YYYY-MM-DD, and date+time and cannot be in the future
  - to be a valid receipt, the sum of prices must add up to total
- Data integrity: I used locks to ensure the in-memory data is consistent
- Multi-thread environment:
  - Gunicorn is a Python lib for running the application in a production-like environment.
  - In our case, since we specified in-memory storage, I used only one instance, but with 5 different threads
- Logging: Logs messages whenever the service finishes processing a receipt.
- Error Handling: Consistent error responses with appropriate HTTP status codes.
- Unit Testing: located in the `/tests` folder

### Features to be implemented in the future

- Data Security Related Features:
  - In a production environment we would expect this to be run through HTTPS via Nginx. I did not implement this for the sake of simplicity and ease of testing.
- High Availability:
  - Load Balancing:
    - If we were to not only use in-memory storage, it might be plausible to implement load balancing to ease the traffic from difference sources.
  - Circuit Breakers:
    - If we were to integrate this API with other services, might be plausible to implement circuit breakers in case this service is unavailable.
- Rate Limiting:
  - In a production environment we shall prevent excessive, malicious requests from a single address in a short time. I did not implement, since it might interfere with your testing

## Requirements

- Docker installed on your system
- This application used Python and Flask, but we could follow this Docker setup

## Setup and Running the Application

### Build the Docker Image

```
docker build -t receipt-processor .
```

### Run the container and map to port 8080:

    ```
    docker run -p 8080:8080 receipt-processor
    ```

## Test the API Endpoints

Use curl or any API client to interact with the service:

### Process a Receipt

    ```
    curl -X POST \
    http://localhost:8080/receipts/process \
    -H 'Content-Type: application/json' \
    -d '{
        "retailer": "Target",
        "purchaseDate": "2022-01-01",
        "purchaseTime": "13:01",
        "items": [
        {
            "shortDescription": "Mountain Dew 12PK",
            "price": "6.49"
        }
        ],
        "total": "6.49"
    }'
    ```

Expected Response:
`{
        "id": "receipt-id"
    }
  `

### Get Points for a Receipt

    ```
    curl http://localhost:8080/receipts/<receipt-id>/points
    ```

Expected Response:`{
    "points": <points>
    }`

### Unit Testing

If you want to add your custom unit testing cases, you can do so by accessing the files in `test/`. To run the tests there, simply run it in interactive mode in shell
`docker run -it receipt-processor /bin/sh` (If you're on Windows using Command Prompt, please kindly ensure that the terminal supports interactive Docker commands.)
then run
`python -m unittest discover -s tests`

## File Structure

```
receipt-processor/
├── dockerfile
├── requirements.txt
├── app.py
├── config.py
├── routes.py
├── services.py
├── validators.py
├── calculate.py
├── tests/
│ ├── **init**.py
│ ├── test_calculate.py
│ └── test_validators.py
└── README.md
```

### What each file does

- dockerfile: defines the environment
- requirements.txt: package requirements
- app.py: entry point for the Flask application
- config.py: Though empty now, it can be used in the future if we want to add security keys and seperate the builds between development and production
- routes.py: the routes (endpoints) of the application
- services.py: business logic for processing receipts and calculating points
- validator.py: how we validate the receipt
- calculator.py: how we calculate the points
- tests/: Contains unit tests for the application.
  - test_calculate.py: Unit tests for calculate.py to verify that points are calculated correctly.
  - test_validators.py: Unit tests for validators.py to ensure receipt validation works as expected.
