import os
os.environ['PATH'] = r"C:\oracle\instantclient_23_5" + ";" + os.environ['PATH']

import cx_Oracle
print(cx_Oracle.clientversion())

import cx_Oracle
cx_Oracle.init_oracle_client(lib_dir=r"C:\oracle\instantclient")
print(cx_Oracle.clientversion())
