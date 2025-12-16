# Roadmap: Waplytics (Powered by frappe_whatsapp)

## 🎯 Goal
Build the **ultimate analytics & growth layer** for `frappe_whatsapp`, transforming it from a communication tool into a revenue engine.

## 🏗️ Architecture
- **Core Engine:** `frappe_whatsapp` (Connectivity).
- **Analytics Layer:** `waplytics` (Intelligence, Tracking, ROI).

---

## 🗺️ The Journey

### Phase 1: Insight & Tracking (The Foundation)
**Objective:** Gain visibility and ensure data quality.
- [x] **Link Shortener & Tracker:**
    -   Native URL shortener (`domain/l/xyz`).
    -   Track "Clicks" to calculate CTR (Click-Through Rate).
- [x] **Automatic UTM Builder:**
    -   Auto-append `?utm_source=whatsapp` to all links.
    -   Ensure Google Analytics/PostHog integration out of the box.
- [x] **Unified Dashboard:**
    -   Visualize `WA Message Log` data (Sent/Delivered/Read).
    -   Full Funnel: Sent -> Delivered -> Read -> Clicked.

### Phase 2: Revenue & Efficiency (The Growth Layer)
**Objective:** Link messages to money and save costs.
- [ ] **💰 Revenue Attribution:**
    -   Track which campaigns led to Sales Orders/invoices in ERPNext.
    -   Metric: "Revenue per 1k Messages".
- [ ] **🧹 Audience Hygiene (Ghost Protocol):**
    -   Auto-tag users who haven't read the last 5 messages.
    -   Exclude "Ghosts" from broadcasts to save API costs.
- [ ] **Smart Audience Builder:**
    -   Filter based on Buying History (e.g., "Bought X but not Y").

### Phase 3: Optimization Scale
**Objective:** Smarter, faster sending.
- [ ] **🕒 Intelligent Scheduling:**
    -   "Best Time to Send" based on historical read patterns.
- [ ] **A/B Testing:**
    -   Split audience 50/50 to test different templates/content.
- [ ] **ClickHouse Integration:**
    -   Offload massive logs (millions of rows) to ClickHouse for sub-second analytics.

### Phase 4: Automation & AI
- [ ] **Conversation Analysis:** Sentiment analysis on replies.
- [ ] **Auto-Replies:** Intent-based flow triggering.
