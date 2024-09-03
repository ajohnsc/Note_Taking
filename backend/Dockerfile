# Use the Rocky Linux base image
FROM rockylinux:8

# Install dependencies
RUN dnf install -y \
    python39 \
    python39-pip \
    python39-devel \
    gcc \
    && dnf clean all

# Setup the working directory
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install --upgrade pip && pip3 install --no-cache-dir -r requirements.txt

# Copy the application code to the container
COPY . .

# Expose port 8000 for the FastAPI app to run on
EXPOSE 8000

# Run the application with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
