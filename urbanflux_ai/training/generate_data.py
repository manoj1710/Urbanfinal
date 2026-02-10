import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

# Ensure directories exist
os.makedirs("data/raw", exist_ok=True)
os.makedirs("data/processed", exist_ok=True)
os.makedirs("models", exist_ok=True) # Ensure models dir exists too

NUM_ROWS = 1500

def generate_datasets():
    print("Generating synthetic datasets...")

    # 1. Product Batches
    products = ['Tomato', 'Milk', 'Onion', 'Meat', 'Fish']
    types = {'Tomato': 'Fresh', 'Milk': 'Chilled', 'Onion': 'Fresh', 'Meat': 'Chilled', 'Fish': 'Chilled'}
    qualities = ['A', 'B', 'C']
    cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix']
    
    data_batches = []
    for i in range(NUM_ROWS):
        prod = random.choice(products)
        produced_date = datetime.now() - timedelta(days=random.randint(1, 10))
        # Shelf life depends on product
        shelf_life = 5 if prod in ['Fish', 'Meat'] else (7 if prod == 'Milk' else 14)
        expiry_date = produced_date + timedelta(days=shelf_life)
        
        data_batches.append({
            'batch_id': f'B-{1000+i}',
            'product_name': prod,
            'product_type': types[prod],
            'quality_grade': random.choice(qualities),
            'produced_date': produced_date.strftime('%Y-%m-%d'),
            'expiry_date': expiry_date.strftime('%Y-%m-%d'),
            'quantity': random.randint(50, 500),
            'storage_type': 'Refrigerated' if types[prod] == 'Chilled' else 'Ambient',
            'city': random.choice(cities)
        })
    
    df_batches = pd.DataFrame(data_batches)
    df_batches.to_csv("data/raw/product_batches.csv", index=False)
    print(f"saved data/raw/product_batches.csv ({len(df_batches)} rows)")

    # 2. Transport Routes
    route_types = ['direct', 'warehouse']
    data_routes = []
    for i in range(NUM_ROWS):
        dist = random.randint(10, 500)
        data_routes.append({
            'route_id': f'R-{1000+i}',
            'batch_id': f'B-{1000+i}',
            'distance_km': dist,
            'estimated_time_hours': round(dist / random.randint(40, 80), 2),
            'route_type': random.choice(route_types)
        })
    df_routes = pd.DataFrame(data_routes)
    df_routes.to_csv("data/raw/transport_routes.csv", index=False)
    print(f"saved data/raw/transport_routes.csv ({len(df_routes)} rows)")

    # 3. Traffic Data
    data_traffic = []
    for city in cities:
        for _ in range(50): # Multiple records per city to simulate different times/zones
            data_traffic.append({
                'city': city,
                'congestion_level': random.choice(['Low', 'Medium', 'High']),
                'delay_factor': round(random.uniform(0.8, 2.5), 2)
            })
    df_traffic = pd.DataFrame(data_traffic)
    df_traffic.to_csv("data/raw/traffic_data.csv", index=False)
    print(f"saved data/raw/traffic_data.csv ({len(df_traffic)} rows)")

    # 4. Warehouse Inventory
    data_inventory = []
    for i in range(NUM_ROWS):
        days_in_storage = random.randint(0, 10)
        # Freshness degrades with time
        base_freshness = 100 - (days_in_storage * random.uniform(2, 10))
        data_inventory.append({
            'batch_id': f'B-{1000+i}',
            'current_freshness': max(0, round(base_freshness, 1)),
            'days_in_storage': days_in_storage,
            'temperature': round(random.uniform(2, 25), 1),
            'humidity': round(random.uniform(30, 90), 1)
        })
    df_inventory = pd.DataFrame(data_inventory)
    df_inventory.to_csv("data/raw/warehouse_inventory.csv", index=False)
    print(f"saved data/raw/warehouse_inventory.csv ({len(df_inventory)} rows)")

    # 5. Customer Demand
    data_demand = []
    for prod in products:
        for city in cities:
            data_demand.append({
                'product_name': prod,
                'city': city,
                'demand_score': random.randint(40, 100)
            })
    df_demand = pd.DataFrame(data_demand)
    df_demand.to_csv("data/raw/customer_demand.csv", index=False)
    print(f"saved data/raw/customer_demand.csv ({len(df_demand)} rows)")

if __name__ == "__main__":
    generate_datasets()
