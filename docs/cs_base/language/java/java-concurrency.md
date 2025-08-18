# Java 并发编程

## 概述

Java并发编程是现代Java开发中的重要技能，它允许程序同时执行多个任务，提高程序的性能和响应性。本章将深入探讨Java并发编程的核心概念和实践。

## 1. 线程基础

### 1.1 什么是线程

线程是程序执行的最小单位，一个进程可以包含多个线程。在Java中，每个线程都有自己的程序计数器、虚拟机栈和本地方法栈，但共享堆内存和方法区。

### 1.2 创建线程的方式

#### 方式一：继承Thread类

```java
class MyThread extends Thread {
    @Override
    public void run() {
        for (int i = 0; i < 5; i++) {
            System.out.println(Thread.currentThread().getName() + ": " + i);
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
}

public class ThreadExample1 {
    public static void main(String[] args) {
        MyThread t1 = new MyThread();
        MyThread t2 = new MyThread();
        
        t1.setName("线程1");
        t2.setName("线程2");
        
        t1.start();
        t2.start();
    }
}
```

#### 方式二：实现Runnable接口

```java
class MyRunnable implements Runnable {
    @Override
    public void run() {
        for (int i = 0; i < 5; i++) {
            System.out.println(Thread.currentThread().getName() + ": " + i);
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
}

public class ThreadExample2 {
    public static void main(String[] args) {
        MyRunnable runnable = new MyRunnable();
        
        Thread t1 = new Thread(runnable, "线程1");
        Thread t2 = new Thread(runnable, "线程2");
        
        t1.start();
        t2.start();
    }
}
```

#### 方式三：实现Callable接口

```java
import java.util.concurrent.*;

class MyCallable implements Callable<String> {
    @Override
    public String call() throws Exception {
        Thread.sleep(2000);
        return "任务完成: " + Thread.currentThread().getName();
    }
}

public class ThreadExample3 {
    public static void main(String[] args) {
        ExecutorService executor = Executors.newFixedThreadPool(2);
        
        Future<String> future1 = executor.submit(new MyCallable());
        Future<String> future2 = executor.submit(new MyCallable());
        
        try {
            System.out.println(future1.get());
            System.out.println(future2.get());
        } catch (InterruptedException | ExecutionException e) {
            e.printStackTrace();
        }
        
        executor.shutdown();
    }
}
```

### 1.3 线程的生命周期

线程在其生命周期中会经历以下状态：

1. **NEW（新建）**：线程对象已创建，但尚未调用start()方法
2. **RUNNABLE（可运行）**：线程正在Java虚拟机中执行
3. **BLOCKED（阻塞）**：线程被阻塞等待监视器锁
4. **WAITING（等待）**：线程无限期等待另一个线程执行特定操作
5. **TIMED_WAITING（超时等待）**：线程等待另一个线程执行操作，但有时间限制
6. **TERMINATED（终止）**：线程已退出

```java
public class ThreadStateExample {
    public static void main(String[] args) throws InterruptedException {
        Thread thread = new Thread(() -> {
            try {
                Thread.sleep(2000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        });
        
        System.out.println("创建后: " + thread.getState()); // NEW
        
        thread.start();
        System.out.println("启动后: " + thread.getState()); // RUNNABLE
        
        Thread.sleep(100);
        System.out.println("睡眠中: " + thread.getState()); // TIMED_WAITING
        
        thread.join();
        System.out.println("结束后: " + thread.getState()); // TERMINATED
    }
}
```

## 2. 线程同步机制

### 2.1 synchronized关键字

`synchronized`是Java中最基本的同步机制，可以用于方法或代码块。

#### 同步方法

```java
class Counter {
    private int count = 0;
    
    // 同步方法
    public synchronized void increment() {
        count++;
    }
    
    public synchronized int getCount() {
        return count;
    }
}

public class SynchronizedMethodExample {
    public static void main(String[] args) throws InterruptedException {
        Counter counter = new Counter();
        
        Thread t1 = new Thread(() -> {
            for (int i = 0; i < 1000; i++) {
                counter.increment();
            }
        });
        
        Thread t2 = new Thread(() -> {
            for (int i = 0; i < 1000; i++) {
                counter.increment();
            }
        });
        
        t1.start();
        t2.start();
        
        t1.join();
        t2.join();
        
        System.out.println("最终计数: " + counter.getCount()); // 应该是2000
    }
}
```

#### 同步代码块

```java
class BankAccount {
    private double balance;
    private final Object lock = new Object();
    
    public BankAccount(double initialBalance) {
        this.balance = initialBalance;
    }
    
    public void deposit(double amount) {
        synchronized (lock) {
            balance += amount;
            System.out.println("存入: " + amount + ", 余额: " + balance);
        }
    }
    
    public void withdraw(double amount) {
        synchronized (lock) {
            if (balance >= amount) {
                balance -= amount;
                System.out.println("取出: " + amount + ", 余额: " + balance);
            } else {
                System.out.println("余额不足，无法取出: " + amount);
            }
        }
    }
    
    public double getBalance() {
        synchronized (lock) {
            return balance;
        }
    }
}
```

### 2.2 Lock接口

`java.util.concurrent.locks.Lock`接口提供了比synchronized更灵活的锁定操作。

```java
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

class LockCounter {
    private int count = 0;
    private final Lock lock = new ReentrantLock();
    
    public void increment() {
        lock.lock();
        try {
            count++;
        } finally {
            lock.unlock();
        }
    }
    
    public int getCount() {
        lock.lock();
        try {
            return count;
        } finally {
            lock.unlock();
        }
    }
    
    // 尝试获取锁，避免无限等待
    public boolean tryIncrement() {
        if (lock.tryLock()) {
            try {
                count++;
                return true;
            } finally {
                lock.unlock();
            }
        }
        return false;
    }
}
```

### 2.3 ReadWriteLock读写锁

```java
import java.util.concurrent.locks.ReadWriteLock;
import java.util.concurrent.locks.ReentrantReadWriteLock;

class ReadWriteCounter {
    private int count = 0;
    private final ReadWriteLock lock = new ReentrantReadWriteLock();
    
    public void increment() {
        lock.writeLock().lock();
        try {
            count++;
        } finally {
            lock.writeLock().unlock();
        }
    }
    
    public int getCount() {
        lock.readLock().lock();
        try {
            return count;
        } finally {
            lock.readLock().unlock();
        }
    }
}
```

## 3. 线程池

### 3.1 为什么使用线程池

- **降低资源消耗**：重复利用已创建的线程
- **提高响应速度**：任务到达时不需要等待线程创建
- **提高线程的可管理性**：统一分配、调优和监控

### 3.2 ThreadPoolExecutor

```java
import java.util.concurrent.*;

public class ThreadPoolExample {
    public static void main(String[] args) {
        // 创建自定义线程池
        ThreadPoolExecutor executor = new ThreadPoolExecutor(
            2,                      // 核心线程数
            4,                      // 最大线程数
            60L,                    // 空闲线程存活时间
            TimeUnit.SECONDS,       // 时间单位
            new LinkedBlockingQueue<>(10), // 工作队列
            Executors.defaultThreadFactory(), // 线程工厂
            new ThreadPoolExecutor.AbortPolicy() // 拒绝策略
        );
        
        // 提交任务
        for (int i = 0; i < 10; i++) {
            final int taskId = i;
            executor.submit(() -> {
                System.out.println("执行任务 " + taskId + 
                    " 在线程 " + Thread.currentThread().getName());
                try {
                    Thread.sleep(2000);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            });
        }
        
        // 关闭线程池
        executor.shutdown();
        try {
            if (!executor.awaitTermination(60, TimeUnit.SECONDS)) {
                executor.shutdownNow();
            }
        } catch (InterruptedException e) {
            executor.shutdownNow();
        }
    }
}
```

### 3.3 常用线程池类型

```java
import java.util.concurrent.*;

public class ExecutorServiceExample {
    public static void main(String[] args) {
        // 1. 固定大小线程池
        ExecutorService fixedPool = Executors.newFixedThreadPool(3);
        
        // 2. 缓存线程池
        ExecutorService cachedPool = Executors.newCachedThreadPool();
        
        // 3. 单线程池
        ExecutorService singlePool = Executors.newSingleThreadExecutor();
        
        // 4. 定时任务线程池
        ScheduledExecutorService scheduledPool = Executors.newScheduledThreadPool(2);
        
        // 定时任务示例
        scheduledPool.scheduleAtFixedRate(() -> {
            System.out.println("定时任务执行: " + System.currentTimeMillis());
        }, 0, 2, TimeUnit.SECONDS);
        
        // 延迟任务示例
        scheduledPool.schedule(() -> {
            System.out.println("延迟任务执行");
        }, 5, TimeUnit.SECONDS);
    }
}
```

## 4. 并发工具类

### 4.1 CountDownLatch

```java
import java.util.concurrent.CountDownLatch;

public class CountDownLatchExample {
    public static void main(String[] args) throws InterruptedException {
        int taskCount = 3;
        CountDownLatch latch = new CountDownLatch(taskCount);
        
        for (int i = 0; i < taskCount; i++) {
            final int taskId = i;
            new Thread(() -> {
                try {
                    System.out.println("任务 " + taskId + " 开始执行");
                    Thread.sleep(2000);
                    System.out.println("任务 " + taskId + " 执行完成");
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                } finally {
                    latch.countDown(); // 计数器减1
                }
            }).start();
        }
        
        System.out.println("等待所有任务完成...");
        latch.await(); // 等待计数器归零
        System.out.println("所有任务已完成");
    }
}
```

### 4.2 CyclicBarrier

```java
import java.util.concurrent.CyclicBarrier;

public class CyclicBarrierExample {
    public static void main(String[] args) {
        int threadCount = 3;
        CyclicBarrier barrier = new CyclicBarrier(threadCount, () -> {
            System.out.println("所有线程都到达屏障点，开始下一阶段");
        });
        
        for (int i = 0; i < threadCount; i++) {
            final int threadId = i;
            new Thread(() -> {
                try {
                    System.out.println("线程 " + threadId + " 正在工作...");
                    Thread.sleep((threadId + 1) * 1000);
                    System.out.println("线程 " + threadId + " 到达屏障点");
                    
                    barrier.await(); // 等待其他线程
                    
                    System.out.println("线程 " + threadId + " 继续执行");
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }).start();
        }
    }
}
```

### 4.3 Semaphore

```java
import java.util.concurrent.Semaphore;

public class SemaphoreExample {
    public static void main(String[] args) {
        // 创建一个信号量，允许最多3个线程同时访问
        Semaphore semaphore = new Semaphore(3);
        
        for (int i = 0; i < 10; i++) {
            final int threadId = i;
            new Thread(() -> {
                try {
                    semaphore.acquire(); // 获取许可
                    System.out.println("线程 " + threadId + " 获得许可，开始执行");
                    Thread.sleep(2000);
                    System.out.println("线程 " + threadId + " 执行完成，释放许可");
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                } finally {
                    semaphore.release(); // 释放许可
                }
            }).start();
        }
    }
}
```

## 5. Java内存模型（JMM）

### 5.1 JMM基本概念

Java内存模型定义了Java程序中各种变量的访问规则，以及在JVM中将变量存储到内存和从内存中读取变量这样的底层细节。

### 5.2 volatile关键字

```java
public class VolatileExample {
    private volatile boolean flag = false;
    private int count = 0;
    
    public void writer() {
        count = 42;     // 1
        flag = true;    // 2
    }
    
    public void reader() {
        if (flag) {     // 3
            int i = count; // 4
            System.out.println("count = " + i);
        }
    }
    
    public static void main(String[] args) {
        VolatileExample example = new VolatileExample();
        
        new Thread(example::writer).start();
        new Thread(example::reader).start();
    }
}
```

### 5.3 happens-before原则

1. **程序顺序规则**：在一个线程内，按照程序代码顺序
2. **监视器锁规则**：unlock操作happens-before后续的lock操作
3. **volatile变量规则**：写操作happens-before后续的读操作
4. **线程启动规则**：Thread.start()happens-before该线程的每一个动作
5. **线程终止规则**：线程中的所有操作happens-before其他线程检测到该线程终止
6. **传递性**：如果A happens-before B，B happens-before C，那么A happens-before C

## 6. 并发集合

### 6.1 ConcurrentHashMap

```java
import java.util.concurrent.ConcurrentHashMap;

public class ConcurrentHashMapExample {
    public static void main(String[] args) {
        ConcurrentHashMap<String, Integer> map = new ConcurrentHashMap<>();
        
        // 线程安全的操作
        map.put("key1", 1);
        map.putIfAbsent("key2", 2);
        
        // 原子操作
        map.compute("key1", (key, val) -> val == null ? 1 : val + 1);
        map.computeIfAbsent("key3", key -> 3);
        
        System.out.println(map);
    }
}
```

### 6.2 BlockingQueue

```java
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.BlockingQueue;

public class BlockingQueueExample {
    public static void main(String[] args) {
        BlockingQueue<String> queue = new ArrayBlockingQueue<>(10);
        
        // 生产者
        Thread producer = new Thread(() -> {
            try {
                for (int i = 0; i < 5; i++) {
                    String item = "Item " + i;
                    queue.put(item);
                    System.out.println("生产: " + item);
                    Thread.sleep(1000);
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        
        // 消费者
        Thread consumer = new Thread(() -> {
            try {
                for (int i = 0; i < 5; i++) {
                    String item = queue.take();
                    System.out.println("消费: " + item);
                    Thread.sleep(2000);
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        
        producer.start();
        consumer.start();
    }
}
```

## 7. 并发编程最佳实践

### 7.1 避免死锁

```java
public class DeadlockAvoidance {
    private final Object lock1 = new Object();
    private final Object lock2 = new Object();
    
    // 错误的做法 - 可能导致死锁
    public void method1() {
        synchronized (lock1) {
            synchronized (lock2) {
                // 业务逻辑
            }
        }
    }
    
    public void method2() {
        synchronized (lock2) {
            synchronized (lock1) {
                // 业务逻辑
            }
        }
    }
    
    // 正确的做法 - 按顺序获取锁
    public void safeMethod1() {
        synchronized (lock1) {
            synchronized (lock2) {
                // 业务逻辑
            }
        }
    }
    
    public void safeMethod2() {
        synchronized (lock1) { // 同样的顺序
            synchronized (lock2) {
                // 业务逻辑
            }
        }
    }
}
```

### 7.2 使用不可变对象

```java
public final class ImmutablePerson {
    private final String name;
    private final int age;
    
    public ImmutablePerson(String name, int age) {
        this.name = name;
        this.age = age;
    }
    
    public String getName() {
        return name;
    }
    
    public int getAge() {
        return age;
    }
    
    // 不提供setter方法，确保不可变性
}
```

### 7.3 正确处理中断

```java
public class InterruptExample {
    public void interruptibleTask() {
        while (!Thread.currentThread().isInterrupted()) {
            try {
                // 可能被中断的操作
                Thread.sleep(1000);
                // 执行任务
            } catch (InterruptedException e) {
                // 恢复中断状态
                Thread.currentThread().interrupt();
                System.out.println("任务被中断");
                break;
            }
        }
    }
}
```

## 总结

Java并发编程是一个复杂但重要的主题。掌握以下要点：

1. **线程基础**：理解线程的创建方式和生命周期
2. **同步机制**：合理使用synchronized、Lock等同步工具
3. **线程池**：使用线程池管理线程资源
4. **并发工具类**：熟练使用CountDownLatch、CyclicBarrier等
5. **内存模型**：理解JMM和happens-before原则
6. **并发集合**：使用线程安全的集合类
7. **最佳实践**：避免死锁，使用不可变对象，正确处理中断

通过合理使用这些并发编程技术，可以编写出高性能、线程安全的Java应用程序。