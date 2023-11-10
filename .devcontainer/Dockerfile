FROM python:3.9-slim
WORKDIR /usr/src/app

# Install any needed packages specified in requirements.txt
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Install system dependencies for PyTesseract
RUN apt-get update && apt-get install -y tesseract-ocr libtesseract-dev

# Copy the current directory contents into the WORKDIR
COPY . .
