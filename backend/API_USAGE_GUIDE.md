# API Usage Guide

Complete guide to using the Fashion Virtual Try-On API endpoints.

## Table of Contents
1. [Authentication](#authentication)
2. [Products](#products)
3. [Affiliate Links](#affiliate-links)
4. [Virtual Try-On](#virtual-try-on)
5. [Pose Transfer](#pose-transfer)
6. [Recommendations](#recommendations)
7. [Admin Panel](#admin-panel)
8. [Error Handling](#error-handling)

---

## Authentication

### Register New User

**Endpoint:** `POST /auth/register`

```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newuser@example.com",
    "username": "newuser",
    "password": "StrongPassword123!",
    "full_name": "New User"
  }'
```

**Response:**
```json
{
  "id": 1,
  "email": "newuser@example.com",
  "username": "newuser",
  "full_name": "New User",
  "role": "user",
  "is_active": true,
  "is_verified": false,
  "avatar_url": null,
  "body_type": null,
  "skin_tone": null,
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

### Login

**Endpoint:** `POST /auth/login`

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newuser@example.com",
    "password": "StrongPassword123!"
  }'
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

**Note:** Use `access_token` for all subsequent authenticated requests:
```bash
-H "Authorization: Bearer {access_token}"
```

### Refresh Token

**Endpoint:** `POST /auth/refresh`

```bash
curl -X POST "http://localhost:8000/auth/refresh" \
  -H "Content-Type: application/json" \
  -d '{
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }'
```

### Get Current User

**Endpoint:** `GET /auth/me`

```bash
curl -X GET "http://localhost:8000/auth/me" \
  -H "Authorization: Bearer {access_token}"
```

### Update Profile

**Endpoint:** `PUT /auth/me`

```bash
curl -X PUT "http://localhost:8000/auth/me" \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Updated Name",
    "avatar_url": "https://example.com/avatar.jpg",
    "body_type": "hourglass",
    "skin_tone": "warm"
  }'
```

---

## Products

### Create Product (Admin/Content Manager)

**Endpoint:** `POST /products/`

```bash
curl -X POST "http://localhost:8000/products/" \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Navy Blue Blazer",
    "brand": "ProStyle",
    "category": "outerwear",
    "subcategory": "blazers",
    "price": 149.99,
    "currency": "INR",
    "image_url": "https://example.com/blazer.jpg",
    "mask_url": "https://example.com/blazer_mask.jpg",
    "description": "Professional navy blue blazer",
    "color": "navy",
    "pattern": "solid",
    "fabric_type": "wool",
    "tags": ["formal", "professional", "office"],
    "size_guide": {
      "XS": {"bust": 32, "length": 24},
      "S": {"bust": 34, "length": 25},
      "M": {"bust": 36, "length": 26}
    }
  }'
```

### List Products

**Endpoint:** `GET /products/`

```bash
# Basic list
curl -X GET "http://localhost:8000/products/" \
  -H "Authorization: Bearer {access_token}"

# With filters
curl -X GET "http://localhost:8000/products/?skip=0&limit=20&category=tops&brand=StyleCo&search=shirt&min_price=20&max_price=100" \
  -H "Authorization: Bearer {access_token}"
```

**Query Parameters:**
- `skip` (int): Pagination offset (default: 0)
- `limit` (int): Items per page (default: 50, max: 100)
- `category` (str): Filter by category
- `brand` (str): Filter by brand
- `search` (str): Search in name/description
- `min_price` (float): Minimum price
- `max_price` (float): Maximum price

### Get Product Details

**Endpoint:** `GET /products/{product_id}`

```bash
curl -X GET "http://localhost:8000/products/1" \
  -H "Authorization: Bearer {access_token}"
```

### Update Product

**Endpoint:** `PUT /products/{product_id}`

```bash
curl -X PUT "http://localhost:8000/products/1" \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "price": 139.99,
    "tags": ["formal", "professional", "office", "sale"]
  }'
```

### Delete Product

**Endpoint:** `DELETE /products/{product_id}`

```bash
curl -X DELETE "http://localhost:8000/products/1" \
  -H "Authorization: Bearer {access_token}"
```

### Get Products by Category

**Endpoint:** `GET /products/category/{category}`

```bash
curl -X GET "http://localhost:8000/products/category/dresses?limit=50" \
  -H "Authorization: Bearer {access_token}"
```

### Search Products

**Endpoint:** `GET /products/search/{query_text}`

```bash
curl -X GET "http://localhost:8000/products/search/blue%20shirt?limit=50" \
  -H "Authorization: Bearer {access_token}"
```

---

## Affiliate Links

### Create Affiliate Link

**Endpoint:** `POST /affiliate/links`

```bash
curl -X POST "http://localhost:8000/affiliate/links" \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "platform": "amazon",
    "affiliate_url": "https://amazon.in/dp/B123456789?tag=myaffiliate",
    "product_sku": "AMAZ-123456",
    "commission_rate": 5.0
  }'
```

### Get Affiliate Links for Product

**Endpoint:** `GET /affiliate/product/{product_id}`

```bash
curl -X GET "http://localhost:8000/affiliate/product/1" \
  -H "Authorization: Bearer {access_token}"
```

### Get Links by Platform

**Endpoint:** `GET /affiliate/platform/{platform}`

```bash
curl -X GET "http://localhost:8000/affiliate/platform/myntra?limit=100" \
  -H "Authorization: Bearer {access_token}"
```

**Supported Platforms:** amazon, myntra, meesho, ajio, flipkart

### List All Platforms

**Endpoint:** `GET /affiliate/platforms/`

```bash
curl -X GET "http://localhost:8000/affiliate/platforms/" \
  -H "Authorization: Bearer {access_token}"
```

### Bulk Create Affiliate Links

**Endpoint:** `POST /affiliate/bulk-create`

```bash
curl -X POST "http://localhost:8000/affiliate/bulk-create" \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d '[
    {
      "product_id": 1,
      "platform": "amazon",
      "affiliate_url": "https://amazon.in/dp/B123456789",
      "commission_rate": 5.0
    },
    {
      "product_id": 1,
      "platform": "myntra",
      "affiliate_url": "https://myntra.com/product/123",
      "commission_rate": 3.0
    }
  ]'
```

---

## Virtual Try-On

### Run Virtual Try-On

**Endpoint:** `POST /tryon/run`

```bash
curl -X POST "http://localhost:8000/tryon/run" \
  -H "Authorization: Bearer {access_token}" \
  -F "product_id=1" \
  -F "avatar_image=@/path/to/avatar.jpg"
```

**Form Parameters:**
- `product_id` (int): Product to try on (required)
- `avatar_image` (file): User's photo (required)
- `target_pose` (dict, optional): Target pose keypoints
- `body_shape` (str, optional): Body type

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "product_id": 1,
  "result_image_url": "data:image/png;base64,iVBORw0KGgoAAAANS...",
  "confidence_score": 0.85,
  "metadata": {
    "model_type": "hr-vton",
    "body_shape": null,
    "garment_type": "tops",
    "execution_time_ms": 1200
  },
  "created_at": "2024-01-15T10:30:00"
}
```

### Get Try-On Result

**Endpoint:** `GET /tryon/results/{tryon_id}`

```bash
curl -X GET "http://localhost:8000/tryon/results/1" \
  -H "Authorization: Bearer {access_token}"
```

### Get User's Try-On Results

**Endpoint:** `GET /tryon/my-results`

```bash
curl -X GET "http://localhost:8000/tryon/my-results?skip=0&limit=20" \
  -H "Authorization: Bearer {access_token}"
```

---

## Pose Transfer

### Run Pose Transfer

**Endpoint:** `POST /pose-transfer/run`

```bash
# Create target pose JSON
TARGET_POSE='{
  "keypoints": [[100, 50], [150, 60], [200, 100], ...],
  "confidence": [0.9, 0.85, 0.88, ...]
}'

curl -X POST "http://localhost:8000/pose-transfer/run" \
  -H "Authorization: Bearer {access_token}" \
  -F "source_image=@/path/to/person.jpg" \
  -F "target_pose=$TARGET_POSE"
```

### Get Pose Transfer Result

**Endpoint:** `GET /pose-transfer/results/{transfer_id}`

```bash
curl -X GET "http://localhost:8000/pose-transfer/results/1" \
  -H "Authorization: Bearer {access_token}"
```

### Get User's Pose Transfer Results

**Endpoint:** `GET /pose-transfer/my-results`

```bash
curl -X GET "http://localhost:8000/pose-transfer/my-results?skip=0&limit=20" \
  -H "Authorization: Bearer {access_token}"
```

---

## Recommendations

### Get Outfit Recommendations

**Endpoint:** `POST /recommendation/outfits`

```bash
# Generic recommendations
curl -X POST "http://localhost:8000/recommendation/outfits?top_k=10" \
  -H "Authorization: Bearer {access_token}"

# Recommendations based on a product
curl -X POST "http://localhost:8000/recommendation/outfits?base_product_id=1&top_k=15" \
  -H "Authorization: Bearer {access_token}"
```

**Query Parameters:**
- `base_product_id` (int, optional): Product to base recommendations on
- `top_k` (int): Number of recommendations (default: 10, max: 50)

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "recommendations": [
    {
      "product_id": 2,
      "product_name": "White Shirt",
      "brand": "StyleCo",
      "image_url": "https://example.com/shirt.jpg",
      "similarity_score": 0.92,
      "price": 34.99,
      "reason": "Similar to Blue T-Shirt"
    },
    ...
  ],
  "created_at": "2024-01-15T10:30:00"
}
```

### Get Similar Products

**Endpoint:** `GET /recommendation/similar/{product_id}`

```bash
curl -X GET "http://localhost:8000/recommendation/similar/1?top_k=10" \
  -H "Authorization: Bearer {access_token}"
```

### Get Trending Outfits

**Endpoint:** `GET /recommendation/trending`

```bash
curl -X GET "http://localhost:8000/recommendation/trending?limit=20"
```

### Get Personalized Recommendations

**Endpoint:** `POST /recommendation/personalized`

```bash
curl -X POST "http://localhost:8000/recommendation/personalized" \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "filters": {
      "category": "dresses",
      "min_price": 50,
      "max_price": 200,
      "color": "blue"
    }
  }'
```

---

## Admin Panel

### Get Dashboard Statistics

**Endpoint:** `GET /admin/stats`

```bash
curl -X GET "http://localhost:8000/admin/stats" \
  -H "Authorization: Bearer {admin_access_token}"
```

### List Users

**Endpoint:** `GET /admin/users`

```bash
curl -X GET "http://localhost:8000/admin/users?skip=0&limit=50&role=user&is_active=true" \
  -H "Authorization: Bearer {admin_access_token}"
```

### Get User Details

**Endpoint:** `GET /admin/users/{user_id}`

```bash
curl -X GET "http://localhost:8000/admin/users/1" \
  -H "Authorization: Bearer {admin_access_token}"
```

### Update User Role

**Endpoint:** `PUT /admin/users/{user_id}/role`

```bash
curl -X PUT "http://localhost:8000/admin/users/1/role" \
  -H "Authorization: Bearer {admin_access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "new_role": "content_manager"
  }'
```

**Valid Roles:** super_admin, affiliate_manager, content_manager, ai_manager, viewer, user

### Deactivate User

**Endpoint:** `POST /admin/users/{user_id}/deactivate`

```bash
curl -X POST "http://localhost:8000/admin/users/1/deactivate" \
  -H "Authorization: Bearer {admin_access_token}"
```

### Activate User

**Endpoint:** `POST /admin/users/{user_id}/activate`

```bash
curl -X POST "http://localhost:8000/admin/users/1/activate" \
  -H "Authorization: Bearer {admin_access_token}"
```

### Get Activity Log

**Endpoint:** `GET /admin/activity-log`

```bash
curl -X GET "http://localhost:8000/admin/activity-log?skip=0&limit=100" \
  -H "Authorization: Bearer {admin_access_token}"
```

### Get Recommendation Metrics

**Endpoint:** `GET /admin/recommendation-metrics`

```bash
curl -X GET "http://localhost:8000/admin/recommendation-metrics" \
  -H "Authorization: Bearer {admin_access_token}"
```

---

## Error Handling

### Common Status Codes

- `200 OK` - Success
- `201 Created` - Resource created
- `204 No Content` - Success (no response body)
- `400 Bad Request` - Invalid input
- `401 Unauthorized` - Missing/invalid token
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

### Error Response Format

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Example Error

```bash
curl -X POST "http://localhost:8000/products/" \
  -H "Authorization: Bearer {invalid_token}" \
  -H "Content-Type: application/json" \
  -d '{"name": "Test"}'

# Response (401):
{
  "detail": "Could not validate credentials"
}
```

---

## Best Practices

1. **Always use HTTPS in production**
2. **Keep tokens secure** - don't expose in logs
3. **Implement rate limiting** on client side
4. **Handle token expiration** - refresh before it expires
5. **Validate image formats** before uploading
6. **Use appropriate roles** for admin operations
7. **Cache product data** client-side when possible
8. **Implement proper error handling** in your client

---

## Rate Limiting

Currently no rate limiting is enforced. For production:

```python
# Add to main.py
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
```

---

## WebSocket Support (Future)

For real-time try-on preview:

```javascript
// Client-side (future)
const ws = new WebSocket('ws://localhost:8000/ws/tryon');
ws.onmessage = (event) => {
  const result = JSON.parse(event.data);
  updatePreview(result.image);
};
```

---

## Testing with Python Requests

```python
import requests

BASE_URL = "http://localhost:8000"

# Register
resp = requests.post(f"{BASE_URL}/auth/register", json={
    "email": "test@example.com",
    "username": "testuser",
    "password": "pass123456"
})
print(resp.json())

# Login
resp = requests.post(f"{BASE_URL}/auth/login", json={
    "email": "test@example.com",
    "password": "pass123456"
})
token = resp.json()["access_token"]

# Get recommendations
headers = {"Authorization": f"Bearer {token}"}
resp = requests.post(f"{BASE_URL}/recommendation/outfits", headers=headers)
print(resp.json())
```

---

## Support

For issues or questions:
1. Check API docs: `/docs`
2. Review this guide
3. Check server logs
4. Verify authentication tokens
5. Ensure all required fields are provided

