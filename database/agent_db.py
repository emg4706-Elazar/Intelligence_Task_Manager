from database.db_connection import DbConnection



class AgentDB:
    def __init__(self, connection: DbConnection):
        self.connection = DbConnection().get_connection()


    def create_agent(self, data):
        columns = list([str(key) for key in data])
        values = list([data[key] for key in data])
        conn = self.connection
        cursor = conn.cursor()
        sql = """
        INSERT INTO agents (%s) VALUES %s;
        """
        cursor.execute(sql, (columns, values))
        conn.commit()
        new_id = cursor.lastrowid
        cursor.execute("""
        SELECT * FROM agents WHERE id = %s """, new_id)
        new_agent = cursor.fetchone()
        cursor.close()
        conn.close()
        return new_agent

    def get_all_agents(self):
        conn = self.connection
        cursor = conn.cursor()
        sql = """SELECT * FROM agents;"""
        cursor.execute(sql)
        rows = cursor.fetchall()
        return rows

    def get_agent_by_id(self, id):
        conn = self.connection
        cursor = conn.cursor()
        sql = """SELECT * FROM agents WHERE id = %s;"""
        cursor.execute(sql, id)
        row = cursor.fetchone()
        return row

    def update_agent(self, id, data):
        columns = list([str(key) for key in data])
        values = list([data[key] for key in data])
        conn = self.connection
        cursor = conn.cursor()
        sql = """
        UPDATE agents (%s) VALUES %s WHERE id = %s;
        """
        cursor.execute(sql, (columns, values, id))
        conn.commit()
        rowcount = cursor.rowcount
        cursor.close()
        conn.close()
        return rowcount > 0



connection_db = DbConnection()
if __name__ == "__main__":
    age_manager = AgentDB(connection_db)
    data1 = {"name": "Moshe", "specialty": "tech", "agent_rank": "Junior"}
    print(age_manager.create_agent(data1))
