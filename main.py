from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from docx import Document
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

def create_offer_letter(name, position, date, salary):
    doc = Document("templates/offer_template.docx")
    for para in doc.paragraphs:
        para.text = para.text.replace("{{name}}", name)
        para.text = para.text.replace("{{position}}", position)
        para.text = para.text.replace("{{date}}", date)
        para.text = para.text.replace("{{salary}}", salary)
    filename = f"{name.replace(' ', '_')}_Offer_Letter.docx"
    doc.save(filename)
    return filename

def send_email(to_email, subject, body, attachment=None):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = to_email
    msg.set_content(body)

    if attachment:
        with open(attachment, "rb") as f:
            msg.add_attachment(f.read(), maintype="application", subtype="octet-stream", filename=attachment)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL, PASSWORD)
        smtp.send_message(msg)

@app.post("/send-offer")
def send_offer(
    name: str = Form(...),
    email: str = Form(...),
    position: str = Form(...),
    salary: str = Form(...),
    joining_date: str = Form(...),
):
    filename = create_offer_letter(name, position, joining_date, salary)
    send_email(email, "Your Offer Letter", "Please find your offer letter attached.", filename)
    return {"status": "Offer letter sent!"}

@app.post("/thank-you")
def send_thank_you(name: str = Form(...), email: str = Form(...), position: str = Form(...)):
    body = f"Dear {name},\n\nThank you for showing interest in the {position} position at our company. We appreciate your application and will get back to you soon.\n\nBest,\nHR Team"
    send_email(email, "Thank you for applying", body)
    return {"status": "Thank you email sent!"}

@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <div style="display:flex; flex-direction:column; align-items:center; justify-content:center; min-height:100vh; font-family:Arial, sans-serif; background:#f0f2f5;">

  <h2 style="color:#2c3e50; margin-bottom:20px;">DALAVE Pvt. Ltd</h2>

  <div style="background:white; padding:30px; border-radius:10px; box-shadow:0 4px 12px rgba(0,0,0,0.1); width:320px; margin-bottom:40px;">
    <h3 style="margin-top:0; margin-bottom:20px; color:#34495e;">Send Offer Letter</h3>
    <form method="POST" action="/send-offer">
      <input name="name" placeholder="Employee Name" required style="width:100%; padding:10px; margin:8px 0; border:1px solid #ccc; border-radius:6px;"><br>
      <input name="email" placeholder="Employee Email" required style="width:100%; padding:10px; margin:8px 0; border:1px solid #ccc; border-radius:6px;"><br>
      <input name="position" placeholder="Position" required style="width:100%; padding:10px; margin:8px 0; border:1px solid #ccc; border-radius:6px;"><br>
      <input name="salary" placeholder="Salary" required style="width:100%; padding:10px; margin:8px 0; border:1px solid #ccc; border-radius:6px;"><br>
      <input name="joining_date" type="date" required style="width:100%; padding:10px; margin:8px 0; border:1px solid #ccc; border-radius:6px;"><br>
      <button type="submit" style="width:100%; padding:10px; background:#3498db; color:white; border:none; border-radius:6px; font-weight:bold; cursor:pointer;">Send Offer Letter</button>
    </form>
  </div>

  <div style="background:white; padding:30px; border-radius:10px; box-shadow:0 4px 12px rgba(0,0,0,0.1); width:320px;">
    <h3 style="margin-top:0; margin-bottom:20px; color:#34495e;">Send Thank You Email</h3>
    <form method="POST" action="/thank-you">
      <input name="name" placeholder="Candidate Name" required style="width:100%; padding:10px; margin:8px 0; border:1px solid #ccc; border-radius:6px;"><br>
      <input name="email" placeholder="Candidate Email" required style="width:100%; padding:10px; margin:8px 0; border:1px solid #ccc; border-radius:6px;"><br>
      <input name="position" placeholder="Applied Position" required style="width:100%; padding:10px; margin:8px 0; border:1px solid #ccc; border-radius:6px;"><br>
      <button type="submit" style="width:100%; padding:10px; background:#2ecc71; color:white; border:none; border-radius:6px; font-weight:bold; cursor:pointer;">Send Thank You Mail</button>
    </form>
  </div>

</div>


    """