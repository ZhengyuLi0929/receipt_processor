# Receipt Processor

A web service that processes receipts and calculates reward points based on specified rules

## Requirements

- Docker installed on your system
- This application used Python and Flask, but following this Docker setup should be fine for the requirement

## Setup and Running the Application

### Build the Docker Image

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/receipt_processor.git
   cd receipt_processor
   ```

2. Build the Docker image:

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

### What each file do

- dockerfile: defines the environment
- requirements.txt: package requirements
- app.py: entry point for the Flask application
- config.py: Contains configuration classes (Config, DevelopmentConfig, ProductionConfig) that define different settings for the application based on the environment
- routes.py: the routes (endpoints) of the application
- services.py: business logic for processing receipts and calculating points
- validator.py: how we validate the receipt
- calculator.py: how we calculate the points
- tests/: Contains unit tests for the application.
  - test_calculate.py: Unit tests for calculate.py to verify that points are calculated correctly.
  - test_validators.py: Unit tests for validators.py to ensure receipt validation works as expected.

## Special Features

- Modular codebase: I understand it's a simple coding challenge, but I still made the code organized into several modules, for the sake of maintainability in a production environment
- Input Validation: Implemented input validation to ensure the quality of receipt inputs
- Data integrity: I used locks to ensure the in-memory data is consistent
- Multi-thread environment: Gunicorn is a Python lib for running the application in a production-like environment.
  In our case, since we specified in-memory storage, I used only one instance, but with 5 different threads
- Logging: Logging features, though commented out, is available for my peers to review the code if it does not meet their expectations
- Error Handling: Consistent error responses with appropriate HTTP status codes.
- Unit Testing: located in the `/tests` folder

## Unimplemented features

- Data Security: In a production environment you would expect this to be run through HTTPS via Nginx. I did not implement this for the sake of simplicity and testing ease.
- High Availability:
  - Load Balancing:
    - Distributing incoming traffic across multiple servers to optimize resource use, maximize throughput, reduce latency, and ensure reliability.
  - Circuit Breakers:
    - Implementing patterns to detect when a service is failing and prevent repeated attempts that are likely to fail, thereby avoiding cascading failures.
- Rate Limiting: Did not implement, since it might interfere with your testing
