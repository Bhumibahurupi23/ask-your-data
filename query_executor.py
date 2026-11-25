
import pandas as pd
from sqlalchemy import text
from schema_inspector import engine
from sql_validator import validate_sql


def execute_query(sql_query):

    # Step 1: Validate SQL
    is_valid, result = validate_sql(sql_query)

    if not is_valid:
        raise ValueError(result)

    safe_sql = result

    # Step 2: Execute validated SQL
    with engine.connect() as connection:
        query_result = connection.execute(text(safe_sql))

        # Step 3: Convert results into a DataFrame
        columns = query_result.keys()
        rows = query_result.fetchall()

        dataframe = pd.DataFrame(rows, columns=columns)

    return safe_sql, dataframe


if __name__ == "__main__":

    test_query = """
    SELECT
        c.customer_name,
        COUNT(DISTINCT o.order_id) AS total_orders
    FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.customer_name
    ORDER BY total_orders DESC
    LIMIT 5
    """

    try:
        sql, results = execute_query(test_query)

        print("\nEXECUTED SQL:")
        print(sql)

        print("\nQUERY RESULTS:")
        print(results.to_string(index=False))

    except Exception as error:
        print("Execution failed:", error)
