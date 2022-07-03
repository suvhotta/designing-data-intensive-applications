## What is the GIL?
- GIL is the global interpreter lock.
- It is a mutex that allows only one thread to take control of the python interpreter at a time. It has a boolean 
    variable, git->locked which holds values 0, 1.
- Currently, the GIL is shared by all interpreters, and only the main thread is responsible to create and destroy it.
- In a single threaded program, the main thread is the only thread. It holds the GIL indefinitely therefore.
- The bytecode evaluation happens inside a loop called the evaluation loop present in `_PyEval_EvalFrame`.
    From time to time, a thread has to suspend bytecode execution. It checks if there are any reasons to do that 
    at the beginning of each iteration of the evaluation loop, like: another thread has requested the GIL.
- In case of a multi-threaded program, multiple threads need to acquire the GIL. To acquire the GIL, a thread first
    checks if some other thread holds the GIL, if not then it immediately acquires the GIL, otherwise waits till GIL is
    released. The default interval for waiting is called `switch interval` with default time of 5ms. If the GIL isn't 
    released still within that interval, then after waiting it sets the `eval_breaker` and `gil_drop_request` to 1.
- The eval_breaker flag tells the GIL holding thread to suspend its bytecode execution(this check is done every time in
    the evaluation loop beginning). The GIL holding thread thus after checking these changed flags, releases the GIL and
    notifies the other threads to acquire the GIL. It is entirely up to the OS to allow anyone of the pending threads to
    occupy the GIL.
- When a thread releases the GIL, it ensures that a different thread waiting for the GIL occupies it.
    It is done so by waiting on a condition variable `switch_cond` until the value of the `last_holder` is changed to
    something other than the existing holder.
- The above explanation is for those threads performing some CPU intensive tasks which would require more than 5ms to
    execute. In case of I/O bound tasks the thread themselves give up control of GIL. This is called cooperative
    multitasking.

## What is a Mutex?
- Mutex is a concept related to the OS. It is a mutually exclusive flag which acts a gatekeeper so that in a
    multi-threaded program only one thread can access some particular resource.
- While requesting exclusive access on some resource protected by a mutex, the thread seeks a mutex.lock() 
    request. It is the job of the OS to check and allow the locking of the mutex by that thread.


## How is python thread different from OS thread?
- Python thread = OS thread + Python thread state
- A Python thread, must capture the call stack of Python functions, the exception state, 
  and other Python-related things. So what CPython does is put those things in a thread state struct and 
  associate the thread state with the OS thread.


Links:
- https://github.com/zpoint/CPython-Internals/blob/master/Interpreter/gil/gil.md#fields
- https://tenthousandmeters.com/blog/python-behind-the-scenes-13-the-gil-and-its-effects-on-python-multithreading/

