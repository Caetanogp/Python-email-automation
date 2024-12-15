# Importação das bibliotecas necessárias
import pandas as pd                     # Manipulação de dados e criação de tabelas
import matplotlib.pyplot as plt         # Criação de gráficos
from fpdf import FPDF                   # Geração de arquivos PDF
import smtplib                          # Envio de e-mails via protocolo SMTP
from email.message import EmailMessage  # Construção do conteúdo do e-mail
import os                               # Manipulação de arquivos (remoção, etc.)

# 1. Função para gerar o relatório em PDF
def gerar_relatorio():
    # Criação de dados fictícios de vendas semanais
    dados = {
        'Dia': ['Seg', 'Ter', 'Qua', 'Qui', 'Sex'],  # Dias da semana
        'Vendas': [100, 200, 150, 300, 250]         # Quantidade de vendas em cada dia
    }
    df = pd.DataFrame(dados)  # Transformando os dados em um DataFrame do pandas

    # Geração do gráfico de barras
    plt.figure(figsize=(8, 5))  # Define o tamanho da figura (8x5 polegadas)
    plt.bar(df['Dia'], df['Vendas'], color='skyblue')  # Cria um gráfico de barras
    plt.title('Relatório de Vendas')  # Título do gráfico
    plt.xlabel('Dia')  # Rótulo do eixo X
    plt.ylabel('Vendas')  # Rótulo do eixo Y
    plt.savefig('relatorio_grafico.png')  # Salva o gráfico como uma imagem

    # Criação do relatório em PDF usando a biblioteca FPDF
    pdf = FPDF()  # Inicializa um objeto PDF
    pdf.add_page()  # Adiciona uma nova página ao PDF
    pdf.set_font("Arial", size=12)  # Define a fonte e o tamanho do texto

    # Adiciona um título ao PDF
    pdf.cell(200, 10, txt="Relatório de Vendas - Semanal", ln=True, align='C')  
    pdf.ln(10)  # Adiciona um espaço vertical

    # Adiciona as informações das vendas no PDF
    for i, row in df.iterrows():  # Itera por cada linha do DataFrame
        pdf.cell(200, 10, txt=f"{row['Dia']}: {row['Vendas']} vendas", ln=True)

    # Insere a imagem do gráfico no PDF
    pdf.image('relatorio_grafico.png', x=60, y=60, w=90)  # x, y são as coordenadas; w é a largura
    pdf.output("relatorio.pdf")  # Salva o relatório como "relatorio.pdf"

    # Remove o arquivo temporário do gráfico (limpeza)
    os.remove('relatorio_grafico.png')


# 2. Função para enviar o e-mail com o relatório em anexo
def enviar_email():
    # Configurações do remetente e do destinatário
    EMAIL_USER = "seugmail@gmail.com"  # Substitua por seu e-mail Gmail
    EMAIL_PASSWORD = "sua senha"        # Substitua pela sua senha ou senha de app gerada
    DESTINATARIO = "seugmail@gmail.com"  # E-mail do destinatário (Gmail)

    # Criação do e-mail
    msg = EmailMessage()  # Inicializa um objeto EmailMessage
    msg['Subject'] = "Relatório Diário de Vendas"  # Assunto do e-mail
    msg['From'] = EMAIL_USER  # E-mail do remetente
    msg['To'] = DESTINATARIO  # E-mail do destinatário
    msg.set_content("Segue em anexo o relatório diário de vendas.")  # Corpo do e-mail

    # Adicionando cabeçalhos de prioridade
    msg["X-Priority"] = "1"  # Alta prioridade
    msg["X-MSMail-Priority"] = "High"

    # Anexando o relatório PDF ao e-mail
    with open("relatorio.pdf", "rb") as f:  # Abre o arquivo em modo binário (leitura)
        file_data = f.read()  # Lê os dados binários do PDF
        file_name = "relatorio.pdf"  # Nome do arquivo anexado
    msg.add_attachment(file_data, maintype="application", subtype="pdf", filename=file_name)

    # Tenta enviar o e-mail
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:  # Conexão com servidor SMTP do Gmail via SSL
            smtp.login(EMAIL_USER, EMAIL_PASSWORD)  # Realiza login com o e-mail e senha fornecidos
            smtp.send_message(msg)  # Envia o e-mail com a mensagem configurada
        print("E-mail enviado com sucesso!")  # Confirmação de envio
    except smtplib.SMTPException as e:
        print(f"Erro ao enviar o e-mail: {e}")  # Caso ocorra um erro ao enviar o e-mail

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
