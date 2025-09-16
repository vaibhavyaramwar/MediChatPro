# MediChat Pro 🏥

Intelligent medical document assistant that lets a user upload one or more PDF medical records and then chat with them using retrieval‑augmented generation (RAG).

## ✨ Core Capabilities
* Multi‑PDF upload (drag & drop in sidebar)
* Text extraction with `pypdf`
* Chunking via `RecursiveCharacterTextSplitter`
* Embedding with `sentence-transformers/all-MiniLM-L6-v2`
* Vector index using FAISS (in‑memory)
* Semantic retrieval (top‑k similarity)
* Contextual answer generation with a hosted / configured chat model (Euri AI wrapper)
* Stateful chat history (Streamlit session)

## 🧱 High-Level Architecture

```mermaid
flowchart LR
	U[User] -->|Upload PDFs| UP[Streamlit Sidebar\n pdf_uploader()]
	UP --> EX[PDF Text Extraction\nextract_text_from_pdf]
	EX --> CH[Chunking\nRecursiveCharacterTextSplitter]
	CH --> EMB[Embedding\nHuggingFaceEmbeddings]
	EMB --> VS[FAISS Index]
	subgraph Chat Loop
		Q[User Question] --> RET[Similarity Search\nretrive_relevant_docs]
		RET --> CTX[Assemble Context]\n
		CTX --> PROMPT[System Prompt Builder]
		PROMPT --> LLM[Chat Model\ncreate_chat_model]
		LLM --> A[Answer]
	end
	VS --> RET
	A --> HIST[Chat History]
	HIST --> Q
```

## 🔁 Detailed Flow
1. **Upload**: User selects one or more PDF files (sidebar component `pdf_uploader`).
2. **Extraction**: Each file processed by `extract_text_from_pdf` using `pypdf`. Pages concatenated to a raw text corpus.
3. **Chunking**: Text split into overlapping windows (`chunk_size=1000`, `chunk_overlap=200`) to preserve semantic continuity.
4. **Embedding**: Each chunk converted into a vector via `HuggingFaceEmbeddings` (MiniLM model) – balances speed & quality.
5. **Indexing**: A FAISS index is built (`FAISS.from_texts`). Stored in `st.session_state.vectorstore`.
6. **Model Init**: Chat model instantiated with `get_chat_model` (Euri AI wrapper pointing to `gpt-4.1-nano`).
7. **Question Handling**:
   * User enters a natural language query.
   * Top‑k (default 4) similar chunks retrieved via `similarity_search`.
   * Retrieved chunks concatenated into a contextual system prompt.
   * Model invoked (`ask_chat_model`).
   * Response appended to chat history for display & continuity.

## 🗂 Key Modules
| File | Role |
|------|------|
| `main.py` | Streamlit UI orchestration & chat loop |
| `app/ui.py` | Upload widget wrapper |
| `app/pdf_utils.py` | PDF text extraction |
| `app/vectorstore_utils.py` | Embedding + FAISS index & retrieval |
| `app/chat_utils.py` | Chat model factory + single prompt invocation |
| `app/config.py` | Environment + model + email config (future extensibility) |

## 🧪 Retrieval Prompt Pattern
The constructed system prompt embeds the concatenated retrieved document contexts and the user question. There is **no** per‑chunk citation logic yet; you may extend with source attribution.

## 🧬 Design Choices & Rationale
| Aspect | Choice | Reason |
|--------|--------|-------|
| Embeddings | MiniLM L6 v2 | Lightweight, widely used baseline |
| Overlap 200 | Mitigate boundary loss | Ensures entities crossing chunk edges aren’t dropped |
| FAISS in‑memory | Simplicity | Fast prototyping; can swap to disk persistence later |
| Single call RAG | Lower latency | Avoids multi‑turn refine chain overhead |
| Session state chat | Streamlit native | Eliminates external cache dependency |

## 🛡 Security & Privacy Notes
* No PHI scrubbing is implemented—assume sanitized test data only.
* For production: add PII redaction, audit logging, consent workflow, and encryption at rest for vector index.

## 🚀 Running Locally
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run main.py
```

Environment variables (see `app/config.py`):
```
EURI_API_KEY=...
OPENAI_API_BASE=...            # if using self-hosted compatible endpoint
OPENAI_API_KEY=...
```

## 🧩 Extensibility Roadmap
| Feature | Description | Effort |
|---------|-------------|--------|
| Source citations | Show which PDF & page each answer segment came from | Medium |
| Persistent vector store | Save & reload FAISS index across sessions | Low |
| Multi‑model routing | Use larger model only for hard questions | Medium |
| Metadata filtering | Per‑document / section filtering controls | Medium |
| PDF OCR fallback | Handle scanned documents with Tesseract | High |
| Feedback loop | Thumbs up/down to refine retrieval weighting | Medium |
| Email export | Send summarized report to configured doctor email | Low |

## 🧪 Quick Test Snippet (Inside a Python Shell)
```python
from app.vectorstore_utils import create_faiss_index, retrive_relevant_docs
from app.chat_utils import get_chat_model, ask_chat_model
docs = ["Patient has hypertension and is prescribed amlodipine.", "No known allergies. Regular exercise recommended."]
vs = create_faiss_index(docs)
query = "What medication is the patient taking?"
ctx_docs = retrive_relevant_docs(vs, query)
ctx = "\n".join(d.page_content for d in ctx_docs)
prompt = f"Context:\n{ctx}\n\nQuestion: {query}\nAnswer:"
model = get_chat_model(api_key="demo-key")
print(ask_chat_model(model, prompt))
```

## 🔍 Troubleshooting
| Issue | Likely Cause | Fix |
|-------|-------------|-----|
| Empty answers | Retrieval missed context | Increase k or reduce chunk_size |
| Slow startup | Downloading embedding model | Pre-warm or cache model directory |
| Memory spike | Large PDFs & overlap | Tune chunk_size / overlap |
| Re-upload required after refresh | Stateless index | Persist FAISS or cache to disk |

## ⚠ Medical Disclaimer
This tool is for informational assistance only and **not** a substitute for professional medical advice, diagnosis, or treatment.

## 📄 License
Currently unspecified; add a license file if distributing.

---
Feel free to extend and adapt for richer clinical workflows.
