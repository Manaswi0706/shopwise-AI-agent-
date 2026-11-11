# 🛍️ SmartCart AI

**SmartCart AI** is an intelligent conversational e-commerce shopping assistant that plans multi-step actions, leverages specialized backend tools, checks real-time inventory and hardware compatibility, and delivers transparent, scored recommendations with clear activity traces.

> ⚠️ **Demo Notice / Sample Data Disclaimer**: All catalogue, product specification, pricing, and stock inventory values presented in this application are **sample/demo data** for demonstration and hackathon testing purposes. They do not represent live marketplace inventory or financial quotes.

---

## 📌 Problem Statement

Online shoppers often struggle with complex, multi-criteria purchasing decisions:
1. **Conflicting Constraints**: Balancing tight budgets with specific hardware requirements (e.g., minimum RAM, display refresh rates, battery capacity).
2. **Opaque Recommendations**: Traditional recommendation systems act as "black boxes", offering zero transparency on *why* an item was recommended.
3. **Compatibility Confusion**: Verifying whether an accessory (such as a high-wattage charger, case, or wireless earbuds) is compatible with a chosen device often requires scouring forums and datasheets.
4. **Context Switching**: Comparing specifications and managing shortlists forces users to open dozens of browser tabs.

**SmartCart AI** solves this by pairing an agentic orchestrator with deterministic tools to create a transparent, interactive shopping experience where planning, tool calls, and scoring are fully visible to the user.

---

## ✨ Features

- **Conversational Shopping Assistant**: Natural language understanding capable of parsing budget caps (e.g., `₹18,000`), RAM specifications (`8 GB RAM`), brand preferences, and action intents.
- **Agent Planning & Execution Tracing**: Real-time display of the agent's goal, step-by-step plan, tool invocations, and execution trace for complete transparency.
- **Multi-Criteria Recommendation Engine**: Scoring model (0–100) weighting budget compliance, technical specifications, customer reviews, and stock availability with human-readable rationale.
- **Hardware Compatibility Verification**: Automated cross-referencing between host devices and accessories (chargers, cases, audio).
- **Direct Side-by-Side Product Comparison**: Compare two products with structured spec tables and price differentials.
- **Shortlisting & Favorites**: Save and inspect preferred items across the shopping session.
- **Hybrid AI Engine**: Runs seamlessly offline with smart rule-based orchestration or integrates with Google Gemini for rich language generation when configured.

---

## 🏗️ Architecture

```
                      +-----------------------------+
                      |      Streamlit UI           |
                      |   (frontend/app.py)         |
                      +--------------+--------------+
                                     |
                                     v
                      +-----------------------------+
                      |     Agent Orchestrator      |
                      |  (agent/orchestrator.py)    |
                      +--------------+--------------+
                                     |
         +---------------------------+---------------------------+
         |                           |                           |
         v                           v                           v
+------------------+       +-------------------+       +--------------------+
|  Backend Tools   |       |   Sample DB &     |       |   Recommendation   |
| (tools/product_  | <---> |    Catalogue      | <---> |      & Ranker      |
|    tools.py)     |       | (database/prod...) |       | (recommendation/..) |
+------------------+       +-------------------+       +--------------------+
```

### Module Responsibilities & Team Roles

- **Person 1 — Agent & Orchestration (`agent/`)**:
  - Owns agent execution loop, intent classification, constraint extraction, plan generation, activity tracing, and final answer synthesis.
- **Person 2 — Database & Backend Actions (`database/`)**:
  - Owns sample product catalogue, search filters, stock validation, product comparison matrix, and in-memory customer shortlist store.
- **Person 3 — Recommendation & Compatibility (`recommendation/`)**:
  - Owns the multi-criteria ranking algorithm, match score calculation (0–100), recommendation reason generation, and device-accessory compatibility checks.
- **Person 4 — Frontend & Integration Developer (`frontend/`, `app.py`)**:
  - Owns the Streamlit UI, repository integration, user interaction controls, recommendation cards, plan/trace expanders, and end-to-end demo flow.

---

## 📂 Repository Structure

```
SmartCart-AI/
├── agent/
│   ├── __init__.py
│   └── orchestrator.py        # Person 1: Agent logic, planning & traces
├── database/
│   ├── __init__.py
│   └── products.py            # Person 2: Sample catalogue & operations
├── tools/
│   ├── __init__.py
│   └── product_tools.py       # Reusable agent tools & wrappers
├── recommendation/
│   ├── __init__.py
│   └── ranker.py              # Person 3: Scoring & compatibility engine
├── frontend/
│   ├── __init__.py
│   └── app.py                 # Person 4: Streamlit web interface
├── tests/
│   ├── __init__.py
│   ├── test_frontend.py       # Frontend integrity tests
│   └── test_integration.py    # Interface contract & prompt tests
├── app.py                     # Root entry point for Streamlit
├── requirements.txt           # Project dependencies
├── .env.example               # Environment variables template
├── .gitignore                 # Standard Python ignore rules
└── README.md                  # Complete documentation
```

---

## 🚀 Setup & Installation Instructions

### 1. Prerequisites
- Python 3.10, 3.11, or 3.12 installed on your system.
- VS Code or terminal of your choice.

### 2. Clone / Open Repository
Navigate into the `SmartCart-AI` directory:
```bash
cd SmartCart-AI
```

### 3. Create & Activate Virtual Environment

**Windows PowerShell:**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables (Optional)
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
*(Optional)* Add your Gemini API key if you wish to enable Google Gemini-assisted response generation. If left unset, SmartCart AI runs fully in deterministic offline mode.

---

## 🧪 Running Tests

Run the test suite using `pytest` to verify the agreed interface contracts and demo prompts:
```bash
pytest -v
```

---

## 🖥️ How to Run the Streamlit Demo

From the `SmartCart-AI` project root with the virtual environment activated:
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 🎯 Demo Prompts & 5-Minute Presentation Flow

### Recommended Demo Prompts

| Step | User Prompt | What to Point Out |
|---|---|---|
| **1** | `"Find a phone under ₹18,000 with at least 8 GB RAM"` | Show requirement extraction, budget filter, stock check, and match scores. |
| **2** | `"Compare the top two options"` | Point out head-to-head comparison matrix and price verdict. |
| **3** | `"Find an accessory for product ID 1 and check compatibility"` | Highlight automated compatibility verification (e.g. 25W charger for M34). |
| **4** | `"Add product ID 1 to my shortlist"` | Demonstrate persistence to customer shortlist and inspect via sidebar. |

### 5-Minute Demo Timeline

- **0:00–0:30 — Problem Statement**: Explain how shoppers struggle with multi-criteria comparisons and opaque black-box recommendations.
- **0:30–1:00 — User Request**: Submit prompt 1 (*"Find a phone under ₹18,000 with at least 8 GB RAM"*).
- **1:00–2:00 — Agent Loop & Trace**: Expand **Agent plan**, **Extracted requirements**, **Tool results**, and **Agent activity trace** to show each planning and execution step.
- **2:00–3:30 — Recommendations & Reasoning**: Review the scored product cards, match percentages, and explanation bullet points.
- **3:30–4:15 — Actions**: Demonstrate side-by-side comparison and adding an item to the shortlist.
- **4:15–5:00 — Impact & Limits**: Highlight sample catalogue disclaimer, lack of live marketplace API, and future roadmap (vector search, live multi-retailer inventory).

---

## 🔧 Troubleshooting

- **`ModuleNotFoundError`**: Run `streamlit run app.py` from the root `SmartCart-AI/` directory. Ensure `__init__.py` exists in every subfolder.
- **`Streamlit command not found`**: Ensure your virtual environment (`.venv`) is activated and run `pip install streamlit`.
- **`Agent key error`**: Verify that Person 1's orchestrator return dictionary matches the agreed interface schema:
  `answer`, `requirements`, `plan`, `tool_results`, `execution_trace`, `ranked_products`, `evaluation`.
- **Products not visible**: Check that `ranked_products` is a list of dictionaries with `name`, `price`, and `product_id`.

---

## 📄 License
This project is developed as part of the SmartCart AI Hackathon Starter. Licensed under the MIT License.
