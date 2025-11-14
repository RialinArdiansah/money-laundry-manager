# Backend Structure Document

## 1. Backend Architecture

This project uses Next.js both as a frontend and backend framework. The backend logic lives in **Next.js API Routes** alongside the React components, creating a single, unified codebase.

Key design choices:
- Framework: Next.js (App Router) with TypeScript
- Authentication: Better Auth handling sign-up, sign-in, session management, and protected routes
- Data layer: Drizzle ORM for type-safe database queries
- Containerization: Docker + Docker Compose for development and deployment

How it supports project goals:
- Scalability: Each API route is an independent function, making it easy to add new features or microservices later.
- Maintainability: Clear folder structure separates pages, API routes, shared logic, and database schemas.
- Performance: Next.js optimizes server-side code and automatically splits routes into serverless functions.

## 2. Database Management

The application uses a **PostgreSQL** database, which can run locally in Docker or in the cloud via Supabase.

Technologies:
- SQL database: PostgreSQL
- ORM: Drizzle ORM (type-safe queries in TypeScript)
- Connection management: Environment variables (`DATABASE_URL`) loaded via a `.env` file
- Containerization: `postgres` service defined in `docker-compose.yaml` for easy local setup

Data management practices:
- Database migrations and schema definitions live alongside code, ensuring migrations stay in sync.
- Connection strings and secrets never live in code; they are provided at runtime through environment variables.
- Drizzle ORM prevents SQL injection by using parameterized queries.

## 3. Database Schema

This project uses a relational (SQL) schema. The main entities and their relationships are:

- **Users**: All system users (employees and owners). Fields include email, name, password hash, and role.
- **Customers**: Laundry customers. Basic contact information and timestamps.
- **Orders**: Laundry orders placed by customers, including service type, weight, cost, status, and dates.

Below is a PostgreSQL schema definition:

```sql
-- Users table holds both employees and owners
enable_extension 'pgcrypto';  -- for UUID generation

CREATE TABLE users (
  id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email          TEXT UNIQUE NOT NULL,
  name           TEXT NOT NULL,
  hashed_password TEXT NOT NULL,
  role           TEXT CHECK (role IN ('Pegawai', 'Owner')) NOT NULL,
  created_at     TIMESTAMP WITH TIME ZONE DEFAULT now(),
  updated_at     TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- Customers table
CREATE TABLE customers (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name        TEXT NOT NULL,
  address     TEXT,
  phone_number TEXT,
  created_at  TIMESTAMP WITH TIME ZONE DEFAULT now(),
  updated_at  TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- Orders table links to customers
CREATE TABLE orders (
  id                   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  order_number         TEXT UNIQUE NOT NULL,
  customer_id          UUID REFERENCES customers(id) ON DELETE CASCADE,
  service_type         TEXT NOT NULL,
  weight               NUMERIC(6,2) NOT NULL,
  total_cost           NUMERIC(10,2) NOT NULL,
  date_received        DATE NOT NULL,
  estimated_completion DATE,
  status               TEXT CHECK (status IN ('Received', 'In Process', 'Completed', 'Picked Up'))
    DEFAULT 'Received',
  created_at           TIMESTAMP WITH TIME ZONE DEFAULT now(),
  updated_at           TIMESTAMP WITH TIME ZONE DEFAULT now()
);
```  

## 4. API Design and Endpoints

The backend follows a RESTful style using Next.js API Routes. Each file under `app/api` becomes an endpoint.

Primary endpoints:
- **Authentication** (`app/api/auth/[...all]/route.ts`)
  - Handles user sign-up, sign-in, and session checks
- **POST /api/orders**
  - Create a new laundry order
- **GET /api/orders**
  - List all orders (with optional filtering by status or date)
- **GET /api/orders/[orderId]**
  - Fetch details for a single order by ID
- **PUT /api/orders/[orderId]/status**
  - Update the status of an existing order
- **GET /api/customers**
  - List all customers
- **POST /api/customers**
  - Add a new customer
- **GET /api/users**
  - List all employees and owners (protected, owner-only access)

Data flow:
1. Frontend form submits JSON to an API route.
2. The route validates input, uses Drizzle ORM to interact with PostgreSQL.
3. A JSON response with data or error is returned.

## 5. Hosting Solutions

The backend can run in Docker containers or be deployed to a cloud platform.

Current setup:
- Local development: Docker Compose spins up Next.js app and PostgreSQL in separate containers.
- Production options:
  - Vercel: Next.js API Routes deploy as serverless functions, auto-scaling by traffic.
  - Cloud VM (AWS EC2, DigitalOcean Droplet): Run Docker Compose in a managed VM.
  - Supabase: Managed PostgreSQL database with automated backups.

Benefits:
- **Reliability**: Managed services handle failover and backups.
- **Scalability**: Serverless functions (Vercel) or container orchestration (Kubernetes) can scale with demand.
- **Cost-effectiveness**: Only pay for resources in use; local Docker for low-cost development.

## 6. Infrastructure Components

Key components working together:
- **Load Balancer / Reverse Proxy**: Nginx or built-in Vercel routing distributes requests across instances.
- **CDN**: Static assets served via Vercel’s global CDN or Cloudflare for fast front-end load times.
- **Caching**: In-memory caching at the API layer (Node.js cache) or Redis for frequently accessed data (optional extension).
- **Container Network**: Docker Compose provides an isolated network for the app and database.

These pieces ensure quick responses, balanced load, and smooth user experience.

## 7. Security Measures

User data and operations are protected through multiple layers:
- **Authentication & Authorization**
  - Better Auth library for secure session management
  - Role-based access control: only users with the "Owner" role can access certain endpoints
- **Data Encryption**
  - TLS/HTTPS for all client-server communications
  - Passwords stored as hashed values
  - Environment variables for secrets (never committed to code)
- **Input Validation**
  - Drizzle ORM ensures parameterized queries to prevent SQL injection
  - API routes validate request bodies before processing

## 8. Monitoring and Maintenance

Tools and practices in place:
- **Logging**: Console logs in API routes; can integrate with services like Sentry or Logflare
- **Performance Monitoring**: Vercel Analytics or APM tools (New Relic, Datadog)
- **Health Checks**: Docker health checks for the PostgreSQL container
- **Backups & Rollbacks**: Automated backups via Supabase or custom scripts for on-premise databases
- **CI/CD**: GitHub Actions or other pipelines to run tests, linting, and deploy on merge

## 9. Conclusion and Overall Backend Summary

This backend is built with modern web development best practices in mind: a unified Next.js codebase, a reliable PostgreSQL database managed by Drizzle ORM, and secure authentication through Better Auth. Containerization with Docker ensures that the development environment mirrors production, reducing surprises on deploy. The RESTful API design, coupled with role-based access controls and clear data schemas, makes the system easy to extend and maintain. Finally, leveraging cloud hosting and CDNs guarantees performance and scalability as your laundry management application grows.