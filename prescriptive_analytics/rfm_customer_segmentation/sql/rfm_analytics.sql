-- ====================================================================
-- Enterprise Customer Intelligence: RFM Metric Aggregation & Ranking
-- Target: Black Friday Transactional Data
-- Engine: DuckDB / ANSI SQL Compatible
-- ====================================================================

WITH raw_transactions AS (
    -- Step 1: Ingest and clean transaction data, handling null product categories
    SELECT 
        User_ID AS customer_id,
        Product_ID AS product_id,
        Gender AS gender,
        Age AS age_group,
        Occupation AS occupation_code,
        City_Category AS city_tier,
        Stay_In_Current_City_Years AS residency_duration,
        Marital_Status AS marital_status,
        COALESCE(Product_Category_1, 0) AS category_1,
        COALESCE(Product_Category_2, 0) AS category_2,
        COALESCE(Product_Category_3, 0) AS category_3,
        CAST(Purchase AS DOUBLE) AS purchase_amount
    FROM read_csv_auto('prescriptive_analytics/rfm_customer_segmentation/data/black_friday_dataset.csv')
    WHERE User_ID IS NOT NULL
      AND Purchase > 0
),

customer_aggregations AS (
    -- Step 2: Compute Frequency (total items) and Monetary (total spend) per customer
    SELECT 
        customer_id,
        gender,
        age_group,
        city_tier,
        residency_duration,
        COUNT(product_id) AS total_orders,
        COUNT(DISTINCT product_id) AS unique_products_bought,
        ROUND(SUM(purchase_amount), 2) AS total_monetary_spend,
        ROUND(AVG(purchase_amount), 2) AS avg_basket_value,
        ROUND(MAX(purchase_amount), 2) AS max_single_purchase
    FROM raw_transactions
    GROUP BY 
        customer_id,
        gender,
        age_group,
        city_tier,
        residency_duration
),

customer_rankings AS (
    -- Step 3: Apply Window Functions to calculate percentiles and spend tiers
    SELECT 
        *,
        DENSE_RANK() OVER (ORDER BY total_monetary_spend DESC) AS revenue_rank,
        NTILE(5) OVER (ORDER BY total_monetary_spend DESC) AS monetary_tier_quantile,
        NTILE(5) OVER (ORDER BY total_orders DESC) AS frequency_tier_quantile
    FROM customer_aggregations
)

-- Step 4: Final output with business segment classifications
SELECT 
    customer_id,
    gender,
    age_group,
    city_tier,
    total_orders,
    total_monetary_spend,
    avg_basket_value,
    revenue_rank,
    monetary_tier_quantile,
    frequency_tier_quantile,
    CASE 
        WHEN monetary_tier_quantile = 1 AND frequency_tier_quantile = 1 THEN 'Tier 1: High-Volume VIP'
        WHEN monetary_tier_quantile = 1 AND frequency_tier_quantile > 1 THEN 'Tier 2: High-Value Whales'
        WHEN monetary_tier_quantile BETWEEN 2 AND 3 THEN 'Tier 3: Core Regulars'
        WHEN monetary_tier_quantile = 4 THEN 'Tier 4: Occasional Buyers'
        ELSE 'Tier 5: Low-Spend / Churn-Risk'
    END AS customer_lifecycle_segment
FROM customer_rankings
ORDER BY total_monetary_spend DESC;