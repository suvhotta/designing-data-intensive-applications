- The threads pick up the interpreter lock, for a number of executions/milliseconds.
One thread runs Python, while N others sleep or await I/O. The other threads could be establishing network connections, but the only
thing that 2 threads can't do simultaneously is to run python.

- C python does use the cooperative multi-tasking feature, which means voluntarily giving up the GIL once a certain task has been achieved by the thread/ thread is performing any network operation.
    So there isn't any truly parallel python. Also there is preemptive multi-tasking implemented in python where the interpreter checks for the time a 
    certain thread has occupied the GIL, once a certain time has passed then it allows some other thread to pick the GIL instead. In python3 its 15ms.

- The purpose of cooperative multi-tasking is to make sure that the threads are releasing the GIL during any I/O related wait.
    The purpose of preemptive multi-tasking is to make sure that there are many different threads working on something rather than one single thread working on anything.