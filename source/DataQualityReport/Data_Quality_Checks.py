import mysql.connector
import pandas as pd

conn = mysql.connector.connect(
    host="localhost",
    user="Your Username",
    password="Your SQL Password",
    database="world"
)

users_query = "select * from users"
receipts_query = "select * from receipts"
brands_query = "select * from brands"
receiptitems_query = "select * from receiptitems"

users_df = pd.read_sql(users_query, conn)
receipts_df = pd.read_sql(receipts_query, conn)
brands_df = pd.read_sql(brands_query, conn)
receiptitems_df = pd.read_sql(receiptitems_query, conn)

#Checking for missing values in the tables
print("Missing values in users table:")
print(users_df.isnull().sum())

print("\nMissing values in receipts table:")
print(receipts_df.isnull().sum())

print("\nMissing values in brands table:")
print(brands_df.isnull().sum())

print("\nMissing values in receiptitems table:")
print(receiptitems_df.isnull().sum())

#Checking for duplicate entries in the tables
print("\nDuplicate entries in users table:")
print(users_df.duplicated().sum())

print("\nDuplicate entries in receipts table:")
print(receipts_df.duplicated().sum())

print("\nDuplicate entries in brands table:")
print(brands_df.duplicated().sum())

print("\nDuplicate entries in receiptitems table:")
print(receiptitems_df.duplicated().sum())

#Check for invalid or inconsistent data types
print("\nData types in users table:")
print(users_df.dtypes)

print("\nData types in receipts table:")
print(receipts_df.dtypes)

print("\nData types in brands table:")
print(brands_df.dtypes)

print("\nData types in receiptitems table:")
print(receiptitems_df.dtypes)

# Checking for outliers or unexpected values
print("\nOutliers in receipts table (negative values in 'TotalSpent' and 'QuantityPurchased'):")
print(receipts_df[(receipts_df['TotalSpent'] < 0) | (receipts_df['PurchasedItemCount'] < 0)])

#Checking for potential data integrity issues, such as missing required fields
print("\nUsers with missing required fields:")
required_columns_users = ['UserID', 'CreatedDate', 'LastLogin']
missing_data_users = users_df[required_columns_users].isnull().sum()
print(missing_data_users[missing_data_users > 0])

print("\nReceipts with missing required fields:")
required_columns_receipts = ['ReceiptID', 'DateScanned', 'TotalSpent', 'UserID']
missing_data_receipts = receipts_df[required_columns_receipts].isnull().sum()
print(missing_data_receipts[missing_data_receipts > 0])

print("\nBrands with missing required fields:")
required_columns_brands = ['BrandID', 'Name']
missing_data_brands = brands_df[required_columns_brands].isnull().sum()
print(missing_data_brands[missing_data_brands > 0])



conn.close()
