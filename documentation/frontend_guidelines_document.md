# Frontend Guideline Document for Money Laundry Manager

This document outlines the frontend architecture, design principles, styling, component structure, state management, routing, performance optimization, testing strategies, and overall summary of the Money Laundry Manager application. It is written in clear, everyday language, ensuring that anyone can understand how the frontend is set up and why certain choices were made.

## 1. Frontend Architecture

### Frameworks and Libraries
- **Next.js (App Router)**: Provides file-based routing, server-side rendering (SSR), static site generation (SSG), and incremental static regeneration (ISR). It combines React components and API routes in a single codebase.
- **React & TypeScript**: Enables a component-based UI structure with strong typing to catch errors early and improve maintainability.
- **shadcn/ui**: A collection of pre-built, customizable UI components based on Tailwind CSS.
- **Tailwind CSS**: Utility-first CSS framework that lets us build custom designs without leaving our HTML.

### Scalability, Maintainability, Performance
- **Scalability**: File-based routing and modular folder structure (`app/`, `components/`, `lib/`) allow teams to add new pages and features without impacting existing code.
- **Maintainability**: Strong typing (TypeScript) and reusable components (`components/ui/`) reduce duplication and make updates predictable.
- **Performance**: Next.js’s automatic code splitting and SSR/SSG ensure fast page loads. Tailwind’s tree-shaking removes unused CSS.

## 2. Design Principles

### Usability
- Clear labels and input states.
- Consistent feedback (toasts or modals) on user actions like “Order saved” or “Error occurred.”

### Accessibility (a11y)
- Semantic HTML tags (e.g., `<button>`, `<nav>`, `<header>`).
- ARIA attributes in custom components when necessary.
- Focus management and keyboard support for all interactive elements.

### Responsiveness
- Mobile-first approach using Tailwind’s responsive utilities (`sm:`, `md:`, `lg:`).
- Flexible grid and flex layouts ensure data tables and forms adapt to screen size.

How We Apply Them:
- All forms have clear labels and error states.
- Buttons and links have focus and hover styles.
- Tables stack or scroll horizontally on small screens.

## 3. Styling and Theming

### Styling Approach
- **Tailwind CSS**: Utility classes for rapid styling.
- **Component-specific styles**: Minimal custom CSS for special cases, kept in scoped files or via `@apply` in `.css` files.

### Theming
- Single `tailwind.config.js` defines colors, fonts, and breakpoints.
- Dark mode support via `class` strategy if needed in the future.

### Visual Style
- **Design Style**: Modern flat design with subtle glassmorphism accents on cards and modals (light background blur and semi-transparent layers).
- **Color Palette**:
  - Primary: #4F46E5 (Indigo)
  - Secondary: #3B82F6 (Blue)
  - Accent: #10B981 (Emerald)
  - Neutral Light: #F3F4F6 (Gray-100)
  - Neutral Dark: #111827 (Gray-900)
  - Background: #FFFFFF

### Typography
- **Font Family**: Inter (system font fallback)
- **Font Sizes**: Scaled in Tailwind (e.g., `text-sm`, `text-base`, `text-lg`, `text-xl`).

## 4. Component Structure

### Organization
- **`app/`**: Page and layout files following Next.js App Router conventions.
- **`components/ui/`**: Reusable primitives (Button, Input, Card, Modal, DataTable).
- **`components/`**: Feature-specific components (e.g., OrderForm, StatusBadge).
- **`lib/`**: Shared logic (auth client, database client).

### Reuse and Composition
- Build small UI primitives first (Input, Select).
- Compose them into higher-level components (OrderForm uses Input + Select + Button).
- Pass data and event handlers via props for flexibility.

### Benefits of Component-Based Architecture
- Single source of truth for styles and behavior.
- Easier testing of isolated components.
- Faster development: reuse existing pieces when building new pages.

## 5. State Management

### Approach
- **Server Components**: Fetch data at the server level for pages and pass as props.
- **Client Components**: Manage local UI state with React’s `useState`, `useEffect`.
- **Context API**: Provide global state for authenticated user info (UserContext) and theme settings if needed.

### Data Fetching
- Use Next.js’s `fetch()` in Server Components or `getServerSideProps` for dynamic data.
- For UI-driven fetches (e.g., filtering table), consider React Query or SWR for caching and revalidation.

### State Sharing
- **Auth Context**: Wrap the app in a provider that exposes `user`, `signIn`, `signOut`.
- **UI Context**: Manage global modals, toasts, or theme toggles.

## 6. Routing and Navigation

### Library
- Next.js App Router handles page routing based on the `/app` folder structure.
- `next/link` for client-side transitions with prefetching.
- `next/navigation` hooks (`useRouter`, `usePathname`) for programmatic navigation.

### Structure
- **Public Pages**: `/app/sign-in`, `/app/sign-up`.
- **Protected Pages**: `/app/dashboard`, `/app/orders`, `/app/customers`, `/app/employees`.
- Layouts (e.g., `/app/layout.tsx`) wrap protected areas with navigation bars and side menus.

### Role-Based Access
- Middleware or higher-order components check `user.role` and redirect unauthorized users to sign-in or “Not Authorized” pages.

## 7. Performance Optimization

### Built-in Next.js Features
- **Automatic Code Splitting**: Each page only loads its code and dependencies.
- **Image Optimization**: `next/image` for responsive, lazy-loaded images.
- **SSR/SSG**: Pre-render pages when data changes infrequently.

### Additional Strategies
- **Dynamic Imports**: Load heavy components (charts, map) only when needed.
- **Lazy Loading**: Use React’s `Suspense` and `dynamic()` import.
- **Asset Optimization**: Compress images and SVGs, minify JS/CSS via built-in optimizers.

## 8. Testing and Quality Assurance

### Unit Tests
- **Jest + React Testing Library**: Test individual components (Button, DataTable) for rendering and user interactions.

### Integration Tests
- Test component composition (OrderForm + API mocks) to ensure form submissions and validations work.

### End-to-End (E2E) Tests
- **Cypress or Playwright**: Automate critical user flows (sign-in, create order, check status).

### Linting and Formatting
- **ESLint**: Enforce code style and catch common errors.
- **Prettier**: Consistent code formatting.

## 9. Conclusion and Overall Frontend Summary

This frontend setup combines Next.js, React, TypeScript, Tailwind CSS, and shadcn/ui to deliver a fast, maintainable, and user-friendly application. Key takeaways:
- **Modular Architecture**: Clear folder structure and reusable components accelerate development.
- **Design for Users**: Usability, accessibility, and responsiveness are built in from day one.
- **Theming and Styling**: A cohesive color palette and modern flat design (with glassmorphism accents) ensure visual consistency.
- **Performance First**: Leveraging Next.js’s optimizations keeps the app fast across devices.
- **Quality Assurance**: A full testing strategy safeguards functionality and prevents regressions.

These guidelines ensure that anyone on the team—regardless of background—can understand, maintain, and extend the Money Laundry Manager frontend with confidence.