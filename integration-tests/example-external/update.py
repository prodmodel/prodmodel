import os
import sqlite3
from pathlib import Path


path = str(Path(os.path.dirname(__file__)) / 'remote.db')
conn = sqlite3.connect(path)
cursor = conn.cursor()
cursor.execute('update education_lookup set score=300 where education="secondary"')
conn.commit()
conn.close()

print('DB updated.')
