from database.db_connection import DbConnection



class MissionDB:
    def __init__(self, connection: DbConnection):
        self.connection = DbConnection()

    def create_mission(self, data):
        columns = list([str(key) for key in data])
        values = list([data[key] for key in data])
        conn = self.connection.get_connection()
        cursor = conn.cursor()
        sql = """
        INSERT INTO missions (%s) VALUES %s;
        """
        cursor.execute(sql, (columns, values))
        conn.commit()
        new_id = cursor.lastrowid
        cursor.execute("""
        SELECT * FROM missions WHERE id = %s """, new_id)
        new_mission = cursor.fetchone()
        cursor.close()
        conn.close()
        return new_mission

    def get_all_missions(self):
        conn = self.connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        sql = "SELECT * FROM missions;"
        try:
            cursor.execute(sql)
            rows = cursor.fetchall()
            return rows
        except Exception as e:
            return f"{e}"
        finally:
            cursor.close()
            conn.close()


    def get_mission_by_id(self, id):
        conn = self.connection.get_connection()
        cursor = conn.cursor(dictionary=True)
        sql = """SELECT * FROM missions WHERE id = %s;"""
        try:
            cursor.execute(sql, (id,))
            row = cursor.fetchone()
            return row
        except Exception as e:
            return f"{e}"
        finally:
            cursor.close()
            conn.close()

    def assign_mission(self, m_id, a_id):
        conn = self.connection.get_connection()
        cursor = conn.cursor()
        try:
            sql = """
            UPDATE missions SET assigned_agent_id = %s  WHERE id = %s;
            """
            cursor.execute(sql, (a_id, m_id))
            conn.commit()
            rowcount = cursor.rowcount
            return rowcount > 0
        except Exception as e:
            return f"{e}"
        finally:
            cursor.close()
            conn.close()


    def update_mission_status(self, id, status):
        conn = self.connection.get_connection()
        cursor = conn.cursor()
        try:
            sql = """
            UPDATE missions SET status = %s  WHERE id = %s;
            """
            cursor.execute(sql, (status, id))
            conn.commit()
            rowcount = cursor.rowcount
            return rowcount > 0
        except Exception as e:
            return f"{e}"
        finally:
            cursor.close()
            conn.close()


            

if __name__ == "__main__":
    mission_manager = MissionDB(DbConnection())
    print(mission_manager.get_all_missions())
    # print(mission_manager.assign_mission(1, 1))
    print(mission_manager.update_mission_status(1, 'ASSIGNED'))

    print(mission_manager.get_mission_by_id(1))


