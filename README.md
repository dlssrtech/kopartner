# KoPartner Clone + Admin/Client/Partner Panels

This project now includes:
- Public marketing homepage clone (`/`)
- Login page (`/login.html`)
- Admin dashboard (`/admin.html`)
- Client dashboard (`/client.html`)
- Partner dashboard (`/partner.html`)
- SQLite database (auto-created at `db/kopartner.db`)
- REST APIs under `/api/*`

## Run
```bash
npm start
```

## Demo credentials
- `admin@kopartner.in` / `admin123`
- `client@kopartner.in` / `client123`
- `partner@kopartner.in` / `partner123`

## Waste Collection Platform Blueprint

A detailed operations-first flow and panel design for the proposed multi-country waste collection marketplace is available in [`docs/waste-collection-platform-flow-design.md`](docs/waste-collection-platform-flow-design.md). It covers the recommended Next.js web panels, Node.js backend modules, PostgreSQL/PostGIS database design, SMS booking, MoMo payments, sack inventory, manual dispatch, future auto-assignment, and phased development plan.

