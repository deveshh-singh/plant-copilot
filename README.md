# Plant Copilot

A multi-agent assistant for industrial maintenance data, built on Databricks with open-source GenAI tools. A personal learning project (started Sep 2026) that rebuilds, on a modern stack, the kind of predictive-maintenance work I did for petrochemical plants at Wipro.

Ask questions such as *"Which engines show abnormal sensor readings in the last 50 cycles, and what does the manual say to check?"* A supervisor agent routes each question to specialists:

- **Text2SQL agent**: answers data questions over Delta tables of sensor readings
- **RAG agent**: retrieves from maintenance and operations documents
- **Anomaly / remaining-life model**: scikit-learn, tracked in MLflow, called as a tool

## Stack
Databricks Free Edition · PySpark · Delta Lake · LangGraph · DSPy · Hugging Face + PyTorch (LoRA fine-tune) · scikit-learn · MLflow (tracking and GenAI evaluation) · Databricks Apps

## Data
NASA C-MAPSS turbofan engine degradation dataset (public), plus public maintenance documents.

## Milestones
- [ ] **M0 Setup**: Databricks Free Edition account, GitHub repo, local Python env (uv)
- [ ] **M1 Data**: download C-MAPSS, load with PySpark into Delta tables, add a table description for each column
- [ ] **M2 ML model**: scikit-learn anomaly / remaining-useful-life model, logged and registered in MLflow
- [ ] **M3 Text2SQL agent**: LLM writes SQL over the Delta tables; 50-question gold set of question → SQL → answer
- [ ] **M4 RAG agent**: chunk, embed and retrieve maintenance documents
- [ ] **M5 Supervisor**: LangGraph graph routing between Text2SQL, RAG and the model tool
- [ ] **M6 Evaluation**: MLflow GenAI evaluation for SQL execution accuracy, retrieval and end-to-end answers
- [ ] **M7 DSPy**: optimise the Text2SQL prompt against the gold set
- [ ] **M8 Fine-tune**: LoRA fine-tune of a small open model (Qwen 1.5B class) on text-to-SQL pairs on a Mac mini M4 (PyTorch MPS or MLX); compare base vs DSPy vs fine-tuned
- [ ] **M9 Ship**: Databricks App front end, architecture diagram, results table, 3-minute demo video

## Results
To be filled in from MLflow evaluation runs.
