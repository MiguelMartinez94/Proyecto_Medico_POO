from ConexionBD import mysql

def mysql(query, params=None, fetch="all", commit=False):
    cursor = None  # Declarar el cursor fuera del try
    try:
        cursor = mysql.connection.cursor()

        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        result = None
        if fetch == "all":
            result = cursor.fetchall()
        elif fetch == "one":
            result = cursor.fetchone()

        if commit:
            mysql.connection.commit()

        return result

    except Exception as e:
        print(f"Error executing query: {e}")
        return None

    finally:
        if cursor:
            cursor.close()
