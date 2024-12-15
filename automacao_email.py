# Importação das bibliotecas necessárias
import pandas as pd                    
import matplotlib.pyplot as plt         
from fpdf import FPDF                   
import smtplib                          
from email.message import EmailMessage  
import os                               


def gerar_relatorio():
    
    dados = {
        'Dia': ['Seg', 'Ter', 'Qua', 'Qui', 'Sex'],  
        'Vendas': [100, 200, 150, 300, 250]         
    }
    df = pd.DataFrame(dados)  

    
    plt.figure(figsize=(8, 5))  
    plt.bar(df['Dia'], df['Vendas'], color='skyblue') 
    plt.title('Relatório de Vendas')  
    plt.xlabel('Dia')  
    plt.ylabel('Vendas')  
    plt.savefig('relatorio_grafico.png')  

    
    pdf = FPDF()  
    pdf.add_page()  
    pdf.set_font("Arial", size=12)  

    
    pdf.cell(200, 10, txt="Relatório de Vendas - Semanal", ln=True, align='C')  
    pdf.ln(10)  

    
    for i, row in df.iterrows(): 
        pdf.cell(200, 10, txt=f"{row['Dia']}: {row['Vendas']} vendas", ln=True)

    
    pdf.image('relatorio_grafico.png', x=60, y=60, w=90)  
    pdf.output("relatorio.pdf")  

    
    os.remove('relatorio_grafico.png')



def enviar_email():
    
    EMAIL_USER = "seugmail@gmail.com"  
    EMAIL_PASSWORD = "sua senha"        
    DESTINATARIO = "seugmail@gmail.com"  

    
    msg = EmailMessage()  
    msg['Subject'] = "Relatório Diário de Vendas"  
    msg['From'] = EMAIL_USER  
    msg['To'] = DESTINATARIO  
    msg.set_content("Segue em anexo o relatório diário de vendas.")  

    
    msg["X-Priority"] = "1"  
    msg["X-MSMail-Priority"] = "High"

    
    with open("relatorio.pdf", "rb") as f:  
        file_data = f.read()  
        file_name = "relatorio.pdf"  
    msg.add_attachment(file_data, maintype="application", subtype="pdf", filename=file_name)

    
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:  
            smtp.login(EMAIL_USER, EMAIL_PASSWORD)  
            smtp.send_message(msg)  
        print("E-mail enviado com sucesso!")  
    except smtplib.SMTPException as e:
        print(f"Erro ao enviar o e-mail: {e}")  

"""
======================================
# Comentário sobre o uso de senhas de app
======================================

- **Por que usar uma senha de app?**  
  O Gmail exige uma senha específica para aplicativos ao usar o protocolo SMTP para envio de e-mails.  
  Isso é necessário **apenas quando a autenticação em dois fatores (2FA)** está **ativada**.

- **Quando a senha de app NÃO é necessária?**  
  Se a autenticação em dois fatores estiver **desativada**, é possível usar a senha principal da conta.  
  No entanto, o Google pode bloquear o acesso por considerar esse procedimento "menos seguro".

- **Recomendação:**  
  Manter a **autenticação em dois fatores ativada** e usar uma **senha de app** específica para o envio de e-mails via SMTP.  
  Isso garante segurança adicional à conta do Gmail.
"""

# 3. Execução do Script Principal
if __name__ == "__main__":
    gerar_relatorio()  # Chama a função para gerar o relatório
    enviar_email()  # Chama a função para enviar o e-mail
