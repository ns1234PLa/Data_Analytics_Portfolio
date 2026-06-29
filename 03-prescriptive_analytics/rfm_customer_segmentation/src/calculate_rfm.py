import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

data_path = '03-prescriptive_analytics/rfm_customer_segmentation/data/black_friday_dataset.csv'
df = pd.read_csv(data_path)
print("Production Pipeline: Dataset loaded successfully.")

df['Product_Category_2'] = df['Product_Category_2'].fillna(0).astype(int)
df['Product_Category_3'] = df['Product_Category_3'].fillna(0).astype(int)
df = df.drop_duplicates()

customer_df = df.groupby('User_ID').agg({
    'Product_ID': 'count',                 # Frequency
    'Purchase': 'sum',                     # Monetary
    'Product_Category_1': 'nunique'        # Category Diversity
}).reset_index()

customer_df.columns = ['customer_id', 'frequency', 'monetary', 'category_diversity']

scaler = StandardScaler()
features = ['frequency', 'monetary', 'category_diversity']
scaled_features = scaler.fit_transform(customer_df[features])

kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
customer_df['cluster'] = kmeans.fit_predict(scaled_features)

cluster_mapping = {
    2: 'Whales / VIPs',
    1: 'High-Value Loyals',
    3: 'Regulars',
    0: 'Casual Shoppers'
}
customer_df['segment_name'] = customer_df['cluster'].map(cluster_mapping)

# Export Final Deliverable
output_path = '03-prescriptive_analytics/rfm_customer_segmentation/dashboard/rfm_segments.csv'
customer_df.to_csv(output_path, index=False)
print(f"Production Pipeline Complete! Segmented customer profiles saved to: {output_path}")