FROM python:3.12-alpine

WORKDIR /app

# Utilisateur non-root
RUN addgroup -S app && adduser -S app -G app

# 1) Dépendances d'abord : couche mise en cache tant que requirements.txt ne change pas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2) Code ensuite : change souvent, donc en dernier
COPY app.py .

USER app
EXPOSE 5000
CMD ["python", "app.py"]