import os 
import mysql.connector
from dotenv import load_dotenv


load_dotenv()

class Mysqldb:
    
  def __init__(self):
    self.__host = os.getenv('HOST')
    self.__user = os.getenv('USER')
    self.__password = os.getenv('PASSWORD')
    self.__database = os.getenv('DATABASE')
    self.conn = self.__connection()

  def __connection(self):
    return mysql.connector.connect(
      user = self.__user,
      password = self.__password,
      host = self.__host,
      database = self.__database, 
    )

  def queries(self,query:str,data:tuple=None):
    if not self.conn.is_connected():
      self.conn = self.__connection()
    
    with self.conn.cursor() as cursor:
      if data:
        cursor.execute(query,data)
        self.conn.commit()
        return True
      else:
        cursor.execute(query)
        response = cursor.fetchall()
        return response
      
a=Mysqldb()
print(a.queries('insert into users values (%s,%s,%s,%s)',('default','joao','mfdsaf@gmail.com','fgsdds')))