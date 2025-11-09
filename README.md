# Autonomous Data Quality Guardian for Enterprises  

 

The **Autonomous Data Quality Guardian for Enterprises** is an end-to-end, containerized system that automates **data quality monitoring, validation, correction, and reporting** across multiple data sources.  

It integrates:  
-  **Great Expectations (GX)** → For data validation and quality rules  
-  **Agentic AI Layer (LangChain + Ollama)** → For intelligent reasoning and auto-correction  
-  **Dockerized Setup** → For easy deployment and environment independence  

This project ensures that **only clean, accurate, and schema-consistent data** flows into your enterprise pipelines, enabling **trustworthy analytics** and **AI-ready datasets**.

---

##  System Architecture Overview  

The system operates in **three functional layers**:

### **1️⃣ Data Ingestion & Validation Layer**
- Ingests data from multiple sources (APIs, CSVs, Databases, Web Scraping).
- Validates using **Great Expectations (GX)** through rule-based checks:
  - ✅ Schema validation  
  - ✅ Null / missing values  
  - ✅ Range / regex checks  
  - ✅ Data type consistency  
  - ✅ Duplicate detection  
- Data that **passes validation** → stored in PostgreSQL.  
- Data that **fails validation** → routed to the **Agentic AI Correction Layer**.

---

### **2️⃣ Agentic AI Correction Layer**
- This layer uses **LangChain + Ollama (LLM reasoning)** to analyze invalid data.
- Detects and auto-corrects:
  -  Schema drift or column mismatches  
  -  Duplicate records  
  -  Missing / null values  
  -  Invalid or inconsistent entries  
- Auto-corrected data is **revalidated** through Great Expectations before storage.

---

### **3️⃣ Human Feedback & Monitoring Layer**
- Generates **GX HTML Reports** for every validation run.  
- Provides **alerts / notifications** for critical errors.  
- Allows **human review** for unresolvable issues.  
- Offers a **visual dashboard** summarizing data quality statistics.

---

##  End-to-End Workflow  

| Step | Process | Tool / Script | Output |
|------|----------|----------------|---------|
| 1 | Data ingestion (CSV/API/DB) | `main.py`, `web_scraper.py` | Raw dataset collected |
| 2 | Validation | `great_expectations_validation.py` | GX Validation Report |
| 3 | Decision (Data Validator 🔹) | GX Rules | YES → Store / NO → Send to AI |
| 4 | Correction | LangChain + Ollama | Schema fixed / Missing data imputed |
| 5 | Storage | PostgreSQL | Clean data saved |
| 6 | Reporting | Great Expectations | HTML report generated |
| 7 | Monitoring | Logs + Dashboard | Alerts and visual summaries |

---

##  Key Validation Rules (Great Expectations)

| Validation Type | Example | Purpose |
|-----------------|----------|----------|
| **Null Check** | `expect_column_values_to_not_be_null("email")` | Ensures no missing critical fields |
| **Range Check** | `expect_column_values_to_be_between("age", 0, 120)` | Detects unrealistic values |
| **Regex Check** | `expect_column_values_to_match_regex("email", r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")` | Validates email formats |
| **Uniqueness** | `expect_column_values_to_be_unique("customer_id")` | Ensures unique identifiers |
| **Schema Consistency** | `expect_table_columns_to_match_set([...])` | Detects schema drift |

---

##  Running the Project with Docker  

### **Step 1 — Clone the Repository**
```bash
git clone https://github.com/priyankakadirvel/Autonomous-Data-Quality-Guardian-for-Enterprises.git
cd Autonomous-Data-Quality-Guardian-for-Enterprises

### **Step 2 — Build the Docker Image**
docker build -t data-quality-guardian .

### **Step 3 — Run with Docker Compose**

(Recommended: starts both PostgreSQL and App containers)

docker-compose up --build

### **Step 4 — View Logs**
docker logs data_quality_app

### **Step 5 — Open Great Expectations Report**

After execution:

great_expectations/uncommitted/data_docs/local_site/index.html

