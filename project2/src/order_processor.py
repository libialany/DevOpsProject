import boto3
import json
import logging
import os
import time
from datetime import datetime
from typing import Dict, Optional

class OrderProcessor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.sqs = boto3.client('sqs',
            aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
            region_name=os.environ.get('AWS_REGION', 'us-east-1')
        )
        self.queue_url = os.environ['QUEUE_URL']
        
    def process_order(self, order_data: Dict) -> bool:
        """
        Process a single order with comprehensive error handling
        
        Args:
            order_data: Dictionary containing order information
            
        Returns:
            bool: Processing success status
        """
        try:
            self.logger.info(f"Processing order {order_data['order_id']} at {datetime.now()}")
            
            # Implement core business logic here
            # Example: Order validation, inventory updates, notification dispatch
            
            self.logger.info(f"Successfully processed order: {order_data['order_id']}")
            return True
            
        except KeyError as e:
            self.logger.error(f"Invalid order data format: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Order processing failed: {e}")
            return False

    def start_processing(self) -> None:
        """Main processing loop with error recovery"""
        self.logger.info(f"Initializing order processor at {datetime.now()}")
        
        while True:
            try:
                response = self.sqs.receive_message(
                    QueueUrl=self.queue_url,
                    MaxNumberOfMessages=5,
                    WaitTimeSeconds=10,
                    AttributeNames=['All']
                )
                
                if messages := response.get('Messages'):
                    for message in messages:
                        order_data = json.loads(message['Body'])
                        
                        if self.process_order(order_data):
                            self.sqs.delete_message(
                                QueueUrl=self.queue_url,
                                ReceiptHandle=message['ReceiptHandle']
                            )
                
            except Exception as e:
                self.logger.error(f"Processing loop error: {e}")
                time.sleep(5)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    processor = OrderProcessor()
    processor.start_processing()
