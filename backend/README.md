# LoveMenu Backend

FastAPI backend for the LoveMenu application.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

API documentation (Swagger UI): `http://localhost:8000/docs`

## Database

The SQLite database file (`lovemenu.db`) will be created automatically on first run.

## API Endpoints

### Dishes
- `GET /api/dishes` - List all dishes
- `GET /api/dishes/{dish_id}` - Get a single dish
- `POST /api/dishes` - Create a new dish
- `PUT /api/dishes/{dish_id}` - Update a dish

### Orders
- `POST /api/orders` - Create a new order
- `GET /api/orders` - Get order history
- `GET /api/orders/active` - Get current active order
- `GET /api/orders/{order_id}` - Get a single order
- `PATCH /api/orders/{order_id}/status` - Update order status


