import logging
import boto3
import os

from botocore.exceptions import ClientError

import json
import uuid


AWS_REGION = "us-east-1"
SERVICE_NAME = "sns"
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

boto_client = Resource(**sqs_resource)

"""
Create a topic

arn:aws:sns:us-east-1:465378058770:Orders
"""
# topic = boto_client.sqs_resource.create_topic(
#     Name='Orders',
#     Tags=[
#         {
#             'Key': 'env',
#             'Value': 'dev'
#         }
#     ]
# )
#
# print(topic["TopicArn"])


"""
To list all subscriptions made to some given topic
"""
# print(boto_client.sqs_resource.list_subscriptions_by_topic(TopicArn="arn:aws:sns:us-east-1:465378058770:Orders"))


"""
To add an SQS subscription to a given topic.
Also after adding the subscription, the SQS also needs to be added with access policy something like the following:
{
  "Version": "2008-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "sns.amazonaws.com"
      },
      "Action": "sqs:SendMessage",
      "Resource": "arn:aws:sqs:us-east-1:465378058770:47c6aa9c-6831-4fcf-99ed-8bdbd4b52ab8.fifo",
      "Condition": {
        "ArnEquals": {
          "aws:SourceArn": "arn:aws:sns:us-east-1:465378058770:sample_sns_test.fifo"
        }
      }
    }
  ]
}
"""
SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:465378058770:Orders"
SQS_ARN = "arn:aws:sqs:us-east-1:465378058770:main_queue"
# subscription = boto_client.sqs_resource.subscribe(
#     TopicArn=SNS_TOPIC_ARN,
#     Protocol="sqs",
#     Endpoint=SQS_ARN,
#     ReturnSubscriptionArn=True
# )
# print(subscription)


"""
    Publish a message to a topic, which is then transferred to all the subscribers.
"""
message = {"nusm": 14}
published_response = boto_client.sqs_resource.publish(
    TopicArn=SNS_TOPIC_ARN,
    Message=json.dumps(message)
)
print(published_response)