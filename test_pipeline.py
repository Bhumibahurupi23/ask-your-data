
from sql_generator import generate_sql
from query_executor import execute_query


question = "Show me the top 5 customers by number of orders"

try:
    print("\nUSER QUESTION:")
    print(question)

    # Generate SQL using Gemini
    generated_sql = generate_sql(question)

    print("\nGENERATED SQL:")
    print(generated_sql)

    # Validate and execute SQL
    safe_sql, results = execute_query(generated_sql)

    print("\nFINAL SQL:")
    print(safe_sql)

    print("\nQUERY RESULTS:")
    print(results.to_string(index=False))

except Exception as error:
    print("\nPIPELINE ERROR:")
    print(error)
