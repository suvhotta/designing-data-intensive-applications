## Data Models:
Most applications are built layering one data model on top of another. For every layer, the question is how it shall be represented in terms of the next lower layer?

For example: There might be an application layer on the top which involves APIs and stuffs. Below that would be the layer where data is being stored in some data structures.These might be some general purpose data model like JSON or XML documents, tables in a relational DB, or a graph model. The next layer is at the database level how to represent the JSON objects in terms of bytes of memory. At the lowest level, the modelling involves on how to represent the bytes in terms of electrical currents, pulses of light, magnetic fields etc.

![data model image](https://github.com/suvhotta/[designing-data-intensive-applications]/blob/master/data-models-and-query-languages/images/data_layer.png?raw=true)

### Impedance Mismatch
The application code is a combination of classes and objects and the relational data model consists of rows and columns. The difference between both models is called *impedance mismatch*. These can be in the form of datatype mismatch. Another mismatch can be that results of queries don't often pinpoint the exact result we want in our program.

## Database Models:
Historically databases were used for business data processing which typically involved transaction processing(entering sales or banking transactions, airline reservations) and batch processing (customer invoicing, payroll, reporting).


**1. IBM's Information Management System (IMS):**
IMS was the leading database in the 1960s. Mostly involved around stock transactions and business data processing, was also used in Apollo space program.

It had a structure similar to document databases and represented all data as a tree of records nested within records, like JSON structure.

The nesting of records works perfectly well for one-to-many relationships however fails miserably in case of many-to-many relationships. This is a common problem even today for most document based databases.

2 popular solutions were proposed to the above problem: **Network Model** and **Relational Model**.


**2. Network Model:**
In the Network model, a record could have multiple parents, much unlike the hierarchical model where the records could have just a single parent.

The links between the records were like pointers, which were stored on disk. The only way to access a record was to follow a path from a root record, this was called the *access path*.

In simplest case, an access path could be like the traversal of a linekd list: start from the head and move one by one until you reach the desired result. But, in a many-to-many scenario, several paths could lead to the same result. So a programmer had to keep track of all these access paths. Even the application code data model had to keep track of all the relationships in order to make a simple query. This is like navigating around an n-dimensional data space.

![network model image](https://github.com/suvhotta/[designing-data-intensive-applications]/blob/master/data-models-and-query-languages/images/network_model.png?raw=true)


**3. Relational Model:**
The relational model laid the data in relation(table) which is a collection of tuples(rows). There is no nested structures or access path related worries here.

In a relational database, the query optimizer automatically decides which parts of the query to execute in which order, and which indexes to use. Those choices are effectively the access path, but the difference is that they are made automatically, in most cases, by the query optimizer. If we need to query our data in some other way then we need to just declare a new index.


**4. No SQL Model:**
No SQL doesn't actually refer to any particular technology. It got its name from a twitter hashtag meant for a meetup on open source, distributed, non-relational databases.  It is interpreted as *Not Only SQL*. 


**Types of NoSQL Databases:**
- Key Value stores: Simple key value pairs, there is some kind of primary key associated with the records. Lookup based on the key becomes very fast. Mostly used when there is rapid access for reads and writes, with relatively less emphasis on durability. 
Examples: Redis, AWS DynamoDB

- Document Databases: Objects are stored kinda similar to JSON objects. To draw parallels with relational databases, it can be thought that one row is one JSON type object known as document.
Examples: MongoDB, AWS DocumentDB

- Columnar Databases: Designed to store data in columns instead of rows. This makes the aggregations and other related OLAP queries faster. The writes are much slower as compared to traditional row based databases.
Examples: Apache Cassandra, AWS Redshift
https://www.youtube.com/watch?v=Vw1fCeD06YI

- Graph Databases: If there are too many relationships to be taken care of then in order to map the scenario in relational DBs, this would lead to too many joins between multiple tables. This is a problem being solved by graph databases.
Examples: Neo4j, AWS Neptune



**Graph Databases:**
If the data has a lot of complex many-to-many relationships then graph database is the natural choice. 
![graph model image](https://github.com/suvhotta/[designing-data-intensive-applications]/blob/master/data-models-and-query-languages/images/Graph-database-sketch.jpg?raw=true)

A graph consists of 2 kinds of objects: *vertices* and *edges*. 

Few scenarios can be: 
- Social Graphs: Vertices are people, edges indicate which people know each other.
- Web Graph: Vertices are web pages, and edges indiciate the HTML links to other pages.
- Road Graph: Vertices are places/sqaures and the edges represent the roads between them.

Algorithms can then work on the data, like for calculating the shortest path between 2 places in a road graph and page ranking to determine the popularity of web pages in web graph.

In the above examples the data represented in a single graph was all kind of similar data but that's not always the case. FB has a very complex graph system where vertices can be anything like people, locations, events etc and edges represent info like which people are friends with each other, checkin happening in which location etc.

## Relational vs NoSQL:
The best DB model to choose can vary from use-case perspective. There is no one size fits all scenario.

- If the application data has document like structure then it makes more sense to use a NoSQL document DB. As long as documents are not too deeply nested, accessing items is not an issue.

- If the application has too many many-to-many relationships or involve joins, then relational DB would be the best for that scenario. Document-oriented databases are designed to store denormalized data. Ideally, there should be no relationship between collections. If the same data is required in two or more documents, it must be repeated. Joins can be emulated in application code by making multiple requests to the DB, but that makes the process slower. In MongoDB, there is a provision to make join using the *$lookup* operator, however it isn't as simple as SQL Joins.

- For highly interconnected data, the document model is awkward, the relational model is acceptable, and the graph models are the most suitable.

- Schema wise, document DBs are at times called as Schemaless, but that term is misleading because any data must adhere to some kind of schema. Rather we can have schema-on-read and schema-on-write. Schema-on-write is being followed by traditional relational based databases, so the reason the data write is usually slower than data reads. 
Schema-on-read is something similar to dynamic type checking in programming languages. So irrespective of the schema, the whole document is being saved during the DB write and during the DB read it is being checked whether the requested field is being present or not. 
Schema-on-read approach is helpful if the items in the collection all don't have similar strucutre, or the strucutre of the data is determined by some external entity which might change over time. Schema changing in a relational database is a tedious task which might lead to several hours of downtime depending on the amount of data and the type of DB used. So in cases when the data's schema is likely to be changed, it makes more sense to have document databases in use.

- Data locality is an advantage provided by document databases if you need a large part of the data to be rendered from a single place.


Different applications have differing requirements, so it's best to use the different kinds of databases we've each alongside one another depending on use-case. Such an idea is termed as [polyglot persistence](https://www.jamesserra.com/archive/2015/07/what-is-polyglot-persistence/).