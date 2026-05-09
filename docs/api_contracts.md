# Customer Ordering System - API Contracts

Base URL: /api

---

## GET /menu
Returns menu grouped by category.

Response 200:
{
  "categories": [
    {
      "name": "Wraps",
      "items": [
        {
          "id": 1,
          "name": "Chicken Shawarma",
          "price": 6.5,
          "available": true
        }
      ]
    }
  ]
}

---

## POST /cart/add
Add item to cart.

Request:
{
  "item_id": 1,
  "quantity": 2
}

Response 200:
{
  "cart_total": 13.0
}

Response 400:
{
  "error": "Item not available"
}

---

## POST /cart/remove
Remove item from cart.

Request:
{
  "item_id": 1
}

Response 200:
{
  "cart_total": 0
}

---

## POST /promo/apply
Apply promo code.

Request:
{
  "code": "SAVE10"
}

Response 200:
{
  "discount": 10,
  "new_total": 11.7
}

Response 400:
{
  "error": "Invalid or expired promo code"
}

---

## POST /checkout
Process order checkout.

Request:
{
  "order_type": "Dine-In",
  "table_number": 5,
  "payment_method": "Mock Card",
  "idempotency_key": "abc123"
}

Response 200:
{
  "order_id": "ORD-00042",
  "status": "Confirmed"
}

Response 402:
{
  "error": "Payment failed"
}

Response 422:
{
  "error": "Stock or price validation failed"
}

---

## GET /order/<order_id>
Get order status.

Response 200:
{
  "order_id": "ORD-00042",
  "status": "Pending",
  "items": []
}

---

## POST /admin/menu
Add new menu item.

Request:
{
  "name": "Falafel Wrap",
  "price": 5.5,
  "category": "Wraps"
}

Response 201:
{
  "message": "Item added"
}

---

## PUT /admin/menu/<id>
Update menu item.

Request:
{
  "price": 6.0,
  "available": false
}

Response 200:
{
  "message": "Updated successfully"
}
