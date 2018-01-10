import sqlite3
import traceback
import sys
from models import Person, Queue

class DBdao(object):
    """ Інтерфейс для доступу до бази даних """
    db_name = 'database.db'
    @staticmethod
    def get_connection():
        return sqlite3.connect(DBdao.db_name)

    @staticmethod
    def _add_person(person):
        try:
            conn = DBdao.get_connection()
            c = conn.cursor()
            attr = (person.id, person.first_name, person.last_name)
            c.execute("INSERT INTO person VALUES (?, ?, ?)", attr)
            conn.commit()
        except Exception as ignored:
            print('Person not added')
        finally:
            conn.close()


    @staticmethod
    def _add_queue(queue):
        try:
            conn = DBdao.get_connection()
            c = conn.cursor()
            c.execute("INSERT INTO queue (name) VALUES (?)", (queue.name,))
            conn.commit()
            conn.close()
            return True
        except Exception as ignored:
            print('Queue not added')
            conn.close()
            return False


    @staticmethod
    def get_queue_id(queue):
        try:
            conn = DBdao.get_connection()
            c = conn.cursor()
            c.execute("""SELECT qid FROM queue WHERE name=?""", (queue.name,))
            return c.fetchone()[0]
        except Exception as ignored:
            pass
        finally:
            conn.close()


    @staticmethod
    def get_queue(id):
        try:
            conn = DBdao.get_connection()
            c = conn.cursor()
            c.execute("""SELECT name FROM queue WHERE qid=?""", (id,))
            return Queue(c.fetchone()[0], id)
        except Exception as ignored:
            pass
        finally:
            conn.close()


    @staticmethod
    def add_order(person, queue):
        try:
            DBdao._add_person(person)
            conn = DBdao.get_connection()
            c = conn.cursor()
            c.execute("SELECT MAX(no) FROM q_order WHERE qid=?", (queue.id,))
            maximum = c.fetchone()[0]
            if maximum is None:
                no = 0
            else:
                no = maximum + 1
            attr = (queue.id, person.id, no)
            c.execute("INSERT INTO q_order (qid, pid, no) VALUES (?, ?, ?)", attr)
            conn.commit()
        except Exception as ignored:
            traceback.print_exc(file=sys.stdout)
            print('Order not added')
        finally:
            conn.close()
        

    @staticmethod
    def get_order(queue):
        try:
            conn = DBdao.get_connection()
            c = conn.cursor()
            rows_count = c.execute("""SELECT no, p.pid, first_name, last_name
                FROM q_order o INNER JOIN person p ON o.pid = p.pid
                WHERE o.qid=?
                ORDER BY 1""", (queue.id,))
            return c.fetchall()
        except Exception as ignored:
            pass
        finally:
            conn.close()


    @staticmethod
    def get_queue_count():
        try:
            conn = DBdao.get_connection()
            c = conn.cursor()
            c.execute("""SELECT COUNT(*) FROM queue;""")
            return c.fetchone()[0]
        except Exception as ignored:
            pass
        finally:
            conn.close()
        
