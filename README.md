# Waplytics 🚧 In Progress

**The Ultimate Open-Source WhatsApp Analytics Engine.**

## Mission
To build the fastest, most robust analytics and tracking tool for the Frappe/ERPNext ecosystem.
**Philosophy:** "Capture Everything, Query Instantly."

## Architecture (Phase 1)
- **Core Engine:** `frappe_whatsapp` (Handles Messaging & Webhooks)
- **Analytics Layer:** `waplytics` (Link Shortener, Enhanced Tracking, Dashboards)
- **Database:** MariaDB (Standard ERPNext DB)

## Project Structure
- `waplytics`: Custom Frappe App containing:
    - **Link Tracker**: `Wa Link Tracker` & `Wa Link Click`
    - **Dashboard**: `Waplytics Dashboard`
    - **Hooks**: Automatic URL shortening interceptor.

## Roadmap
See [Roadmap](./docs/roadmap.md) for detailed implementation plans.

## Installation
```bash
bench get-app waplytics --local [path-to-folder]
bench --site [your-site] install-app waplytics
```
