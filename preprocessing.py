# Import necessary libraries for pre-processing
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Charger les datasets générés
users_df = pd.read_csv("users.csv")
products_df = pd.read_csv("products.csv")
interactions_df = pd.read_csv("interactions.csv")



# Step 1: Handle missing values
# Checking for missing values in all datasets
print("Missing values in users data:\n", users_df.isnull().sum())
print("Missing values in products data:\n", products_df.isnull().sum())
print("Missing values in interactions data:\n", interactions_df.isnull().sum())

# Step 2: Encoding categorical variables
label_encoder = LabelEncoder()

# Encode the gender column in users data (M -> 0, F -> 1)
users_df['gender_encoded'] = label_encoder.fit_transform(users_df['gender'])

# Encode the location column in users data
users_df['location_encoded'] = label_encoder.fit_transform(users_df['location'])

# Encode the category column in products data
products_df['category_encoded'] = label_encoder.fit_transform(products_df['category'])

# Step 3: Create a User-Product Rating Matrix
user_product_matrix = interactions_df.pivot_table(index='user_id', columns='product_id', values='rating').fillna(0)

# Step 4: Train-test split
train_data, test_data = train_test_split(interactions_df, test_size=0.2, random_state=42)

# Display the first few rows of the pre-processed data to verify
print("User-Product Matrix:\n", user_product_matrix.head())
print("Train Data Sample:\n", train_data.head())
print("Test Data Sample:\n", test_data.head())
