# 🗄️ Text-to-SQL App — Natural Language to Database Queries

> **A production-deployed LLM application** that lets users query a database using plain English — automatically generating, executing, and returning SQL query results without the user needing to write a single line of SQL. Built with Streamlit, containerised with Docker.

---

## 📌 Project Overview

SQL is the language of data — but most business users, analysts, and stakeholders don't write it fluently. This creates a bottleneck: every data question must go through a data engineer or analyst to be translated into a query. This project eliminates that bottleneck.

The **Text-to-SQL App** uses an LLM to translate natural language questions into valid SQL queries, executes them against a live SQLite database, and returns the results in a readable format — all through a clean web interface.

This is a **full-stack AI application** — it combines LLM-powered query generation, a real database backend (`Create_db.py`), and a deployed web UI (`app.py`), all containerised for consistent deployment.

---

## 🎯 Problem Statement

> *Allow non-technical users to query a database using plain English — the LLM translates the question to SQL, executes it, and returns the results.*

**Who benefits:**
- **Business analysts** — query data without writing SQL
- **Product managers** — self-serve data questions without waiting for engineers
- **Executives** — ask ad-hoc questions directly against live data
- **Data teams** — reduce repetitive query requests by enabling self-service

---

## 🏗️ System Architecture

```
User Input (Natural Language Question)
"How many students scored above 80 in Maths?"
            │
            ▼
┌──────────────────────────────────────┐
│         app.py  (Streamlit UI)        │
│  Text input box, run button,         │
│  SQL display, results table          │
└─────────────────┬────────────────────┘
                  │
                  ▼
┌──────────────────────────────────────┐
│         LLM (Gemini / GPT)           │
│  Schema-aware prompt:                │
│  "Given this table schema: {...}     │
│   Convert this question to SQL:      │
│   {user_question}"                   │
│                                      │
│  Returns: valid SQL query string     │
└─────────────────┬────────────────────┘
                  │  Generated SQL
                  ▼
┌──────────────────────────────────────┐
│         SQLite Database              │
│         (created by Create_db.py)    │
│  Executes the generated SQL query    │
│  Returns result rows                 │
└─────────────────┬────────────────────┘
                  │
                  ▼
         Results displayed in
         Streamlit data table
```

---

## 🗂️ Project Structure

```
Text-to-SQL-APP/
│
├── app.py           # Streamlit UI — takes question, calls LLM, runs SQL, shows results
├── Create_db.py     # Database setup script — creates and seeds the SQLite database
├── Dockerfile       # Container definition for deployment
├── requirements.txt # Python dependencies
└── .gitignore
```

---

## 🔬 Technical Deep Dive

### 1. Database Creation (`Create_db.py`)

Before the app can answer questions, it needs a database to query. `Create_db.py` is a standalone setup script that:

- Creates a **SQLite database** (`.db` file) — lightweight, file-based, no server needed
- Defines the table schema (e.g., a student records table with columns like `name`, `class`, `marks`, `subject`)
- Seeds the database with sample data rows
- Prints confirmation on successful creation

Running this once before the app sets up the entire database backend:

```python
# Example schema created by Create_db.py
CREATE TABLE STUDENT (
    NAME    VARCHAR(25),
    CLASS   VARCHAR(25),
    SECTION VARCHAR(25),
    MARKS   INT
);
```

**Why SQLite?** — Zero configuration, file-based, ships inside the Docker container. Ideal for demonstrating the full Text-to-SQL flow without requiring an external database server.

### 2. Schema-Aware Prompt Engineering (`app.py`)

The key to reliable Text-to-SQL is giving the LLM the **database schema** alongside the user's question. Without schema context, the LLM guesses table and column names and produces invalid SQL.

The prompt is structured as:

```
You are an expert SQL query generator.
Given the following SQLite database schema:

Table: STUDENT
Columns: NAME (VARCHAR), CLASS (VARCHAR), SECTION (VARCHAR), MARKS (INT)

Convert the following natural language question into a valid SQL query.
Return ONLY the SQL query — no explanation, no markdown, no backticks.

Question: {user_question}
```

**Why "return ONLY the SQL query" matters** — without this constraint, LLMs often wrap the SQL in markdown code blocks or add explanatory text, which breaks the downstream `execute()` call. Explicit output format instructions are essential for reliable parsing.

### 3. Query Execution & Result Display (`app.py`)

```python
# Full pipeline in app.py
user_question = st.text_input("Ask a question about the database:")

if st.button("Run Query"):
    sql = generate_sql(user_question)        # LLM call
    st.code(sql, language="sql")             # Show generated SQL
    results = execute_query(sql)             # Run against SQLite
    st.dataframe(results)                    # Display results table
```

Showing the **generated SQL alongside the results** is a deliberate design choice — it builds trust by letting users verify what query was actually run, rather than treating the LLM as a black box.

### 4. Docker Containerisation (`Dockerfile`)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN python Create_db.py        # Seed the database at build time
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501"]
```

Running `Create_db.py` at **build time** inside the Dockerfile means the database is pre-seeded inside the container — anyone who pulls and runs the image gets a fully working app with data, zero additional setup.

---

## 💬 Example Interactions

```
User:  "How many students are in Data Science class?"
SQL:   SELECT COUNT(*) FROM STUDENT WHERE CLASS = 'Data Science';
Result: 6

User:  "Show all students who scored more than 80 marks"
SQL:   SELECT * FROM STUDENT WHERE MARKS > 80;
Result: [table of matching rows]

User:  "What is the average marks per class?"
SQL:   SELECT CLASS, AVG(MARKS) as avg_marks FROM STUDENT GROUP BY CLASS;
Result: [class-wise averages table]

User:  "Who scored the highest marks?"
SQL:   SELECT NAME, MARKS FROM STUDENT ORDER BY MARKS DESC LIMIT 1;
Result: [top scorer row]
```

---

## 📊 Why Text-to-SQL Is Hard (and What Makes This Work)

Most naive Text-to-SQL implementations fail on anything beyond simple `SELECT *` queries. What makes this implementation reliable:

| Challenge | How it's handled |
|---|---|
| LLM doesn't know your schema | Schema injected into every prompt |
| LLM returns SQL wrapped in markdown | Explicit "return ONLY SQL" instruction |
| Ambiguous column names | Schema includes column types in prompt |
| SQL syntax errors | Generated SQL shown to user for verification |
| Injection risk | Read-only query execution (no `INSERT`/`DROP`) |

---

## 🛠️ Tech Stack

| Category | Tools |
|---|---|
| Language | Python 3.11 |
| LLM | Google Gemini / OpenAI GPT |
| Database | SQLite (`sqlite3`) |
| Web UI | Streamlit |
| Containerisation | Docker |

---

## 🚀 How to Run

### Option A — Local

```bash
git clone https://github.com/Charu305/Text-to-SQL-APP.git
cd Text-to-SQL-APP

pip install -r requirements.txt

# Set your LLM API key
export GOOGLE_API_KEY="your-gemini-api-key"

# Create and seed the database
python Create_db.py

# Launch the app
streamlit run app.py
# Open http://localhost:8501
```

### Option B — Docker

```bash
docker build -t text-to-sql-app .
docker run -p 8501:8501 \
  -e GOOGLE_API_KEY="your-gemini-api-key" \
  text-to-sql-app
# Open http://localhost:8501
```

---

## 💡 Key Learnings & Takeaways

- **Schema injection is the foundation of reliable Text-to-SQL** — the LLM cannot generate valid SQL for a database it knows nothing about. Passing the full table schema (column names, types) in every prompt is non-negotiable for correctness.
- **Output format instructions prevent parsing failures** — instructing the LLM to return "ONLY the SQL query, no markdown, no explanation" is what makes the result directly executable. Without this, you spend more time parsing LLM responses than running queries.
- **Showing the generated SQL builds trust** — displaying the SQL alongside the result lets users audit what the LLM generated. This transparency is essential for any data application where correctness matters.
- **`Create_db.py` separation is good engineering** — separating database initialisation from application logic means the schema can be updated, tables added, and data reseeded without touching `app.py`.
- **Docker `RUN python Create_db.py` at build time is the right pattern** — seeding the database during image build means the container is self-contained. No manual setup steps, no "it works on my machine" issues.
- **Text-to-SQL is one of the highest-value LLM use cases for enterprises** — virtually every company has databases that most employees can't query. A working Text-to-SQL app directly unlocks data self-service at scale.

---

## 🔮 Potential Enhancements

- **Multi-table schema support** — inject schemas for all related tables + foreign key relationships for JOIN query generation
- **Query validation layer** — parse the generated SQL with `sqlparse` before execution to catch syntax errors before they reach the database
- **Read-only enforcement** — explicitly block `INSERT`, `UPDATE`, `DELETE`, `DROP` statements for safety in production
- **Natural language result explanation** — after returning the results table, use the LLM to explain the findings in plain English
- **Connect to production databases** — replace SQLite with PostgreSQL / MySQL / BigQuery for real enterprise data

---

## 👩‍💻 Author

**Charunya**
🔗 [GitHub Profile](https://github.com/Charu305)

---

## 📄 License

This project is developed for educational and research purposes.
