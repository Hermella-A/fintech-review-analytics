
import psycopg2
import pandas as pd
from sqlalchemy import create_engine
import os

# --- Database Connection Parameters ---
DB_NAME = "bank_reviews"
DB_USER = "postgres"
DB_PASSWORD = "password123" 
DB_HOST = "localhost"
DB_PORT = "5432"

def create_database():
    """Connects to default 'postgres' db and creates 'bank_reviews' if it doesn't exist."""
    conn = psycopg2.connect(dbname='postgres', user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{DB_NAME}'")
    exists = cur.fetchone()
    if not exists:
        cur.execute(f"CREATE DATABASE {DB_NAME}")
        print(f"Database '{DB_NAME}' created successfully.")
    else:
        print(f"Database '{DB_NAME}' already exists.")

    cur.close()
    conn.close()

def create_tables():
    """Creates the 'banks' and 'reviews' tables."""
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cur = conn.cursor()

    # SQL for banks table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS banks (
            bank_id SERIAL PRIMARY KEY,
            bank_name VARCHAR(255) UNIQUE NOT NULL,
            app_name VARCHAR(255)
        );
    """)

    # SQL for reviews table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            review_id SERIAL PRIMARY KEY,
            bank_id INTEGER REFERENCES banks(bank_id),
            review_text TEXT,
            rating INTEGER,
            review_date DATE,
            sentiment_label VARCHAR(10),
            sentiment_score FLOAT,
            identified_theme VARCHAR(100),
            source VARCHAR(50)
        );
    """)

    conn.commit()
    print("Tables 'banks' and 'reviews' created (if they didn't exist).")
    cur.close()
    conn.close()

def populate_data():
    """Reads the cleaned CSV and inserts data into the tables."""
    try:
        # Load the data (adjust path if your file is elsewhere)
        reviews_df = pd.read_csv('data/raw/reviews_with_sentiment.csv')
        reviews_df['review_date'] = pd.to_datetime(reviews_df['date']).dt.date
    except FileNotFoundError:
        print("Error: reviews_with_sentiment.csv not found. Have you run Task 2?")
        return

    # --- Insert unique banks first ---
    # Extract unique bank names and assign a placeholder app name
    banks_df = reviews_df[['bank']].drop_duplicates().reset_index(drop=True)
    banks_df['app_name'] = banks_df['bank'] + " Mobile App" # A simple placeholder
    
    banks_df = banks_df.rename(columns={'bank': 'bank_name'})

    # Using SQLAlchemy for efficient bulk insert
    engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')
    banks_df.to_sql('banks', engine, if_exists='append', index=False)
    print("Banks data inserted.")

    # --- Now insert the reviews, linking with correct bank_id ---
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cur = conn.cursor()

    for index, row in reviews_df.iterrows():
        # Get the bank_id for this review
        cur.execute("SELECT bank_id FROM banks WHERE bank_name = %s", (row['bank'],))
        bank_id = cur.fetchone()[0]

        # Insert the review
        cur.execute("""
            INSERT INTO reviews (bank_id, review_text, rating, review_date, sentiment_label, sentiment_score, identified_theme, source)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (bank_id, row['review'], row['rating'], row['review_date'], row['sentiment_label'], row['sentiment_score'], None, row['source']))

    conn.commit()
    print(f"Inserted {len(reviews_df)} reviews.")
    cur.close()
    conn.close()

if __name__ == "__main__":
    create_database()
    create_tables()
    populate_data()