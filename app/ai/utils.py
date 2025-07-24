import glob
import os
import pandas as pd
import sqlite3

def load_faq_documents(faq_dir):
    """Load all .txt FAQ documents from a directory."""
    docs = []
    for filepath in glob.glob(os.path.join(faq_dir, '*.txt')):
        with open(filepath, 'r', encoding='utf-8') as f:
            docs.append({
                'filename': os.path.basename(filepath),
                'content': f.read()
            })
    return docs

def load_sales_data(csv_path):
    """Load sales data from a CSV file into a pandas DataFrame."""
    return pd.read_csv(csv_path)

def csv_to_sqlite(csv_path, db_path, table_name="sales"):
    """Load CSV into a SQLite database, replacing the table if it exists."""
    import pandas as pd
    df = pd.read_csv(csv_path)
    conn = sqlite3.connect(db_path)
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.commit()
    conn.close()

def run_sql_query(db_path, query):
    """Run a SQL query and return results as a list of dicts."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    result = [dict(row) for row in rows]
    conn.close()
    return result 