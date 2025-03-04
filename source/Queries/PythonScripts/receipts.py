import json
import mysql.connector
from datetime import datetime
import uuid


conn = mysql.connector.connect(
    host="localhost",
    user="Your Username",
    password="Your Password",
    database="world"
)
cursor = conn.cursor()

cursor.execute("""
  create table Receipts (
    ReceiptID varchar(50) primary key,
    BonusPointsEarned int,
    BonusPointsEarnedReason text,
    CreateDate datetime,
    DateScanned datetime,
    FinishedDate datetime,
    ModifyDate datetime,
    PointsAwardedDate datetime,
    PointsEarned varchar(10),
    PurchaseDate datetime,
    PurchasedItemCount int,
    RewardsReceiptStatus varchar(50),
    TotalSpent decimal(10,2),
    UserID varchar(50)
    );
""")

cursor.execute("""
  create table ReceiptItems (
    ReceiptItemID varchar(50) primary key,
    ReceiptID varchar(50),
    Barcode varchar(50),
    Description text,
    FinalPrice decimal(10,2),
    ItemPrice decimal(10,2),
    PartnerItemID varchar(50),
    QuantityPurchased int,
    UserFlaggedBarcode varchar(50),
    UserFlaggedNewItem boolean,
    UserFlaggedPrice decimal(10,2),
    UserFlaggedQuantity int,
    NeedsFetchReview boolean,
    BrandCode varchar(50),
    foreign key (ReceiptID) references Receipts(ReceiptID)
  );
""")
file_path = r'C:/Users/Ramya Ravikanti/Documents/Assignment_fetch/TestData/receipts.json'
receipts = []

with open(file_path, 'r', encoding='utf-8') as f:
    for line in f:
        receipts.append(json.loads(line.strip()))

for receipt in receipts:
    cursor.execute("""
        insert into Receipts(
            ReceiptID, BonusPointsEarned, BonusPointsEarnedReason, CreateDate, DateScanned, 
            FinishedDate, ModifyDate, PointsAwardedDate, PointsEarned, PurchaseDate, PurchasedItemCount, 
            RewardsReceiptStatus, TotalSpent, UserID
        ) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        receipt['_id']['$oid'],
        receipt.get('bonusPointsEarned', 0),
        receipt.get('bonusPointsEarnedReason', None),
        datetime.fromtimestamp(receipt['createDate']['$date'] / 1000),
        datetime.fromtimestamp(receipt['dateScanned']['$date'] / 1000),
        datetime.fromtimestamp(
            receipt.get('finishedDate', {}).get('$date', 0) / 1000) if 'finishedDate' in receipt else None,
        datetime.fromtimestamp(receipt['modifyDate']['$date'] / 1000),
        datetime.fromtimestamp(
            receipt.get('pointsAwardedDate', {}).get('$date', 0) / 1000) if 'pointsAwardedDate' in receipt else None,

        receipt.get('pointsEarned', "0"),
        datetime.fromtimestamp(receipt.get('purchaseDate', {}).get('$date', 0) / 1000) if 'purchaseDate' in receipt else None,
        receipt.get('purchasedItemCount', 0),
        receipt.get('rewardsReceiptStatus', "UNKNOWN"),
        receipt.get('totalSpent', "0.00"),
        receipt.get('userId', "UNKNOWN")
    ))


for receipt in receipts:
    receipt_id = receipt['_id']['$oid']
    for item in receipt.get('rewardsReceiptItemList', []):  # Handle missing items safely
        cursor.execute("""
            insert into ReceiptItems (
                ReceiptItemID, ReceiptID, Barcode, Description, FinalPrice, ItemPrice, 
                PartnerItemID, QuantityPurchased, UserFlaggedBarcode, UserFlaggedNewItem, 
                UserFlaggedPrice, UserFlaggedQuantity, NeedsFetchReview, BrandCode
            ) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            str(uuid.uuid4()),  # Generate a unique ID if missing
            receipt_id,
            item.get('barcode', "UNKNOWN"),
            item.get('description', "NO DESCRIPTION"),
            item.get('finalPrice', "0.00"),
            item.get('itemPrice', "0.00"),
            item.get('partnerItemId', "UNKNOWN"),
            item.get('quantityPurchased', 1),
            item.get('userFlaggedBarcode', None),
            item.get('userFlaggedNewItem', False),
            item.get('userFlaggedPrice', None),
            item.get('userFlaggedQuantity', 1),
            item.get('needsFetchReview', False),
            item.get('brandcode',None)
        ))


conn.commit()
cursor.close()
conn.close()

print(" Data successfully inserted into MySQL.")
