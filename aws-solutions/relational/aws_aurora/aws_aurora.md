## What is Amazon Aurora?
It's a relational managed DB service.

## Aurora Architecture:
- Log stream is maintained from the beginning of the DB. Any version of the DB can be hence constructed using the 
  log stream. However relying solely on log stream for page reads is not practical, its too slow. 
  Because if we have a 1-year old DB, then we need to start checking from t0 which will be time consuming. The solution
  is to have periodic checkpoints. It uses a distributed storage fleet to maintain the checkpoints.
  
- The compute and storage are kept as separate options. The storage system underneath leverages Amazon DynamoDB for 
  metadata store, Amazon Route53 for naming, Amazon EC2 instances with attached SSDs, Amazon S3 for storing backups.
  
- There might be continuous independent failures due to failing nodes, disks etc. The solution is replication accross
  availability zones. 3 AZs they use with 2 copies each.
  
- Aurora uses segmented storage i.e. the entire DB isn't stored in a single SSD. The volume is partitioned into n 
  fixed-size segments. Size of the segments should be choosen ideally, it the segment is too small then failures are 
  more likely. If segments are too big, repairs might take a long time. Currently AWS is using 10-GB segment size, which
  can be repaired within a minute.
  
- Aurora supports global databases - globally distributed applications using a single Aurora DB that spans across
  multiple AWS Regions. Write replica(primary) is available for one region with multiple read replicas(secondary).