FROM python:3.11
WORKDIR /var/www/html
RUN pip install --upgrade pip
# Copy only requirements txt before copying the rest to leverage cache
COPY ../requirements.txt . 
# Install all dependencies
RUN pip install -r requirements.txt
# Copy all files into the container
COPY ../ .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
