# Concurrency and Synchronization
Concurrency Synchronization coordinates the execution order of multiple threads or processes so that they don't produce data conflicts when accessing shared resources (variables, data structures, files). Key concepts:

### Key concepts

1. **Race Condition**: A race condition occurs when two or more threads or processes concurrently access and modify the same shared resource, and the final result depends on the order of access. Race conditions can lead to inconsistent data or undefined behavior.

2. **Critical Section**: Refers to a block of code in a concurrent program that accesses a shared resource. At any moment, only one thread may execute the code inside a critical section, to prevent data conflicts.

3. **Mutual Exclusion**: Refers to ensuring that at any moment only one thread can enter a critical section, avoiding multiple threads executing critical-section code at the same time. Mutual exclusion can be implemented with a Lock mechanism.

### Synchronization techniques

1. **Lock**: A lock is the most basic synchronization mechanism. By locking and unlocking, it ensures that at any moment only one thread can access a shared resource. Common lock types are the Mutex and the Read-Write Lock.

2. **Semaphore**: A semaphore is a more advanced synchronization mechanism, used to control access to a shared resource. A semaphore can limit the number of threads accessing a resource at the same time. A Binary Semaphore is similar to a mutex, while a Counting Semaphore can allow multiple threads to access a resource simultaneously.

3. **Condition Variable**: A condition variable is used to block a thread until a specific condition becomes true. It is usually used together with a mutex, to release the lock while waiting for the condition and re-acquire the lock once the condition is satisfied.

4. **Spinlock**: A spinlock is a busy-waiting lock mechanism; the thread waiting for the lock to be released keeps looping, checking the lock's state. Spinlocks suit scenarios with very short wait times, because they avoid the overhead of thread context switches.

5. **Barrier**: A barrier is a synchronization mechanism that lets multiple threads meet up and synchronize at a specific point. Only when all threads have reached the barrier point can the threads continue executing.

6. **Atomic Operations**: Atomic operations are indivisible operations, guaranteed not to be interrupted by other threads while they execute. Common atomic operations include atomic increment/decrement and atomic swap.

### Common concurrency synchronization problems

1. **Deadlock**: A deadlock occurs when two or more threads each wait on a resource held by another and can't continue. Ways to avoid deadlocks include resource allocation policies, avoiding circular waits, and timed locks.

2. **Starvation**: Starvation occurs when a thread can't obtain the resource it needs for a long time and so can't continue. Fair locks and priority scheduling can reduce starvation.

3. **Livelock**: A livelock occurs when threads keep trying to resolve a conflict but always interfere with each other and can't proceed. Reasonable retry mechanisms and randomized wait times can reduce livelocks.

Race conditions are prevented with locks and atomic operations, deadlocks are solved with resource allocation order and timed locks, starvation with fair locks, livelocks with reasonable retry intervals — the fix for each problem lives in its respective section.

## References

- [sync standard library](https://pkg.go.dev/sync)
- [Go memory model](https://go.dev/ref/mem)
- [Official blog · Introducing the Go Race Detector](https://go.dev/blog/race-detector)


## Sibling pages

- [Atomic](/sync/Atomic.md)
- [Context](/sync/Context.md)
- [CriticalSection](/sync/CriticalSection.md)
- [Spinlock](/sync/Spinlock.md)

<!-- BACKLINKS-AUTO -->
## Related pages

- [Spinlock](/sync/Spinlock.md)
