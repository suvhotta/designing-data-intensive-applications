Quoroms:
https://www.youtube.com/watch?v=uNxl3BFcKSA

## Why need to understand DB storage mechanism?
To select a storage engine the best suitable for the application we are working on. Storage engines are very differently built depending on the purpose they serve, so a storage engine
designed for transactional workload will be very different from that built for an analytical workload.


## Log Structured Storage Engine:
- Many DBs internally use a log, which is an append-only data file. The appended data mightn't be human-readable & mostly would be binary.
- However, searching from a random log one by one has a time complexity of O(n). To increase the efficiency of finding value to particular key, we need a DS: **Index**. The idea is to
  keep some additional metadata, which acts as a signpost and helps to locate the data we want. If we need to search the data in some different manner, then we need several indices on
  different parts of the data.
  
- Index is an additional DS derived from the primary data. Most DBs allow us to add/remove indices, and this won't mess anything with the existing data. However once an index is 
  defined, it needs to be maintained and incurs overheads especially on writes. So its no longer as fast as simply appending to a log file anymore. This trade-off between fast read
  or write operations is something best left to the corresponding application developer/DBA. 
  
  ## Hash Table Indexes:
  - The Simplest possible strategy of index: keep an in memory hash map where each key is mapped to a byte offset in the actual log/data file, where that particular key and value is present.
    This kind of strategy can be implemented when the number of keys are relatively less and can be stored in the mem and can support a large num of writes per key. A situation can be:
    the url to a video is the key, and the num of likes is the value. The num of likes per url might keep on increasing, but the num of urls will increase at relatively slower pace.
    
  - **Segmentation and Compaction:** Rather than forever appending to a single file, we can have a size limit on a per-log basis. After that we can throw away the duplicate keys in the 
    log and only have the latest update for each key, a process known as **compaction**. After compaction if the size of segments are much smaller, then they can be merged together to a new
    file. Merging and compaction doesn't affect the primary files, and can be running in parallel threads. After the process is completed, we can switch the read requests to the new 
    merged segments instead of the old ones, and the old ones could be simply deleted. Now there are segment-wise hash tables and when a read operation is performed, it keeps on 
    checking segments as per the descending order of modified date. Since the merging makes the segments smaller, lookups don't need to check many hash maps.
    
  - This is being used in NoSQL Key-val DB Riak. The underneath storage engine - BitCask uses hash table indexes.
  
  - Deleting Records: Deletion of records can be done by passing some extra flag along with the data to be deleted. This can be taken care of during the merging of segments, where
    it would discard any prev values for that particular key.
    
  - Crash recovery: Since the hash maps/tables are in-mem data structures, there is always a chance of them getting lost during any crash event. Although, they can still be recovered
    by reading through the records present in all the segments, but that's a very time-consuming activity. However, the problem can be solved by taking timely snapshots of the hash-maps
    and keeping them on the disk, which can be then loaded on to the memory quickly. Since the writes are sequential, it doesn't matter if a crash happened while a value was being 
    overwritten, we can have a separate new value and that will be updated in the upcoming merge cycle.
    
  - Concurrency: As writes are appended to the log in a sequential order, its always preferred to have a single writer thread. They're otherwise immutable hence they can be read
    concurrently by multiple threads.
    
    ### Limitations:
  - Hash table has to fit in memory, if we've a very large number of keys then it's difficult to maintain the keys in the memory. One solution might be to maintain them on disk, but
    random I/O operations to the hash map present on disk makes the queries slower.
    
  - Range of queries aren't efficient: to search for all keys between some range, we've to look up each key individually in all the hash maps.
  
  ## Sorted String Tables(SSTables) & Log Structure Merged Trees(LSMTrees):
  - If a simple change is being made to the way we segment the files: sort by key and store the (key, val) pairs, most of the problems encountered above in the hash indexes will be solved.
  - Sorting during the merge process is easier to perform than it looks and can be done by a simple merge sort algorithm. This produces a new merged segment file, also sorted by key.
    If the same key appears over multiple segments during then the key present in the latest segment is considered. 
    
  - If the keys are sorted, then we needn't store the offsets for all the keys in memory. We can store the offsets for some keys and that can be done in the order of 1 key for every few KBs.
    For example: if we know the offset of 'BEAN' & 'BEST' then we know that 'BEER' will lie somewhere in between both of them. 
    
  - There are many balanced tree DS like red-black trees or AVL trees where we can insert keys in any order and get them back in sorted order. The process would be first to write the keys into
    some in mem balanced DS, also known as Memtable. Once the memory of the memtable reaches some threshold it is written to disk as a SSTable file. This file becomes the latest segment. Merging and
    compaction can run in the background. For read operation, first the memtable is searched then the latest segments and so on.
  - So in short in LSM, there are many log-type/log-structured segments and each segment has an in memory hashtable storing the index. The index contains the key and byte offset in ranges.
  - Crash Recovery: As part of crash recovery, everything written to the memtable is written in a separate log(commit log) on to the disk. That log isn't sorted and its only purpose is to restore the 
    memtable after a crash.
    
  - Avoid un-necessary querying: The above algorithm can be slower if we are trying to look for keys that aren't present. Such cases can be avoided by using **Bloom filters**. Bloom filter is a DS
    that approximates the contents of a set and let us know if a key is present or not in the DB and thus prevents un-necessary querying.

  - Originally this indexing structure was called as log structured merged tree(LSM). This was also explained in the [Google's Bigtable Paper](https://static.googleusercontent.com/media/research.google.com/en//archive/bigtable-osdi06.pdf)
  
  - Such search engines are used in Cassandra and HBase. Lucene, used by Elasticsearch, also uses this storage engine to keep inverted index i.e. given a word in a search query, it finds all the
    documents that mention the word. This is implemented with a key-value structure where key is the word, and the value is list of IDs of the documents that contain the word.
    
  - The compaction process can sometimes interfere with the performance of ongoing reads and writes, while performing an expensive compaction. If the write-throughput becomes very high and compaction
    isn't configured carefully, it can happen that compaction cannot keep up with the rate of incoming writes. In this case, the num of unmerged segments keep on piling up and soon we run out of disk mem.
    Also reads keep on becoming slower as they've to consider too many segments to read from.

## B-Tree Indexing:
  - LSM breaks the entire DB into segments. B-Trees break the DB into pages of usually 4KB size, and storage engine can read/write one page at a time. Each page can be identified using an address,
    similar to that of a pointer. These pages are then arranged in the form of a balanced Binary tree. The root page is usually the one where the look up originates or begins. The page contains
    several keys and references to child pages. Each child is responsible for a continuous range of keys. Eventually, we get down to a page containing individual keys(a leaf page), which either
    contains the value for each key inline or contains references to the pages where the values can be found. The num of references to child pages in one page of the B-tree is called the 
    *branching factor*. Typically branching factor is in the range of several hundred.
    
  - To update an existing key, search and find the page, then change the value and write back the page to disk. To add a new key, first find the page whose range encompasses the new key and add to
    that page. If there isn't enough free space in that page, then the page is split into 2 new full pages and data is split into half. This algorithm ensures that the B-tree is always balanced. The 
    basic update operation overrides the existing data, much in contrast to the approach followed in LSM.
    
  - crash resilient: To make DBs crash resilient, another on disk DS called **Write-ahead log** is maintained where the actual operation is written first before it can be performed on the DB. 
    After any crash, the write-ahead log is checked, and the DB is brought back to a consistent state.
    
  - To maintain data consistency, DBs are attached with latches/locks so that only one writer thread at a time can modify the underneath data.

## B-Trees vs LSM:
- LSM-trees are generally faster for writes, where as B-trees are thought to be faster for reads. Reads are typically slower on LSM-trees because they've to search data segment wise. Writes are
  slower on B-trees because they've to take into account the pagination part. There is also an overhead of writing an entire page again even if there is only a few bytes in the page which actually
  changed.
  
- LSM trees can be compressed better, and thus produce smaller files on disk than B-trees. This is because keys with similar convention can be clubbed together and compressed. B-tree storage engine
  on the other hand, leaves some disk space unused due to fragmentation.
  
- Each key in a B-tree is only present at one place, thus offering strong transactional semantics as compared to LSM trees.
  
## Storing data in indexes:
- The key in an index is what the queries search for, and the value can be either of 2 things: the actual row, document , the actual value or a reference to the location where the actual value
  is present. In the second case, such a location is called heap file. The heap file approach is mostly used because it avoids data duplication, and when secondary indexes are present, each index
  just references a location in the heap.
  
- During data update if the heap file doesn't have enough memory then it needs to be moved to a new location and all the indexes are either to be changed to this new location or a forwarding pointer
  needs to be placed at the earlier location to point to the new location.
  
- The index where the actual data instead is present is called a clustered index. They are common in MySQL and SQL Server. Quite the opposite to this is the idea of non-clustered index where actual
  data isn't present as part of the index, instead a pointer to the heap file location is present where the actual data resides. Non-clustered indexes were common in postgres.
  

## OLAP
- Traditionally databases were designed to serve transactional purposes mostly related to banking and stuffs, those were primarily served by relational databases and the process known as
  online transactional processing (OLTP). But, in the last 2 decades the importance of data analysis has increased and thus there has been use of a newer database modelling process called as
  online analytical processing (OLAP).
  
- Relational databases aren't as good when doing aggregate functions over certain specific columns, involving millions of records. Such kinds of databases are usually referred to as data warehouses.
  These DBs are designed specifically to cater the needs of data analysts and not to be queried by end users through application code. These DBs are usually columnar in nature. 
  Examples: AWS Redshift, Terradata, SAP data warehouses etc.
  
- Here the data storage process is different from that of traditional databases. In traditional DB, data is stored usually in a row wise format. In columnar databases each column is stored in a 
  separate file, with some offset containing the info about the row num. 'SELECT *' queries are rarely used for analytics purpose so columnar DBs are the best suitable for that purpose.
  
- In columnar DBs, the columns may have repetitive data. Such data can be compressed by encoding techniques like bitmap encoding. So bitmap indexed storages are common for columnar DBs.



