# Data Analytics Portfolio

Hi! I'm a Data Analyst focused on translating raw data into actionable business insights through interactive dashboards, predictive modeling, and automated data pipelines.

---

## Project Portfolio

### 01. Exploratory Data Analysis

* **[Zomato Bangalore Market Analysis](01-EDA/zomato/)**
    * **The Problem & Solution:** Evaluated market penetration for 51,000+ restaurants. Developed a Python preprocessing pipeline that optimized memory usage by 98% and engineered robust missing-value logic, paired with an interactive Power BI dashboard tracking regional market drivers.
    * **Data Source:** [Kaggle Zomato Bangalore Restaurants Dataset](https://www.kaggle.com/datasets/himanshupoddar/zomato-bangalore-restaurants)
    * **Tech Stack:** Python, Pandas, NumPy, Seaborn, Matplotlib, Power BI Desktop, DAX

* **[HR Analytics Dashboard](01-EDA/hr_analytics/)**
    * **The Problem & Solution:** Explored corporate workforce data to uncover hidden retention trends and employee distributions, packaging the operational insights into a clean, intuitive business intelligence layout.
    * **Data Source:** [Kaggle HR Analytics Dataset](https://www.kaggle.com/datasets/saadharoon27/hr-analytics-dataset)
    * **Tech Stack:** Power BI, Power Query, Python, Pandas

---

### 02. Descriptive Analytics & Automation

* **[Automated Crypto Data Warehouse Pipeline](02-descriptive_analytics/crypto_tracking_pipeline/)**
    * **The Problem & Solution:** Built a lightweight, hands-off infrastructure to monitor volatile assets. This end-to-end pipeline extracts live market metrics from a REST API, structures them into a relational SQLite warehouse via scheduled automation, and pipes snapshots to a cloud-hosted reporting layer.
    * **Data Source:** Live data streaming via the public [CoinGecko REST API v3](https://docs.coingecko.com/docs/keyless-public-api) endpoint.
    * **Tech Stack:** Python, SQLite, GitHub Actions (CI/CD Cron), Google Sheets Cloud Layer, Looker Studio
    * **Live Report:** [View Live Interactive Report](https://datastudio.google.com/reporting/2d193c5e-fdde-4091-b0c5-63badaebd7b2)

---

### 03. Prescriptive Analytics & Modeling

* **[Enterprise Customer Intelligence Engine](03-prescriptive_analytics/rfm_customer_segmentation/)**
    * **The Problem & Solution:** Segmented 5,891 high-volume holiday shoppers to target marketing spend. Designed an end-to-end data pipeline using K-Means clustering based on RFM metrics (Recency, Frequency, Monetary value) and purchase diversity, complete with a dynamic Streamlit data-slicing interface.
    * **Data Source:** [Kaggle Black Friday Sales Dataset](https://www.kaggle.com/datasets/syedhaideralizaidi/black-friday-dataset)
    * **Tech Stack:** Python, Scikit-Learn, Streamlit, Plotly, Pandas
    * **Live Application:** [Interact with the Live Engine](https://dataanalyticsportfolio-6j2wrbykyotmshnqpd8ic4.streamlit.app/)
