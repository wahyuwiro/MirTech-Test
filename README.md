# Mirtech Test – Monorepo (FastAPI + Next.js)

A high-performance full-stack monorepo project featuring a FastAPI backend and a Next.js frontend. Designed for scalability, low-latency responses (sub-100ms), and modern UI/UX. Built with Docker Compose for seamless local development and deployment.

---

## 📦 Tech Stack

- **Backend**: FastAPI, PostgreSQL, Redis
- **Frontend**: Next.js (App Router) with TypeScript
- **UI**: TailwindCSS
- **Dev Tools**: Docker Compose, Axios, ESLint, Pydantic v2
- **Database**: Seeded with 100,000+ records (products, users, orders, transactions)

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/mirtech-test.git
cd mirtech-test
```

### 2. Setup Docker (recommended)

Ensure Docker Desktop is installed and running. Then simply:
```bash
docker-compose up --build
```
This will:
- Start the PostgreSQL and Redis services
- Launch the FastAPI backend on http://localhost:8000
- Launch the Next.js frontend on http://localhost:3000

### 3. Backend: FastAPI
✅ Features:
- High-speed filtering, pagination, and sorting (sub-100ms)
- Caching with Redis
- Seed data generation for:
   - 100,000 Products
   - 1,000 Users
   - 10,000 Orders
   - 50,000 Transactions
 
### 4. Frontend: Next.js (TypeScript)
✅ Features:
- Products table with server data (via Axios)
- Pagination
- Responsive, modern UI with TailwindCSS

**Hot Reloading (Dev mode):**
For smooth frontend development with auto-refresh:
```bash
cd frontend
npm install
npm run dev
```
(We recommend using this mode instead of Docker for FE development due to faster reloads.)

### ⚙️ Performance Optimizations
- **Database Indexing:** (To be implemented) for optimized queries
- **Redis Caching:** Frequently accessed queries are cached
- **Pagination & Sorting:** All handled via query params for large datasets
- **Docker Compose:** Streamlined multi-service orchestration

### 🧠 Architecture Decisions
- **Monorepo** structure simplifies shared configuration and deployments
- **FastAPI** chosen for async support, blazing fast APIs
- **Next.js** with App Router enables flexible frontend pages + API handling
- **PostgreSQL** for relational consistency and performance
- **Redis** for caching and performance tuning

### 💡 UI/UX Considerations
- Clean and responsive layout using TailwindCSS
- Focus on fast data rendering, especially for large datasets
- Minimal navigation with clear endpoints (/products, etc.)

### 🔍 What I'd Improve with More Time
With more time, I would:
- Implement full CRUD operations for all entities (Users, Orders, Transactions)
- Add JWT authentication to secure API access
- Enable full-text search and advanced filters
- Implement a loading skeleton and error state UI
- Write unit/integration tests for backend and frontend

### 📂 Directory Structure
```bash
mirtech-test/
├── backend/           # FastAPI project
│   ├── main.py
│   ├── models/
│   ├── schemas/
│   └── ...
├── frontend/          # Next.js (App Router) frontend
│   ├── src/app/
│   ├── tailwind.config.ts
│   └── ...
├── docker-compose.yml
└── README.md
```


