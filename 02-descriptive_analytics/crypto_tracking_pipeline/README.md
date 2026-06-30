# ⚡ Automated Crypto Data Warehouse & Analytics Pipeline

An end-to-end automated ETL pipeline that extracts live market tracking metrics, structures them inside a relational localized data warehouse, and streams flattened snapshots to a live cloud reporting dashboard.

## 🔗 Live Project Links
* **Interactive Analytics Dashboard:** [View Live Looker Studio Report](https://datastudio.google.com/reporting/2d193c5e-fdde-4091-b0c5-63badaebd7b2)

## 🛠️ Tech Stack & Architecture
* **Language:** Python 3.x
* **Data Source:** CoinGecko Developer REST API
* **Storage & Layering:** Relational Schema (Fact & Dimension tracking via SQLite Data Warehouse)
* **Orchestration:** Cloud automation via GitHub Actions workflows (Cron triggers)
* **Presentation Layer:** Google Sheets Cloud Layer & Looker Studio Engine

## 🚀 Key Features & Engineering Implementation
* **Automated Extraction (ETL):** Developed a modular Python engine to interface with external REST APIs, handling rate limits and parsing raw JSON responses into clean structural data frames.
* **Data Warehousing:** Designed a relational tracking warehouse (`crypto_warehouse.db`) to log chronological asset prices, volume fluctuations, and market capitalization shifts.
* **CI/CD Cloud Orchestration:** Deployed a automated workflow using GitHub Actions. The runner awakens on a daily cron schedule, executes the ingestion scripts, handles localized binary states, and commits a clean flattened analytical snapshot view (`dashboard_clean_snapshot.csv`) straight to production.
* **Data Delivery:** Linked the flattened presentation views directly into a cloud reporting ecosystem, using parsed timestamp dimensions to create live interactive charts.

## ⏱️ How It Is Real-Time (Automation Flow)
While traditional dashboards require manual data uploads, this pipeline is completely hands-off:
1. **Cloud Trigger:** A GitHub Actions runner automatically wakes up on a daily cron schedule.
2. **Live Extraction:** The Python script hits the live CoinGecko REST API to fetch up-to-the-minute market metrics.
3. **Database Sink:** The script updates the SQLite localized data warehouse (`crypto_warehouse.db`) and overwrites the flat snapshot file.
4. **Instant Stream:** Google Sheets instantly fetches the updated cloud snapshot file using `IMPORTDATA`, which dynamically repopulates your Looker Studio visuals without you ever opening your laptop.