import json
import os

import boto3


AWS_REGION = "us-east-1"
SERVICE_NAME = "events"
AWS_ACCESS_KEY_ID = os.environ.get("PERSONAL_AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.environ.get("PERSONAL_AWS_ACCESS_SECRET")


account_details = {
    "region_name": AWS_REGION,
    "aws_access_key_id": AWS_ACCESS_KEY_ID,
    "aws_secret_access_key": AWS_SECRET_KEY
}


event_bridge_client = boto3.client(service_name=SERVICE_NAME, **account_details)

detail_type = {
    "detail-type": ["test_*"]
}


"""
Put rule func gives the facility of creating a new rule/modify an existing rule.
"""

# rule_response = event_bridge_client.put_rule(
#     Name='test-scheduled-event-rule',
#     State="ENABLED",
#     EventPattern=json.dumps(detail_type),
#     ScheduleExpression="rate(2 minutes)"
# )
#
# print(rule_response)

"""
{
	'RuleArn': 'arn:aws:events:us-east-1:465378058770:rule/test-scheduled-event-rule',
	'ResponseMetadata': {
		'RequestId': 'b52786d3-8bb5-47d8-9a9a-91d589c65b88',
		'HTTPStatusCode': 200,
		'HTTPHeaders': {
			'x-amzn-requestid': 'b52786d3-8bb5-47d8-9a9a-91d589c65b88',
			'content-type': 'application/x-amz-json-1.1',
			'content-length': '82',
			'date': 'Sat, 12 Mar 2022 07:28:21 GMT'
		},
		'RetryAttempts': 0
	}
}
"""

lambda_client = boto3.client(service_name="lambda", **account_details)

lambda_func_arn = lambda_client.get_function(FunctionName="sqs_lambda")["Configuration"]["FunctionArn"]

"""
Here, the input is a valid json which can be passed on to the target. 
If this input is set, then the actual contents of the event won't be passed on to the target.
"""
response = event_bridge_client.put_targets(
    Rule='test-scheduled-event-rule',
    EventBusName='default',
    Targets=[
        {
            "Id": "test",
            "Arn": lambda_func_arn,
            "Input": json.dumps({"Records": [{"body": json.dumps({"Message": {"num": 2}})}]})
        }
    ]
)

print(response)

"""
{
	'FailedEntryCount': 0,
	'FailedEntries': [],
	'ResponseMetadata': {
		'RequestId': 'f1f8a08e-35d1-4e4e-90e2-333e3441c905',
		'HTTPStatusCode': 200,
		'HTTPHeaders': {
			'x-amzn-requestid': 'f1f8a08e-35d1-4e4e-90e2-333e3441c905',
			'content-type': 'application/x-amz-json-1.1',
			'content-length': '41',
			'date': 'Sat, 12 Mar 2022 07:53:26 GMT'
		},
		'RetryAttempts': 0
	}
}
"""

