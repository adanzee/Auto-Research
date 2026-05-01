## 🛠️ Final Stack 

---

## 1. 🏗️ Core Backend
| Tool | Purpose | Cost |
|---|---|---|
| Python 3.11 | Language |  open source |
| FastAPI | Web framework |  open source |
| Uvicorn | ASGI server (dev) |  open source |
| Gunicorn | Process manager (prod) |  open source |
| Pydantic v2 | Data validation |  open source |
| pydantic-settings | Config from .env |  open source |

---

## 2. 🗄️ Database
| Tool | Purpose | Cost |
|---|---|---|
| PostgreSQL 16 | Primary database |  open source |
| pgvector | Vector embeddings in PG |  open source |
| SQLAlchemy 2.0 | Async ORM |  open source |
| psycopg2-binary | Sync driver for Alembic |  open source |
|

---

## 3. ⚡ Cache & Queue
| Tool | Purpose | Cost |
|---|---|---|
| Redis 7 | Cache + message broker |  open source |
| redis-py | Python Redis client |  open source |
| Celery | Background task queue |  open source |
| Celery Beat | Scheduled tasks (timeouts) |  open source |
| Flower | Celery monitoring UI |  open source |

---

## 4. 🤖 AI / Agent Layer
| Tool | Purpose | Cost |
|---|---|---|
| LangGraph | Multi-agent orchestration |  open source |
| LangChain | LLM utilities + prompt tools |  open source |
| Google AI Studio | Secondary LLM provider |  free tier forever |
| gemini-1.5-flash | Extraction (1M context) |  AI Studio |
| OpenRouter | Fallback LLM provider |  free models |


---

## 5. 🔍 Search & Scraping
| Tool | Purpose | Cost |
|---|---|---|
| Tavily | AI-optimized web search | free-tier |
| httpx | Async HTTP client |  open source |
| BeautifulSoup4 | HTML parsing |  open source |


---

## 6. 📄 Report Generation
| Tool | Purpose | Cost |
|---|---|---|
| WeasyPrint | HTML → PDF conversion |  open source |
| Jinja2 | HTML report templates |  open source |
| markdown | Markdown → HTML |  open source |
| pygments | Syntax highlighting in PDF |  open source |

---

## 7. 🔐 Auth & Security
| Tool | Purpose | Cost |
|---|---|---|
| python-jose | JWT encode/decode |  open source |
| passlib[bcrypt] | Password hashing |  open source |
| python-multipart | Form data parsing |  open source |
| fastapi-limiter | Rate limiting via Redis |  open source |

---

## 8. 📡 API Layer
| Tool | Purpose | Cost |
|---|---|---|
| REST (FastAPI native) | Primary API | no cost |
| Strawberry GraphQL | GraphQL endpoint |  open source |
| websockets | Real-time WS support |  open source |

---

## 9. 📧 Notifications
| Tool | Purpose | Cost |
|---|---|---|
| fastapi-mail | Email sending library |  open source |
| Gmail SMTP | Email provider |  free account |

---

## 10. 🧪 Testing
| Tool | Purpose | Cost |
|---|---|---|
| pytest | Test runner |  open source |
| pytest-asyncio | Async test support |  open source |
| pytest-cov | Code coverage reports |  open source |
| httpx | API test client |  open source |
| 

---

## 11. 📊 Observability
| Tool | Purpose | Cost |
|---|---|---|
| structlog | Structured JSON logging |  open source |
| Flower | Celery pipeline monitor |  open source |
| pgAdmin 4 | PostgreSQL UI |  open source |


---

## 12. 🐳 Containerization & Infra
| Tool | Purpose | Cost |
|---|---|---|
| Docker | Containerization |  open source |
| Docker Compose | Local multi-container setup |  open source |
| Nginx (alpine) | Reverse proxy + SSL |  open source |

---

