# Use uma imagem base leve do Python
FROM python:alpine


# install google chrome


# Define o diretório de trabalho como /app
WORKDIR /app

# Copia os arquivos do aplicativo para o contêiner
COPY . /app

# Instala as dependências
RUN pip install -r requirements.txt

# Expõe a porta 8000 para o Gunicorn
EXPOSE 5000

# Inicia o servidor Gunicorn para servir o aplicativo Flask
CMD ["flask", "run"]
