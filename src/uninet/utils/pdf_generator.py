from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_portfolio_pdf(student_data):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    p.drawString(100, 750, f"Co-Curricular Portfolio: {student_data.get('name', 'Student')}")
    p.drawString(100, 730, f"Email: {student_data.get('email', 'N/A')}")
    
    y = 690
    p.drawString(100, y, "Badges & Achievements:")
    y -= 20
    
    for badge in student_data.get('badges', []):
        p.drawString(120, y, f"- {badge}")
        y -= 15
        
    p.showPage()
    p.save()
    
    buffer.seek(0)
    return buffer
