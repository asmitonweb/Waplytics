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

## 🚀 Installation

Ensure you have a Frappe Bench with `frappe_whatsapp` installed.

1.  **Get the App**:
    ```bash
    bench get-app https://github.com/asmitonweb/waplytics
    ```
2.  **Install on Site**:
    ```bash
    bench --site [your-site.com] install-app waplytics
    ```
3.  **Migrate (Important)**:
    ```bash
    bench --site [your-site.com] migrate
    ```

---

## 📖 User Guide

### 1. Link Tracking (The "Magic")
Waplytics automatically shortens URLs in your WhatsApp messages to track clicks and assign UTM parameters.

**How it works:**
1.  Compose a message in `frappe_whatsapp` (or any app that writes to `Wa Message Log`).
2.  Include a standard link, e.g., `https://myshop.com/product`.
3.  **Waplytics intercepts the save**:
    -   Generates a short link: `https://yoursite.com/l/AbCd12`.
    -   Appends default UTMs: `?utm_source=whatsapp&utm_medium=waplytics`.
    -   Replaces the long link in the message body.
4.  The user receives the short link. When they click, we log the **IP** and **User Agent** before redirecting them.

**Manual creation:**
You can also manually create shortened links:
1.  Go to **Wa Link Tracker** list.
2.  Click **New**.
3.  Enter the **Original URL**.
4.  Save.
5.  Copy the **Short Code** or constructed URL.

### 2. Analytics Dashboard
View your performance at a glance.

1.  Search for **"Waplytics Dashboard"** in the awesome bar.
2.  **Charts available**:
    -   **Message Status**: Live breakdown of Sent vs. Delivered vs. Read vs. Failed.
    -   **Engagement Funnel**: Visualizes the drop-off from Reading to Clicking (CTR).

### 3. Campaign Attribution (Coming Soon)
In Phase 2, we will link these clicks directly to Sales Orders to show you the exact Revenue per Message.

---

## 🛠️ Configuration
No complex configuration needed.
-   **UTM Defaults**: Configure default `utm_source` and `utm_medium` in `Wa Link Tracker` (currently hardcoded to `whatsapp`/`waplytics` but customizable in code).

## Troubleshooting
-   **Redirect 404?** Ensure your site's Nginx/Supervisor is running and `bench migrate` was successful.
-   **No Stats?** Ensure `frappe_whatsapp` webhooks are correctly receiving status updates from Meta.
