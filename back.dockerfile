FROM python:3.12
WORKDIR /app

COPY requirements.txt .

# Install core dependencies (pip...)
RUN pip install --no-cache-dir -r requirements.txt

COPY back ./back
COPY basic_json ./apollo/organizations

CMD ["python", "back"]