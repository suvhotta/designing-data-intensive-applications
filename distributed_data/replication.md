## Reasons to replicate:
- to keep the data closer to the users and reduce the latency
- making the system fault-tolerant so that even if some part fails, some other can take its place.
- To increase the read throughput by increasing the number of read replicas.

DB replication would have been very easy if the data didn't change over time. In that case we could just once put all our data into the nodes and leave them there forever.
But in reality the data present in the nodes change over time. 

There are 3 algorithms to replicate changes between nodes:
1. Single-leader 
2. Multi-leader
3. Leaderless

Every node that stores a copy of the DB is called a replica.


## Single-Leader Replication/Master-Slave Replication:
- One of the replicas is the leader to which clients send data when they've to write something to the DB. First the leader writes the new data to its local storage, then it also sends
    the data changes to its followers by a replication log or change stream. Each follower then takes the log from the leader and updates its own local copy of the DB. If a client wants
    to read anything, it can be queried from the leader or any of the followers. This mode of replication is followed in most of the relational DBs like: Postgres, MySQL, SQL Server's always
    on availability groups. Also used in non-relational DBs like MongoDB, RethinkDB, and Espresso. Leader based replication model is also followed in distributed message brokers like Kafka,
    RabbitMQ etc.

- Replication to followers can happen **synchronously** or **asynchronously**. The advantage of sync replication is that the follower is guaranteed to have an up-to-date copy of the data which
    is consistent with the leader. However, if the follower has somehow fallen behind the leader due to some network issue/max CPU Utilization then in that case the leader has to halt any further 
    write operation and wait till the follower responds.

- Due to the prob mentioned above, not all followers should be sync in nature, any one node outage would halt the entire system then. Practically, one of the followers should be sync and all others
    async. If the sync follower somehow becomes unavailable, then another one of the async followers is made sync. It guarantees updated data on at-least 2 nodes: the leader and the sync follower.
    This configuration is known as **semi-synchronous**.

- Fully async configuration helps in having fast writes but in case of the failure of the leader, doesn't guarantee the most updated data.


## How to add new followers?
- Simply copying the files from one node to another won't be helpful as the clients might be writing data constantly. One option could be to lock the DB and then copy all the data to the new follower,
    but in that case it would lead to some downtime and thus violation of high availability.
- The process is as follows:
  - Take a consistent snapshot of the leader's DB at some point in time. Note the exact position in the replication log where the snapshot was taken.
  - Copy the snapshot to the new follower node.
  - The follower then connects to the leader to request all the data after the snapshot was taken based on the position noted above.


## Handling Node Outages:
- Any node can go down due to a fault or due to some planned maintenance.
- **When follower fails:** Every follower has its own set of log of the data changes that it has received from the leader. If a follower goes down, the follower checks from its log the last transaction 
    that was applied and then asks data changes from the Leader after that point.
- **When leader fails:** Whenever a leader fails, there are too many steps involved: promoting one of the followers as the new leader, re-configuring the clients to send writes to the new leader, and
    followers consuming data changes from this new leader. This entire process is called **failover**. Failover can happen manually or automatically.
    Steps in an automatic failover:
  - **Determining that leader has failed:** The nodes send messages among themselves in a fixed interval of around 30s, so if a node doesn't respond, then it is assumed to be dead.
  - **Choosing new leader:** This could be either done through an election process, or a new leader could be appointed by a controller node. The best candidate is usually the one which is most updated with
    the prev leader, to minimize any loss in data.
  - **Re-configuring the system:** Clients need to now send their write requests to the new leader. But if the old leader comes up then it might think that it is still the leader, hence it is forcefully brought
    down. The system ensures that the old leader becomes a follower and recognizes the new leader.
- **Things that could go wrong in failover:**
  - If async replication is used, the new leader mayn't have received all the writes from the old leader before it failed. If the former leader rejoins, then what happens to those writes? One option is to
    discard them, however it may violate the durability expectations of the system.
  - At times 2 nodes can act as leaders, thus resulting in conflicts and possible data loss/corruption. As a safety catch, some systems have mechanism to shut down one node if such situation is detected.
    However, if this mechanism isn't properly implemented then it may lead to both leaders being shut down.
  - Deciding the right timeout before the leader is declared dead. A longer timeout means time taken for the recovery when leader fails is longer. However, if the timeout is too short then there maybe unnecessary
    fail-overs.


## How are Replication Logs implemented?
- **Statement based replication:** In the simplest case, the leader logs every write statement it executes and sends the statement log to the followers. For a relational DB context, it means that the SQL statements
    are passed on to the followers as they're received from the client. However, this approach has its own problems: if any nondeterministic func is used in the statement like NOW(), RAND() then it will lead to 
    generating diff values on the replicas.
- **Write-ahead log(WAL):** The log is an append-only sequence of bytes containing all the writes to the DB. So whenever any write request comes, the leader first writes to the log. Besides, writing the log to the
    disk, the leader also sends it across the network to its followers. The follower has its own set of WAL, where it writes before processing to disk.

## Problems with Replication Lag:
- Theoretically whenever a write request comes to a leader it can be immediately sent over to the followers and the result can be stored in the latter. It holds true for a sync replication system. But if the 
    replication mechanism is async, then there is no assurance/surety as to when the changes would exactly be reflected in the followers. This inconsistency of data between the leader and follower is a temporary
    state. If the writing is stopped for a while then the followers will eventually catch up and become consistent with the leader. This effect is called **eventual consistency**. The term eventual is deliberately
    vague, because nobody knows how long it actually might take for the follower to sync with the leader.
    There can be some problems listed below, which might occur when this replication gap/lag becomes noticeable.
- **Reading own writes:** If the user submits some data and then views what they've submitted immediately in that case if the view data is being brought from some follower which has a lag, then it might bring stale
    data and give a poor experience and worse, the user might think the change didn't happen and retry doing the change. In such situation, we need **read-after-write consistency/read-your-writes consistency**. This
    would be a guarantee that if the user reloads the page, they will always see any updates they sent themselves, this mayn't be true for other users' updates but only for their own updates.
    How to implement read-your-own-writes consistency in a leader-based replication:
  - When trying to read about something that the user might have possibly modified, read it from a leader else read from a follower. For this to happen, it requires some application knowledge to predict what all the user
    can modify. So mostly things like user profiles and all should be read from the leader, and any other users' profile from a follower. This approach looks good if the system has very less things the user can edit. 
    If there are too many things the user can edit then everytime it will be a read from the Leader, negating the benefit of read scaling. In such cases, there might be other approaches to read from leader. The time of the
    last update can be tracked and if it is within some specific threshold then make reads from the leader. Another approach could monitor the replication lag on followers and prevent queries on any follower which is at 
    some threshold behind the leader.
  - If replicas are distributed across multiple datacenters, then the request needs to be served by the leader which has to be first routed through the datacenter that contains the leader. Another complication is when the
    same user is accessing the service from multiple devices, for example desktop web browser and a mobile app. In this case it is essential to have **cross-device-read-after-write consistency**.
    If the replicas are distributed across datacenters then there isn't any guarantee that connections from different devices will be routed to the same datacenter. If the approach requires reading from the leader,
    then we've to first route requests from all of a user's device to the same datacenter.
- **Monotonic Reads:** If a user makes several reads from different replicas and there isn't consistent data in all of them, then a user might first read from a fresh replica, then from a stale replica. So time appeaers
    to go backwards. To prevent such kind of anomaly, we need monotonic reads. **Monotonic reads** is a guarantee that such anomaly doesn't happen. It's a lesser guarantee than strong consistency, but a stronger guarantee
    than eventual consistency. One way to achieve monotonic reads is to make sure that the user always makes their reads from the same replica. The replica might be chosen based on the hash of the user ID. In case of future
    failures of that replica, there should be provision of rerouting to another replica.


## Solutions for Replication Lag:
- All the problems mentioned above suggest ways in which the problem can be tackled from the application for example: by performing certain kinds of reads on the leader. Hence, it is important to keep these issues in mind
    while designing the application.


## Multi-Leader Replication:
### Use cases:
- **Multi-datacenter operation:** We can have one leader in each datacenter. Within each datacenter, regular leader-follower replication is used, Between the datacenters, each datacenter's leader replicates its changes to the 
    leaders in other datacenters.
  - Performance: If there are multiple data-centers and a single leader then there can be too much latency in cross data-center writes. It might contravene the purpose of having multiple data-centers in the first place.
    In a multi-leader model, every write can be processed by the corresponding local datacenter and is replicated asynchronously. Thus, the inter-data-center network latency is hidden from users and thus enhancing the performance.
  - Data-center outage tolerance: In single leader config, if the data-center with the leader fails, failover can promote a follower in another data-center to tbe the leader. In multi-leader configuration, each data-center can 
    continue operating independently and replication will catch up.
  - Network problems Tolerance: Traffic between datacenters goes over the public internet and with a single leader in multiple datacenters the network issue might cause problems in writing to followers. But within a data-center,
    there is a local network over which writes are written to followers. So a temp network interruption doesn't prevent writes being processed.
- **Clients with offline operation:** When we have clients that can stay disconnected from the internet, for example a note keeping app on the phone, in that case a local DB is kept which acts as a leader, and there is async
    multi-leader replication process once the system is connected to the network again.


### Handling Write Conflicts:
- When 2 leaders updating same thing, write conflicts occur. Business scenario example: 2 people trying to book same room in a hotel booking app.
- Give each write a unique ID(timestamp based, long random num, UUID etc) pick the one with the longest ID as the winner and discard the rest. This is prone to data loss.
- Give each replica a unique ID, always write from the one with higher ID.  This is also prone to data loss.
- Record the conflict in an explicit DS, and let application code resolve the conflict later. The code may be executed on write or on read.
  - On write: As soon as the DB detects a conflict in log of replicated changes, it calls the conflict handler. It runs a background proces, and it must execute quickly.
  - On read: When a conflict is detected, all the conflicting writes are stored. Next time data is read, user may be prompted/automatic conflict resolution and writes back to DB.
- Conflict resolution usually applied at row/document level. If 1 transaction has several atomic changes and makes multiple writes, each write is taken separately for conflict resolution.


### Multi-Leader Replication Topologies:
- Replication topology describes the comm. path to send writes from one node to another.
- Circular topology, star topology, all to all topology. Mostly all to all topology is preferred.


## Leaderless Replication:
- No concept of leader. 