# Order Matching Application

A high-performance order matching system built with FastAPI and PostgreSQL, containerized with Docker for easy deployment and development.

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- [Docker](https://docs.docker.com/get-docker/) (version 20.10 or higher)
- [Docker Compose](https://docs.docker.com/compose/install/) (version 2.0 or higher)
- [Git](https://git-scm.com/downloads)

## 🛠️ Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/Antony-evm/Order-Book-Matching.git
cd Order-Book-Matching
```

### 2. Start the Application

```bash
# Build and start all services
docker-compose up --build
```

This command will:

- Build the application Docker image using multi-stage build
- Start PostgreSQL database container
- Run database migrations automatically
- Start the Order Matching application

### 3. Verify Installation

Once all services are running, you can access:

- **Health Check**: http://localhost:8080/api/v1/order-book/health
- **Order Book API**: http://localhost:8080/api/v1/order-book/

## 📖 API Endpoints

### Health Check

```http
GET /api/v1/order-book/health
```

Returns the health status of the application.

### Get Open Orders

```http
GET /api/v1/order-book/open?symbol=AAPL&side=BUY&price=150
```

Retrieve open orders with optional filters:

- `symbol` (optional): Filter by stock symbol
- `side` (optional): Filter by order side (`BUY` or `SELL`)
- `price` (optional): Filter by price

### Add Order

Add an order to the order book. If there are orders from the opposite side, at the required price, then the order will automatically fill based on demand. The response indicates how much quantity is left from the order and if it's still an open order.

```http
POST /api/v1/order-book/add
Content-Type: application/json

{
    "symbol": "AAPL",
    "side": "BUY",
    "quantity": 100,
    "price": 150.50
}
```

## 🧪 Testing

### Manual Testing with curl

1. **Health Check**:

```bash
curl http://localhost:8080/api/v1/order-book/health
```

2. **Add a Buy Order**:

```bash
curl -X POST http://localhost:8080/api/v1/order-book/add \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "AAPL",
    "side": "BUY",
    "quantity": 100,
    "price": 15050
  }'
```

3. **Get Open Orders**:

```bash
curl http://localhost:8080/api/v1/order-book/open
```

4. **Add a Sell Order**:

```bash
curl -X POST http://localhost:8080/api/v1/order-book/add \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "AAPL",
    "side": "SELL",
    "quantity": 50,
    "price": 15050
  }'
```

5. **Get Open Orders**:

```bash
curl http://localhost:8080/api/v1/order-book/open
```

### Running Unit Tests

If you want to run the test suite, ensure you have poetry installed and a TEST_DATABASE_URL in your .env

```
poetry run pytest
```
