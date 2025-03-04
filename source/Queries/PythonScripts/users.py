import json
import mysql.connector
from datetime import datetime

conn = mysql.connector.connect(
    host="localhost",
    user="Your Username",
    password="Your Password",
    database="world"
)
cursor = conn.cursor()

cursor.execute("""
    create or replace table Users (
        UserID varchar(50) primary key,
        Active boolean not null,
        CreatedDate datetime not null,
        LastLogin datetime not null,
        Role varchar(50),
        SignUpSource varchar(100),
        State varchar(10)
    );
""")

with open(r'C:/Users/Ramya Ravikanti/Documents/Assignment_fetch/TestData/users.json', 'r', encoding='utf-8') as f:
    for line in f:
        user = json.loads(line)
        user_id = user['_id']['$oid']
        active = user['active']

        created_date = datetime.fromtimestamp(
            user.get('createdDate', {}).get('$date', 0) / 1000) if 'createdDate' in user else None

        last_login = datetime.fromtimestamp(
            user.get('lastLogin', {}).get('$date', 0) / 1000) if 'lastLogin' in user else None

        role = user.get('role', None)
        sign_up_source = user.get('signUpSource', None)
        state = user.get('state', None)

        cursor.execute("""
            insert ignore into Users (UserID, Active, CreatedDate, LastLogin, Role, SignUpSource, State)
            values (%s, %s, %s, %s, %s, %s, %s)
        """, (
            user_id,
            active,
            created_date,
            last_login,
            role,
            sign_up_source,
            state
        ))
conn.commit()
cursor.close()
conn.close()

print("Data inserted successfully.")
