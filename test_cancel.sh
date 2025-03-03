#!/bin/bash

# Create an order
echo "Creating order..."
ORDER_RESPONSE=$(curl -s -X POST http://localhost:8003/api/v1/orders/ -H "Content-Type: application/json" -d '{
  "user_id": "aee9b86d-aa75-4fb0-ae5c-3d0e7f9d9710",
  "items": [{"product_id": "76f103dc-7c97-4927-9eab-67ad5d61a308", "quantity": 1}],
  "shipping_address": "101 Elm St, City, Country",
  "billing_address": "101 Elm St, City, Country"
}')

# Extract order ID
ORDER_ID=$(echo $ORDER_RESPONSE | grep -o '"id":"[^"]*' | cut -d'"' -f4)
echo "Order created with ID: $ORDER_ID"

# Wait 1 second
echo "Waiting 1 second..."
sleep 1

# Try to cancel the order
echo "Attempting to cancel order..."
CANCEL_RESPONSE=$(curl -s -X POST http://localhost:8003/api/v1/orders/$ORDER_ID/cancel -H "Content-Type: application/json")
echo "Cancel response: $CANCEL_RESPONSE"

# Wait 5 seconds
echo "Waiting 5 seconds..."
sleep 5

# Check final order status
echo "Checking final order status..."
STATUS_RESPONSE=$(curl -s -X GET http://localhost:8003/api/v1/orders/$ORDER_ID)
echo "Final status: $STATUS_RESPONSE" 