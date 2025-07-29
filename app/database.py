import mysql.connector
import os
from dotenv import load_dotenv


load_dotenv()

class Mysqldb:

  def __init__(self):
    self.host = os.getenv("HOST")
    self.user = os.getenv("USER")
    self.password = os.getenv("PASSWORD")
    self.database = os.getenv("DATABASE")
    self.conn = self.connect_db()

  def connect_db(self):
    return mysql.connector.connect(
      password = self.password,
      host = self.host,
      user = self.user,
      database = self.database
    )

  def execute_query(self,query:str,data):
    try:
      cursor = self.conn.cursor()
      cursor.execute(query,data)
    except mysql.connector.Error as e:
      raise f'error:{e}'
