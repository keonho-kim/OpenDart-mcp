# 1. Base Image
FROM python:3.13-slim

# 2. Set Environment Variables for Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Set Working Directory
WORKDIR /app

# 4. Install uv package manager
RUN pip install uv

# 5. Copy dependency definition files
COPY README.md pyproject.toml uv.lock ./

# 6. Install dependencies and the project itself using uv
RUN uv venv
RUN uv pip install . 

# 7. Copy application code
COPY app.py .
COPY src/ ./src/

# 8. Create data directory for the database
RUN mkdir sqlite

# 9. Set the entrypoint
CMD ["uv", "run", "python", "app.py"] 