# Project Requirements Document (PRD)

## 1. Project Overview

**Money Laundry Manager** is a digital laundry management system designed to help laundry shop employees (Pegawai) and owners manage the end-to-end process of receiving, tracking, and delivering laundry orders. It replaces manual spreadsheets and paper slips with a modern web interface where staff can log in, create new orders, update statuses, and view real-time dashboards. Owners get a high-level view of business metrics like transaction volume, pending orders, and customer lists.

This application is being built to standardize laundry operations, reduce errors, and improve transparency between employees and management. Key objectives are:

- Secure authentication and role-based access control (Pegawai vs. Owner).
- Fast, intuitive order intake and status updates.
- Centralized customer and employee records with CRUD operations.
- Interactive dashboards that surface the right data to each user role.
- A maintainable, Docker-ready architecture that can be deployed consistently across environments.

Success will be measured by how quickly a new employee can log in and process a laundry order, how easily an owner can spot bottlenecks, and how stable and responsive the app remains under normal load.

---

## 2. In-Scope vs. Out-of-Scope

### In-Scope (Version 1.0)
- User authentication (sign-up, sign-in, password reset).
- Role-based access control (Pegawai vs. Owner).
- **Order Management**: input new orders, set weight/service type, calculate estimated cost, assign status.
- **Order Status Tracking**: update statuses (e.g., Received, Washing, Ready for Pickup).
- **Customer Management**: add/edit/delete customer profiles (name, contact, address).
- **Employee Management**: view list of staff, assign roles (Pegawai or Owner).
- **Dashboards**:
  - Pegawai view: quick links to input orders and update statuses.
  - Owner view: overview charts, recent transactions, pending orders count.
- REST API endpoints for all CRUD operations.
- Docker & Docker Compose setup for app + PostgreSQL.
- Environment configuration via `.env` files.

### Out-of-Scope (Deferred to Later Phases)
- Mobile application or native iOS/Android support.
- Payment gateway integration (online checkout).
- Advanced financial reporting (profit/loss statements).
- SMS or email notifications to customers.
- Multi-branch/multi-tenant support.
- Offline mode or local data sync.
- AI-driven features (e.g., demand forecasting).

---

## 3. User Flow

A new or returning user lands on the Sign In page and enters their email and password. After successful authentication, the system checks their role. If the user is a **Pegawai**, they are redirected to the **Pegawai Dashboard**, which shows buttons to “Create New Order” and “Update Order Status,” along with a quick table of today’s pending orders. If the user is an **Owner**, they see the **Owner Dashboard** with summary charts: total orders, revenue estimates, and a list of recent transactions.

From the Pegawai Dashboard, clicking **Create New Order** opens a form where the employee selects or adds a customer, chooses service type (e.g., wash, dry clean), inputs weight, and submits. The form calls the `POST /api/orders` endpoint, saving the order in the database and returning a confirmation with an order number and estimated completion date. To update status, the employee visits “Update Order Status,” selects an order from a searchable table, chooses the next status, and submits a `PUT /api/orders/{id}/status` request.

Meanwhile, the Owner can click on chart widgets to drill into details (e.g., view all orders by status), or go to dedicated pages (**Data Pelanggan**, **Data Pegawai**, **Daftar Transaksi**) to perform CRUD operations or export data. All pages use a consistent navigation sidebar, a top bar with user info, and data tables with pagination and filters.

---

## 4. Core Features

- **Authentication & Authorization**
  - Secure sign-up, sign-in, password reset.
  - Role-based route protection.
- **Order Management**
  - Create order: customer lookup/creation, service type, weight, cost calc.
  - Retrieve order details by order number.
  - Update order status (chain of statuses).
- **Customer Management**
  - List, search, add, edit, delete customers.
- **Employee Management**
  - List all staff, assign roles, disable accounts.
- **Dashboards**
  - Pegawai: pending orders list, quick actions.
  - Owner: metrics charts (orders per day, revenue), recent transactions.
- **Data Tables**
  - Reusable component with pagination, sorting, filtering.
- **API Endpoints**
  - CRUD for orders, customers, employees.
  - Status update endpoint.
- **Deployment**
  - Docker/Docker Compose for local and production.
  - Environment variable support (.env).

---

## 5. Tech Stack & Tools

- **Backend**:
  - Python 3.10+ with Django 4.x.
  - Django REST Framework for API layer.
  - Django’s built-in auth or django-allauth for user management.
  - PostgreSQL as the primary database.
- **Frontend**:
  - Next.js 13+ (App Router) with React and TypeScript.
  - Tailwind CSS for utility-first styling.
  - shadcn/ui component library for pre-built UI elements.
- **ORM & Database**:
  - Django ORM (replaces Drizzle ORM example).
  - Migration management via Django’s migrations.
- **Authentication**:
  - Django sessions + JWT (optional) for API protection.
- **Containerization & Deployment**:
  - Docker and Docker Compose.
  - Environment variables managed via `.env`.
- **Development Tools**:
  - VS Code with Python, ESLint, Prettier extensions.
  - Git for version control, GitHub Actions for CI/CD (optional).

---

## 6. Non-Functional Requirements

- **Performance**: API response time under 200 ms under normal load; page load under 1 s on standard broadband.
- **Security**: All traffic over HTTPS; input validation to prevent injections; password hashing and secure session cookies; role checks on every protected endpoint.
- **Scalability**: Stateless backend so multiple containers can run behind a load balancer; indexed database tables for query speed.
- **Usability**: Responsive design for desktop and tablet; clear navigation labels; form validation with inline error messages.
- **Maintainability**: Modular code organization; documented API schemas; consistent coding standards (Black/isort for Python, Prettier/ESLint for JS).

---

## 7. Constraints & Assumptions

- **Constraints**:
  - Must use PostgreSQL (hosted on Supabase or self-managed).
  - Docker must be available in all environments.
  - shadcn/ui requires React 18+ and Tailwind CSS.
- **Assumptions**:
  - Employees and owners have modern web browsers (Chrome, Firefox, Edge).
  - No offline usage required in v1.
  - Customer data volume is moderate (<10 000 records) initially.
  - Network latency is low in target deployment region.

---

## 8. Known Issues & Potential Pitfalls

- **Concurrency & Race Conditions**: Two employees updating the same order status simultaneously could cause conflicts. Mitigation: database transactions and optimistic locking / version fields.
- **API Rate Limits**: If hosted on platforms like Supabase Edge Functions, watch the rate tiers. Plan for throttling in DRF settings.
- **CORS & CSRF**: Ensure proper configuration of CORS headers in Django for the Next.js frontend, and CSRF protections on state-changing routes.
- **Data Migrations**: Adding new fields (e.g., `estimasi_selesai`) requires careful migration scripts to avoid downtime.
- **UI Component Versioning**: Upgrading shadcn/ui or Tailwind may introduce breaking changes. Lock versions in `package.json` and test thoroughly.
- **Deployment Secrets**: Leaking `.env` files can expose database credentials. Store secrets in a secure vault or CI/CD secrets manager.


*This PRD is intended as the single source of truth for developing the Money Laundry Manager. It covers the key requirements, scope, user journeys, technical choices, and potential risks to guide all subsequent design and implementation documents.*