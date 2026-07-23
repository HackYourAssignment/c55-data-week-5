FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ ./src/
RUN curl -sL https://aka.ms/InstallAzureCLIDeb | bash
RUN apt-get update && apt-get install -y curl ca-certificates \
&& curl -sL https://aka.ms/InstallAzureCLIDeb | bash \
&& rm -rf /var/lib/apt/lists/*
CMD ["python", "-m", "src.pipeline"]