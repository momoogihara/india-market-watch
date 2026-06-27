# test_db_conn.py の中身
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# .envファイルを読み込む
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
# 変更前
DATABASE_URL = os.getenv("DATABASE_URL")

# 変更後：環境変数の「db」を強制的に「localhost」に置換する
#DATABASE_URL = os.getenv("DATABASE_URL").replace("@db:", "@localhost:")

print(f"Connecting to: {DATABASE_URL}")

engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as connection:
        # 1. 接続テスト
        result = connection.execute(text("SELECT version();"))
        print(f"PostgreSQL Version: {result.fetchone()[0]}")
        
        # 2. テーブル一覧の確認
        tables = connection.execute(text(
            "SELECT table_name FROM information_schema.tables WHERE table_schema='public';"
        ))
        print("Tables in 'public':", [row[0] for row in tables])
        
        # 3. articlesテーブルの件数確認
        count = connection.execute(text("SELECT COUNT(*) FROM articles;")).fetchone()[0]
        print(f"Total articles in DB: {count}")
        
except Exception as e:
    print(f"❌ Connection Failed: {e}")