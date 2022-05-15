## Features:
- Its a managed service that provides message delivery from publishers to subscribers(Pub-Sub model). Publishers send async messages to a **topic**. Subscribers can
    subscribe to that topic to receive messages.
- Topics can be standard or FIFO topics. Only AWS SQS FIFO can subcribe to FIFO topics. When message duplication and message order aren't critical then standard topic
    can be used.
- SNS has an extensive retry policy and also supports dead-letter queue. Unlike SQS which has a visibility timeout concept for retries,
    SNS has retry in different phases(immediate retry, Pre-backoff phase, Backoff phase, Post-backoff phase) for both AWS managed endpoints and
    customer managed endpoints.
- There is also option for message filtering. By default, a subscriber will receive all the messages published to the subscribed topic.
    However the subscriber can also choose to get a subset of the messages. For this, the subscriber must assign a filter policy to the topic subscription.