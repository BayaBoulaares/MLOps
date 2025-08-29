# Import necessary libraries
import pandas as pd  # To handle data in tabular form
import numpy as np   # To generate random data
import matplotlib.pyplot as plt

# Step 1: Define the number of users and products
# Let's assume we have 1000 users and 500 products in our ecommerce platform.
num_users = 1000
num_products = 500

# Step 2: Generating the Users Data
# Each user has an ID, age, gender, and location.
user_data = {
    'user_id': np.arange(1, num_users + 1),  # Generate user IDs from 1 to 1000
    'age': np.random.randint(18, 70, size=num_users),  # Random ages between 18 and 70
    'gender': np.random.choice(['M', 'F'], size=num_users),  # Randomly assign gender as Male (M) or Female (F)
    'location': np.random.choice(['Urban', 'Suburban', 'Rural'], size=num_users)  # Randomly assign location type
}

# Convert the user data dictionary into a pandas DataFrame
users_df = pd.DataFrame(user_data)

# Step 3: Generating the Products Data
# Each product has an ID, category, price, and rating.
product_data = {
    'product_id': np.arange(1, num_products + 1),  # Generate product IDs from 1 to 500
    'category': np.random.choice(['Electronics', 'Clothing', 'Home', 'Books'], size=num_products),  # Randomly assign product category
    'price': np.round(np.random.uniform(5, 500, size=num_products), 2),  # Random prices between $5 and $500, rounded to 2 decimal places
    'rating': np.round(np.random.uniform(1, 5, size=num_products), 1)  # Random ratings between 1 and 5, rounded to 1 decimal place
}

# Convert the product data dictionary into a pandas DataFrame
products_df = pd.DataFrame(product_data)

# Step 4: Generating the User-Product Interaction Data (Purchase History or Ratings)
# We simulate how users interact with products. For example, users can rate or buy products.

interaction_data = {
    'user_id': np.random.choice(users_df['user_id'], size=5000),  # Randomly select users who interacted with products
    'product_id': np.random.choice(products_df['product_id'], size=5000),  # Randomly select products that were interacted with
    'rating': np.random.randint(1, 6, size=5000),  # Assign random ratings (1 to 5 stars) for these interactions
    'timestamp': pd.date_range(start='2023-01-01', periods=5000, freq='T')  # Generate random timestamps for interactions, 1 minute apart
}

# Convert the interaction data dictionary into a pandas DataFrame
interactions_df = pd.DataFrame(interaction_data)

# Let's check the first few rows of each dataset
users_df.head(), products_df.head(), interactions_df.head()


# Save datasets to CSV files
users_df.to_csv("users.csv", index=False)
products_df.to_csv("products.csv", index=False)
interactions_df.to_csv("interactions.csv", index=False)

# -------------------------------
# 📊 Visualization
# -------------------------------

# Histogramme des âges des utilisateurs
plt.figure(figsize=(7, 5))
plt.hist(users_df['age'], bins=15, color='skyblue', edgecolor='black')
plt.title("Distribution des âges des utilisateurs")
plt.xlabel("Âge")
plt.ylabel("Nombre d'utilisateurs")
plt.grid(True)
plt.show()

# Histogramme des prix des produits
plt.figure(figsize=(7, 5))
plt.hist(products_df['price'], bins=20, color='orange', edgecolor='black')
plt.title("Distribution des prix des produits")
plt.xlabel("Prix ($)")
plt.ylabel("Nombre de produits")
plt.grid(True)
plt.show()

# Nombre d’interactions par note (rating)
plt.figure(figsize=(6, 5))
interactions_df['rating'].value_counts().sort_index().plot(kind='bar', color='green')
plt.title("Répartition des notes dans les interactions")
plt.xlabel("Note donnée (1-5)")
plt.ylabel("Nombre d'interactions")
plt.grid(True)
plt.show()
