from mcp.server.fastmcp import FastMCP

mcp = FastMCP("EmployeeServer")

# In-memory employee dataset (from training examples)
EMPLOYEES = [
    {"id": 1, "name": "John",  "department": "IT",      "position": "Senior Developer",   "salary": 80000, "email": "john@company.com",  "phone": "+91-9876543210", "city": "Delhi"},
    {"id": 2, "name": "Alice", "department": "HR",      "position": "HR Manager",          "salary": 65000, "email": "alice@company.com", "phone": "+91-9876543211", "city": "Mumbai"},
    {"id": 3, "name": "Bob",   "department": "Finance", "position": "Financial Analyst",   "salary": 90000, "email": "bob@company.com",   "phone": "+91-9876543212", "city": "Bangalore"},
    {"id": 4, "name": "David", "department": "IT",      "position": "Lead Engineer",        "salary": 95000, "email": "david@company.com", "phone": "+91-9876543213", "city": "Hyderabad"},
    {"id": 5, "name": "Emma",  "department": "Sales",   "position": "Sales Executive",      "salary": 70000, "email": "emma@company.com",  "phone": "+91-9876543214", "city": "Pune"},
    {"id": 6, "name": "Priya", "department": "IT",      "position": "Backend Developer",    "salary": 75000, "email": "priya@company.com", "phone": "+91-9876543215", "city": "Chennai"},
    {"id": 7, "name": "Rahul", "department": "Finance", "position": "Account Manager",      "salary": 85000, "email": "rahul@company.com", "phone": "+91-9876543216", "city": "Delhi"},
    {"id": 8, "name": "Sara",  "department": "HR",      "position": "Recruitment Specialist","salary": 60000, "email": "sara@company.com",  "phone": "+91-9876543217", "city": "Mumbai"},
]


@mcp.tool()
def list_all_employees() -> list:
    """
    Return a complete list of all employees with full details
    including their department, position, salary, email, phone and city.
    """
    return EMPLOYEES


@mcp.tool()
def get_employee_by_name(name: str) -> dict:
    """
    Look up an employee by their name (case-insensitive).
    Returns full details of the matched employee or a not-found message.
    """
    for emp in EMPLOYEES:
        if emp["name"].lower() == name.lower():
            return emp
    return {"error": f"Employee '{name}' not found."}


@mcp.tool()
def get_employees_by_department(department: str) -> list:
    """
    Return all employees who belong to a specific department.
    Example departments: IT, HR, Finance, Sales.
    """
    result = [e for e in EMPLOYEES if e["department"].lower() == department.lower()]
    if not result:
        return [{"message": f"No employees found in department '{department}'."}]
    return result


@mcp.tool()
def get_employees_by_city(city: str) -> list:
    """
    Return all employees who are located in a specific city.
    """
    result = [e for e in EMPLOYEES if e["city"].lower() == city.lower()]
    if not result:
        return [{"message": f"No employees found in city '{city}'."}]
    return result


@mcp.tool()
def get_department_salary_summary() -> list:
    """
    Return a summary showing the total salary, average salary,
    and employee count for each department.
    """
    from collections import defaultdict
    dept_map = defaultdict(list)
    for emp in EMPLOYEES:
        dept_map[emp["department"]].append(emp["salary"])

    summary = []
    for dept, salaries in dept_map.items():
        summary.append({
            "department": dept,
            "employee_count": len(salaries),
            "total_salary": sum(salaries),
            "average_salary": round(sum(salaries) / len(salaries), 2),
            "min_salary": min(salaries),
            "max_salary": max(salaries)
        })
    return sorted(summary, key=lambda x: x["department"])


if __name__ == "__main__":
    mcp.run()
