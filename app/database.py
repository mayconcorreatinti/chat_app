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

  def _querie(self,query:str,data=None) -> bool | list[tuple]:
    if not self.conn.is_connected():
      self.conn = self.__connection()
    
    with self.conn.cursor() as cursor:
      cursor.execute(query,data)
      response = cursor.fetchall()
      if data:
        self.conn.commit()
        return True
      return response
    
  def select_users_into_table(self) -> list[tuple]:
    return self._querie('SELECT * FROM users LIMIT 35;')

  def insert_user_into_table(self,data:tuple) -> bool:
    return self._querie('INSERT INTO users VALUES (%s,%s,%s,%s);',data)
    
  def delete_user_into_table(self,data:tuple) -> bool:
    return self._querie("DELETE FROM users WHERE id = (%s)",data)

