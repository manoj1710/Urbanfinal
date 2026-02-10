import pandas as pd
import numpy as np
import os
from datetime import datetime

def preprocess_data(
    batches_path="data/raw/product_batches.csv",
    routes_path="data/raw/transport_routes.csv",
    inventory_path="data/raw/warehouse_inventory.csv",
    traffic_path="data/raw/traffic_data.csv",
    demand_path="data/raw/customer_demand.csv",
    output_path="data/processed/merged_training_data.csv"
):
    # Ensure processed directory exists
    os.makedirs("data/processed", exist_ok=True)
    
    print("Preprocessing data...")
    
    # Check if files exist
    if not os.path.exists(batches_path):
        print(f"Error: {batches_path} not found. Run generate_data.py first.")
        return

    # Load raw data
    df_batches = pd.read_csv(batches_path)
    df_routes = pd.read_csv(routes_path)
    df_inventory = pd.read_csv(inventory_path)
    df_traffic = pd.read_csv(traffic_path)
    df_demand = pd.read_csv(demand_path)

    # Merge Data
    # 1. Merge Batches with Routes (on batch_id)
    df = pd.merge(df_batches, df_routes, on="batch_id", how="left")
    
    # 2. Merge with Inventory (on batch_id)
    df = pd.merge(df, df_inventory, on="batch_id", how="left")
    
    # 3. Merge with Traffic (on city)
    traffic_agg = df_traffic.groupby('city').agg({
        'delay_factor': 'mean',
        'congestion_level': lambda x: pd.Series.mode(x)[0]
    }).reset_index()
    df = pd.merge(df, traffic_agg, on="city", how="left")
    
    # 4. Merge with Demand (on product_name and city)
    df = pd.merge(df, df_demand, on=["product_name", "city"], how="left")
    
    # Feature Engineering
    
    # Calculate shelf_life_days & days_used
    df['produced_date'] = pd.to_datetime(df['produced_date'])
    df['expiry_date'] = pd.to_datetime(df['expiry_date'])
    df['shelf_life_days'] = (df['expiry_date'] - df['produced_date']).dt.days
    
    df['days_used'] = df['days_in_storage']
    
    # Calculate expiry_urgency
    df['days_remaining'] = df['shelf_life_days'] - df['days_used']
    df['expiry_urgency'] = np.where(df['days_remaining'] <= 2, 1, 0)
    
    # Spoilage Risk Score Logic
    def calculate_spoilage_risk(row):
        risk_score = 0
        if row['storage_type'] == 'Refrigerated' and row['temperature'] > 5:
            risk_score += (row['temperature'] - 5) * 5
        if row['delay_factor'] > 1.5:
            risk_score += 20
        if row['current_freshness'] < 50:
            risk_score += 30
        
        if risk_score < 20: return "Low"
        elif risk_score < 50: return "Medium"
        else: return "High"

    df['spoilage_risk'] = df.apply(calculate_spoilage_risk, axis=1)

    # Priority Score Logic
    raw_priority = (df['demand_score'] * 0.4) + (df['current_freshness'] * 0.3) - (df['distance_km'] * 0.01)
    df['priority_score'] = np.clip(raw_priority / 10, 0, 10).round(1)

    # Save processed data
    df.to_csv(output_path, index=False)
    print(f"saved {output_path} ({len(df)} rows)")

if __name__ == "__main__":
    preprocess_data()
