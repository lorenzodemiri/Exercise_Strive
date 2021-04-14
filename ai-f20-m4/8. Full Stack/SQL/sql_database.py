import sqlite3
import pandas as pd
from sqlalchemy import create_engine

conn = ""
try:
    conn = sqlite3.connect("strive.db")
except Exception as ex:
    print(ex)

def get_conn():
    try:
        conn = sqlite3.connect("./Database/strive.db")
        return conn
    except Exception as ex:
        print(ex)
        return ex


def get_conn_remote(user, pass, IP, port):
    try:
        engine = create_engine(
            f'mysql+pymysql://{user}:{pass}@{IP}/{user}?host={IP}?port={port}')
        conn = engine.connect
        return conn
    except Exception as ex:
        print(ex)
        return ex

def sql_query(stc):
    
    try:
        c = conn.cursor()
        reply = c.execute(stc)
        conn.commit()
        return reply
    except Exception as ex:
        print(ex)

def pandas_select(stc):
    try:
        if stc.split()[0].lower() == "select":  
            df = pd.read_sql_query(stc, conn)
            return df
        else:  
            return pd.DataFrame()
    except Exception as ex:
        return pd.DataFrame()
    
def upload_data(name : str, path,  head = 0):
    
    try:
        df = pd.read_csv(path)
        frame = df.to_sql(name, conn, if_exists= 'append', index = False)
    except Exception as ex:
        print(ex)


def sql_execute(stc):
    try:
        c = conn.cursor()
        a = c.execute(stc)
        conn.commit()
        print(a)
    except Exception as ex:
        print(ex)
        return ex
        

def close():
    conn.close()
