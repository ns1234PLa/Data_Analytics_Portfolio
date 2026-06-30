import os
import sqlite3
from datetime import datetime
import pandas as pd
import requests

# API Endpoint Configuration
COINGECKO_URL = "https://api.coingecko.com/api/v3/coins/markets"
PARAMS = {
    "vs_currency": "usd",
    "ids": "bitcoin,ethereum,solana,cardano,ripple",
    "order": "market_cap_desc",
    "price_change_percentage": "24h"
}

def run_etl():
    print(f"--- Starting ETL Execution: {datetime.now()} ---")
    
    # Define paths relative to this script's position
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "data", "crypto_warehouse.db")
    
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    # EXTRACT: Fetch real-time market data
    try:
        response = requests.get(COINGECKO_URL, params=PARAMS)
        response.raise_for_status()
        raw_data = response.json()
        print("Data successfully pulled from CoinGecko API.")
    except Exception as e:
        print(f"Extraction step failed: {e}")
        return

    # TRANSFORM: Format, structure, and create audit trails
    df = pd.DataFrame(raw_data)
    columns_to_keep = [
        "id", "name", "symbol", "current_price", 
        "market_cap", "total_volume", "price_change_percentage_24h"
    ]
    df_cleaned = df[columns_to_keep].copy()
    
    # Standardize column mappings to match SQL naming guidelines
    df_cleaned.rename(columns={"price_change_percentage_24h": "price_change_24h"}, inplace=True)
    
    # Inject system data lineage metrics
    df_cleaned["extracted_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df_cleaned["date_id"] = int(datetime.now().strftime("%Y%m%d"))

    # LOAD: Relational Storage Operations (Star Schema Setup)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create Dimension Table (Asset Categorization Metadata)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dim_assets (
            id TEXT PRIMARY KEY,
            name TEXT,
            symbol TEXT
        )
    """)

    # Create Fact Table (Historical Transaction Metrics Logging)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fact_market_status (
            id TEXT,
            date_id INTEGER,
            current_price REAL,
            market_cap REAL,
            total_volume REAL,
            price_change_24h REAL,
            extracted_at TEXT,
            FOREIGN KEY (id) REFERENCES dim_assets(id)
        )
    """)

    # Populate Dimension Table 
    for _, row in df_cleaned.iterrows():
        cursor.execute("""
            INSERT OR REPLACE INTO dim_assets (id, name, symbol)
            VALUES (?, ?, ?)
        """, (row["id"], row["name"], row["symbol"]))

    # Populate Fact Table 
    for _, row in df_cleaned.iterrows():
        cursor.execute("""
            INSERT INTO fact_market_status (
                id, date_id, current_price, market_cap, total_volume, price_change_24h, extracted_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            row["id"], row["date_id"], row["current_price"], 
            row["market_cap"], row["total_volume"], row["price_change_24h"], 
            row["extracted_at"]
        ))

    conn.commit()
    print(f"Data loading complete. Database updated at: {db_path}")

    # AUTOMATED DASHBOARD EXPORT LAYER
    print("Generating flattened snapshot for Looker Studio...")
    query_flat = """
    SELECT 
        fact.date_id,
        dim.name AS asset_name,
        dim.symbol AS ticker,
        fact.current_price,
        fact.market_cap,
        fact.total_volume,
        fact.price_change_24h,
        fact.extracted_at
    FROM fact_market_status fact
    JOIN dim_assets dim ON fact.id = dim.id;
    """
    
    df_dashboard = pd.read_sql_query(query_flat, conn)
    csv_export_path = os.path.join(base_dir, "data", "dashboard_clean_snapshot.csv")
    df_dashboard.to_csv(csv_export_path, index=False)
    print(f"Flattened CSV generated successfully at: {csv_export_path}")
    
    conn.close()

if __name__ == "__main__":
    run_etl()