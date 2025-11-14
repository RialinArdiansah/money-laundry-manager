# money-laundry-manager Tech Stack

This document explains, in simple terms, the technology choices behind the **money-laundry-manager** project. It outlines the tools and services we’ve picked, why we picked them, and how they work together to deliver a secure, reliable, and user-friendly laundry management system.

## 1. Frontend Technologies

Our goal on the frontend is to build a fast, responsive, and consistent user interface that anyone can use on desktop or mobile. Here’s how we do that:

- **Next.js (React + TypeScript)**
  - Why: Next.js makes it easy to build web pages that load quickly (with built-in server rendering and code splitting). React gives us reusable components, and TypeScript helps catch errors early.
  - Benefit for users: Smooth page transitions, faster loading times, and fewer bugs in the interface.

- **Tailwind CSS**
  - Why: A utility-first styling framework that lets us write class names for colors, spacing, layouts, and more without leaving our HTML/JSX.
  - Benefit for users: Consistent look and feel across all pages and components, plus rapid styling updates.

- **shadcn/ui**
  - Why: A library of pre-built, Tailwind-styled UI components (buttons, forms, tables, modals) that integrate seamlessly with Next.js.
  - Benefit for users: Polished, professional design out of the box, with consistent spacing, typography, and interactions.

## 2. Backend Technologies

On the server side, we handle data storage, user authentication, and the core business logic for managing orders. Here are the main pieces:

- **Next.js API Routes**
  - Why: Built-in API handlers within the same codebase as the pages. This keeps frontend and backend logic together in one project.
  - Role: Define endpoints like `/api/auth`, `/api/orders`, and `/api/customers` to process requests from the UI.

- **Better Auth**
  - Why: A simple, secure authentication library that plugs into Next.js API Routes.
  - Role: Handle user sign-up, sign-in, session management, and role checks (e.g., “Pegawai” vs. “Owner”).

- **Drizzle ORM**
  - Why: A lightweight, type-safe library for working with SQL databases in TypeScript.
  - Role: Define database schemas and run queries (create orders, update statuses, fetch customer lists) in a safe, structured way.

- **PostgreSQL (via Supabase or local Docker)**
  - Why: A reliable, scalable relational database for storing users, orders, customers, and employees.
  - Role: Central data store for all business information (order history, customer profiles, transaction logs).

## 3. Infrastructure and Deployment

These choices ensure that developers can run the app locally, and that we can deploy it reliably to production:

- **Docker & docker-compose**
  - Why: Containerization lets us package the app and database together with all dependencies.
  - Benefit: Every team member and server runs the same environment—no more “works on my machine” issues.

- **Environment Variables (`.env`)**
  - Why: Keep sensitive information (database URLs, API keys, secrets) out of the code.
  - Benefit: Secure configuration and easy swapping between development, staging, and production settings.

- **Git & GitHub (Version Control)**
  - Why: Track code changes, collaborate via branches and pull requests.
  - Benefit: Clear history of who changed what, easy rollbacks, and peer reviews.

- **CI/CD Pipeline (e.g., GitHub Actions)**
  - Why: Automate tests, builds, and deployments whenever code is pushed.
  - Benefit: Faster, more reliable releases with fewer manual steps.

- **Cloud Hosting (e.g., Vercel, AWS, or any Docker-friendly platform)**
  - Why: Host the frontend and backend with global performance optimizations.
  - Benefit: Automatic scaling, global edge networks for low latency, simple environment management.

## 4. Third-Party Integrations

We rely on a few external services to speed up development and add robust features:

- **Supabase**
  - What: A hosted PostgreSQL database with built-in APIs and dashboards.
  - Why: Easy setup for cloud-based storage and admin tools without managing your own database server.

- **Better Auth**
  - What: Authentication and session management library for Next.js.
  - Why: Secure login flows, password handling, and token management out of the box.

*(Note: If you add payment processing, email notifications, or analytics later, you would list them here in the same way.)*

## 5. Security and Performance Considerations

To protect user data and ensure a smooth experience, we’ve built in several safeguards and optimizations:

- **Authentication & Role-Based Access Control (RBAC)**
  - Users must sign in to access any page.
  - Pages and API routes check user roles (Pegawai vs. Owner) before allowing data access.

- **Environment-Based Configurations**
  - Secrets and keys stay out of the code repository.
  - Separate settings for development, testing, and production.

- **Type-Driven Development (TypeScript + Drizzle)**
  - Minimizes runtime errors by catching type mismatches at compile time.

- **Next.js Performance Features**
  - Server-Side Rendering (SSR) and Static Site Generation (SSG) where appropriate for fastest load times.
  - Automatic code splitting and image optimization.

- **Database Query Optimization**
  - Structured queries via Drizzle ORM ensure we only fetch the data we need.
  - Indexing key columns (e.g., order ID, customer ID) for quick lookups.

## 6. Conclusion and Overall Tech Stack Summary

In building the money-laundry-manager application, we chose a **modern, unified stack** that covers every layer from user interface to data storage:

- **Frontend:** Next.js, React, TypeScript, Tailwind CSS, shadcn/ui
- **Backend:** Next.js API Routes, Better Auth, Drizzle ORM, PostgreSQL (Supabase)
- **Infrastructure:** Docker, environment variables, GitHub, CI/CD, cloud hosting
- **Integrations:** Supabase for hosting, Better Auth for authentication
- **Security & Performance:** Role checks, secret management, type safety, SSR/SSG, query optimization

These choices work together to give your team a solid, scalable foundation. You get a polished user interface, secure login flows, clear data management, and a straightforward path to deploying and maintaining the system in any environment. Whether you stick with Next.js or adapt the patterns to another framework like Django, these principles will guide you to a reliable, easy-to-maintain laundry management solution.