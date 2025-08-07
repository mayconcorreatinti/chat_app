import os 
import mysql.connector
from dotenv import load_dotenv


load_dotenv()

class Mysqldb:
    
  def __init__(self):
    self._host = os.getenv('HOST')
    self._user = os.getenv('USER')
    self._password = os.getenv('PASSWORD')
    self._database = os.getenv('DATABASE')
    self.conn = self._connection()

  def _connection(self):
    return mysql.connector.connect(
      user = self._user,
      password = self._password,
      host = self._host,
      database = self._database, 
    )

  def _query(self,query:str,data=None) -> bool | list[dict]:
    if not self.conn.is_connected():
      self.conn = self._connection()
    
    with self.conn.cursor(dictionary=True) as cursor:
      cursor.execute(query,data)
      response = cursor.fetchall()
      if data:
        self.conn.commit()
      return response
  
  def select_user_from_table(self,data:tuple,column='email') -> list[dict]:
    return self._query(f"SELECT * FROM users WHERE name = (%s) or {column} = (%s) LIMIT 1;",data)
  
  def select_users_from_table(self) -> list[dict]:
    return self._query("SELECT * FROM users LIMIT 35;")

  def insert_user_from_table(self,data:tuple) -> bool:
    return self._query("INSERT INTO users(name,email,password) VALUES (%s,%s,%s);",data)
    
  def delete_user_from_table(self,data:tuple) -> bool:
    return self._query("DELETE FROM users WHERE id = (%s);",data)



