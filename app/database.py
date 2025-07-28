import mysql.connector
import os
from dotenv import load_dotenv


load_dotenv()

mydb = mysql.connector.connect(
  host=os.getenv('HOST'),
  user=os.getenv('USER'),
  password=os.getenv('PASSWORD')
)

print(mydb)