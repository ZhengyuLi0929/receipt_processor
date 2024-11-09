# Receipt Processor

A web service that processes receipts and calculates reward points based on specified rules.

## Requirements

- Docker installed on your system.

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
   Run the Docker Container

   ```

### Run the container and map port 8080:

    ```
    docker run -p 8080:8080 receipt-processor
    ```

## Test the API Endpoints

Use curl or any API client to interact with the service.

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
`    {
        "id": "your-generated-receipt-id"
    }
   `

### Get Points for a Receipt

    ```
    curl http://localhost:8080/receipts/<your-generated-receipt-id>/points
    ```

    Expected Response:

    ```
    {
    "points": <calculated-points>
    }
    ```

## Additional Notes

The application uses in-memory storage; data will not persist if the container is stopped or restarted.
Ensure that port 8080 is not being used by another application on your host machine.
