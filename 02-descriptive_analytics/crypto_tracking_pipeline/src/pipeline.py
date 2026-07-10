import os
import sqlite3
import time
from datetime import datetime, timedelta
import pandas as pd
import requests

ASSET_IDS = ["bitcoin", "ethereum", "solana", "cardano", "ripple"]

def get_missing_date_range(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(date_id) FROM fact_market_status")
    result = cursor.fetchone()[0]
    
    if not result:
        print("Database empty. Initializing 90-day backfill...")
        start_date = datetime.now() - timedelta(days=90)
    else:
        # last_date represents the latest day we have data for
        last_date = datetime.strptime(str(result), "%Y%m%d")
        # To ensure we catch updates throughout the day or get the next day's interval,
        # we start collecting right from that last date forward.
        start_date = last_date
        
    end_date = datetime.now()
    
    # Simple check to make sure our start date makes logical sense
    if start_date.date() > end_date.date():
        return None, None
        
    start_unix = int(time.mktime(start_date.replace(hour=0, minute=0, second=0).timetuple()))
    end_unix = int(time.mktime(end_date.replace(hour=23, minute=59, second=59).timetuple()))
    return start_unix, end_unix

def run_etl():
    print(f"--- Starting ETL Run: {datetime.now()} ---")
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, "data", "crypto_warehouse.db")
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dim_assets (
            id TEXT PRIMARY KEY,
            name TEXT,
            symbol TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fact_market_status (
            id TEXT,
            date_id INTEGER,
            current_price REAL,
            market_cap REAL,
            total_volume REAL,
            extracted_at TEXT,
            PRIMARY KEY (id, date_id),
            FOREIGN KEY (id) REFERENCES dim_assets(id)
        )
    """)
    
    static_assets = [
        ("bitcoin", "Bitcoin", "btc"),
        ("ethereum", "Ethereum", "eth"),
        ("solana", "Solana", "sol"),
        ("cardano", "Cardano", "ada"),
        ("ripple", "Ripple", "xrp")
    ]
    cursor.executemany("INSERT OR IGNORE INTO dim_assets VALUES (?, ?, ?)", static_assets)
    conn.commit()

    start_unix, end_unix = get_missing_date_range(conn)
    if start_unix is None:
        print("Database is already up to date according to date validation logic.")
        conn.close()
        return

    all_records = []
    for coin in ASSET_IDS:
        print(f"Fetching data for {coin}...")
        url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart/range"
        params = {"vs_currency": "usd", "from": start_unix, "to": end_unix}
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            prices = data.get("prices", [])
            market_caps = data.get("market_caps", [])
            total_volumes = data.get("total_volumes", [])
            
            daily_groups = {}
            for i in range(len(prices)):
                ts = prices[i][0]
                dt = datetime.fromtimestamp(ts / 1000.0)
                date_key = dt.strftime("%Y%m%d")
                
                # Using INSERT OR REPLACE allows us to overwrite data rows safely with fresh values
                daily_groups[date_key] = {
                    "id": coin,
                    "date_id": int(date_key),
                    "current_price": prices[i][1],
                    "market_cap": market_caps[i][1] if i < len(market_caps) else 0,
                    "total_volume": total_volumes[i][1] if i < len(total_volumes) else 0,
                    "extracted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            all_records.extend(daily_groups.values())
            time.sleep(2) # Avoid public API rate limits
        except Exception as e:
            print(f"Failed to fetch data for {coin}: {e}")
            continue

    if all_records:
        for rec in all_records:
            cursor.execute("""
                INSERT OR REPLACE INTO fact_market_status (id, date_id, current_price, market_cap, total_volume, extracted_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (rec["id"], rec["date_id"], rec["current_price"], rec["market_cap"], rec["total_volume"], rec["extracted_at"]))
        conn.commit()

    # Generate flattened data structure for visualization tools
    query_flat = """
    SELECT fact.date_id, dim.name AS asset_name, dim.symbol AS ticker, fact.current_price, fact.market_cap, fact.total_volume
    FROM fact_market_status fact
    JOIN dim_assets dim ON fact.id = dim.id;
    """
    df_dashboard = pd.read_sql_query(query_flat, conn)
    csv_export_path = os.path.join(base_dir, "data", "dashboard_clean_snapshot.csv")
    df_dashboard.to_csv(csv_export_path, index=False)
    print(f"Local files synchronized successfully.")

    # =========================================================================
    # PRODUCTION SECURITY LAYER: DYNAMIC CLOUD SYNCHRONIZATION VIA WEBHOOK
    # =========================================================================
    print("Initiating streaming synchronization to Tableau Cloud Bridge...")
    
    # Securely retrieve target URL from environment variables to prevent credentials exposure in source control
    web_app_url = os.environ.get("TABLEAU_WEBHOOK_URL")
    
    if not web_app_url:
        print("CRITICAL: TABLEAU_WEBHOOK_URL variable is absent. Aborting cloud matrix sync layer.")
    else:
        # Structure payload dynamically as a structured text matrix
        payload = [df_dashboard.columns.tolist()] + df_dashboard.fillna("").values.tolist()
        
        try:
            response = requests.post(web_app_url, json=payload, timeout=30)
            if response.status_code == 200:
                print("Tableau Cloud Bridge data sync executed successfully.")
            else:
                print(f"Cloud Bridge sync rejected payload with status code: {response.status_code}")
        except Exception as e:
            print(f"Failed to stream transmission payload to Cloud Bridge endpoint: {e}")

    conn.close()

if __name__ == "__main__":
    run_etl()