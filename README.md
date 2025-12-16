# Waplytics

**The Ultimate Open-Source WhatsApp Analytics Engine.**

## Mission
To build the fastest, most robust analytics and tracking tool for the Frappe/ERPNext ecosystem.
**Philosophy:** "Capture Everything, Query Instantly."

## Architecture
- **Control Plane:** Frappe Framework (Python)
- **Data Plane:** ClickHouse (OLAP Database)
- **Ingestion:** Go (High-performance Webhook Listener)

## Project Structure
- `apps/wapi_analytics`: The Frappe App (UI & Logic)
- `services/ingest`: The Go Webhook Listener
- `docker`: Infrastructure (ClickHouse, Redis) configuration

## Roadmap
See [Roadmap](./docs/roadmap.md) for detailed implementation plans.
