# 🛡️ GRC Audit Tool

A multi-framework **Governance, Risk & Compliance (GRC) Audit Tool** built for cybersecurity professionals. Assess your organisation against leading frameworks, visualise gaps, and track remediation — all in one place.

![Tech Stack](https://img.shields.io/badge/Backend-FastAPI-009688?style=flat-square&logo=fastapi)
![Tech Stack](https://img.shields.io/badge/Frontend-React-61DAFB?style=flat-square&logo=react)
![Tech Stack](https://img.shields.io/badge/Database-PostgreSQL-4169E1?style=flat-square&logo=postgresql)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## 📋 Supported Frameworks

| Framework | Version | Domains |
|---|---|---|
| NIST Cybersecurity Framework | CSF 2.0 | Govern, Identify, Protect, Detect, Respond, Recover |
| ISO/IEC 27001 | 2022 | 4 Clauses, Annex A Controls |
| CIS Controls | v8 | 18 Control Groups, 153 Safeguards |

---

## 🏗️ Architecture

```
grc-audit-tool/
├── backend/          # FastAPI Python backend
│   ├── app/
│   │   ├── api/      # Route handlers
│   │   ├── models/   # SQLAlchemy ORM models
│   │   ├── schemas/  # Pydantic schemas
│   │   ├── services/ # Business logic
│   │   └── data/     # Framework JSON seed data
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/         # React + Tailwind CSS
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── api/
│   └── Dockerfile
├── docker-compose.yml
└── .github/workflows/ # CI/CD pipeline
```

---

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 18+
- Python 3.11+

### Run with Docker Compose
```bash
git clone https://github.com/AryanKedare/grc-audit-tool.git
cd grc-audit-tool
docker-compose up --build
```

App will be available at:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs (Swagger)**: http://localhost:8000/docs

### Run Locally (without Docker)
```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend (new terminal)
cd frontend
npm install
npm start
```

---

## ✨ Features

- ✅ **Multi-Framework Assessments** — Assess against NIST CSF, ISO 27001, CIS Controls
- ✅ **Cross-Framework Control Mapping** — See overlapping controls across frameworks
- ✅ **Compliance Scoring** — Per-framework and per-domain compliance percentage
- ✅ **Gap Analysis Dashboard** — Visual radar/bar charts of compliance posture
- ✅ **Remediation Tracker** — Assign gaps to owners with due dates and status tracking
- ✅ **Evidence Notes** — Attach notes and evidence references per control
- ✅ **Export Reports** — Download gap reports as CSV/PDF
- ✅ **JWT Authentication** — Secure user accounts with role-based access

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/frameworks` | List all supported frameworks |
| `GET` | `/api/frameworks/{id}/controls` | Get controls for a framework |
| `POST` | `/api/assessments` | Create a new assessment |
| `PUT` | `/api/assessments/{id}/controls/{control_id}` | Submit control response |
| `GET` | `/api/assessments/{id}/score` | Get compliance score |
| `GET` | `/api/assessments/{id}/gaps` | Get gap analysis |
| `GET` | `/api/remediation` | List remediation tasks |

---

## 🗺️ Roadmap

- [ ] GDPR & HIPAA framework support
- [ ] Automated evidence collection via API integrations
- [ ] AI-powered control suggestions
- [ ] Multi-user organisation workspaces
- [ ] OSCAL-format import/export

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

> Built by [Aryan Kedare](https://github.com/AryanKedare) as a cybersecurity portfolio project.
