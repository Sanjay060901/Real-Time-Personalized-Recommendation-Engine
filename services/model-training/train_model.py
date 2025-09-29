# services/model-training/train_model.py
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import joblib


# read processed events parquet
df = pd.read_parquet('/data/delta/events')


# Build user-item matrix
user_item = df.pivot_table(index='user_id', columns='product_id', values='score', aggfunc='sum', fill_value=0)


# compute item-item similarity
item_matrix = user_item.T
sim = cosine_similarity(item_matrix)
sim_df = pd.DataFrame(sim, index=item_matrix.index, columns=item_matrix.index)


# Save similarity matrix for serving
joblib.dump(sim_df, '/data/models/item_sim.pkl')
print('Model saved to /data/models/item_sim.pkl')
