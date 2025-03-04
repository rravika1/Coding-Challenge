import json
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="Your Username",
    password="Your Password",
    database="world"
)
cursor = conn.cursor()

cursor.execute("""
    create table Brands (
        BrandID varchar(50) primary key,
        Brandcode varchar(50),
        Barcode varchar(50),
        Category varchar(100),
        CategoryCode varchar(100),
        CpgID varchar(50),
        TopBrand boolean, 
        Name varchar(255)  
    );
""")

with open(r'C:/Users/Ramya Ravikanti/Documents/Assignment_fetch/TestData/brands.json', 'r', encoding='utf-8') as f:
    for line in f:
        brand = json.loads(line)

        brand_id = brand['_id']['$oid']
        brand_code = brand.get('brandCode', None)
        barcode = brand.get('barcode', None)
        category = brand.get('category', None)
        category_code = brand.get('categoryCode', None)
        cpg_id = brand.get('cpg', {}).get('$id', {}).get('$oid', None)
        name = brand.get('name', None)
        top_brand = brand.get('topBrand', False)

        cursor.execute("""
            insert ignore into Brands (BrandID, brandcode, Barcode, Category, CategoryCode, CpgID, TopBrand, Name)
            values (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            brand_id,
            brand_code,
            barcode,
            category,
            category_code,
            cpg_id,
            top_brand,
            name
        ))

conn.commit()
cursor.close()
conn.close()

print("Brands data inserted successfully.")
