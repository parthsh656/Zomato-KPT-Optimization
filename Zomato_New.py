import pandas as pd
import numpy as np
import random

np.random.seed(42)
random.seed(42)

NUM_ROWS = 3000
NUM_MERCHANTS = 300

# 1. Geographic & Merchant Setup
cities = ['Bengaluru', 'Mumbai', 'Delhi', 'Hyderabad', 'Pune', 'Chennai', 'Kolkata', 'Jaipur', 'Ahmedabad', 'Bhilwara']

prefixes = ['The', 'Royal', 'Spicy', 'Golden', 'Grand', 'Classic', 'Urban', 'Desi', 'Shree', 'Bombay']
cuisines = ['Biryani', 'Tandoor', 'Dosa', 'Bake', 'Grill', 'Cafe', 'Dhaba', 'Kitchen', 'Chaat', 'Wok']
suffixes = ['House', 'Point', 'Darbar', 'Junction', 'Corner', 'Hub', 'Palace', 'Story', 'Express', 'Lounge']

restaurant_names = set()
while len(restaurant_names) < NUM_MERCHANTS:
    name = f"{random.choice(prefixes)} {random.choice(cuisines)} {random.choice(suffixes)}"
    restaurant_names.add(name)
restaurant_names = list(restaurant_names)

merchants = pd.DataFrame({
    'Merchant_ID': [f'M_{str(i).zfill(3)}' for i in range(1, NUM_MERCHANTS + 1)],
    'Restaurant_Name': restaurant_names,
    'City': np.random.choice(cities, NUM_MERCHANTS),
    'Tier': np.random.choice(['Tier 1', 'Tier 2', 'Tier 3'], NUM_MERCHANTS, p=[0.15, 0.35, 0.50]),
    'Inherent_Reliability': np.random.beta(a=2, b=2, size=NUM_MERCHANTS)
})

# 2. Cuisine & Dish Complexity Catalog
menu_catalog = [
    {'Cuisine': 'Biryani', 'Dish_Name': 'Hyderabadi Mutton Biryani', 'Base_Time': 20},
    {'Cuisine': 'Biryani', 'Dish_Name': 'Chicken Dum Biryani', 'Base_Time': 18},
    {'Cuisine': 'North Indian', 'Dish_Name': 'Paneer Butter Masala & Naan', 'Base_Time': 15},
    {'Cuisine': 'North Indian', 'Dish_Name': 'Dal Makhani Combo', 'Base_Time': 12},
    {'Cuisine': 'South Indian', 'Dish_Name': 'Masala Dosa', 'Base_Time': 8},
    {'Cuisine': 'South Indian', 'Dish_Name': 'Idli Vada Set', 'Base_Time': 5},
    {'Cuisine': 'Fast Food', 'Dish_Name': 'Zinger Burger & Fries', 'Base_Time': 10},
    {'Cuisine': 'Fast Food', 'Dish_Name': 'Peri Peri Pizza', 'Base_Time': 14},
    {'Cuisine': 'Chinese', 'Dish_Name': 'Hakka Noodles', 'Base_Time': 10},
    {'Cuisine': 'Beverages', 'Dish_Name': 'Cold Coffee', 'Base_Time': 4},
    {'Cuisine': 'Desserts', 'Dish_Name': 'Choco Lava Cake', 'Base_Time': 6}
]
menu_df = pd.DataFrame(menu_catalog)

# 3. Generate Orders
orders = pd.DataFrame({
    'Order_ID': [f'ORD_{str(i).zfill(4)}' for i in range(1, NUM_ROWS + 1)],
    'Merchant_ID': np.random.choice(merchants['Merchant_ID'], NUM_ROWS)
})

order_dishes = menu_df.sample(n=NUM_ROWS, replace=True).reset_index(drop=True)
orders = pd.concat([orders, order_dishes], axis=1)
df = pd.merge(orders, merchants, on='Merchant_ID')

# 4. Simulate Live Rush (Chaos Index)
df['POS_Tickets'] = np.where(df['Tier'] == 'Tier 1', np.random.randint(10, 30, NUM_ROWS),
                             np.where(df['Tier'] == 'Tier 2', np.random.randint(2, 12, NUM_ROWS), 0))

df['Acoustic_dB'] = 60 + (df['POS_Tickets'] * 1.5) + np.random.normal(0, 3, NUM_ROWS)
df['Acoustic_dB'] = df['Acoustic_dB'].clip(upper=95).round(1)

df['Chaos_Index'] = 1.0 + (df['POS_Tickets'] * 0.05) + ((df['Acoustic_dB'] - 60) * 0.02)
df['Chaos_Index'] = df['Chaos_Index'].round(2)

# 5. FIXING THE TIME-TRAVEL BUG
# First, calculate when the food is ACTUALLY sitting on the counter ready to go.
df['Actual_Food_Ready_Mins'] = (df['Base_Time'] * df['Chaos_Index']).clip(lower=3).round(1)

# Dishonest merchants mark FOR early to trick the system.
gap = (1 - df['Inherent_Reliability']) * np.random.uniform(5, 15, NUM_ROWS)
df['Manual_FOR_Mins'] = (df['Actual_Food_Ready_Mins'] - gap).clip(lower=2).round(1)

# The system dispatches the rider based on the (often fake) Manual FOR.
# Rider arrives some time after dispatch.
df['Rider_Arrival_Mins'] = (df['Manual_FOR_Mins'] + np.random.uniform(3, 8, NUM_ROWS)).round(1)

# RIDER DEPARTURE STRICT LOGIC:
# The rider cannot leave until the food is ready AND they are physically present.
df['Rider_Depart_Mins'] = np.maximum(df['Actual_Food_Ready_Mins'], df['Rider_Arrival_Mins']).round(1)

# Wait time is now perfectly logical (Departure - Arrival)
df['Actual_Rider_Wait_Mins'] = (df['Rider_Depart_Mins'] - df['Rider_Arrival_Mins']).round(1)

# 6. The ETL Transform Logic
# Trust Score evaluates the gap between when they SAID it was ready, and when the rider actually left with it.
df['Gap'] = df['Rider_Depart_Mins'] - df['Manual_FOR_Mins']
df['Trust_Score'] = np.maximum(0.1, 1.0 - (df['Gap'] / 15)).round(2)

df['Adjusted_KPT_Signal'] = (df['Trust_Score'] * df['Manual_FOR_Mins']) + \
                            ((1 - df['Trust_Score']) * df['Rider_Depart_Mins'])
df['Adjusted_KPT_Signal'] = df['Adjusted_KPT_Signal'].round(2)

# Cleanup and arrange columns logically
final_df = df[['Order_ID', 'Merchant_ID', 'Restaurant_Name', 'City', 'Tier',
               'Cuisine', 'Dish_Name', 'Base_Time',
               'Acoustic_dB', 'POS_Tickets', 'Chaos_Index',
               'Manual_FOR_Mins', 'Actual_Food_Ready_Mins', 'Rider_Arrival_Mins',
               'Rider_Depart_Mins', 'Actual_Rider_Wait_Mins',
               'Trust_Score', 'Adjusted_KPT_Signal']].sort_values('Order_ID').reset_index(drop=True)

final_df.to_csv('zomato_kpt_enhanced_dataset.csv', index=False)
print("Successfully generated 3000 rows. Time paradoxes resolved!")
