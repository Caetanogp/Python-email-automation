import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import smtplib
from email.message import EmailMessage
import os

def generate_report():
    data = {
        'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
        'Sales': [100, 200, 150, 300, 250]
    }
    df = pd.DataFrame(data)
    
    plt.figure(figsize=(8, 5))
    plt.bar(df['Day'], df['Sales'], color='skyblue')
    plt.title('Sales Report')
    plt.xlabel('Day')
    plt.ylabel('Sales')
    plt.savefig('report_chart.png')
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    pdf.cell(200, 10, txt="Weekly Sales Report", ln=True, align='C')
    pdf.ln(10)
    
    for i, row in df.iterrows():
        pdf.cell(200, 10, txt=f"{row['Day']}: {row['Sales']} sales", ln=True)
    
    pdf.image('report_chart.png', x=60, y=60, w=90)
    pdf.output("report.pdf")
    
    os.remove('report_chart.png')

def send_email():
    EMAIL_USER = "youremail@gmail.com"
    EMAIL_PASSWORD = "yourpassword"
    RECIPIENT = "youremail@gmail.com"
    
    msg = EmailMessage()
    msg['Subject'] = "Daily Sales Report"
    msg['From'] = EMAIL_USER
    msg['To'] = RECIPIENT
    msg.set_content("Attached is the daily sales report.")
    
    msg["X-Priority"] = "1"
    msg["X-MSMail-Priority"] = "High"
    
    with open("report.pdf", "rb") as f:
        file_data = f.read()
        file_name = "report.pdf"
    msg.add_attachment(file_data, maintype="application", subtype="pdf", filename=file_name)
    
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_USER, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print("Email sent successfully!")
    except smtplib.SMTPException as e:
        print(f"Error sending the email: {e}")

if __name__ == "__main__":
    generate_report()
    send_email()
"""
=======================================
# Explanation about the use of app passwords
=======================================

- **Why use an app password?**
  Gmail requires a specific app password when using the SMTP protocol to send emails. 
  This is necessary **only when two-factor authentication (2FA)** is **enabled** for your Gmail account.

- **When is the app password NOT required?**
  If two-factor authentication is **disabled**, you can use the main password of your Gmail account. 
  However, Google may block access because it considers this procedure "less secure."

- **Recommendation:**
  Keep **two-factor authentication enabled** and use a **unique app password** specifically for sending emails via SMTP. 
  This ensures additional security for your Gmail account.
"""
