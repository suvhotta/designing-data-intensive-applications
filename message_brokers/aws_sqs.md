## AWS SQS(Simple Queue Service):
- It offers asynchronous message based communication as opposed to traditional synchronous API calls.
- Helps in decoupling of the services.
- Its fully managed and scalable service. It can serve both for applications which have a high volume of messages to be
  published concurrently or an application that have a huge number of consumers(high concurrent processing of messages).
- Its used in data processing, real time event processing, ad-hoc job queueing.

### Queue:
- Queue is a holding pool of messages. Messages are JSON objects with a size limit of 256KB.
- The publishers/producers put the messages into the queue, operation is called enqueue.
- The consumers/processors consume the messages from the queue, operation is called dequeue. The consumer creates threads
  which continuously poll the queue to check for messages. If there is no message, the polling will be retried. If there
  is some message, then SQS will reply the poller with the body of that message. Once the message is sent, it will 
  temporarily disappear from the message queue, once processing is completed by the consumer, it will be marked as completed
  and would be visible in the queue.
- Only a single consumer can claim and process a message at once. 2 Threads can't grab and start processing the message
  together.

### Message Processing Workflow:
- A message is published to the queue.
- Message is claimed by some consumer and the visibility timeout countdown starts. The countdown is like a lock on a 
    message that ensures that the same message isn't consumed by some other thread. Visibility timeout is the wait time
    which the queue waits for any response from the consumer. If no such response is received by the queue within the 
    permissible time then the queue restores back the original message to the queue so that it can be visible to be
    consumed by other consumer threads. This visibility timeout is needed because the consumer might have some external
    dependencies which in case of failure may need to be retried.

### Why use SQS?
- To have a control over rate of processing of messages.
- Publisher needn't directly interact with the part that is processing the message. Thus, decoupling is achieved.
- Eventual guaranteed processing is achieved, which is great for async applications.

### Types of SQS queues?
- **Standard queues:** Order isn't guaranteed. At-least Once Delivery, SQS may give the same message again for a different request. Although
    the likelihood of something as such is very less. The benefit is unlimited throughput, so unlimited publish and processing rate. 

- **FIFO queues:** Whatever written first is guaranteed to be processed first. Exactly once delivery. There is a max transaction per second
    300 TPS Max or 3000 with batch processing where each batch will have 10 transactions to reduce the API calls. It is around 25%
    more expensive than Standard queue. Another advantage is that there is provision of message group IDs. This feature will be handy
    when we have multiple tenants/customers, and we've to process the messages of each one of them in order. So there would be multiple
    channels tagged by group id. So there is no mix-up of messages of different channels and there is some sort of parallelization.

- Queues once created can't be changed from one type to another.

### Common Patterns:
- Fanout processing to do one to many processes. Mostly used together with SNS topic. Publish one message to SNS topic from producer. In SQS, many
    queues are waiting for such message, they're linked to the SNS through subscription. So one message sent to the SNS is now fanned out to multiple
    SQS queues.
- Serverless Processing with Backpressure Control: Queue in conjunction with AWS Lambda. Concurrent message processing and rate limiting can be done.
- Job Buffering: We've a backup/some job that needs to run regularly like DB backup. We could create a cloudwatch event and set a cron job to trigger
    a message to SQS queue, which in turn fires an EC2 instance/lambda 


### Dead letter queue:
- It stores failed messages for later processing.
- Amazon SQS does not create the dead-letter queue automatically. You must first create the queue before using it as a dead-letter queue.

## Parameters:
- Visibility timeout: the default lock in period till which the message isn't visible to other consumer threads once a thread acquires that message.
- Message retention period: the time period till which the message will be part of the queue even if successfully consumed.
- Delivery delay: whenever a message is initially published to the queue, the message won't be visible until a certain amount of time.
- Receive message wait time: Used in long polling. Long polling is when a polling thread tries to acquire a message and doesn't get anything then instead of 
    returning immediately, it will wait for a certain amount of time before returning and thus reducing the number of eventual API calls.
- Purge: To delete all the messages in one go.

## Doubts:
1. Does message automatically send from DLQ to original queue for re-processing?


## Things to explore:
1. retry limit for DLQ.
2. Batching of messages.
3. Short and long polling
4. How SQS works internally: https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-how-it-works.html
5. Server side encryption of messages in queue.


### Features:
- De-duplication ID: It's the ID that is maintained to check for duplicated messages within a 5 minute default interval set by AWS. If any message
    with the same de-duplication ID is sent within 5 minutes, then that message is accepted successfully but aren't delivered during the 5 minute de-duplication
    interval. If a producer detects a failed send message action, then it can retry sending as many times as necessary using the same message deduplication ID.
    If Content-based deduplication is explicitly enabled on the FIFO queue, MessageDeduplicationId will be automatically generated using a SHA-256 hash of the message body (content only, not attributes).
    If high throughput is enabled then the deduplication will only be maintained across message groups.

- Max receive count:  Every message in the SQS will have a maximum receive count. If the message has not been processed by the consumer even after several retries 
  and the maximum receive count of the message has also exceeded, then the message is sent to the Dead Letter Queue. 

- Payload Size: Message payload can contain messages of size 256kb in any format. 256kb is divided into 64kbs chunks. Each of these 64kb chunks is considered as 1 request.
  So if you send a message payload of size 256kb, then it is considered as 4 requests.

- Polling: The basic idea of polling is that the consumer application repeatably sends(polls) “RecieveMessage Request” to the SQS to get a message to process. 
  In case if the queue is empty, the SQS will send an empty response back. However, in Long Polling, the consumer requests messages from the queue exactly as in normal polling, 
  but with the expectation that the SQS queue may not respond immediately. The long polling wait time begins. Let's assume that the long polling wait time is 10 seconds. 
  If the SQS does not have any message available for the consumer, instead of sending an empty response, the queue holds the request and waits until some data become available or 
  until the long polling wait time(10 secs) expires. Once the message becomes available, a full response is sent to the consumer else an empty response is sent after 10 secs.

- Receive Request Attempt id: Used in the request message flow by consumers. It is a token used for deduplication of ReceiveMessage calls. If a networking issue occurs after a 
    Message receive action then we will get some error. It is possible to retry the same by using the same ReceiveRequestAttemptId even if the visibility timeout has not yet expired.
    If the same hasn't been passed on by user then AWS would by default add it.

## When to use SNS vs SQS?
- When we've to only send a message without caring for if it got processed or not then its a SNS usecase.
- When other systems care for the event then its SNS use case. If our own internal system cares if an event occurred and takes action accordingly then its SQS. 