# API Documentation

## Base URL
```
http://localhost:8000/api/
```

## Authentication

All API endpoints (except login/register) require JWT authentication. Include the token in the Authorization header:

```
Authorization: Bearer <access_token>
```

---

## Authentication Endpoints

### 1. Login (Obtain Token)

**Endpoint:** `POST /api/token/`

**Description:** Authenticate user and receive JWT access and refresh tokens.

**Request Body:**
```json
{
  "username": "admin",
  "password": "password123"
}
```

**Response (200 OK):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "role": "admin",
  "user_id": 1
}
```

**Error Response (401 Unauthorized):**
```json
{
  "detail": "No active account found with the given credentials"
}
```

---

### 2. Refresh Token

**Endpoint:** `POST /api/token/refresh/`

**Description:** Get a new access token using refresh token.

**Request Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response (200 OK):**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

### 3. Register User

**Endpoint:** `POST /api/register/`

**Description:** Register a new user (Admin only in production).

**Request Body:**
```json
{
  "username": "newuser",
  "password": "password123",
  "email": "user@example.com",
  "role": "staff"
}
```

**Response (201 Created):**
```json
{
  "message": "User created successfully",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "role": "staff",
  "user_id": 2
}
```

---

## Prescription Endpoints

### 4. Upload Prescription

**Endpoint:** `POST /api/prescriptions/upload/`

**Description:** Upload a prescription image/PDF and process it with OCR and AI.

**Authentication:** Required

**Content-Type:** `multipart/form-data`

**Request Body:**
- `file` (file): Prescription image (jpg, jpeg, png) or PDF

**Response (201 Created):**
```json
{
  "prescription_id": 1,
  "extracted_text": "Dr. John Doe\nParacetamol 500mg\nAmoxicillin 250mg\n...",
  "medicines_found": ["Paracetamol 500mg", "Amoxicillin 250mg"],
  "results": [
    {
      "medicine_name": "Paracetamol 500mg",
      "status": "Available",
      "stock": 150,
      "alternative": null
    },
    {
      "medicine_name": "Amoxicillin 250mg",
      "status": "Out of Stock",
      "stock": 0,
      "alternative": {
        "name": "Azithromycin 500mg",
        "stock": 60
      }
    }
  ]
}
```

**Error Response (400 Bad Request):**
```json
{
  "error": "Invalid file type. Allowed: jpg, jpeg, png, pdf"
}
```

**Error Response (500 Internal Server Error):**
```json
{
  "error": "Error processing prescription: OCR failed"
}
```

---

### 5. Get Prescription History

**Endpoint:** `GET /api/prescriptions/history/`

**Description:** Get all prescriptions uploaded by the authenticated user.

**Authentication:** Required

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "file_url": "/media/prescriptions/2026/02/16/prescription_1.pdf",
    "created_at": "2026-02-16T10:30:00Z",
    "results_count": 3
  },
  {
    "id": 2,
    "file_url": "/media/prescriptions/2026/02/16/prescription_2.jpg",
    "created_at": "2026-02-16T09:15:00Z",
    "results_count": 2
  }
]
```

---

## Medicine Endpoints

### 6. List All Medicines

**Endpoint:** `GET /api/medicines/`

**Description:** Get all medicines in inventory.

**Authentication:** Required (Admin only)

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Paracetamol 500mg",
    "composition": "Paracetamol",
    "stock_quantity": 150,
    "manufacturer": "ABC Pharmaceuticals",
    "created_at": "2026-02-16T08:00:00Z"
  },
  {
    "id": 2,
    "name": "Amoxicillin 250mg",
    "composition": "Amoxicillin",
    "stock_quantity": 80,
    "manufacturer": "XYZ Pharma Ltd",
    "created_at": "2026-02-16T08:00:00Z"
  }
]
```

**Error Response (403 Forbidden):**
```json
{
  "error": "Admin access required"
}
```

---

### 7. Create Medicine

**Endpoint:** `POST /api/medicines/`

**Description:** Add a new medicine to inventory.

**Authentication:** Required (Admin only)

**Request Body:**
```json
{
  "name": "Ibuprofen 400mg",
  "composition": "Ibuprofen",
  "stock_quantity": 100,
  "manufacturer": "ABC Pharmaceuticals"
}
```

**Response (201 Created):**
```json
{
  "id": 3,
  "name": "Ibuprofen 400mg",
  "composition": "Ibuprofen",
  "stock_quantity": 100,
  "manufacturer": "ABC Pharmaceuticals"
}
```

**Error Response (400 Bad Request):**
```json
{
  "error": "Medicine name is required"
}
```

---

### 8. Get Medicine Details

**Endpoint:** `GET /api/medicines/{id}/`

**Description:** Get details of a specific medicine.

**Authentication:** Required (Admin only)

**Response (200 OK):**
```json
{
  "id": 1,
  "name": "Paracetamol 500mg",
  "composition": "Paracetamol",
  "stock_quantity": 150,
  "manufacturer": "ABC Pharmaceuticals"
}
```

**Error Response (404 Not Found):**
```json
{
  "error": "Medicine not found"
}
```

---

### 9. Update Medicine

**Endpoint:** `PUT /api/medicines/{id}/`

**Description:** Update medicine information.

**Authentication:** Required (Admin only)

**Request Body:**
```json
{
  "name": "Paracetamol 500mg",
  "composition": "Paracetamol",
  "stock_quantity": 200,
  "manufacturer": "ABC Pharmaceuticals"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "name": "Paracetamol 500mg",
  "composition": "Paracetamol",
  "stock_quantity": 200,
  "manufacturer": "ABC Pharmaceuticals"
}
```

---

### 10. Delete Medicine

**Endpoint:** `DELETE /api/medicines/{id}/`

**Description:** Delete a medicine from inventory.

**Authentication:** Required (Admin only)

**Response (200 OK):**
```json
{
  "message": "Medicine deleted successfully"
}
```

---

### 11. Search Medicines

**Endpoint:** `GET /api/medicines/search/?q={query}`

**Description:** Search medicines by name, composition, or manufacturer.

**Authentication:** Required

**Query Parameters:**
- `q` (required): Search query string

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Paracetamol 500mg",
    "composition": "Paracetamol",
    "stock_quantity": 150,
    "manufacturer": "ABC Pharmaceuticals",
    "is_available": true
  }
]
```

**Error Response (400 Bad Request):**
```json
{
  "error": "Query parameter \"q\" is required"
}
```

---

## Example API Usage

### Using cURL

```bash
# 1. Login and get token
TOKEN=$(curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"password123"}' \
  | jq -r '.access')

# 2. Upload prescription
curl -X POST http://localhost:8000/api/prescriptions/upload/ \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@prescription.jpg"

# 3. Get all medicines
curl -X GET http://localhost:8000/api/medicines/ \
  -H "Authorization: Bearer $TOKEN"

# 4. Search medicines
curl -X GET "http://localhost:8000/api/medicines/search/?q=paracetamol" \
  -H "Authorization: Bearer $TOKEN"
```

### Using Python Requests

```python
import requests

BASE_URL = "http://localhost:8000/api"

# Login
response = requests.post(f"{BASE_URL}/token/", json={
    "username": "admin",
    "password": "password123"
})
token = response.json()["access"]

# Upload prescription
headers = {"Authorization": f"Bearer {token}"}
with open("prescription.jpg", "rb") as f:
    files = {"file": f}
    response = requests.post(
        f"{BASE_URL}/prescriptions/upload/",
        headers=headers,
        files=files
    )
    print(response.json())

# Get medicines
response = requests.get(
    f"{BASE_URL}/medicines/",
    headers=headers
)
print(response.json())
```

### Using JavaScript Fetch

```javascript
const BASE_URL = 'http://localhost:8000/api';

// Login
const loginResponse = await fetch(`${BASE_URL}/token/`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    username: 'admin',
    password: 'password123'
  })
});
const { access } = await loginResponse.json();

// Upload prescription
const formData = new FormData();
formData.append('file', fileInput.files[0]);

const uploadResponse = await fetch(`${BASE_URL}/prescriptions/upload/`, {
  method: 'POST',
  headers: { 'Authorization': `Bearer ${access}` },
  body: formData
});
const result = await uploadResponse.json();
console.log(result);
```

---

## Error Codes

| Status Code | Description |
|------------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request - Invalid input |
| 401 | Unauthorized - Missing or invalid token |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource doesn't exist |
| 500 | Internal Server Error - Server error |

---

## Rate Limiting

Currently, there are no rate limits implemented. In production, consider implementing rate limiting for API endpoints.

---

## Notes

- All timestamps are in ISO 8601 format (UTC)
- File uploads are limited to 10MB
- Supported image formats: JPG, JPEG, PNG
- Supported document formats: PDF
- JWT tokens expire after 1 hour (access) and 7 days (refresh)
