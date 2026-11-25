
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect
from sqlalchemy.engine import URL

load_dotenv()

connection_url = URL.create(
    drivername="mysql+pymysql",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT", "3306")),
    database=os.getenv("DB_NAME")
)

engine = create_engine(connection_url)


def get_database_schema():

    inspector = inspect(engine)
    schema = []

    for table in inspector.get_table_names():

        schema.append(f"\nTABLE: {table}")

        for column in inspector.get_columns(table):
            schema.append(
                f"  COLUMN: {column['name']} ({column['type']})"
            )

        for fk in inspector.get_foreign_keys(table):
            schema.append(
                f"  FOREIGN KEY: {fk['constrained_columns']} "
                f"references {fk['referred_table']}."
                f"{fk['referred_columns']}"
            )

    return "\n".join(schema)


if __name__ == "__main__":
    print("DATABASE SCHEMA")
    print("====================")
    print(get_database_schema())
