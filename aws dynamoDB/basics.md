## What is DynamoDB?
- No SQL managed DB solution provided by AWS.
- Data resides on SSDs and spread across data centers globally.

## Components:
- Tables, items and attributes correspond to table, row and column of RDBMS.


## Primary Key:
- There are 2 ways of having primary keys: individual and composite primary key.

- ## Partition Key:
  - Whenever only a single primary key is to be maintained then partition key is specified. DynamoDB uses the partition's key
    as an input to an internal hash function, and the output of that hash function determines the physical partition/storage 
    where the actual value would be stored.
- ## Composite Primary key:
  - DynamoDB offers the support of using composite primary key by using a combination of partition key and sort key.
  - The sort key of an item is also known as the **range attribute**. DynamoDB stores the values in the partitions sorted by the 
    order of their sort keys.

- In a table having only partition key, those values should be unique. In case of table supporting composite primary key, the 
    partition key and sort key combination should be unique. i.e. if partition key value can be common for multiple entities but
    with distinct sort keys.

- There can be certain conditions put on the sort key like greater than, less than, begins with, ends with, equals etc.


## DynamoDB streams:
- These are sort of event listeners, which captures data modification events in dynamoDB tables. These events can be fired when
  a new item is added to the table, item being updated, item is deleted.
- DynamoDB streams can be used together with AWS Lambda to take actions on events. Eg: when a new user is added, there can be a 
  welcome mail sent.


## Datatype support:
- scalar types: number, string, binary, boolean and null.
- Doc types: list(JSON Array) and map.
- Set types: multiple scalar values. (unique values of the same datatype)


## Table classes:
DynamoDB offers 2 table classes designed to optimize for cost.
- Standard table class: Default class and recommended for most of the workloads.
- Standard-Infrequent Access table class: Optimized for tables storing data which isn't accessed frequently.


## Read Consistency:
- DynamoDB supports 2 consistency models for data reads: Eventually consistent reads and Strongly consistent reads.
- The eventual consistency model always returns data with low latency. Also, this model prioritizes availability over consistency. 
  An eventual consistent read model is suitable to perform independent tasks from each and will impact the scalability, performance, 
  and availability of systems at scale. The downside of the eventual consistency model is that it may return stale data. 
  Again the implementation of the application will be complex with eventual consistency since it makes the debugging process hard.
- Strong consistency gives the guarantee as it will return the most updated data. The system will be more accurate with the strongly consistent model
  but there drawbacks with this model. For example, some operations may fail if an insufficient number of object replicas are available. 
  Also, a strongly consistent read might not be available if there is a network delay or outage. In this case, DynamoDB may return a 
  server error (HTTP 500). Having higher latency than eventually consistent reads, not supported on global secondary indexes, 
  using more throughput capacity than eventually consistent reads are other drawbacks for strong consistency read models.
- While querying there can be a field passed to specify if it is a strongly consistent read or not.


## Read/Write Capacity Modes:
- There are 2 modes of reading/writing in dynamoDB:
  - On-Demand Mode:
    - This is a mode that supports variable traffic. the dynamodb manages the scaling for any change in traffic.
    - DynamoDB can support scaling up-to double the previous peak within 30 minutes.  However, throttling can occur if one exceeds 
      double the previous peak within 30 minutes.
    - This switching can also be done for earlier existing tables.
  - Provisioned mode:
    - This is good for predictive load.


## DynamoDB auto scaling:
- We can define a range for read and write capacity units. We could also define a target utilization percentage and dynamoDB autoscaling
  maintains the target utilization despite any change in traffic.'


## DynamoDB Global Tables:
- DynamoDB offers replication solutions across multiple AWS regions. The global tables are mostly useful for globally scalable applications.
- Changes to one table are propagated across tables in other regions simultaneously. These changes are propagated through DynamoDB streams.
- It allows users to interact with the closest table for the best performance.
- Transactions however are only supported in a region basis.
- DynamoDB global tables use a last-writer-wins reconciliation between concurrent updates.