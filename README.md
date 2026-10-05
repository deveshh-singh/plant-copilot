# Plant Copilot

A multi-agent assistant for industrial maintenance data, built on Databricks with open-source GenAI tools. A personal learning project (started Sep 2026) that rebuilds, on a modern stack, the kind of predictive-maintenance work I did for petrochemical plants at Wipro.

Ask questions such as *"Which engines show abnormal sensor readings in the last 50 cycles, and what does the manual say to check?"* A supervisor agent routes each question to specialists:

- **Text2SQL agent**: answers data questions over Delta tables of sensor readings
- **RAG agent**: retrieves from maintenance and operations documents
- **Anomaly / remaining-life model** (later, L1): scikit-learn, tracked in MLflow, called as a tool

## Stack
Core: Databricks Free Edition · PySpark · Delta Lake · Databricks SQL · LangGraph · MLflow (GenAI evaluation) · Docker · one public cloud (AWS first choice)

Later: scikit-learn · DSPy · Hugging Face + PyTorch (LoRA fine-tune) · Databricks Apps

## Data
NASA C-MAPSS turbofan engine degradation dataset (public), plus public maintenance documents.

## Milestones
Core path, in order. Each milestone also practises one foundation skill: SQL, LangGraph, Docker or a public cloud.

- [ ] **M0 Setup**: Databricks Free Edition account, GitHub repo, local Python env (uv), local Spark tests
- [ ] **M1 Data**: download C-MAPSS, load with PySpark into Delta tables, add a table description for each column
- [ ] **M2 SQL gold set**: hand-write 50 question → SQL → answer pairs over the Delta tables (joins, CTEs, window functions, aggregations); this is the Text2SQL evaluation set
- [ ] **M3 Text2SQL agent**: a LangGraph agent that writes, runs and repairs SQL over the Delta tables, scored for execution accuracy against the M2 gold set
- [ ] **M4 RAG agent**: chunk, embed and retrieve maintenance documents
- [ ] **M5 Supervisor**: LangGraph graph routing between the Text2SQL and RAG agents
- [ ] **M6 Evaluation**: MLflow GenAI evaluation for SQL execution accuracy, retrieval and end-to-end answers
- [ ] **M7 Docker**: package the agent app as a container image; `docker compose up` runs it locally against Databricks
- [ ] **M8 Cloud deploy**: run the container on one public cloud (AWS first choice) on a free tier; nothing paid without asking first (rule 3)
- [ ] **M9 Ship**: architecture diagram, results table, 3-minute demo video

### Later (kept for after M9)
- [ ] **L1 ML model**: scikit-learn anomaly / remaining-useful-life model, logged and registered in MLflow, added to the supervisor as a tool
- [ ] **L2 DSPy**: optimise the Text2SQL prompt against the gold set
- [ ] **L3 Fine-tune**: LoRA fine-tune of a small open model (Qwen 1.5B class) on text-to-SQL pairs on a Mac mini M4 (PyTorch MPS or MLX); compare base vs DSPy vs fine-tuned
- [ ] **L4 Databricks App**: a Databricks App front end alongside the container

## Results
To be filled in from MLflow evaluation runs.
