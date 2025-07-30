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

  def connection(self):
    return mysql.connector.connect(
      user = self.__user,
      password = self.__password,
      host = self.__host,
      database = self.__database, 
    )