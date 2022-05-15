import logging
import boto3
import os

from botocore.exceptions import ClientError


import json
import uuid

AWS_REGION = "us-east-1"
SERVICE_NAME = "sqs"
AWS_ACCESS_KEY_ID = os.environ.get("PERSONAL_AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.environ.get("PERSONAL_AWS_ACCESS_SECRET")

# logger config
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s: %(levelname)s: %(message)s')

sqs_resource = {
    "service_name": SERVICE_NAME,
    "region_name": AWS_REGION,
    "aws_access_key_id": AWS_ACCESS_KEY_ID,
    "aws_secret_access_key": AWS_SECRET_KEY
}

class Resource:
    def __init__(self, **kwargs):
        self.sqs_resource = boto3.client(**kwargs)


class Queue(Resource):
    def __init__(self, queue_details, **kwargs):
        super().__init__(**kwargs)
        self.queue_name = queue_details.get("queue_name")
        self.queue_url = queue_details.get("queue_url")
        self.queue_attributes = None
        self.message_attributes = None

    def set_queue_attributes(self, **kwargs):
        self.queue_attributes = {
            "DelaySeconds": kwargs.get("delay_seconds", "10"),
            "MessageRetentionPeriod": kwargs.get("message_retention_period", "172800"),
            "VisibilityTimeout": kwargs.get("delay_seconds", "300")
        }

    def create_queue(self):
        logger.info(f"Creating queue: {self.queue_name}")
        try:
            response = self.sqs_resource.create_queue(
                QueueName=self.queue_name,
                Attributes=self.queue_attributes
            )
        except ClientError:
            logger.exception("Couldn't create SQS queue")
        else:
            return response

    def set_message_attributes(self, **kwargs):
        if not self.queue_url:
            raise NotImplementedError("Queue url not set")
        self.message_attributes = {
            "QueueUrl": self.queue_url,
            "MessageBody": kwargs.get("message_body")
        }

    def send_message(self):
        return self.sqs_resource.send_message(**self.message_attributes)

    def get_queue_url_by_name(self):
        if not self.queue_name:
            raise NotImplementedError("Queue name not set")

        response = self.sqs_resource.get_queue_url(QueueName=self.queue_name)

        # except ClientError:
        #     logger.exception(f'Could not get the {self.queue_name} queue.')

        return response

    def receive_message(self):
        return self.sqs_resource.receive_message(QueueUrl=self.queue_url, AttributeNames=['All'])

    def delete_message(self, receipt_handle):
        return self.sqs_resource.delete_message(QueueUrl=self.queue_url, ReceiptHandle=receipt_handle)


class FIFOQueue(Queue):
    def __init__(self, queue_details, **kwargs):
        if queue_details.get("queue_name") and not queue_details.get("queue_name").endswith(".fifo"):
            queue_details["queue_name"] = queue_details["queue_name"] + ".fifo"
        super().__init__(queue_details, **kwargs)

    def set_queue_attributes(self, **kwargs):
        super().set_queue_attributes(**kwargs)
        fifo_attributes = {
            "FifoQueue": "true",
            "ContentBasedDeduplication": kwargs.get("content_based_duplication", "false")
        }
        self.queue_attributes.update(fifo_attributes)

    def set_message_attributes(self, **kwargs):
        super().set_message_attributes(**kwargs)
        fifo_message_attributes = {
            "MessageDeduplicationId": kwargs.get("deduplication_id", str(uuid.uuid4())),
            "MessageGroupId": kwargs.get("message_group_id", str(uuid.uuid4())),
        }
        self.message_attributes.update(fifo_message_attributes)



if __name__ == '__main__':
    """
        Queue creation
    """
    # fifo_queue = FIFOQueue(queue_name=str(uuid.uuid4()), **sqs_resource)
    # fifo_queue.set_queue_attributes(**{
    #     "delay_seconds": "10",
    #     "message_retention_period": "172800",
    #     "visibility_timeout": "300"
    # })
    # response = fifo_queue.create_queue()
    # if response:
    #     logger.info(f"Created queue with following details: {response}")

    # url = 'https://queue.amazonaws.com/465378058770/47c6aa9c-6831-4fcf-99ed-8bdbd4b52ab8.fifo'
    #
    # """
    #     Sending message to SQS queue
    # """
    # queue_details = {"queue_url": url}
    # message_attributes = {
    #     "message_body": json.dumps({"num": 2}),
    #     "deduplication_id": "1",
    #     "message_group_id": "1"
    # }
    # fifo_queue = FIFOQueue(queue_details=queue_details, **sqs_resource)
    # fifo_queue.set_message_attributes(**message_attributes)
    # response = fifo_queue.send_message()
    # logger.info(f"Sent message to queue: {url} with the following details: {response}")
    """
        Get queue url from queue name
    """
    # queue_details = {
    #     "queue_name": "47c6aa9c-6831-4fcf-99ed-8bdbd4b52ab8"
    # }
    # fifo_queue = FIFOQueue(queue_details=queue_details, **sqs_resource)
    # print(fifo_queue.get_queue_url_by_name())
    """
        Read received messages and then delete them.
    """
    # queue_details = {"queue_url": url}
    # fifo_queue = FIFOQueue(queue_details=queue_details, **sqs_resource)
    # messages = fifo_queue.receive_message()
    # for msg in messages["Messages"]:
    #     print(json.loads(msg["Body"]))
    #     print(msg["ReceiptHandle"])
    #     fifo_queue.delete_message(msg["ReceiptHandle"])

    fifo_queue = FIFOQueue(queue_details={"queue_name": "abc"}, **sqs_resource)
    try:
        fifo_queue.get_queue_url_by_name()
    except fifo_queue.sqs_resource.exceptions.QueueDoesNotExist as e:
        print("fifo_queue.sqs_resource")
    #
