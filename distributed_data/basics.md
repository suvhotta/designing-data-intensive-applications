## Why to distribute DB across multiple machines:
- Scalability: If too many reads and writes are taking place simultaneously and a single machine can't suffice the needs then the load can be spread across multiple machines.
- Fault tolerance: If there is a single DB in place, and it goes down then business continuity will be affected. So a solution is to have multiple machines to give redundancy. If one fails,
    another can take over.
- Latency: If users across the globe are using the system, then those situated far away from the datacenter would be experiencing latency. A solution would be to distribute the DB worldwide so
    that there will be some uniform latency throughout.

## Higher load scaling:
- Simple solution to scale for higher load is to **scale up**:buy more powerful machine than the existing one.

## Shared architecture:
1. **Shared-memory architecture:** One type of scale-up is to: Use many CPUs, RAMS, and disks joined together under one OS. Problems: Cost increases very sharply, don't provide any fault tolerance.
2. **Shared-disk architecture:** Another type of scale-up: to have many independent systems with their own CPUs and RAMs but storing data centrally on an array of disks that is shared between the machines.
    It has limitations due to locking as in when which machine would be locking the Disk to write.
3. **Shared-Nothing architecture:** Also known as ***horizontal scaling/scale-out***. In this approach, each machine is an independent entity running the DB software and is called a **node**. Each node uses its
    CPUs, RAM and disks independently. Coordination between the nodes happens through a software level by using some network connection. No specific hardware is needed. Problems of scalability, fault-tolerance and 
    latency all can be solved.
    There are 2 ways to distribute data across nodes:
   1. **Replication**: Keeping a copy of the same data in multiple nodes, mostly in diff geolocations.
   2. **Partitioning/Sharding**: Splitting a big DB into smaller subsets called partitions and assigning them to diff nodes.