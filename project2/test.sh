#!/bin/bash
for i in {1..20}; do
  aws sqs send-message     --queue-url https://sqs.us-east-1.amazonaws.com/<user-id>/keda  --message-body "{\"order_id\": \"test123\", \"timestamp\": \"2025-08-17T05:12:22Z\"}"
done
