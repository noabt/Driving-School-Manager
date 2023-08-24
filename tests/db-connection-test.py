import unittest
import mysql.connector

class TestMySQLConnection(unittest.TestCase):

    def test_mysql_connection(self):
        try:
            connection = mysql.connector.connect(
                host='172.17.0.2',  
                user='root',  
                password='noabt2410',  
                database='dsm'  
            )

            self.assertTrue(connection.is_connected())
            connection.close()
        except mysql.connector.Error as err:
            self.fail(f"Failed to connect to MySQL: {err}")

if __name__ == '__main__':
    unittest.main()
