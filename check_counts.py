from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

url = (
    f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}"
    f"/{os.getenv('DB_NAME')}"
)

engine = create_engine(url)

tables = ["customers", "products", "orders", "order_items"]

with engine.connect() as connection:
    for table in tables:
        result = connection.execute(
            text(f"SELECT COUNT(*) FROM `{table}`")
        )
        print(f"{table}: {result.scalar()}")