# Fashion Virtual Try-On API Backend

Complete Python FastAPI backend with AI pipeline for fashion virtual try-on, pose transfer, and outfit recommendations.

## Features

✅ **Authentication & Authorization**
- JWT-based authentication with access/refresh tokens
- Role-Based Access Control (RBAC) with 6 user roles
- User registration and login

✅ **Virtual Try-On (2D)**
- HR-VTON or CP-VTON model support
- Body pose estimation (OpenPose/MediaPipe)
- Clothing segmentation
- Garment warping to body shape
- Seamless blending

✅ **Pose Transfer**
- PG2 or HR-VTON-Pose models
- Human pose extraction and transfer
- Skeleton visualization

✅ **AI Recommendation Engine**
- CLIP embeddings for fashion items
- KNN similarity search
- Fashion rules (color harmony, category compatibility)
- Body-type-based recommendations
- Personalized outfit suggestions

✅ **Product Management**
- CRUD operations for fashion items
- Filtering by category, brand, price
- Search functionality

✅ **Affiliate Integration**
- Support for Amazon, Myntra, Meesho, Ajio, Flipkart
- Bulk link management
- Commission tracking

✅ **Admin Panel**
- User management
- Dashboard statistics
- Activity monitoring
- Role management

## Project Structure

```
backend/
├── main.py                 # FastAPI entry point
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
│
├── core/
│   ├── config.py          # Settings & configuration
│   ├── security.py        # JWT & RBAC
│   ├── db.py              # Database setup
│   └── __init__.py
│
├── schemas/
│   ├── base.py            # SQLAlchemy ORM models
│   ├── models.py          # Pydantic request/response models
│   └── __init__.py
│
├── services/
│   ├── auth_service.py         # Authentication logic
│   ├── product_service.py      # Product CRUD
│   ├── affiliate_service.py    # Affiliate management
│   ├── vton_service.py         # Virtual try-on
│   ├── pose_transfer_service.py # Pose transfer
│   ├── reco_engine.py          # Recommendation engine
│   └── __init__.py
│
├── api/
│   ├── auth/              # Authentication routes
│   ├── products/          # Product routes
│   ├── affiliate/         # Affiliate routes
│   ├── tryon/            # Try-on routes
│   ├── pose_transfer/    # Pose transfer routes
│   ├── recommendation/   # Recommendation routes
│   ├── admin/            # Admin panel routes
│   └── users/
│
├── ml_models/
│   ├── hr_vton/          # HR-VTON model (stub)
│   ├── pg2/              # PG2 model (stub)
│   └── openpose/         # OpenPose model (stub)
│
└── static/
    ├── avatars/          # User avatar uploads
    ├── inputs/           # Input images
    └── outputs/          # Generated images
```

## Installation

### Prerequisites
- Python 3.9+
- Virtual Environment (recommended)
- GPU support optional (CUDA 11.8+)

### Setup Steps

1. **Clone/Navigate to backend directory**
```bash
cd backend
```

2. **Create virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup environment variables**
```bash
# Copy example to .env
cp .env.example .env

# Edit .env with your settings
```

5. **Initialize database** (automatic on first run)
Database initializes automatically when you start the server.

## Running the Server

### Development Mode
```bash
uvicorn main:app --reload
```

Server runs at: `http://localhost:8000`

### Production Mode
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000
```

## API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health
- **API Info**: http://localhost:8000/api/v1/info

## Authentication

### Register
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "username",
    "password": "securepass123",
    "full_name": "Full Name"
  }'
```

### Login
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepass123"
  }'
```

Response includes access_token - use for all protected routes:
```bash
Authorization: Bearer {access_token}
```

## Main API Endpoints

### Products
- `POST /products/` - Create product (Admin)
- `GET /products/` - List products with filters
- `GET /products/{id}` - Get product details
- `PUT /products/{id}` - Update product
- `DELETE /products/{id}` - Delete product
- `GET /products/category/{category}` - Products by category
- `GET /products/search/{query}` - Search products

### Affiliate Links
- `POST /affiliate/links` - Create affiliate link
- `GET /affiliate/links/{id}` - Get link details
- `GET /affiliate/product/{product_id}` - Get links for product
- `GET /affiliate/platform/{platform}` - Links by platform
- `PUT /affiliate/links/{id}` - Update link
- `DELETE /affiliate/links/{id}` - Delete link
- `POST /affiliate/bulk-create` - Bulk create links

### Virtual Try-On
- `POST /tryon/run` - Run try-on
- `GET /tryon/results/{id}` - Get result
- `GET /tryon/my-results` - User's results

### Pose Transfer
- `POST /pose-transfer/run` - Transfer pose
- `GET /pose-transfer/results/{id}` - Get result
- `GET /pose-transfer/my-results` - User's results

### Recommendations
- `POST /recommendation/outfits` - Get outfit recommendations
- `GET /recommendation/similar/{product_id}` - Similar products
- `GET /recommendation/trending` - Trending outfits
- `POST /recommendation/personalized` - Personalized recommendations

### Admin
- `GET /admin/stats` - Dashboard stats
- `GET /admin/users` - List users
- `GET /admin/users/{id}` - User details
- `PUT /admin/users/{id}/role` - Update user role
- `POST /admin/users/{id}/deactivate` - Deactivate user
- `POST /admin/users/{id}/activate` - Activate user
- `GET /admin/activity-log` - Activity log
- `GET /admin/recommendation-metrics` - Recommendation metrics

## User Roles

1. **super_admin** - Full system access
2. **affiliate_manager** - Manage affiliate links
3. **content_manager** - Manage products
4. **ai_manager** - Monitor AI models
5. **viewer** - View-only access
6. **user** - Regular user (default)

## Database Models

### User
- id, email, username, hashed_password
- full_name, role, is_active, is_verified
- avatar_url, body_type, skin_tone
- created_at, updated_at

### Product
- id, name, description, brand
- category, subcategory, price, currency
- image_url, mask_url, tags
- fabric_type, color, pattern, size_guide
- is_active, created_at, updated_at

### AffiliateLink
- id, product_id, platform
- affiliate_url, product_sku, commission_rate
- is_active, created_at, updated_at

### TryOnResult
- id, user_id, product_id
- avatar_image_path, garment_image_path, result_image_path
- pose_used, confidence_score, metadata
- created_at

### PoseTransferResult
- id, user_id, source_image_path
- source_pose, target_pose, result_image_path
- confidence_score, metadata, created_at

### Recommendation
- id, user_id, recommended_products
- reason, base_product_id, similarity_scores
- created_at

## Integrating ML Models

### HR-VTON Virtual Try-On
Place actual model files in `ml_models/hr_vton/`
Update `services/vton_service.py` to load model instead of stub:
```python
from models.hr_vton import HRVTONModel
self.vton_model = HRVTONModel(device=self.device)
```

### PG2 Pose Transfer
Place model files in `ml_models/pg2/`
Update `services/pose_transfer_service.py` similarly.

### MediaPipe Pose Estimation
```bash
pip install mediapipe
```
Update services to use actual pose detection.

### CLIP Embeddings
```bash
pip install clip-by-openai torch
```
Update `services/reco_engine.py` to use actual CLIP.

## Configuration

Edit `.env` file to customize:

```env
# AI Models
VTON_MODEL_NAME="hr-vton"           # hr-vton or cp-vton
POSE_TRANSFER_MODEL="pg2"           # pg2 or hr-vton-pose
MODEL_DEVICE="cpu"                  # cpu or cuda

# Security
SECRET_KEY="change-this-key"
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database
DATABASE_URL="sqlite:///./fashion_app.db"

# Paths
AVATAR_UPLOAD_DIR="./static/avatars"
OUTPUT_DIR="./static/outputs"
```

## Database Migrations

For production with PostgreSQL, use Alembic:

```bash
# Install Alembic
pip install alembic

# Initialize migrations
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

## Deployment

### Docker (Optional)
Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t fashion-api .
docker run -p 8000:8000 fashion-api
```

### Production Checklist
- [ ] Set `DEBUG=False` in `.env`
- [ ] Use strong `SECRET_KEY`
- [ ] Use PostgreSQL instead of SQLite
- [ ] Enable HTTPS
- [ ] Setup logging
- [ ] Configure CORS properly
- [ ] Use Gunicorn or similar
- [ ] Setup monitoring/alerting

## Performance Optimization

1. **Enable GPU**
   ```bash
   # Install CUDA
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   # Set MODEL_DEVICE="cuda"
   ```

2. **Database Indexes**
   - Already on: id, email, username, product name/category, user_id

3. **Caching**
   - Embedding cache in recommendation engine
   - Consider Redis for scaling

4. **Image Optimization**
   - Compress inputs before processing
   - Store outputs with quality settings

## Troubleshooting

### Database Issues
```bash
# Reset database (WARNING: Deletes all data)
python -c "from core.db import drop_db; drop_db()"
```

### Port Already in Use
```bash
# Use different port
uvicorn main:app --port 8001
```

### Import Errors
```bash
# Ensure PYTHONPATH includes backend directory
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
uvicorn main:app --reload
```

## Testing

```bash
pytest
# With coverage
pytest --cov=.
```

## Documentation

- API Docs: `http://localhost:8000/docs`
- Architecture: See folder structure above
- Models: See `schemas/base.py`
- Services: See `services/` directory

## Future Enhancements

- [ ] Real-time WebSocket support for live try-on
- [ ] Advanced color theory matching
- [ ] 3D virtual fitting room
- [ ] Video try-on
- [ ] Multiple model ensemble
- [ ] A/B testing framework
- [ ] Analytics dashboard
- [ ] Mobile app backend optimization

## License

Proprietary - Fashion Virtual Try-On Project

## Support

For issues or questions:
1. Check API docs at `/docs`
2. Review logs in console output
3. Check `.env` configuration
4. Ensure all dependencies installed

---

**Built with:** FastAPI, SQLAlchemy, OpenCV, NumPy, Scikit-learn
