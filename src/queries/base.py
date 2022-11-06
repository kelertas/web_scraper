from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple

from mysql.connector.connection_cext import CMySQLConnection

class BaseModel(ABC):
    __table__:Optional[str] = None
    
    
    def __init__(self, db_connection: CMySQLConnection) -> None:
        self._db_connection = db_connection
        self._create_table()
        
        
    def _create_table(self) -> None:
        query = self._initialization_query()
        cur = self._db_connection.cursor()
        cur.execute(query)
        return None

    
    @abstractmethod
    def _initialization_query(self) -> str:
        pass
    
    
    def get_all(self) -> List[Dict]:
        cur =  self._db_connection.cursor(dictionary=True)
        cur.execute(f"SELECT * FROM {self.__table__}")
        return [val for val in cur]
    
    
    def get_by_id(self, id: int) -> Dict:
        cur =  self._db_connection.cursor(dictionary=True)
        cur.execute(f"SELECT * FROM {self.__table__} WHERE id = {id}")
        return [val for val in cur][0]
    
    
    def insert(self, insert_values: Dict) -> Dict:
        cur = self._db_connection.cursor()
        
        insert_dimensions = ", ".join(
            [insert_title for insert_title in insert_values.keys()]
        )
        
        _insert_values = ", ".join(
            [f"'{insert_value}'" for insert_value in insert_values.values()]
        )
        
        query = f"""INSERT INTO {self.__table__}
            ({insert_dimensions}) values ({insert_values});
            """
        
        cur.execute(query)
        self._db_connection.commit()
        
        return self.get_by_id(cur.lastrowid)
    
    def update(self, update_values: Dict, id: int) -> Optional[Dict]:
        cur =   self._db_connection.cursor()
        
        update_query_values = ", ".join(
            [f"{key} = '{value}'" for key, value in update_values.items()]
        )
        
        query = f"""UPDATE {self.__table__} SET
            {update_query_values} WHERE id = {id};
        """
        cur.execute(query)
        affected_rows = cur.rowcount
        if affected_rows > 0:
            self._db_connection.commit()
            return self.get_by_id(id)
        return None
    
    
    def delete_by_id(self, id: int) -> bool:
        cur =   self._db_connection.cursor()
        query = f"""DELETE FROM {self.__table__} WHERE id = {id};
        """
        cur.execute(query)
        affected_rows = cur.rowcount
        if affected_rows > 0:
            self._db_connection.commit()
            return True
        return False        