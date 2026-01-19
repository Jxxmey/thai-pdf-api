# Thai PDF API 🇹🇭

A robust and fast API for generating PDF documents from HTML, specifically optimized for the **Thai language**. Built with Python (FastAPI) and WeasyPrint.

## 🚀 Features
- **Perfect Thai Rendering:** Solves common issues with Thai vowels and tone marks.
- **Pre-loaded Fonts:** Includes official 'Sarabun' font.
- **High Performance:** Lightweight and fast generation.
- **Production Ready:** Dockerized and ready to deploy.

## 🛠 Installation & Setup

### Local Development
1. Clone the repo
2. Install requirements: `pip install -r requirements.txt`
3. Run server: `uvicorn main:app --reload`

### Docker Support
```bash
docker build -t thai-pdf-api .
docker run -p 80:80 thai-pdf-api
