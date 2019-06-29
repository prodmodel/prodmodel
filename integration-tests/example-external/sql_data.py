import os
import sqlite3
from pathlib import Path


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def load_table(table):
  result = []
  path = str(Path(os.path.dirname(__file__)) / 'remote.db')
  conn = sqlite3.connect(path)
  try:
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM {table}')
    for row in cursor.fetchall():
      result.append(row)
  finally:
    conn.close()
  return result
