##Compatibility:
Whenever we make any changes to the data format in a phase by phase manner, 
we need to keep 2 types of compatibilities into account:

- Backward Compatibility: Newer code can read what was written by older code.
   It means that readers with a newer schema can correctly parse data from writers with an older schema.
- Forward Compatibility: Older code can read what was written by newer code.
    It means that readers with an older schema can correctly parse data from writers with a newer schema.

- In short the source from which data comes/data is written decides if the system is to be backwards compatible or forward.
    If the source is behind the reader/older in terms of schema changes then the system needs to be backwards compatible,
    if the source is ahead, then system needs to be forward compatible.

For clients and servers:
- Backward compatibility on the server ensures that older clients can still parse the results you return
- Forward compatibility ensures that older clients can still call your methods.

For databases:
- Backward compatibility is essential if you want to avoid modifying existing data
- Forward compatibility is a nice bonus but not necessary if you control all the readers

## Need for Serialization?
In mem, data is kept in objects, lists, arrays, hash tables and other such data structures, for efficient access and manipulation by CPU using pointers.
When it is to be written to a file or sent over network, it needs to be done using a sequence of bytes, as pointer won't make sense in transition.
Thus, we need some kind of translation from the in-mem representation to the byte sequence this process is called **encoding/serialization/marshalling**.
The reverse process is called **parsing/de-serialization/unmarshalling**.

**Note:** Encoding isn't same as encryption.

## Encoding Formats:
- Every programming lang has its own encoding process, but it is generally not advisable to use the same because then it becomes very tightly coupled with a
    specific programming lang.

- For encoding 2 things are to be noted when dealing with huge amount of data say GBs or TBs: how compact it is and how fast it parses. JSON and XML use a lot
    of space compared to binary formats. That lead to many binary encodings for JSON: MessagePack, BSON, BJSON, UBSJON, BISON, Smile etc.

- Some JSON encoders are: MessagePack, Thrift and Protocol Buffers.

- To make the data more compact, the field names are replaced with tags and a schema is maintained both for read and write operations.
    The tags can act as markers for different fields.
    It is the job of these schemas to ensure forward/backwards compatibility. 
    But how does the reader schema knows what the write-schema is like?
  - **Large file with lots of records:** The writer of the file can just add the writer schema once at the beginning of the file and all the subsequent
        data abides by that schema. Currently, used in Avro for hadoop.
  - **Individually written records:** The individual records can have some sort of version number and the versions can be maintained in the DB.
        Presently, used in Espresso at Linkedin.
  - **Sending Records over a network Connection:** A separate bi-directional connection is created for data transfer

- Advantages of having binary encoding based on schemas:
  - More compact as they can omit the field names from the encoded data.
  - Schema can act as a valuable documentation.
  - Schema can help in maintaining the backwards/forward compatibility.


## Dataflow through DBs:
- The process that writes data to DB encodes the data, and the process which reads data decodes it. It may so happen that a value in the DB may be written by a newer version of the code and read by an
    older version of the code thus forward compatibility is required.
- It may also happen that the data is written by an older version but read by a newer version hence backwards compatibility is also required.
- There might be also situations where a newer format of the code has written the data into the DB, the older format then reads it and then subsequently writes to the DB. In that case, there is a chance
    of data loss.

## Dataflow thorough Services:
- whenever there is a communication between resources on the internet, the clients connect to the service exposed by the server using some web protocol like HTTP, and following certain set of previously
    agreed upon rules like the REST protocol.
- There is also an XML based protocol called as SOAP for making API requests. The API of a SOAP based web service is described using an XML based lang called the web services description lang(WSDL). WSDL
    enables code generation so that a client can access a remote service using local classes and method calls. SOAP is mostly used in statically typed programming langs.