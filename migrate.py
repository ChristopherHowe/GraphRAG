import os
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from db_funcs import get_db_con

def ensure_migration_table(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS migration_history (
                id SERIAL PRIMARY KEY,
                migration_file TEXT UNIQUE NOT NULL,
                applied_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            )
        """)
    conn.commit()

def get_applied_migrations(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT migration_file FROM migration_history")
        return {row[0] for row in cur.fetchall()}

def apply_migration(conn, filename, content):
    with conn.cursor() as cur:
        print(f"Applying migration: {filename}")
        cur.execute(content)
        cur.execute(
            "INSERT INTO migration_history (migration_file) VALUES (%s)",
            (filename,)
        )
    conn.commit()

def main():
    conn = get_db_con()
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    
    ensure_migration_table(conn)
    applied_migrations = get_applied_migrations(conn)
    
    migrations_dir = "migrations"
    migration_files = sorted([f for f in os.listdir(migrations_dir) if f.endswith('.sql')])
    
    for filename in migration_files:
        if filename in applied_migrations:
            print(f"Skipping already applied migration: {filename}")
            continue
            
        with open(os.path.join(migrations_dir, filename), 'r') as f:
            content = f.read()
            apply_migration(conn, filename, content)
    
    conn.close()
    print("Migrations completed successfully")

if __name__ == "__main__":
    main()
