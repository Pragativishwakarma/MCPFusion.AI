import os
import traceback
import pymysql
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()

mcp = FastMCP("DatabaseServer")


def get_connection():
    """Establish a connection to the MySQL employee_db database."""
    return pymysql.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "employee_db"),
        cursorclass=pymysql.cursors.DictCursor
    )


@mcp.tool()
def db_get_all_employees() -> list:
    """
    Fetch all employees from the MySQL database.
    Returns id, name, department, and salary for every employee.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, department, salary FROM employees ORDER BY id")
            return cur.fetchall()
    except Exception as e:
        traceback.print_exc()
        return [{"error": str(e)}]
    finally:
        conn.close()


@mcp.tool()
def db_get_employees_by_department(department: str) -> list:
    """
    Fetch employees from the database who belong to a specific department.
    Example: IT, HR, Finance, Sales.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, name, department, salary FROM employees WHERE department = %s ORDER BY name",
                (department,)
            )
            results = cur.fetchall()
            if not results:
                return [{"message": f"No employees found in department '{department}' in the database."}]
            return results
    except Exception as e:
        traceback.print_exc()
        return [{"error": str(e)}]
    finally:
        conn.close()


@mcp.tool()
def db_get_employee_by_name(name: str) -> dict:
    """
    Find an employee in the MySQL database by their name (partial match supported).
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, name, department, salary FROM employees WHERE name LIKE %s LIMIT 1",
                (f"%{name}%",)
            )
            result = cur.fetchone()
            if result:
                return result
            return {"message": f"No employee named '{name}' found in the database."}
    except Exception as e:
        traceback.print_exc()
        return {"error": str(e)}
    finally:
        conn.close()


@mcp.tool()
def db_get_salary_statistics() -> dict:
    """
    Return salary statistics from the database:
    total employees, average salary, highest salary, lowest salary.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    COUNT(*) AS total_employees,
                    ROUND(AVG(salary), 2) AS average_salary,
                    MAX(salary) AS highest_salary,
                    MIN(salary) AS lowest_salary,
                    SUM(salary) AS total_salary_budget
                FROM employees
            """)
            return cur.fetchone()
    except Exception as e:
        traceback.print_exc()
        return {"error": str(e)}
    finally:
        conn.close()


@mcp.tool()
def db_get_department_summary() -> list:
    """
    Return a department-level summary from the database:
    employee count, average salary, and total salary per department.
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    department,
                    COUNT(*) AS employee_count,
                    ROUND(AVG(salary), 2) AS avg_salary,
                    SUM(salary) AS total_salary,
                    MAX(salary) AS max_salary,
                    MIN(salary) AS min_salary
                FROM employees
                GROUP BY department
                ORDER BY department
            """)
            return cur.fetchall()
    except Exception as e:
        traceback.print_exc()
        return [{"error": str(e)}]
    finally:
        conn.close()


@mcp.tool()
def db_get_top_earners(limit: int = 3) -> list:
    """
    Return the top earning employees from the database.
    limit: how many top earners to return (default 3, max 10).
    """
    limit = max(1, min(limit, 10))
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, name, department, salary FROM employees ORDER BY salary DESC LIMIT %s",
                (limit,)
            )
            return cur.fetchall()
    except Exception as e:
        traceback.print_exc()
        return [{"error": str(e)}]
    finally:
        conn.close()


if __name__ == "__main__":
    mcp.run()