import pandas as pd
import psycopg2

def load_and_clean_data(csv_file):
    """
    Loads the CSV file and renames columns.
    """
    df = pd.read_csv(csv_file, skiprows=[1])  # Read the CSV file
    print("Columns before renaming:", df.columns)  # Debugging statement

    df.rename(columns={
        "Date": "date",
        "Close": "close",
        "High": "high",
        "Low": "low",
        "Open": "open",
        "Volume": "volume"
    }, inplace=True)

    print("Columns after renaming:", df.columns)  # Debugging statement

    df["date"] = pd.to_datetime(df["date"])  # Convert date column
    df.set_index("date", inplace=True)  # Set date as index
    print(df.head())  # Debugging statement
    print("✅ Data cleaned successfully!")
    return df

def store_in_postgres(df, db_name="trading", table_name="market_data"):
    """
    Stores market data in PostgreSQL.
    """
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(dbname=db_name, user="postgres", password="password", host="localhost")
        cur = conn.cursor()

        # Create table if not exists
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                date DATE PRIMARY KEY,
                open FLOAT,
                high FLOAT,
                low FLOAT,
                close FLOAT,
                volume BIGINT
            );
        """)
        print(f"✅ Table '{table_name}' ensured in database '{db_name}'.")

        # Insert data
        for index, row in df.iterrows():
            try:
                cur.execute(f"""
                    INSERT INTO {table_name} (date, open, high, low, close, volume)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (date) DO NOTHING;
                """, (index, row["open"], row["high"], row["low"], row["close"], row["volume"]))
                print(f"Inserted row: {index}, {row.to_dict()}")  # Debugging statement
            except Exception as e:
                print(f"❌ Error inserting row {index}: {e}")  # Log any errors during insertion

        # Commit the transaction
        conn.commit()
        print(f"✅ Data committed to table '{table_name}' in database '{db_name}'.")

    except Exception as e:
        print(f"❌ Error connecting to the database or executing queries: {e}")
    finally:
        # Close the connection
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()
        print("✅ Database connection closed.")
    print(f"✅ Data stored in PostgreSQL ({table_name})!")

if __name__ == "__main__":
    file_path = "../data/SPY.csv"
    df = load_and_clean_data(file_path)
    store_in_postgres(df)