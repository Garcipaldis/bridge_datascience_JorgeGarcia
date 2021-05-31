import os, sys
import pymysql

utils_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(utils_path)
print(utils_path)

from utils.folders_tb import read_json

settings_file = utils_path + os.sep + "utils" + os.sep + "sql_settings.json"

json = read_json(fullpath=settings_file)

IP_DNS = json["IP_DNS"]
PORT = json["PORT"]
USER = json["USER"]
PASSWORD = json["PASSWORD"]
BD_NAME = json["BD_NAME"]

class MySQL:

    def __init__(self, IP_DNS, USER, PASSWORD, BD_NAME, PORT):
        self.IP_DNS = IP_DNS
        self.USER = USER
        self.PASSWORD = PASSWORD
        self.BD_NAME = BD_NAME
        self.PORT = PORT
        self.SQL_ALCHEMY = 'mysql+pymysql://' + self.USER + ':' + self.PASSWORD + '@' + self.IP_DNS + ':' + str(self.PORT) + '/' + self.BD_NAME
        # 'mysql+pymysql://user:password@91.76.54.33:20001/apr_july_2021_tb'
    def connect(self):
        # Open database connection
        self.db = pymysql.connect(host=self.IP_DNS,
                                user=self.USER, 
                                password=self.PASSWORD, 
                                database=self.BD_NAME, 
                                port=self.PORT)
        # prepare a cursor object using cursor() method
        self.cursor = self.db.cursor()
        print("Connected to MySQL server [" + self.BD_NAME + "]")
        return self.db

    def close(self):
        # disconnect from server
        self.db.close()
        print("Close connection with MySQL server [" + self.BD_NAME + "]")
    
    def execute_interactive_sql(self, sql, delete=False):
        """ NO SELECT """
        result = 0
        try:
            # Execute the SQL command
            self.cursor.execute(sql)
            # Commit your changes in the database
            self.db.commit()
            print("Executed \n\n" + str(sql) + "\n\n successfully")
            result = 1
        except Exception as error:
            print(error)
            # Rollback in case there is any error
            self.db.rollback()
        return result
        
    def execute_get_sql(self, sql):
        """SELECT"""
        results = None
        print("Executing:\n", sql)
        try:
            # Execute the SQL command
            self.cursor.execute(sql)
            # Fetch all the rows in a list of lists.
            results = self.cursor.fetchall()
        except Exception as error:
            print(error)
            print ("Error: unable to fetch data")
        
        return results

    def get_columns(self, df):
        columns = [col.upper() for col in df.columns]
        string_col = '('
        for col in columns:
            if col == columns[-1]:
                string_col += col
            else:
                string_col += col + ', '
        return string_col

    def generate_insert_into_row_sql(self, table, df, row):
        """
        This must be modified according to the table structure
            - table: Table name in string format
            - df: Dataframe from which to extract the columns.
            - row: values.
        """
        values = ''
        for i, value in enumerate(row):
            if i == len(row)-1:
                values += value
            else:
                values += value + ', '

        string_col = self.get_columns(df)
        
        sql = f"""INSERT INTO {table}
            ({string_col})
            VALUES
            ({values})"""

        sql = sql.replace("\n", "").replace("            ", " ")
        return sql

    def generate_create_table(self, table, df):
        pass

if __name__ == '__main__':
    driver = MySQL(IP_DNS, USER, PASSWORD, BD_NAME, PORT)
    driver.connect()
    sql = """CREATE TABLE base ID INT NOT NULL AUTO_INCREMENT 
    netflix_id INT NOT NULL, netflix_rating FLOAT(24) NOT NULL, 
    number_of_votes INT NOT NULL, title VARCHAR(255) NOT NULL, 
    year VARCHAR(255) NOT NULL, rated VARCHAR(255) NOT NULL, 
    released VARCHAR(255) NOT NULL, runtime VARCHAR(255) NOT NULL, 
    genre VARCHAR(255) NOT NULL, director VARCHAR(255) NOT NULL, 
    writer VARCHAR(255) NOT NULL, actors VARCHAR(255) NOT NULL, 
    plot VARCHAR(255) NOT NULL, language VARCHAR(255) NOT NULL, 
    country VARCHAR(255) NOT NULL, awards VARCHAR(255) NOT NULL, 
    poster VARCHAR(255) NOT NULL, ratings VARCHAR(255) NOT NULL, 
    metascore FLOAT(24) NOT NULL, imdbrating FLOAT(24) NOT NULL, 
    imdbvotes VARCHAR(255) NOT NULL, imdbid VARCHAR(255) NOT NULL, 
    type VARCHAR(255) NOT NULL"""
    driver.execute_interactive_sql(sql)