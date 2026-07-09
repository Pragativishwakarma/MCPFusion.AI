# 🚀 MCPFusion.AI

### **Enterprise Multi-Server AI Assistant using Model Context Protocol (MCP), Groq LLM & Intelligent Tool Calling**

<p align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![MCP](https://img.shields.io/badge/Model_Context_Protocol-MCP-blue?style=for-the-badge)
![Groq](https://img.shields.io/badge/Groq-LLM-orange?style=for-the-badge)
![LangGraph](https://img.shields.io/badge/LangGraph-Agent-green?style=for-the-badge)
![MySQL](https://img.shields.io/badge/MySQL-Database-4479A1?style=for-the-badge\&logo=mysql\&logoColor=white)
![AI](https://img.shields.io/badge/Generative_AI-Assistant-purple?style=for-the-badge)

</p>

---

# 🌟 Overview

**MCPFusion.AI** is an **Enterprise-grade AI Assistant** built using the **Model Context Protocol (MCP)**.

Instead of relying on a single backend, the assistant intelligently communicates with **multiple specialized MCP servers**. Every server exposes a set of tools, while a unified AI client powered by **Groq LLM (Llama-3.3-70B-Versatile)** dynamically discovers and invokes the appropriate tools to answer user queries.

The project demonstrates how modern AI systems can orchestrate multiple services through **tool calling**, creating a scalable and modular architecture similar to enterprise AI platforms.

---

# 🎯 Key Highlights

* 🤖 AI-powered intelligent assistant
* ⚡ Groq LLM Integration
* 🔧 Dynamic MCP Tool Discovery
* 🌦 Weather Intelligence Server
* 👨‍💼 Employee Directory Server
* 🗄 MySQL Database Server
* 🔗 Multi-server orchestration
* 🧠 Intelligent Tool Calling
* 💬 Natural Language Interaction
* 📦 Modular Architecture
* 🚀 Easily Scalable

---

# 🏗 System Architecture

```text
                           USER
                             │
                             ▼
               +-----------------------------+
               |      MCP AI CLIENT          |
               | Groq Llama-3.3-70B          |
               +-------------+---------------+
                             │
             Discovers Available MCP Tools
                             │
      ─────────────────────────────────────────────
        │                  │                  │
        ▼                  ▼                  ▼

+----------------+  +----------------+  +-----------------+
| Weather Server |  | Employee Server|  | Database Server |
|     MCP        |  |      MCP       |  |      MCP        |
+----------------+  +----------------+  +-----------------+
| Weather API    |  | Employee Data  |  | MySQL Database  |
+----------------+  +----------------+  +-----------------+

```

---

# ✨ Features

## 🌦 Weather Server

* Current Weather
* Weather Forecast
* Temperature
* Humidity
* Wind Speed
* Air Quality
* Multi-day Forecast

---

## 👨‍💼 Employee Server

* List Employees
* Search Employee
* Department Lookup
* City Lookup
* Salary Summary
* Employee Details
* Employee Statistics

---

## 🗄 Database Server

* Connect to MySQL
* Fetch Employees
* Salary Statistics
* Department Summary
* Top Earners
* Employee Count
* Database Queries

---

## 🤖 AI Client

* Connects to all MCP servers
* Automatically discovers tools
* Uses Groq LLM reasoning
* Calls correct tool dynamically
* Combines multiple tool outputs
* Returns conversational responses

---

# 📸 Project Preview

## MCP Client Startup

> The client initializes the Groq LLM, connects to all MCP servers, and automatically discovers available tools.

*<img width="485" height="746" alt="Screenshot 2026-07-10 at 12 32 57 AM" src="https://github.com/user-attachments/assets/f2795c15-41ee-4a85-8c5b-e0f6623bb85b" />
*

---

## Intelligent Question Answering

> Users interact with a single AI assistant that automatically selects the appropriate MCP server(s) to answer natural language questions.

*![Uploading Screenshot 2026-07-10 at 12.33.18 AM.png…]()

*

---

# 📂 Project Structure

```text
MCPFusion.AI
│
├── client.py
├── weather_server.py
├── employee_server.py
├── database_server.py
│
├── requirements.txt
├── README.md
├── .env.example
└── .gitignore
```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/Pragativishwakarma/MCPFusion.AI.git
```

---

## Navigate

```bash
cd MCPFusion.AI
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv
```

### macOS/Linux

```bash
python3 -m venv venv
```

---

## Activate Environment

### Windows

```bash
venv\Scripts\activate
```

### macOS/Linux

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file

```env
GROQ_API_KEY=your_groq_api_key

DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=employee_db
```

---

# ▶️ Run Servers

### Weather Server

```bash
python weather_server.py
```

### Employee Server

```bash
python employee_server.py
```

### Database Server

```bash
python database_server.py
```

---

# ▶️ Start AI Client

```bash
python client.py
```

---

# 💬 Example Questions

### 🌦 Weather

```
What's the weather in Mumbai?

```

```
Will it rain tomorrow in Delhi?

```

```
Give me a 5-day forecast for Bangalore.
```

---

### 👨‍💼 Employee

```
List all employees.
```

```
Who works in the IT department?
```

```
Show employees located in Delhi.
```

```
What is Alice's salary?
```

---

### 🗄 Database

```
Fetch all employees from the database.
```

```
Show top 5 earners.
```

```
Give me salary statistics.
```

```
Department-wise salary summary.
```

---

### 🚀 Combined AI Queries

The real power of MCPFusion.AI is its ability to combine information across multiple servers.

Example:

```
Show IT employees and today's weather in their cities.
```

```
Who earns the highest salary and what's the weather there?
```

```
Compare employee directory data with the database.
```

```
How many Finance employees are there, and what is the weather in the city where most of them work?
```

---

# 🧠 MCP Workflow

```text
User Question
      │
      ▼
Groq LLM
      │
      ▼
Reasoning
      │
      ▼
Tool Discovery
      │
      ▼
Choose MCP Server
      │
      ▼
Execute Tool
      │
      ▼
Collect Results
      │
      ▼
Generate Final Answer
```

---

# 🛠 Technology Stack

| Category        | Technology                   |
| --------------- | ---------------------------- |
| Language        | Python                       |
| Protocol        | Model Context Protocol (MCP) |
| AI Model        | Groq Llama-3.3-70B-Versatile |
| Agent Framework | LangGraph                    |
| Database        | MySQL                        |
| API             | Weather API                  |
| Environment     | python-dotenv                |
| Version Control | Git & GitHub                 |

---

# 📚 Skills Demonstrated

* Generative AI
* MCP (Model Context Protocol)
* Tool Calling
* AI Agents
* Multi-Server Architecture
* Client-Server Communication
* Prompt Engineering
* LangGraph
* Groq LLM
* MySQL Integration
* Python Programming
* API Integration
* Enterprise AI Systems

---

# 🚀 Future Enhancements

* 🌍 Web Search MCP Server
* 📧 Email MCP Server
* 📄 PDF RAG Server
* 📅 Calendar Server
* 🗣 Voice Assistant
* 🌐 Streamlit Dashboard
* 🔐 User Authentication
* 📊 Analytics Dashboard
* ☁ Cloud Deployment
* 🐳 Docker Support

---

# 👩‍💻 Author

## **Pragati Vishwakarma**

**AI & Data Science Engineer | Generative AI Developer | Python Developer**

🔗 **GitHub:**
[https://github.com/Pragativishwakarma](https://github.com/Pragativishwakarma)

💼 **LinkedIn:**
[https://www.linkedin.com/in/pragati-vishwakarma-893ba8284](https://www.linkedin.com/in/pragati-vishwakarma-893ba8284)

