import os 
from mysql.connector.aio import connect
from dotenv import load_dotenv
import asyncio

load_dotenv()

class Mysqldb:
    
  def __init__(self):
    self._host = os.getenv('HOST')
    self._user = os.getenv('USER')
    self._password = os.getenv('PASSWORD')
    self._database = os.getenv('DATABASE')
    self.conn = None

  async def _connection(self):
    return await connect(
      user = self._user,
      password = self._password,
      host = self._host,
      database = self._database
    )
  
  async def _query(self,query:str,data=None) -> list:
    if not self.conn:
      self.conn = await self._connection()

    async with await self.conn.cursor(dictionary=True) as cursor:
      await cursor.execute(query,data)
      response = await cursor.fetchall()
      if data:
        await self.conn.commit()
      return response
  
  async def select_user_from_table(self,username:str,email:str = '') -> list[dict]:
    users = await self._query("""
      SELECT id,
        username,
        email,
        password
      FROM users
      WHERE username = (%s) or
      email = (%s)
      LIMIT 1;
      """,
      (username,email)
    )
    for user in users:
      return user
  
  async def select_users_from_table(self) -> list[dict]:
    return await self._query("""
        SELECT id,
          username,
          email,
          password
        FROM users 
        LIMIT 35;
      """
    )

  async def insert_user_from_table(self,data:tuple) -> None:
    await self._query("""
        INSERT INTO users(username,email,password)
        VALUES (%s,%s,%s);
      """,data
    )
  
  async def delete_user_from_table(self,data:tuple) -> None:
    await self._query("""
        DELETE FROM users 
        WHERE id = (%s);
      """,data
    )

db=Mysqldb()