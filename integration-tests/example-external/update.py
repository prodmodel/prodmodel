import os
import sqlite3
from pathlib import Path


def __main__():
  path = str(Path(os.path.dirname(__file__)) / 'remote.db')
  conn = sqlite3.connect(path)
  try:
    cursor.execute('update education_lookup set score=300 where education="secondary"')
  finally:
    conn.close()
