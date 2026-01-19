from fastapi import FastAPI, HTTPException, Response, Security, Depends, status
from fastapi.security import APIKeyHeader
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel, Field
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
from jinja2 import Environment, FileSystemLoader
from typing import List, Optional
import os

# --- 1. Security (Updated for RapidAPI) ---
API_KEY_NAME = "X-RapidAPI-Proxy-Secret"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
API_SECRET = os.getenv("RAPIDAPI_SECRET", "dev-secret-123")

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == API_SECRET:
        return api_key_header
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Access Denied: Request must come from RapidAPI"
        )

# --- 2. App Config ---
app = FastAPI(
    title="Thai PDF API Service", 
    version="1.1.0",
    docs_url=None,    
    redoc_url=None,   
    openapi_url="/openapi.json"
)

if os.path.exists("templates"):
    templates = Environment(loader=FileSystemLoader("templates"))
else:
    templates = None

if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/docs", include_in_schema=False)
async def scalar_html():
    if not templates:
        return HTMLResponse("Templates folder not found")
    template = templates.get_template("docs.html")
    return HTMLResponse(template.render())

# --- 3. Data Models ---
class PdfRequest(BaseModel):
    html_content: str
    paper_size: str = "A4"
    orientation: str = "portrait"

class OrderItem(BaseModel):
    name: str
    quantity: int
    price: str
    total: str

class InvoiceData(BaseModel):
    logo_url: Optional[str] = Field(None)
    invoice_no: str
    date: str
    provider_name: str = Field(..., example="บริษัท ของเรา จำกัด")
    provider_address: str = Field(..., example="ที่อยู่บริษัท...")
    provider_tax_id: Optional[str] = Field(None, example="1234567890123")
    customer_name: str
    customer_address: str
    customer_tax_id: Optional[str] = Field(None, example="")
    items: List[OrderItem]
    subtotal: str
    vat: str
    grand_total: str

# --- 4. Helper ---
def get_base_css(paper_size="A4", orientation="portrait"):
    return f"""
        @page {{ size: {paper_size} {orientation}; margin: 1.5cm; }}
        @font-face {{ font-family: 'Sarabun'; src: local('Sarabun'), local('Sarabun-Regular'); }}
        body {{ font-family: 'Sarabun', sans-serif; }}
    """

# --- 5. Endpoints ---
@app.get("/", include_in_schema=False)
async def read_index():
    if os.path.exists("static/index.html"): return FileResponse('static/index.html')
    return {"message": "API Running"}

@app.post("/generate-pdf", dependencies=[Depends(get_api_key)])
async def generate_pdf(req: PdfRequest):
    try:
        font_config = FontConfiguration()
        base_css = CSS(string=get_base_css(req.paper_size, req.orientation), font_config=font_config)
        pdf_file = HTML(string=req.html_content).write_pdf(stylesheets=[base_css], font_config=font_config)
        return Response(content=pdf_file, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=document.pdf"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/create-demo", tags=["Templates"])
async def create_demo(data: InvoiceData):
    try:
        if not templates: raise HTTPException(status_code=500, detail="No templates")
        template = templates.get_template("invoice_demo.html")
        html_content = template.render(**data.model_dump())
        font_config = FontConfiguration()
        base_css = CSS(string=get_base_css(), font_config=font_config)
        pdf_file = HTML(string=html_content).write_pdf(stylesheets=[base_css], font_config=font_config)
        return Response(content=pdf_file, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=demo_invoice.pdf"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/create-invoice", tags=["Templates"], dependencies=[Depends(get_api_key)])
async def create_invoice(data: InvoiceData):
    try:
        if not templates: raise HTTPException(status_code=500, detail="No templates")
        template = templates.get_template("invoice.html")
        html_content = template.render(**data.model_dump())
        font_config = FontConfiguration()
        base_css = CSS(string=get_base_css(), font_config=font_config)
        pdf_file = HTML(string=html_content).write_pdf(stylesheets=[base_css], font_config=font_config)
        return Response(content=pdf_file, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=invoice.pdf"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))