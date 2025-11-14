# Django Backend Setup for Money Laundry Management System

## Prerequisites

- Python 3.8+
- pip package manager
- Supabase account and database (for production)

## Quick Start (Development)

1. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   - Copy `.env.example` to `.env` if not exists
   - For development, keep `USE_SQLITE=True` to use local SQLite database
   - For production, set `USE_SQLITE=False` and configure Supabase

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser:**
   ```bash
   python manage.py createsuperuser
   # Or use the existing admin account: admin / admin123
   ```

6. **Run development server:**
   ```bash
   python manage.py runserver
   ```

   - Admin interface: http://localhost:8000/admin/
   - API endpoints: http://localhost:8000/api/

## Production Setup with Supabase

### 1. Configure Supabase

1. **Create a new Supabase project:**
   - Go to https://supabase.com
   - Create a new project
   - Note down your project URL and anon key

2. **Get database credentials:**
   - In Supabase dashboard, go to Settings > Database
   - Find the connection string details
   - Copy the following:
     - Host (something like `xxxxx.supabase.co`)
     - Database name (usually `postgres`)
     - Port (usually `5432`)
     - User (usually `postgres`)
     - Password (generated password)

### 2. Configure Environment Variables

Update your `.env` file:

```env
# Django Configuration
SECRET_KEY=your-unique-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database Configuration - Supabase
USE_SQLITE=False

# Supabase PostgreSQL Configuration
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-actual-supabase-password
POSTGRES_HOST=your-project-id.supabase.co
POSTGRES_PORT=5432
```

### 3. Database Setup

1. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```

2. **Create superuser:**
   ```bash
   python manage.py createsuperuser
   ```

3. **Collect static files:**
   ```bash
   python manage.py collectstatic
   ```

## Project Structure

```
money_laundry/              # Django project settings
├── settings.py            # Main configuration
├── urls.py               # URL routing
└── wsgi.py               # WSGI configuration

accounts/                  # User management
├── models.py             # Custom User model with roles
├── admin.py              # Admin interface configuration
└── migrations/           # Database migrations

customers/                # Customer management
├── models.py             # Customer model
├── admin.py              # Admin interface
└── migrations/           # Database migrations

orders/                   # Order management
├── models.py             # Order and related models
├── admin.py              # Admin interface
└── migrations/           # Database migrations
```

## Database Schema

### User Model (accounts.User)
- Extends Django's AbstractUser
- **Fields:**
  - `role`: 'pegawai' or 'owner'
  - `phone_number`: Contact number
  - Standard Django auth fields

### Customer Model (customers.Customer)
- **Fields:**
  - `name`: Customer name
  - `address`: Customer address
  - `phone_number`: Contact number
  - `email`: Email address (optional)
  - `is_active`: Active status

### Order Model (orders.Order)
- **Fields:**
  - `order_number`: Auto-generated unique ID (format: ML-YYYYMMDD-XXXX)
  - `customer`: Foreign key to Customer
  - `service_type`: 'express' (1 hari) or 'regular' (3 hari)
  - `weight`: Weight in kg
  - `unit_price`: Price per kg (auto-calculated)
  - `total_cost`: Total cost (weight × unit_price)
  - `date_received`: Order received date
  - `estimated_completion`: Auto-calculated based on service type
  - `status`: 'diterima', 'proses', 'selesai', 'diambil'
  - `notes`: Additional notes
  - `storage_deadline`: Pickup deadline for completed orders

## Features Implemented

### ✅ Completed (Task 1: Django Models and Database Schema)

1. **Django Project Structure**
   - Custom User model with role-based access control
   - Customer management system
   - Order management with automatic calculations

2. **Database Configuration**
   - Support for both SQLite (development) and PostgreSQL/Supabase (production)
   - Environment-based configuration switching
   - Database migrations applied successfully

3. **Admin Interface**
   - Full CRUD operations for all models
   - Custom admin displays with statistics
   - Search and filtering capabilities

4. **Business Logic**
   - Automatic order number generation
   - Price calculation based on service type and weight
   - Estimated completion date calculation
   - Order status tracking
   - Overdue order detection
   - Storage deadline management

## Next Steps

The remaining tasks will implement:
- Authentication system and role-based access control
- Core order management system with forms and views
- Role-specific dashboards for Pegawai and Owner
- Public status check functionality
- Employee management system

## Deployment Notes

For production deployment with Supabase:

1. **Security:**
   - Set `DEBUG=False`
   - Use a strong `SECRET_KEY`
   - Configure `ALLOWED_HOSTS`
   - Enable HTTPS

2. **Performance:**
   - Configure PostgreSQL connection pooling
   - Enable database indexing
   - Use CDN for static files

3. **Monitoring:**
   - Set up logging
   - Monitor database performance
   - Implement backup strategies

## Testing

Run tests to verify everything works:
```bash
python manage.py test
python manage.py check
```

## Support

For issues related to:
- Django setup: Check Django documentation
- Supabase connection: Verify credentials and network connectivity
- Database migrations: Ensure proper database permissions