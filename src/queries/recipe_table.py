from typing import Dict
from mysql.connector.connection_cext import CMySQLConnection
from src.queries.base import BaseModel

class Recipe(BaseModel):
    __table__: str = "recipes"
    
    def __init__(self, db_connection: CMySQLConnection) -> None:
        super().__init__(db_connection)
        
    def _initialization_query(self) -> str:
        query = """CREATE TABLE IF NOT EXISTS recipes (
            id int NOT NULL AUTO_INCREMENT,
            title varchar(255) NOT NULL,
            image_url varchar(255),
            about text,
            making_time varchar(255),
            ingredients text,
            making_steps text,
            PRIMARY KEY(id)
        );
        """
        
        return query 


