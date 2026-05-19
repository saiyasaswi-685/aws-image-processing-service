# AWS Distributed Image Processing System

A scalable distributed backend system for asynchronous image processing using Flask, AWS S3, AWS SQS, Docker, and worker-based architecture.

This project allows users to upload images through an API, process them asynchronously using background workers, and store processed images in AWS S3 buckets.

---

# 🚀 Features

- Image Upload API
- Asynchronous Image Processing
- AWS S3 Integration
- AWS SQS Queue-Based Communication
- Background Worker Architecture
- Image Resizing
- Watermarking
- Dockerized Services
- Docker Compose Support
- Environment Variable Management
- Scalable Distributed Architecture
- Cloud Deployment using Render

---

# 🌐 Live Demo

## Live API

https://image-api-service.onrender.com

### Test API

```http
GET https://image-api-service.onrender.com/
```

### Expected Response

```json
{
  "message": "API Service Running"
}
```

---

## Deployment Note

The Flask API service is deployed publicly using Render.

The worker service was tested successfully in a local Docker environment because Render background workers require a paid plan for continuous worker execution.

The complete asynchronous workflow, Docker orchestration, S3 integration, and SQS communication were fully tested locally.

---


# 🏗️ Project Architecture

```text
User
  ↓
Flask API Service
  ↓
AWS S3 (Raw Bucket)
  ↓
AWS SQS Queue
  ↓
Worker Service
  ↓
Image Processing (Resize + Watermark)
  ↓
AWS S3 (Processed Bucket)
```

---

# 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend Development |
| Flask | REST API |
| AWS S3 | Image Storage |
| AWS SQS | Queue Communication |
| Pillow | Image Processing |
| Docker | Containerization |
| Docker Compose | Multi-Container Management |
| Boto3 | AWS SDK for Python |
| Render | Cloud Deployment |
| Git & GitHub | Version Control |

---

# 📂 Project Structure

```text
aws-image-processing-service/
│
├── api-service/
│   ├── src/
│   │   ├── app.py
│   │   └── config.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── .env
│   └── .env.example
│
├── worker-service/
│   ├── src/
│   │   ├── worker.py
│   │   └── config.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── .env
│   └── .env.example
│
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

# ⚙️ Requirements

Before running the project, install:

- Python 3.12+
- Docker Desktop
- Git
- AWS Account
- AWS S3 Buckets
- AWS SQS Queue

---

# ☁️ AWS Resources Used

| Service | Purpose |
|---|---|
| AWS S3 Raw Bucket | Store original uploaded images |
| AWS S3 Processed Bucket | Store processed images |
| AWS SQS Queue | Queue communication between API and worker |

---

# 🔐 Environment Variables

Create `.env` files inside both:

```text
api-service/
worker-service/
```

Add:

```env
AWS_ACCESS_KEY=your_access_key

AWS_SECRET_KEY=your_secret_key

AWS_REGION=your_region

S3_BUCKET_RAW=your_raw_bucket

S3_BUCKET_PROCESSED=your_processed_bucket

SQS_QUEUE_URL=your_queue_url
```

---

# ▶️ Run Locally

## 1️⃣ Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/aws-image-processing-service.git
```

---

## 2️⃣ Move Into Project

```bash
cd aws-image-processing-service
```

---

## 3️⃣ Start Docker Containers

```bash
docker-compose up --build
```

---

# 📡 API Endpoints

## Home Route

### Request

```http
GET /
```

### Response

```json
{
  "message": "API Service Running"
}
```

---

## Upload Image

### Request

```http
POST /images/upload
```

### Body

form-data:

| Key | Type |
|---|---|
| image | File |

---

### Response

```json
{
  "message": "Image uploaded to S3 and queued for processing",
  "image_id": "sample-image-id",
  "s3_key": "original/sample-image-id.jpg"
}
```

---

## Get Processed Image

### Request

```http
GET /images/<image_id>
```

### Response

```json
{
  "image_id": "sample-image-id",
  "processed_image_url": "https://bucket-url"
}
```

---

# 🧠 Image Processing Workflow

1. User uploads image through Flask API.
2. API uploads original image to AWS S3 Raw Bucket.
3. API sends image metadata to AWS SQS Queue.
4. Worker continuously listens to SQS Queue.
5. Worker downloads image from S3.
6. Worker resizes image.
7. Worker adds watermark.
8. Worker uploads processed image to Processed S3 Bucket.
9. Worker deletes processed message from SQS Queue.

---

# 🧪 Testing

## API Testing

Tested using:

- Postman
- Browser
- Docker Compose

---

## Test Cases

| Test Case | Status |
|---|---|
| API Running | ✅ |
| Image Upload | ✅ |
| Invalid File Validation | ✅ |
| Empty File Validation | ✅ |
| S3 Upload | ✅ |
| SQS Message Send | ✅ |
| Worker Queue Polling | ✅ |
| Image Download from S3 | ✅ |
| Image Resize | ✅ |
| Watermark Processing | ✅ |
| Processed Image Upload | ✅ |
| Docker Compose Integration | ✅ |
| Render API Deployment | ✅ |

---

# 🐳 Docker Support

## API Service

Containerized Flask API Service.

---

## Worker Service

Containerized background worker service for asynchronous image processing.

---

## Docker Compose

Used for multi-container orchestration.

---

# 🔒 Security Improvements

- Environment variables using `.env`
- Secret key protection using `.gitignore`
- Removed hardcoded AWS credentials

---

# 📈 Future Improvements

- JWT Authentication
- Redis Caching
- Kubernetes Deployment
- CI/CD Pipeline
- Auto Scaling Workers
- Image Compression
- Multiple Image Formats Support

---

# 👨‍💻 Author

Bandaru Sai Yasaswi

---

# ⭐ Conclusion

This project demonstrates real-world distributed backend architecture using asynchronous processing, cloud services, Docker-based deployment, and scalable worker communication patterns.
