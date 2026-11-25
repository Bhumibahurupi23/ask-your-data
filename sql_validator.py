
import sqlglot
from sqlglot import exp

MAX_ROWS = 1000


def validate_sql(sql_query):

    try:
        # Parse SQL using MySQL syntax
        parsed_queries = sqlglot.parse(
            sql_query,
            read="mysql"
        )

        # Reject empty or multiple statements
        if len(parsed_queries) != 1 or parsed_queries[0] is None:
            return False, "Only one SQL statement is allowed."

        query = parsed_queries[0]

        # Allow only SELECT statements
        if not isinstance(query, exp.Select):
            return False, "Only SELECT queries are allowed."

        # Reject SELECT INTO and locking queries
        if query.args.get("into") or query.args.get("lock"):
            return False, "SELECT INTO and locking queries are not allowed."

        # Add a row limit if missing
        limit = query.args.get("limit")

        if limit is None:
            query = query.limit(MAX_ROWS)

        else:
            limit_value = limit.args.get("expression")

            if (
                isinstance(limit_value, exp.Literal)
                and limit_value.is_number
                and int(limit_value.this) > MAX_ROWS
            ):
                query.set(
                    "limit",
                    exp.Limit(
                        expression=exp.Literal.number(MAX_ROWS)
                    )
                )

        # Convert back to MySQL SQL
        safe_sql = query.sql(dialect="mysql")

        return True, safe_sql

    except Exception as error:
        return False, f"Invalid SQL: {error}"


if __name__ == "__main__":

    test_queries = [
        "SELECT * FROM customers",
        "DROP TABLE customers;",
        "DELETE FROM customers;",
        "UPDATE customers SET segment = 'Test'"
    ]

    for sql in test_queries:
        is_valid, result = validate_sql(sql)

        print("\nQuery:", sql)
        print("VALID:", is_valid)
        print("RESULT:", result)