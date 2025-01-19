# Use uma imagem base leve do Python
FROM python:3.12.5-slim

# Defina o diretório de trabalho dentro do container
WORKDIR /app

# Copie os arquivos necessários para o container
COPY . .

# Instale as dependências da aplicação
RUN pip install --no-cache-dir -r requirements.txt

# Exponha a porta 8000 para o tráfego HTTP
EXPOSE 8000

# Comando para rodar a aplicação usando gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8000", "wsgi:app"]
