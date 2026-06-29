import pandas as pd

df = pd.read_csv('data/black_friday_dataset.csv')

rfm = df.groupby('User_ID').agg({
    'Purchase': ['count', 'sum']
}).reset_index()

rfm.columns = ['customer_id', 'frequency', 'monetary']

rfm['r_score'] = pd.qcut(rfm['frequency'].rank(method='first'), q=5, labels=[5,4,3,2,1], duplicates='drop')
rfm['f_score'] = pd.qcut(rfm['frequency'], q=5, labels=[1,2,3,4,5], duplicates='drop')
rfm['m_score'] = pd.qcut(rfm['monetary'], q=5, labels=[1,2,3,4,5], duplicates='drop')

rfm['segment'] = rfm.apply(lambda x: 
    'Champions' if x['r_score'] >= 4 and x['f_score'] >= 4 else
    'Loyal' if x['r_score'] >= 3 and x['f_score'] >= 3 else
    'At Risk' if x['r_score'] <= 2 else
    'Potential' if x['f_score'] <= 2 else 'Lost', axis=1)

rfm.to_csv('dashboard/rfm_segments.csv', index=False)

print(rfm['segment'].value_counts())
print("RFM saved to dashboard/rfm_segments.csv")