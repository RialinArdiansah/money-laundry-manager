# Security Guidelines for "money-laundry-manager"

This document outlines essential security principles and actionable recommendations tailored to the `money-laundry-manager` Next.js application (with Drizzle ORM, Better Auth, PostgreSQL/Supabase, Docker, and shadcn/ui). Adhere to these guidelines throughout development, testing, and deployment to ensure a robust, secure, and maintainable system.

## 1. Security by Design
- Embed security in every phase: design, implementation, testing, deployment, and maintenance.  
- Adopt threat modeling early on: identify high-risk features (authentication, file uploads) and design mitigations from the start.
- Maintain clear separation of concerns (UI vs. API vs. data layer) to minimize attack surfaces.

## 2. Authentication & Access Control

### 2.1. Robust Authentication
- Use Better Auth’s secure defaults; ensure you’ve configured it to:
  - Enforce email verification for new accounts.
  - Rate-limit login attempts to prevent brute-force attacks.
  - Rotate secrets (OAuth keys, JWT signing secrets) regularly.

### 2.2. Strong Password Policies
- Mandate a minimum length (≥ 12 characters), complexity (uppercase, lowercase, numbers, symbols).
- Back passwords with bcrypt or Argon2 (unique per-user salt). Do **not** use deprecated hashing algorithms.

### 2.3. Secure Session Management
- Prefer HTTP-only, Secure, SameSite=strict cookies for session or JWT storage.  
- Enforce idle and absolute timeouts (e.g., 30-minute idle, 8-hour absolute).  
- Invalidate sessions on logout and credential changes.  
- Protect against session fixation by regenerating session ID upon login.

### 2.4. Role-Based Access Control (RBAC)
- Define “Pegawai” and “Owner” roles in your database schema (`users.role`).  
- Apply server-side guards on every API route and page:
  - Middleware example (Next.js):
    ```js
    // middleware.ts
    import { getSession } from "@better-auth/session";
    export async function middleware(req) {
      const session = await getSession(req);
      if (!session) return new Response(null, { status: 401 });
      if (req.nextUrl.pathname.startsWith('/owner') && session.role !== 'Owner')
        return new Response(null, { status: 403 });
      return NextResponse.next();
    }
    ```
- Never rely solely on client-side role checks.

## 3. Input Handling & Processing

### 3.1. Server-Side Validation
- Use a schema validation library (e.g., Zod or Joi) on every API route.  
- Reject or sanitize invalid input before ORM interaction:
  ```ts
  const OrderSchema = z.object({
    pelangganId: z.string().uuid(),
    jenisLayanan: z.enum(['cuci','setrika','cuci-setrika']),
    berat: z.number().positive(),
    estimasiSelesai: z.string().refine(date => !isNaN(Date.parse(date)))
  });
  const data = OrderSchema.parse(req.body);
  ```

### 3.2. Prevent Injection
- Drizzle ORM uses parameterized queries by default—continue using it for all DB operations.  
- Never build SQL queries via string concatenation.

### 3.3. XSS & Output Encoding
- Escape or sanitize any user-supplied data rendered in React components.  
- If you must render HTML, use a vetted sanitizer (e.g., DOMPurify).
- Implement a strong Content Security Policy (CSP) to restrict script sources.

### 3.4. File Upload Security (if applicable)
- Validate file type/size on both client and server.  
- Store uploads outside the webroot or in a dedicated object store (e.g., S3) with limited permissions.  
- Scan for malware on upload (integrate a virus-scanning service).

## 4. Data Protection & Privacy

### 4.1. Encryption in Transit & at Rest
- Enforce HTTPS (TLS 1.2+) on all endpoints.  
- Instruct Docker containers to terminate SSL at a reverse proxy (e.g., Nginx) if not in serverless.  
- Enable database encryption or use a managed service (Supabase with encryption-at-rest).

### 4.2. Secret Management
- Do **not** commit `.env` files or secrets to Git.  
- Use a secrets manager (AWS Secrets Manager, Vault, or Vercel’s encrypted environment variables).

### 4.3. Prevent Information Leakage
- Hide stack traces from end users (configure `next.config.js`:
  ```js
  module.exports = {
    reactStrictMode: true,
    productionBrowserSourceMaps: false,
  };  
  ```
- Redact PII in logs; Log only metadata (request IDs, timestamps).

## 5. API & Service Security

### 5.1. Rate Limiting & Throttling
- Integrate a rate-limiting middleware (e.g., `express-rate-limit` or `next-rate-limit`).  
- Apply stricter limits to login, password-reset, and other sensitive endpoints.

### 5.2. CORS Configuration
- Configure `next.config.js` or a custom API handler to allow only your front-end origin:
  ```js
  const cors = require('micro-cors')({
    origin: process.env.FRONTEND_URL,
    allowMethods: ['GET','POST','PUT','DELETE']
  });
  ```

### 5.3. Versioned API Endpoints
- Prefix routes with `/api/v1/…` to safely introduce breaking changes in the future.

## 6. Web Application Security Hygiene

### 6.1. Security Headers
- Use `next-secure-headers` or custom middleware:
  ```js
  async headers() {
    return [
      { key: 'Strict-Transport-Security', value: 'max-age=63072000; includeSubDomains; preload' },
      { key: 'X-Frame-Options', value: 'DENY' },
      { key: 'X-Content-Type-Options', value: 'nosniff' },
      { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
      { key: 'Content-Security-Policy', value: "default-src 'self'; script-src 'self'" }
    ];
  }
  ```

### 6.2. CSRF Protection
- Next.js API routes with cookie-based auth require CSRF tokens.  
- Use a library such as `next-csrf` to generate and validate tokens for state-changing requests.

### 6.3. Secure Cookies
- Always set `HttpOnly`, `Secure`, `SameSite=Strict` on auth cookies.

### 6.4. Subresource Integrity (SRI)
- If loading any external scripts/styles, include integrity hashes in `<script>` and `<link>` tags.

## 7. Infrastructure & Configuration Management

### 7.1. Docker Best Practices
- Build minimal images (use `node:18-alpine`).  
- Run processes under a non-root user (`USER node`).
- Add a `.dockerignore` to exclude `node_modules` and other non-essential files.

### 7.2. Secure Defaults & Hardening
- Disable Next.js debug in production.  
- Close unused ports in Docker and your cloud firewall.
- Regularly patch OS and base images.

## 8. Dependency Management

- Lock dependencies via `package-lock.json` or `yarn.lock` to ensure reproducible installs.
- Use Dependabot or a similar SCA tool to scan for CVEs in both direct and transitive dependencies.
- Audit packages with `npm audit` and address high-severity findings promptly.
- Remove unused dependencies to reduce the attack surface.

## 9. Monitoring, Logging & Incident Response

- Implement centralized logging (e.g., LogRocket, Sentry) with PII masking.  
- Configure alerts for anomalous activity (e.g., repeated failed logins).  
- Maintain an incident response plan: roles, communication channels, and recovery procedures.

---

Adhering to these guidelines will help ensure that `money-laundry-manager` is built with security and privacy at its core. Regularly review and update these practices as new threats and technologies emerge.