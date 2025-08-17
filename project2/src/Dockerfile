FROM python:3.11-slim
ENV QUEUE_URL=https://sqs.us-east-1.amazonaws.com/<user-id>/keda
RUN apt-get update && apt-get install -y \
    unzip curl groff less \
    && rm -rf /var/lib/apt/lists/*
# Install AWS CLI v2
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install \
    && rm -rf awscliv2.zip aws
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY order_processor.py .
CMD ["python", "order_processor.py"]
