# ⚡ Automated Crypto Data Warehouse & Analytics Pipeline

An end-to-end automated ETL pipeline that extracts live market tracking metrics, structures them inside a relational localized data warehouse, and streams flattened snapshots securely to a live cloud reporting dashboard.

## 🔗 Live Project Links
* **Interactive Analytics Dashboard:** [View Live Tableau Report](https://public.tableau.com/app/profile/samruddhi.naykodi/viz/DynamicCryptoAnalyticsWarehouse/Dashboard1#1)

---

## 🛠️ Tech Stack & Architecture
* **Language:** Python 3.10+ (Pandas, Requests)
* **Data Source:** CoinGecko Developer REST API
* **Storage & Layering:** Relational Schema (Fact & Dimension tracking via SQLite Data Warehouse)
* **Orchestration:** Cloud automation via GitHub Actions workflows (Cron triggers on Ubuntu runners)
* **Presentation Layer:** Google Sheets Cloud Bridge & Tableau Public

---

## 🚀 Key Features & Engineering Implementation
* **Automated Extraction (ETL):** Developed a modular Python engine to interface with external REST APIs, handling public rate limits seamlessly and parsing raw JSON data arrays into clean tabular structures.
* **Data Warehousing:** Designed a star-schema relational tracking warehouse (`crypto_warehouse.db`) featuring separated Dimension (`dim_assets`) and Fact (`fact_market_status`) tables with structured primary/foreign keys to maintain historical data integrity.
* **CI/CD Cloud Orchestration:** Deployed a fully automated workflow using GitHub Actions. The runner initializes on a daily cron schedule at midnight, executes the ingestion scripts, handles localized binary states, and updates production files automatically.
* **Enterprise-Grade Secrets Management:** Implemented zero-trust parameter safeguards. Production webhook URLs and infrastructure keys are completely decoupled from source control, securely sealed inside GitHub's encrypted secrets engine, and injected into environmental memory only at runtime.

---

## ⏱️ Automated Pipeline Flow (Hands-Off Synchronization)
While traditional dashboards require manual data preparation and flat-file uploads, this infrastructure functions as a completely self-sustaining automated data loop:

1. **Cloud Trigger:** A GitHub Actions workflow automatically initializes on a daily cron schedule at midnight.
2. **Live Ingestion:** The hosted runner executes the Python script, querying the CoinGecko API to capture historical missing intervals and live tracking metrics.
3. **Warehouse Sink:** The pipeline processes changes, commits fresh rows into the localized SQLite analytical data warehouse, and generates a flattened analytical dataset.
4. **Secure Webhook Stream:** Python securely streams the updated matrix via a specialized `POST` network request to an obfuscated Google Apps Script microservice gateway. 
5. **Visual Canvas Presentation:** The gateway writes the data directly into your cloud repository (`crypto_warehouse_live`), allowing Tableau Public to detect the state transition and dynamically update your public visual layouts automatically.
6. **Cloud Trigger:** A GitHub Actions workflow automatically initializes on a daily cron schedule at midnight IST (capturing the finalized daily closing data for the elapsed date).