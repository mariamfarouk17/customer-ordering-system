# Customer Ordering System - API Contracts

---

## GET /menu
### Description
Returns menu items grouped by category

### Response (200 OK)
{
  "categories": [
    {
      "name": "Category Name",
      "items": [
        {
          "id": "string",
          "name": "string",
          "price": number,
          "available": true
        }
      ]
    }
  ]
}

---

## POST /cart/items
### Description
Add item to shopping cart

### Request
{
  "item_id": "string",
  "quantity": number
}

### Rules
- quantity must be between 1 and 10
- item must be available

### Response (200 OK)
{
  "status": "success",
  "cart_total": number
}

### Error (400)
{
  "status": "error",
  "message": "Invalid item or quantity"
}

---

## DELETE /cart/items/{item_id}
### Description
Remove item from cart

### Response (200 OK)
{
  "status": "success",
  "cart_total": number
}

### Error (404)
{
  "status": "error",
  "message": "Item not found in cart"
}

---

## POST /orders
### Description
Create new order after validation

### Request
{
  "items": [
    {
      "item_id": "string",
      "quantity": number
    }
  ],
  "order_type": "dine-in | takeaway",
  "table_number": "optional string",
  "delivery_address": "string"
}

### Server Rules
- Stock must be validated at checkout
- Price is calculated on server side
- Cart must not be empty

### Response (200 OK)
{
  "status": "success",
  "order_id": "string"
}

### Errors
400 → invalid input  
409 → cart empty  
422 → stock not available  

---

## POST /payments/checkout
### Description
Process payment (mock system)

### Request
{
  "order_id": "string",
  "payment_method": "cash | mock_card",
  "idempotency_key": "string"
}

### Rules
- duplicate requests with same key must not charge twice

### Response (200 OK)
{
  "status": "success",
  "payment_status": "confirmed"
}

### Error (402)
{
  "status": "error",
  "message": "Payment failed"
}

---

## POST /promo/validate
### Description
Validate promo code

### Request
{
  "code": "string",
  "order_id": "string"
}

### Response (200 OK)
{
  "valid": true,
  "discount": number
}

### Error (429)
{
  "status": "error",
  "message": "Too many attempts"
}

---

## GET /orders/{order_id}
### Description
Track order status

### Response
{
  "order_id": "string",
  "status": "Pending | Confirmed | Cancelled"
}
