# AquaLogic RAG: AI-Powered Water Policy Navigator

**Grounding IBM Granite AI in Municipal Law for Sustainable Water Action**
*1M1B AI for Sustainability Virtual Internship | IBM SkillsBuild | AICTE*

---

## Architecture Overview

AquaLogic utilizes a modular Retrieval-Augmented Generation (RAG) architecture to bridge the gap between complex legal policy and citizen-led conservation.

```text
[ Citizen Query ] --> [ Streamlit UI ] --> [ RAG Pipeline ] --> [ IBM Granite-13B ]
                             |                    ^                  |
                             v                    |                  v
                    [ ChromaDB Vector Store ] ----┘           [ Actionable Advice ]
                    (Municipal Policy Library)
```

## Key Features

* **Jargon-to-Action Translator:** Simplifies technical legal terms such as "riparian rights" into direct, actionable instructions for non-technical users.

* **Policy Comparison Agent:** Provides compliance assessment of user behavior against municipal wastewater and water extraction bylaws.

* **Conservation Checklist:** Generates personalized and prioritized efficiency plans based on regional scarcity tiers and legislative requirements.

* **Enterprise Dashboard:** A professional Streamlit interface featuring real-time impact metrics and downloadable action plans.

## SDG 6 Alignment (Clean Water and Sanitation)

| Target        | Description               | Project Implementation                                            |
| :------------ | :------------------------ | :---------------------------------------------------------------- |
| **6.1 & 6.5** | Equitable access and IWRM | Democratizes legal knowledge for non-technical stakeholders.      |
| **6.3**       | Wastewater Management     | Surfaces discharge standards for households and small businesses. |
| **6.4**       | Water-use Efficiency      | Provides policy-grounded checklists to reduce urban water waste.  |
| **6.b**       | Local Participation       | Lowers the barrier to entry for community-led water governance.   |

## Responsible AI and Ethics

* **Zero-Hallucination Guardrails:** The AquaLogic Sustainability Engine utilizes a strict grounding contract. If the factual basis is missing from the retrieved legal context, the system triggers a hard-stop response.

* **Source Transparency:** Every AI-generated response provides a citation of the municipal code, relevant section, and page used for the reasoning.

* **Metadata Evidence:** A hidden `.bob` directory is maintained in the root, containing the technical audit trail of AI-assisted planning using IBM Bob.

## Project Methodology and Structure

This project follows professional software engineering standards using a modular directory structure.

```text
AquaLogic-RAG/
│
├── src/
│   ├── RAG logic
│   ├── Retrieval modules
│   └── Grounded prompt templates
│
├── app.py
├── data/
│   └── Municipal policy library
│
├── run_diagnostic.py
├── configs/
│   └── config.yaml
├── requirements.txt
└── README.md
```

| Component           | Description                                                                         |
| :------------------ | :---------------------------------------------------------------------------------- |
| `src/`              | Core RAG logic, retrieval modules, and grounded prompt templates.                   |
| `app.py`            | Streamlit-based application dashboard.                                              |
| `data/`             | Multi-document policy library containing domestic and industrial datasets.          |
| `run_diagnostic.py` | Technical pipeline simulation tool for logic verification and architecture testing. |
| `configs/`          | Centralized model and retrieval parameters.                                         |
| `config.yaml`       | Model and retrieval configuration.                                                  |
| `requirements.txt`  | Python dependencies required to run the project.                                    |

## Setup and Usage

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Execute Diagnostic Logic Proof

```bash
python run_diagnostic.py
```

### 3. Launch the Dashboard

```bash
streamlit run app.py
```

## Technology Stack

* Python
* Streamlit
* IBM Granite
* Retrieval-Augmented Generation (RAG)
* ChromaDB
* Vector Embeddings
* Municipal Policy Documents
* IBM SkillsBuild
* AICTE
* 1M1B AI for Sustainability

## Project Objective

AquaLogic aims to make municipal water policies easier to understand and act upon by combining Generative AI, Retrieval-Augmented Generation, and policy-grounded information retrieval.

The system helps citizens and other non-technical stakeholders understand relevant water regulations and translate them into practical conservation actions.

## Technical Note

This repository is a technical prototype developed for the **1M1B AI for Sustainability Virtual Internship**. All AI logic is designed around the IBM Granite foundation model family, with an emphasis on grounded retrieval, source transparency, and responsible AI practices.
