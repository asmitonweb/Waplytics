# Roadmap: Ultimate Open-Source WhatsApp Analytics for Frappe

## 🎯 Goal
Build the **fastest, most robust** open-source campaign and tracking engine for the Frappe/ERPNext ecosystem.
**Philosophy:** "Capture Everything, Query Instantly."

## 🏗️ Technical Architecture (The "Fastest" Stack)
To achieve "absolute maximum data" tracking without slowing down your ERP, we will use a **Hybrid Architecture**.

1.  **Control Plane (Frappe Framework / Python):**
    *   **Role:** User Interface, Campaign creation, Contact management, Authentication.
    *   **Why:** seamless integration with your existing ERPNext data.
2.  **Data Plane (ClickHouse):**
    *   **Role:** Storing millions of tracking logs (Sent, Delivered, Read, Clicked).
    *   **Why:** It is 100-1000x faster than MariaDB/PostgreSQL for analytics queries. It enables real-time dashboards on massive datasets.
3.  **Ingestion Engine (Go or Rust):**
    *   **Role:** A microservice that receives Webhooks from Meta and writes them to ClickHouse immediately.
    *   **Why:** Handling thousands of webhooks per second without crashing your ERP.

---

## 🗺️ The Journey (Phases)

### Phase 1: The Foundation (System Design & Setup)
**Objective:** Set up the high-performance infrastructure.
- [ ] **Infrastructure Setup:**
    -   Install **ClickHouse** (Docker).
    -   Install **Redis** (for queuing).
- [ ] **Frappe App ("Wapi Analytics"):**
    -   Create a new Frappe App.
    -   Create DocTypes: `WaCampaign`, `WaTemplate`, `WaLinkTracker`.
- [ ] **Ingestion Service:**
    -   Write a small **Go** (Golang) server to accept `POST /webhook` from Meta.
    -   Benchmark it to handle 1k req/sec.

### Phase 2: "Absolute" Data Tracking
**Objective:** Track every micro-interaction.
- [ ] **Status Tracking:**
    -   Capture `Sent`, `Delivered`, `Read` timestamps with millisecond precision.
    -   Calculate "Time to Open" (Read Time - Delivered Time).
- [ ] **Link Tracking (The Magic):**
    -   Build a URL Shortener service inside the app (`wapi.link/xyz`).
    -   When sending a message, replace links with short links.
    -   **Track:** Device Type (Mobile/Desktop), OS (iOS/Android), IP Location.
- [ ] **Session Tracking:**
    -   Track distinct "Conversation Sessions" (when a user replies).

### Phase 3: The Campaign Engine
**Objective:** Easy-to-start, reliable bulk sending.
- [ ] **Audience Builder:**
    -   SQL-based segment builder (e.g., "Customers who bought X but not Y").
- [ ] **Smart Throttling:**
    -   Implement a "Token Bucket" algorithm in Redis to respect WhatsApp limits (e.g., send exactly 75 msg/sec).
- [ ] **A/B Testing Support:**
    -   Split campaign 50/50 with different specific templates.

### Phase 4: Visualization (The "Expert" Dashboard)
**Objective:** Beautiful, real-time insights.
- [ ] **Dashboard Tech:** Use **Frappe UI** (Vue.js) + **Apache ECharts**.
- [ ] **Key Metrics:**
    -   🔥 Real-time "Live View" (like Google Analytics Realtime).
    -   Cohort Analysis: "Do users who receive msg A buy more than msg B?"
    -   Funnel Visualization: Sent -> Delivered -> Read -> Clicked -> Replied.
