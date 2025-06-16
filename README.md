# ReAlloc - Food Allocation Management System

A comprehensive Django-based food allocation and inventory management system designed for NGOs and food banks to efficiently manage food distribution to families in need.

## 🎯 Overview

ReAlloc is a full-featured web application that helps organizations manage:
- **Inventory Management**: Track food products, storage locations, and expiration dates
- **Family Management**: Maintain records of beneficiary families and their nutritional needs
- **Allocation Algorithm**: Intelligent food allocation using optimization algorithms
- **Package Management**: Handle packing and delivery of food packages
- **Real-time Updates**: WebSocket support for live status updates
- **Notifications**: Firebase Cloud Messaging integration for alerts

## 🏗️ Architecture

### Technology Stack
- **Backend**: Django 4.2+ with Django REST Framework
- **Database**: PostgreSQL
- **Task Queue**: Celery with RabbitMQ
- **Cache/Channels**: Redis
- **Real-time**: Django Channels with WebSockets
- **Storage**: MinIO (S3-compatible)
- **Notifications**: Firebase Cloud Messaging
- **AI/ML**: Google Gemini API for nutritional label recognition
- **Optimization**: OR-Tools for allocation algorithms

### Key Components
- **Authentication**: Token-based authentication with role management
- **Models**: Comprehensive data models for inventory, families, allocations, and packages
- **Services**: Business logic separation with service layer architecture
- **Tasks**: Background job processing with Celery
- **Real-time**: WebSocket consumers for live updates

## 📋 Features

### Core Functionality

#### 🏪 Inventory Management
- Product catalog with nutritional information
- Storage location tracking with halal/non-halal separation
- Expiration date monitoring and alerts
- Automated inbound/outbound inventory tracking
- OCR-based nutritional label extraction using AI

#### 👨‍👩‍👧‍👦 Family Management
- Family profile management with member details
- Nutritional requirement calculations based on age, gender, activity level
- Food restriction and dietary preference tracking
- Household income and priority scoring

#### 🎯 Smart Allocation System
- Advanced optimization algorithm using OR-Tools
- Multi-objective optimization considering:
  - Nutritional requirements
  - Food restrictions and preferences
  - Inventory availability and expiration dates
  - Family priority scoring
  - Product diversification
- Real-time allocation status updates

#### 📦 Package Management
- Automated package generation from allocations
- Multi-stage workflow: New → Packed → Delivered
- Expiration date validation during packing
- Delivery tracking and family history

#### 🔔 Notification System
- Firebase Cloud Messaging integration
- Automated alerts for:
  - Expiring inventory
  - Allocation status updates
  - Package state changes
  - System notifications

### Advanced Features

#### 🤖 AI-Powered OCR
- Nutritional label recognition using Google Gemini
- Automatic extraction of nutritional information from product images
- Support for multiple label formats

#### 📊 Dashboard & Analytics
- Real-time metrics and KPIs
- Inventory turnover tracking
- Package delivery statistics
- Period-based reporting

#### ⚡ Real-time Updates
- WebSocket integration for live updates
- Allocation progress monitoring
- Package status changes
- System-wide notifications

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- PostgreSQL 12+
- Redis 6+
- RabbitMQ 3.8+
- MinIO or S3-compatible storage
- Firebase project (for notifications)

### Environment Variables
Create a `.env` file with the following variables:

```bash
# Django
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=True

# Database
POSTGRES_DB=food_allocation
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-password

# Message Broker
RABBITMQ_DEFAULT_USER=rabbitmq
RABBITMQ_DEFAULT_PASS=password

# Storage
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=minioadmin
MINIO_BUCKET_NAME=food-allocation
MINIO_ENDPOINT_URL=http://localhost:9000

# External APIs
GEMINI_API_KEY=your-gemini-api-key

# Frontend
FRONTEND_BASE_URL=http://localhost:3000
```

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd food_allocation
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate  # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up external services**
   ```bash
   # Start PostgreSQL, Redis, RabbitMQ, MinIO
   # Or use Docker Compose (if available)
   docker-compose up -d
   ```

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start services**
   ```bash
   # Terminal 1: Django server
   python manage.py runserver

   # Terminal 2: Celery worker
   celery -A food_allocation worker -l info -Q realloc_allocation,realloc_scheduled_daily

   # Terminal 3: Celery beat scheduler
   celery -A food_allocation beat -l info
   ```

## 📚 API Documentation

The API is fully documented using OpenAPI/Swagger:
- **Swagger UI**: `http://localhost:8000/api/schema/swagger-ui/`
- **ReDoc**: `http://localhost:8000/api/schema/redoc/`
- **Schema**: `http://localhost:8000/api/schema/`

### Key Endpoints

#### Authentication
- `POST /api/v1/authentication/login` - User login
- `POST /api/v1/authentication/register` - User registration
- `POST /api/v1/authentication/logout` - User logout

#### Inventory Management
- `GET /api/v1/inventory-management/inventories/search` - Search inventories
- `POST /api/v1/inventory-management/inventories/inbound` - Add inventory
- `PATCH /api/v1/inventory-management/inventories/{id}/adjust` - Adjust quantities

#### Master Data
- `GET /api/v1/master-data/products/search` - Search products
- `POST /api/v1/master-data/products/create` - Create product
- `GET /api/v1/master-data/families/search` - Search families

#### Allocation
- `POST /api/v1/allocation/create` - Create allocation
- `GET /api/v1/allocation/search` - Search allocations
- `PATCH /api/v1/allocation/family/{id}/accept` - Accept allocation

#### Package Management
- `GET /api/v1/package/search` - Search packages
- `PATCH /api/v1/package/{id}/pack` - Pack package
- `PATCH /api/v1/package/{id}/deliver` - Deliver package

## 🧮 Allocation Algorithm

The system uses a sophisticated optimization algorithm built with OR-Tools:

### Algorithm Features
- **Multi-objective optimization** considering nutritional needs, preferences, and constraints
- **Adaptive heuristic** with destroy-and-repair operators
- **Flexibility parameters** allowing partial fulfillment of requirements
- **Priority-based allocation** considering family socioeconomic status
- **Diversification control** ensuring variety in food packages

### Process Flow
1. **Data Preparation**: Extract family nutritional needs and available inventory
2. **Constraint Generation**: Apply food restrictions, halal requirements, and quantities
3. **Optimization**: Run adaptive heuristic with multiple destroy operators
4. **Result Validation**: Verify allocations against current inventory state
5. **Package Creation**: Generate delivery packages for accepted families

## 🔧 Configuration

### Celery Configuration
The system uses Celery for background task processing:
- **Allocation Queue**: `realloc_allocation` - Handles resource-intensive allocation algorithms
- **Scheduled Queue**: `realloc_scheduled_daily` - Daily maintenance tasks

### Scheduled Tasks
- **Daily 00:00**: Reject expired allocations
- **Daily 00:00**: Cancel packages with expired inventory
- **Daily 00:00**: Send expiration notifications
- **Daily 00:00**: Clean up expired notifications

### WebSocket Endpoints
- `ws://localhost:8000/ws/allocation` - Allocation status updates
- `ws://localhost:8000/ws/package` - Package state changes

## 🛡️ Security & Permissions

### Role-Based Access Control
- **NGO Manager**: Full system access including user management
- **Volunteer**: Limited access to operational features

### Authentication
- Token-based authentication
- Configurable token expiration
- Secure password validation

## 🚀 Deployment

### Production Considerations
1. **Environment Variables**: Use proper secret management
2. **Database**: Configure PostgreSQL with proper backup strategies
3. **Static Files**: Set up proper static file serving
4. **Background Tasks**: Deploy Celery workers with proper monitoring
5. **WebSockets**: Configure proper WebSocket support (nginx, etc.)
6. **Caching**: Optimize Redis configuration for production
7. **Monitoring**: Set up application monitoring and logging

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose -f docker-compose.prod.yml up -d
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the API documentation for endpoint details
- Review the Django admin interface for data management

## 🔄 Version History

- **v1.0.0**: Initial release with core allocation functionality
- **Features**: Full CRUD operations, allocation algorithm, real-time updates, notification system

---

*Built with ❤️ for food security and community support*
