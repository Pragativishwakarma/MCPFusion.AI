"""
=========================================================
  ADVANCED MCP CLIENT  — 1 Client + 3 Servers
=========================================================
  Servers:
    1. weather_server.py  — Real-time weather & forecasts
    2. employee_server.py — In-memory employee data
    3. database_server.py — MySQL employee database

  AI Backend: Groq (llama-3.3-70b-versatile)
  Framework : LangGraph ReAct Agent
=========================================================
"""

import asyncio
import os
import sys
import traceback
from pathlib import Path

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

load_dotenv()

# ─── ANSI Colour helpers ────────────────────────────────
RESET  = "\033[0m"
BOLD   = "\033[1m"
CYAN   = "\033[96m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
MAGENTA= "\033[95m"
RED    = "\033[91m"
BLUE   = "\033[94m"

def banner():
    print(f"""
{CYAN}{BOLD}
╔══════════════════════════════════════════════════════════╗
║        🤖  ADVANCED MCP MULTI-SERVER CLIENT  🤖          ║
║                                                          ║
║  Servers connected:                                      ║
║    🌤  weather_server  — Real-time weather & forecasts   ║
║    👥  employee_server — In-memory employee directory    ║
║    🗄  database_server — MySQL employee database         ║
║                                                          ║
║  Powered by: Groq (llama-3.3-70b-versatile)             ║
╚══════════════════════════════════════════════════════════╝
{RESET}""")

def print_tool_list(tools):
    print(f"\n{YELLOW}{BOLD}{'═'*58}")
    print(f"  ✅  {len(tools)} Tools Loaded Successfully")
    print(f"{'═'*58}{RESET}")

    categories = {
        "🌤  Weather"  : [],
        "👥  Employee" : [],
        "🗄  Database" : [],
    }
    for tool in tools:
        n = tool.name
        if n.startswith("get_current") or n.startswith("get_weather"):
            categories["🌤  Weather"].append(tool)
        elif n.startswith("db_"):
            categories["🗄  Database"].append(tool)
        else:
            categories["👥  Employee"].append(tool)

    for cat, cat_tools in categories.items():
        if cat_tools:
            print(f"\n  {MAGENTA}{BOLD}{cat}{RESET}")
            for t in cat_tools:
                print(f"    {GREEN}▸ {t.name}{RESET}")
                print(f"      {t.description[:80]}{'...' if len(t.description)>80 else ''}")

    print(f"\n{YELLOW}{'─'*58}{RESET}")

def print_help():
    print(f"""
{CYAN}{BOLD}Sample Questions you can ask:{RESET}
  {GREEN}Weather:{RESET}
    • What is the weather in Mumbai?
    • Give me a 3-day forecast for Delhi
    • Is it going to rain in Bangalore today?

  {GREEN}Employee Directory:{RESET}
    • List all employees
    • Who works in the IT department?
    • Show me employees in Delhi
    • What is Alice's salary?
    • Give me a salary summary by department

  {GREEN}Database:{RESET}
    • Fetch all employees from the database
    • Who are the top 3 earners in the database?
    • What is the average salary in the Finance department?
    • Give me database salary statistics

  {GREEN}Combined:{RESET}
    • Show me IT employees and what's the weather in their cities?
    • Compare employee data from memory and database
    • Who earns the most and what's the weather in their city?

  {YELLOW}Type 'help' to see this again | 'exit' to quit{RESET}
""")


async def main():
    banner()

    # ── Validate API key ───────────────────────────────────
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print(f"{RED}ERROR: GROQ_API_KEY not found in .env file.{RESET}")
        sys.exit(1)

    # ── Validate server files exist ────────────────────────
    base_dir = Path(__file__).parent
    servers = {
        "weather_server.py"  : "🌤  WeatherServer",
        "employee_server.py" : "👥  EmployeeServer",
        "database_server.py" : "🗄  DatabaseServer",
    }
    for fname, label in servers.items():
        path = base_dir / fname
        if not path.exists():
            print(f"{RED}ERROR: {label} file not found → {path}{RESET}")
            sys.exit(1)

    # ── Initialize LLM ─────────────────────────────────────
    print(f"{BLUE}🔌 Initializing Groq LLM (llama-3.3-70b-versatile)...{RESET}")
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=api_key,
        temperature=0,
    )

    # ── Connect to all 3 MCP servers ───────────────────────
    print(f"{BLUE}🔗 Connecting to all 3 MCP servers...{RESET}")

    client = MultiServerMCPClient(
        {
            "weather": {
                "command": sys.executable,
                "args": [str(base_dir / "weather_server.py")],
                "transport": "stdio",
            },
            "employee": {
                "command": sys.executable,
                "args": [str(base_dir / "employee_server.py")],
                "transport": "stdio",
            },
            "database": {
                "command": sys.executable,
                "args": [str(base_dir / "database_server.py")],
                "transport": "stdio",
            },
        }
    )

    try:
        tools = await client.get_tools()
    except Exception as e:
        print(f"{RED}ERROR: Failed to connect to MCP servers:{RESET}")
        traceback.print_exc()
        sys.exit(1)

    print_tool_list(tools)

    # ── Build ReAct agent ──────────────────────────────────
    system_prompt = """You are an intelligent assistant connected to three specialized servers:

1. **Weather Server**: Provides real-time weather data and multi-day forecasts for any city worldwide.
2. **Employee Server**: Contains an in-memory directory of employees with their departments, positions, salaries, contact info, and cities.
3. **Database Server**: Connects to a live MySQL database with employee records for salary statistics and department summaries.

Your job is to answer user questions by intelligently calling the right tools from the right servers.
- For weather questions, use the weather tools.
- For employee lookup by name, department or city, use the employee server tools.
- For database statistics, salary analysis, or top earners, use the database server tools.
- For complex questions, combine multiple tools and provide a well-structured, comprehensive answer.
- Always present data in a clear, readable format. Use bullet points, tables (in text), or numbered lists where appropriate.
- If an error occurs, explain it clearly and suggest alternatives.
"""

    agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt=system_prompt,
    )

    print_help()

    # ── Interactive chat loop ──────────────────────────────
    print(f"{CYAN}{BOLD}{'═'*58}{RESET}")
    print(f"{CYAN}{BOLD}  Ready! Ask me anything...{RESET}")
    print(f"{CYAN}{BOLD}{'═'*58}{RESET}\n")

    while True:
        try:
            question = input(f"{GREEN}{BOLD}You ▸ {RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n{YELLOW}Goodbye! 👋{RESET}")
            break

        if not question:
            continue

        if question.lower() in ("exit", "quit", "bye", "q"):
            print(f"\n{YELLOW}Goodbye! 👋{RESET}")
            break

        if question.lower() == "help":
            print_help()
            continue

        print(f"\n{BLUE}🤔 Thinking...{RESET}\n")

        try:
            response = await agent.ainvoke(
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": question,
                        }
                    ]
                }
            )

            answer = response["messages"][-1].content
            print(f"{MAGENTA}{BOLD}Assistant ▸{RESET}")
            print(f"{answer}")
            print(f"\n{CYAN}{'─'*58}{RESET}\n")

        except Exception as e:
            print(f"{RED}ERROR while processing your question:{RESET}")
            print(f"  {str(e)}")
            traceback.print_exc()
            print(f"\n{YELLOW}Please try a different question.{RESET}\n")


if __name__ == "__main__":
    asyncio.run(main())
