FROM python:3.11-slim

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    libnss3 \
    libgdk-pixbuf2.0-0 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libxss1 \
    libxtst6 \
    xdg-utils \
    wget

# Baixar e instalar o Google Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    dpkg -i google-chrome-stable_current_amd64.deb && \
    apt-get -y install -f

# Instalar as dependências do Python
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copiar o código do projeto
COPY . /app
WORKDIR /app

# Definir a variável de ambiente DISPLAY
ENV DISPLAY=:99

# Expor a porta
EXPOSE 5000

# Comando para rodar o Flask
CMD ["python", "app.py"]
