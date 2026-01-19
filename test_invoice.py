import requests
import os
import platform

# ข้อมูลที่เราจะส่ง (ไม่มี HTML เลย มีแต่ Data ล้วนๆ)
invoice_data = {
    "customer_name": "บริษัท ร่ำรวย จำกัด (มหาชน)",
    "customer_address": "999 ชั้น 20 ตึกเอ็มไพร์ สาทร กทม.",
    "invoice_no": "INV-2024-888",
    "date": "19 ม.ค. 2569",
    "items": [
        {"name": "ค่าบริการทำ API", "quantity": 1, "price": "5,000.00", "total": "5,000.00"},
        {"name": "ค่าเช่า Server รายปี", "quantity": 1, "price": "12,000.00", "total": "12,000.00"},
        {"name": "ส่วนลดพิเศษ", "quantity": 1, "price": "-1,000.00", "total": "-1,000.00"}
    ],
    "subtotal": "16,000.00",
    "vat": "1,120.00",
    "grand_total": "17,120.00"
}

print("Creating Invoice from Template...")

try:
    # ยิงไปที่ Endpoint ใหม่ /create-invoice
    response = requests.post("http://localhost:8000/create-invoice", json=invoice_data)

    if response.status_code == 200:
        with open("invoice_template.pdf", "wb") as f:
            f.write(response.content)
        print("✅ สำเร็จ! เปิดไฟล์ invoice_template.pdf ดูเลย")
        
        # เปิดไฟล์อัตโนมัติ
        if platform.system() == 'Windows': os.startfile("invoice_template.pdf")
    else:
        print("❌ Error:", response.text)

except Exception as e:
    print("❌ Connection Error:", e)