---
icon: material/database
comments: true
---

# Java 集合框架

!!! note "本章内容"
    本章介绍 Java 集合框架：Collection 接口体系、Map 接口体系、集合选择指南和遍历方法。

## 一、集合框架概述

### 1.1 集合框架结构

```java
/*
Java 集合框架层次结构：

Iterable
└── Collection
    ├── List (有序，可重复)
    │   ├── ArrayList
    │   ├── LinkedList
    │   └── Vector
    ├── Set (无序，不可重复)
    │   ├── HashSet
    │   ├── LinkedHashSet
    │   └── TreeSet
    └── Queue (队列)
        ├── LinkedList
        ├── PriorityQueue
        └── ArrayDeque

Map (键值对，键不可重复)
├── HashMap
├── LinkedHashMap
├── TreeMap
└── Hashtable
*/

import java.util.*;

public class CollectionFrameworkOverview {
    public static void main(String[] args) {
        System.out.println("=== Java 集合框架概述 ===");
        
        // Collection 接口的主要方法
        demonstrateCollectionMethods();
        
        // 集合的基本特性
        demonstrateCollectionCharacteristics();
    }
    
    public static void demonstrateCollectionMethods() {
        System.out.println("\n--- Collection 接口主要方法 ---");
        
        Collection<String> collection = new ArrayList<>();
        
        // 添加元素
        collection.add("Apple");
        collection.add("Banana");
        collection.add("Cherry");
        System.out.println("添加元素后: " + collection);
        
        // 查询操作
        System.out.println("集合大小: " + collection.size());
        System.out.println("是否为空: " + collection.isEmpty());
        System.out.println("是否包含Apple: " + collection.contains("Apple"));
        
        // 批量操作
        Collection<String> fruits = Arrays.asList("Orange", "Grape");
        collection.addAll(fruits);
        System.out.println("批量添加后: " + collection);
        
        // 删除操作
        collection.remove("Banana");
        System.out.println("删除Banana后: " + collection);
        
        // 转换为数组
        String[] array = collection.toArray(new String[0]);
        System.out.println("转换为数组: " + Arrays.toString(array));
    }
    
    public static void demonstrateCollectionCharacteristics() {
        System.out.println("\n--- 集合特性对比 ---");
        
        // List: 有序，可重复
        List<String> list = new ArrayList<>();
        list.add("A");
        list.add("B");
        list.add("A");  // 可重复
        System.out.println("List (有序，可重复): " + list);
        
        // Set: 无序，不可重复
        Set<String> set = new HashSet<>();
        set.add("A");
        set.add("B");
        set.add("A");  // 重复元素不会被添加
        System.out.println("Set (无序，不可重复): " + set);
        
        // Map: 键值对，键不可重复
        Map<String, Integer> map = new HashMap<>();
        map.put("Apple", 10);
        map.put("Banana", 20);
        map.put("Apple", 15);  // 键重复，值会被覆盖
        System.out.println("Map (键值对，键不可重复): " + map);
    }
}
```

## 二、List 接口及其实现

### 2.1 ArrayList

```java
import java.util.*;

public class ArrayListDemo {
    public static void main(String[] args) {
        System.out.println("=== ArrayList 详解 ===");
        
        // 创建和初始化
        createAndInitialize();
        
        // 基本操作
        basicOperations();
        
        // 性能特点
        performanceCharacteristics();
        
        // 线程安全问题
        threadSafetyIssue();
    }
    
    public static void createAndInitialize() {
        System.out.println("\n--- 创建和初始化 ---");
        
        // 1. 默认构造器
        ArrayList<String> list1 = new ArrayList<>();
        System.out.println("默认容量的ArrayList: " + list1.size());
        
        // 2. 指定初始容量
        ArrayList<String> list2 = new ArrayList<>(20);
        System.out.println("指定容量的ArrayList: " + list2.size());
        
        // 3. 从其他集合创建
        List<String> sourceList = Arrays.asList("A", "B", "C");
        ArrayList<String> list3 = new ArrayList<>(sourceList);
        System.out.println("从其他集合创建: " + list3);
        
        // 4. 使用集合工厂方法（Java 9+）
        List<String> list4 = List.of("X", "Y", "Z");  // 不可变列表
        System.out.println("不可变列表: " + list4);
    }
    
    public static void basicOperations() {
        System.out.println("\n--- 基本操作 ---");
        
        ArrayList<String> list = new ArrayList<>();
        
        // 添加元素
        list.add("First");
        list.add("Second");
        list.add(1, "Middle");  // 在指定位置插入
        System.out.println("添加元素后: " + list);
        
        // 访问元素
        System.out.println("第一个元素: " + list.get(0));
        System.out.println("最后一个元素: " + list.get(list.size() - 1));
        
        // 修改元素
        String oldValue = list.set(1, "Updated");
        System.out.println("修改元素，旧值: " + oldValue + ", 新列表: " + list);
        
        // 查找元素
        int index = list.indexOf("Second");
        System.out.println("Second的索引: " + index);
        
        // 删除元素
        list.remove("First");  // 按值删除
        list.remove(0);        // 按索引删除
        System.out.println("删除元素后: " + list);
        
        // 子列表
        list.addAll(Arrays.asList("A", "B", "C", "D"));
        List<String> subList = list.subList(1, 3);
        System.out.println("子列表: " + subList);
    }
    
    public static void performanceCharacteristics() {
        System.out.println("\n--- 性能特点 ---");
        
        ArrayList<Integer> list = new ArrayList<>();
        
        // 测试添加性能
        long startTime = System.nanoTime();
        for (int i = 0; i < 100000; i++) {
            list.add(i);
        }
        long endTime = System.nanoTime();
        System.out.println("添加10万个元素耗时: " + (endTime - startTime) / 1000000 + "ms");
        
        // 测试随机访问性能
        startTime = System.nanoTime();
        for (int i = 0; i < 10000; i++) {
            int randomIndex = (int) (Math.random() * list.size());
            list.get(randomIndex);
        }
        endTime = System.nanoTime();
        System.out.println("随机访问1万次耗时: " + (endTime - startTime) / 1000000 + "ms");
        
        // 测试中间插入性能
        startTime = System.nanoTime();
        for (int i = 0; i < 1000; i++) {
            list.add(list.size() / 2, i);
        }
        endTime = System.nanoTime();
        System.out.println("中间插入1000次耗时: " + (endTime - startTime) / 1000000 + "ms");
    }
    
    public static void threadSafetyIssue() {
        System.out.println("\n--- 线程安全问题 ---");
        
        // ArrayList 不是线程安全的
        ArrayList<Integer> unsafeList = new ArrayList<>();
        
        // 线程安全的替代方案
        // 1. 使用 Collections.synchronizedList
        List<Integer> syncList = Collections.synchronizedList(new ArrayList<>());
        
        // 2. 使用 Vector（不推荐，性能较差）
        Vector<Integer> vector = new Vector<>();
        
        // 3. 使用 CopyOnWriteArrayList（读多写少场景）
        // CopyOnWriteArrayList<Integer> cowList = new CopyOnWriteArrayList<>();
        
        System.out.println("线程安全的List创建完成");
    }
}
```

### 2.2 LinkedList

```java
import java.util.*;

public class LinkedListDemo {
    public static void main(String[] args) {
        System.out.println("=== LinkedList 详解 ===");
        
        // 基本操作
        basicOperations();
        
        // 队列操作
        queueOperations();
        
        // 栈操作
        stackOperations();
        
        // 性能对比
        performanceComparison();
    }
    
    public static void basicOperations() {
        System.out.println("\n--- 基本操作 ---");
        
        LinkedList<String> list = new LinkedList<>();
        
        // 添加元素
        list.add("Middle");
        list.addFirst("First");
        list.addLast("Last");
        System.out.println("添加元素后: " + list);
        
        // 访问元素
        System.out.println("第一个元素: " + list.getFirst());
        System.out.println("最后一个元素: " + list.getLast());
        System.out.println("索引1的元素: " + list.get(1));
        
        // 删除元素
        String removedFirst = list.removeFirst();
        String removedLast = list.removeLast();
        System.out.println("删除的第一个: " + removedFirst + ", 删除的最后一个: " + removedLast);
        System.out.println("删除后: " + list);
    }
    
    public static void queueOperations() {
        System.out.println("\n--- 队列操作 ---");
        
        Queue<String> queue = new LinkedList<>();
        
        // 入队
        queue.offer("First");
        queue.offer("Second");
        queue.offer("Third");
        System.out.println("入队后: " + queue);
        
        // 查看队首元素
        System.out.println("队首元素: " + queue.peek());
        
        // 出队
        while (!queue.isEmpty()) {
            String element = queue.poll();
            System.out.println("出队: " + element + ", 剩余: " + queue);
        }
    }
    
    public static void stackOperations() {
        System.out.println("\n--- 栈操作 ---");
        
        LinkedList<String> stack = new LinkedList<>();
        
        // 压栈
        stack.push("Bottom");
        stack.push("Middle");
        stack.push("Top");
        System.out.println("压栈后: " + stack);
        
        // 查看栈顶元素
        System.out.println("栈顶元素: " + stack.peek());
        
        // 弹栈
        while (!stack.isEmpty()) {
            String element = stack.pop();
            System.out.println("弹栈: " + element + ", 剩余: " + stack);
        }
    }
    
    public static void performanceComparison() {
        System.out.println("\n--- ArrayList vs LinkedList 性能对比 ---");
        
        int size = 100000;
        
        // ArrayList
        ArrayList<Integer> arrayList = new ArrayList<>();
        long startTime = System.nanoTime();
        for (int i = 0; i < size; i++) {
            arrayList.add(0, i);  // 在开头插入
        }
        long arrayListTime = System.nanoTime() - startTime;
        
        // LinkedList
        LinkedList<Integer> linkedList = new LinkedList<>();
        startTime = System.nanoTime();
        for (int i = 0; i < size; i++) {
            linkedList.addFirst(i);  // 在开头插入
        }
        long linkedListTime = System.nanoTime() - startTime;
        
        System.out.println("在开头插入" + size + "个元素:");
        System.out.println("ArrayList: " + arrayListTime / 1000000 + "ms");
        System.out.println("LinkedList: " + linkedListTime / 1000000 + "ms");
        
        // 随机访问性能对比
        startTime = System.nanoTime();
        for (int i = 0; i < 10000; i++) {
            arrayList.get(i);
        }
        long arrayListAccessTime = System.nanoTime() - startTime;
        
        startTime = System.nanoTime();
        for (int i = 0; i < 10000; i++) {
            linkedList.get(i);
        }
        long linkedListAccessTime = System.nanoTime() - startTime;
        
        System.out.println("\n随机访问性能对比:");
        System.out.println("ArrayList: " + arrayListAccessTime / 1000000 + "ms");
        System.out.println("LinkedList: " + linkedListAccessTime / 1000000 + "ms");
    }
}
```

## 三、Set 接口及其实现

### 3.1 HashSet

```java
import java.util.*;

public class HashSetDemo {
    public static void main(String[] args) {
        System.out.println("=== HashSet 详解 ===");
        
        // 基本操作
        basicOperations();
        
        // 去重特性
        duplicateRemoval();
        
        // 自定义对象的HashSet
        customObjectHashSet();
        
        // 性能特点
        performanceCharacteristics();
    }
    
    public static void basicOperations() {
        System.out.println("\n--- 基本操作 ---");
        
        HashSet<String> set = new HashSet<>();
        
        // 添加元素
        set.add("Apple");
        set.add("Banana");
        set.add("Cherry");
        set.add("Apple");  // 重复元素不会被添加
        System.out.println("添加元素后: " + set);
        
        // 查询操作
        System.out.println("集合大小: " + set.size());
        System.out.println("是否包含Apple: " + set.contains("Apple"));
        System.out.println("是否为空: " + set.isEmpty());
        
        // 删除操作
        boolean removed = set.remove("Banana");
        System.out.println("删除Banana: " + removed + ", 结果: " + set);
        
        // 集合运算
        HashSet<String> otherSet = new HashSet<>(Arrays.asList("Apple", "Date", "Elderberry"));
        
        // 交集
        HashSet<String> intersection = new HashSet<>(set);
        intersection.retainAll(otherSet);
        System.out.println("交集: " + intersection);
        
        // 并集
        HashSet<String> union = new HashSet<>(set);
        union.addAll(otherSet);
        System.out.println("并集: " + union);
        
        // 差集
        HashSet<String> difference = new HashSet<>(set);
        difference.removeAll(otherSet);
        System.out.println("差集: " + difference);
    }
    
    public static void duplicateRemoval() {
        System.out.println("\n--- 去重特性 ---");
        
        // 数组去重
        Integer[] array = {1, 2, 3, 2, 4, 3, 5, 1};
        HashSet<Integer> uniqueSet = new HashSet<>(Arrays.asList(array));
        System.out.println("原数组: " + Arrays.toString(array));
        System.out.println("去重后: " + uniqueSet);
        
        // 转回数组
        Integer[] uniqueArray = uniqueSet.toArray(new Integer[0]);
        System.out.println("去重数组: " + Arrays.toString(uniqueArray));
    }
    
    public static void customObjectHashSet() {
        System.out.println("\n--- 自定义对象的HashSet ---");
        
        HashSet<Person> personSet = new HashSet<>();
        
        Person p1 = new Person("张三", 25);
        Person p2 = new Person("李四", 30);
        Person p3 = new Person("张三", 25);  // 与p1相同
        
        personSet.add(p1);
        personSet.add(p2);
        personSet.add(p3);
        
        System.out.println("Person集合大小: " + personSet.size());
        for (Person p : personSet) {
            System.out.println(p);
        }
    }
    
    public static void performanceCharacteristics() {
        System.out.println("\n--- 性能特点 ---");
        
        HashSet<Integer> set = new HashSet<>();
        
        // 添加性能
        long startTime = System.nanoTime();
        for (int i = 0; i < 100000; i++) {
            set.add(i);
        }
        long addTime = System.nanoTime() - startTime;
        
        // 查找性能
        startTime = System.nanoTime();
        for (int i = 0; i < 100000; i++) {
            set.contains(i);
        }
        long containsTime = System.nanoTime() - startTime;
        
        System.out.println("添加10万个元素耗时: " + addTime / 1000000 + "ms");
        System.out.println("查找10万次耗时: " + containsTime / 1000000 + "ms");
    }
}

// 自定义Person类，重写equals和hashCode
class Person {
    private String name;
    private int age;
    
    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }
    
    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        Person person = (Person) obj;
        return age == person.age && Objects.equals(name, person.name);
    }
    
    @Override
    public int hashCode() {
        return Objects.hash(name, age);
    }
    
    @Override
    public String toString() {
        return "Person{name='" + name + "', age=" + age + "}";
    }
    
    // getter方法
    public String getName() { return name; }
    public int getAge() { return age; }
}
```

### 3.2 TreeSet

```java
import java.util.*;

public class TreeSetDemo {
    public static void main(String[] args) {
        System.out.println("=== TreeSet 详解 ===");
        
        // 基本操作
        basicOperations();
        
        // 排序特性
        sortingFeatures();
        
        // 自定义排序
        customSorting();
        
        // 范围操作
        rangeOperations();
    }
    
    public static void basicOperations() {
        System.out.println("\n--- 基本操作 ---");
        
        TreeSet<Integer> treeSet = new TreeSet<>();
        
        // 添加元素（自动排序）
        treeSet.add(5);
        treeSet.add(2);
        treeSet.add(8);
        treeSet.add(1);
        treeSet.add(9);
        System.out.println("添加元素后（自动排序）: " + treeSet);
        
        // 访问第一个和最后一个元素
        System.out.println("最小元素: " + treeSet.first());
        System.out.println("最大元素: " + treeSet.last());
        
        // 删除第一个和最后一个元素
        System.out.println("删除并返回最小元素: " + treeSet.pollFirst());
        System.out.println("删除并返回最大元素: " + treeSet.pollLast());
        System.out.println("删除后: " + treeSet);
    }
    
    public static void sortingFeatures() {
        System.out.println("\n--- 排序特性 ---");
        
        // 字符串的自然排序
        TreeSet<String> stringSet = new TreeSet<>();
        stringSet.addAll(Arrays.asList("banana", "apple", "cherry", "date"));
        System.out.println("字符串排序: " + stringSet);
        
        // 数字的自然排序
        TreeSet<Double> numberSet = new TreeSet<>();
        numberSet.addAll(Arrays.asList(3.14, 2.71, 1.41, 1.73));
        System.out.println("数字排序: " + numberSet);
    }
    
    public static void customSorting() {
        System.out.println("\n--- 自定义排序 ---");
        
        // 使用Comparator进行自定义排序
        // 1. 按字符串长度排序
        TreeSet<String> lengthSortedSet = new TreeSet<>(Comparator.comparing(String::length));
        lengthSortedSet.addAll(Arrays.asList("a", "hello", "world", "java", "programming"));
        System.out.println("按长度排序: " + lengthSortedSet);
        
        // 2. 逆序排序
        TreeSet<Integer> reverseSet = new TreeSet<>(Collections.reverseOrder());
        reverseSet.addAll(Arrays.asList(1, 5, 3, 9, 2, 7));
        System.out.println("逆序排序: " + reverseSet);
        
        // 3. 自定义对象排序
        TreeSet<Student> studentSet = new TreeSet<>(Comparator.comparing(Student::getScore).reversed());
        studentSet.add(new Student("张三", 85));
        studentSet.add(new Student("李四", 92));
        studentSet.add(new Student("王五", 78));
        studentSet.add(new Student("赵六", 95));
        
        System.out.println("学生按分数降序排序:");
        for (Student student : studentSet) {
            System.out.println(student);
        }
    }
    
    public static void rangeOperations() {
        System.out.println("\n--- 范围操作 ---");
        
        TreeSet<Integer> set = new TreeSet<>();
        for (int i = 1; i <= 10; i++) {
            set.add(i);
        }
        System.out.println("原集合: " + set);
        
        // 子集操作
        System.out.println("小于5的元素: " + set.headSet(5));
        System.out.println("大于等于7的元素: " + set.tailSet(7));
        System.out.println("3到8之间的元素: " + set.subSet(3, 8));
        
        // 查找操作
        System.out.println("小于等于6的最大元素: " + set.floor(6));
        System.out.println("大于等于6的最小元素: " + set.ceiling(6));
        System.out.println("小于6的最大元素: " + set.lower(6));
        System.out.println("大于6的最小元素: " + set.higher(6));
    }
}

class Student {
    private String name;
    private int score;
    
    public Student(String name, int score) {
        this.name = name;
        this.score = score;
    }
    
    public String getName() { return name; }
    public int getScore() { return score; }
    
    @Override
    public String toString() {
        return "Student{name='" + name + "', score=" + score + "}";
    }
}
```

## 四、Map 接口及其实现

### 4.1 HashMap

```java
import java.util.*;

public class HashMapDemo {
    public static void main(String[] args) {
        System.out.println("=== HashMap 详解 ===");
        
        // 基本操作
        basicOperations();
        
        // 遍历方式
        iterationMethods();
        
        // 常用方法
        commonMethods();
        
        // 性能特点
        performanceCharacteristics();
    }
    
    public static void basicOperations() {
        System.out.println("\n--- 基本操作 ---");
        
        HashMap<String, Integer> map = new HashMap<>();
        
        // 添加键值对
        map.put("Apple", 10);
        map.put("Banana", 20);
        map.put("Cherry", 15);
        System.out.println("添加元素后: " + map);
        
        // 获取值
        Integer appleCount = map.get("Apple");
        System.out.println("Apple的数量: " + appleCount);
        
        // 获取值（带默认值）
        Integer orangeCount = map.getOrDefault("Orange", 0);
        System.out.println("Orange的数量（默认值）: " + orangeCount);
        
        // 检查键和值
        System.out.println("是否包含键Apple: " + map.containsKey("Apple"));
        System.out.println("是否包含值20: " + map.containsValue(20));
        
        // 删除元素
        Integer removedValue = map.remove("Banana");
        System.out.println("删除Banana，返回值: " + removedValue);
        System.out.println("删除后: " + map);
        
        // 替换值
        map.replace("Apple", 25);
        System.out.println("替换Apple的值后: " + map);
    }
    
    public static void iterationMethods() {
        System.out.println("\n--- 遍历方式 ---");
        
        Map<String, Integer> map = new HashMap<>();
        map.put("Java", 25);
        map.put("Python", 30);
        map.put("JavaScript", 28);
        map.put("C++", 35);
        
        // 1. 遍历键
        System.out.println("遍历键:");
        for (String key : map.keySet()) {
            System.out.println("Key: " + key + ", Value: " + map.get(key));
        }
        
        // 2. 遍历值
        System.out.println("\n遍历值:");
        for (Integer value : map.values()) {
            System.out.println("Value: " + value);
        }
        
        // 3. 遍历键值对
        System.out.println("\n遍历键值对:");
        for (Map.Entry<String, Integer> entry : map.entrySet()) {
            System.out.println("Key: " + entry.getKey() + ", Value: " + entry.getValue());
        }
        
        // 4. 使用Lambda表达式（Java 8+）
        System.out.println("\n使用Lambda表达式:");
        map.forEach((key, value) -> System.out.println(key + " -> " + value));
        
        // 5. 使用Stream API
        System.out.println("\n使用Stream API过滤:");
        map.entrySet().stream()
           .filter(entry -> entry.getValue() > 28)
           .forEach(entry -> System.out.println(entry.getKey() + ": " + entry.getValue()));
    }
    
    public static void commonMethods() {
        System.out.println("\n--- 常用方法 ---");
        
        HashMap<String, List<String>> groupMap = new HashMap<>();
        
        // putIfAbsent - 如果键不存在才添加
        groupMap.putIfAbsent("fruits", new ArrayList<>());
        groupMap.get("fruits").add("apple");
        groupMap.get("fruits").add("banana");
        
        groupMap.putIfAbsent("vegetables", new ArrayList<>());
        groupMap.get("vegetables").add("carrot");
        
        System.out.println("分组数据: " + groupMap);
        
        // compute - 计算新值
        HashMap<String, Integer> countMap = new HashMap<>();
        String[] words = {"apple", "banana", "apple", "cherry", "banana", "apple"};
        
        for (String word : words) {
            countMap.compute(word, (key, value) -> (value == null) ? 1 : value + 1);
        }
        System.out.println("单词计数: " + countMap);
        
        // merge - 合并值
        HashMap<String, Integer> map1 = new HashMap<>();
        map1.put("a", 1);
        map1.put("b", 2);
        
        HashMap<String, Integer> map2 = new HashMap<>();
        map2.put("b", 3);
        map2.put("c", 4);
        
        // 将map2合并到map1中
        map2.forEach((key, value) -> map1.merge(key, value, Integer::sum));
        System.out.println("合并后的map: " + map1);
    }
    
    public static void performanceCharacteristics() {
        System.out.println("\n--- 性能特点 ---");
        
        HashMap<Integer, String> map = new HashMap<>();
        
        // 测试插入性能
        long startTime = System.nanoTime();
        for (int i = 0; i < 100000; i++) {
            map.put(i, "Value" + i);
        }
        long insertTime = System.nanoTime() - startTime;
        
        // 测试查找性能
        startTime = System.nanoTime();
        for (int i = 0; i < 100000; i++) {
            map.get(i);
        }
        long searchTime = System.nanoTime() - startTime;
        
        System.out.println("插入10万个元素耗时: " + insertTime / 1000000 + "ms");
        System.out.println("查找10万次耗时: " + searchTime / 1000000 + "ms");
        
        // 负载因子的影响
        System.out.println("\n负载因子对性能的影响:");
        testLoadFactor(0.5f);
        testLoadFactor(0.75f);  // 默认值
        testLoadFactor(1.0f);
    }
    
    private static void testLoadFactor(float loadFactor) {
        HashMap<Integer, String> map = new HashMap<>(16, loadFactor);
        
        long startTime = System.nanoTime();
        for (int i = 0; i < 10000; i++) {
            map.put(i, "Value" + i);
        }
        long time = System.nanoTime() - startTime;
        
        System.out.println("负载因子 " + loadFactor + " 插入耗时: " + time / 1000000 + "ms");
    }
}
```

### 4.2 TreeMap

```java
import java.util.*;

public class TreeMapDemo {
    public static void main(String[] args) {
        System.out.println("=== TreeMap 详解 ===");
        
        // 基本操作
        basicOperations();
        
        // 排序特性
        sortingFeatures();
        
        // 范围操作
        rangeOperations();
        
        // 导航方法
        navigationMethods();
    }
    
    public static void basicOperations() {
        System.out.println("\n--- 基本操作 ---");
        
        TreeMap<String, Integer> treeMap = new TreeMap<>();
        
        // 添加元素（按键自动排序）
        treeMap.put("Charlie", 25);
        treeMap.put("Alice", 30);
        treeMap.put("Bob", 28);
        treeMap.put("David", 35);
        
        System.out.println("添加元素后（按键排序）: " + treeMap);
        
        // 获取第一个和最后一个键值对
        System.out.println("第一个键值对: " + treeMap.firstEntry());
        System.out.println("最后一个键值对: " + treeMap.lastEntry());
        
        // 获取第一个和最后一个键
        System.out.println("第一个键: " + treeMap.firstKey());
        System.out.println("最后一个键: " + treeMap.lastKey());
    }
    
    public static void sortingFeatures() {
        System.out.println("\n--- 排序特性 ---");
        
        // 自然排序（字符串）
        TreeMap<String, String> naturalOrder = new TreeMap<>();
        naturalOrder.put("zebra", "斑马");
        naturalOrder.put("apple", "苹果");
        naturalOrder.put("banana", "香蕉");
        System.out.println("自然排序: " + naturalOrder);
        
        // 自定义排序（按键长度）
        TreeMap<String, String> lengthOrder = new TreeMap<>(Comparator.comparing(String::length));
        lengthOrder.put("a", "短");
        lengthOrder.put("hello", "中等");
        lengthOrder.put("programming", "长");
        System.out.println("按长度排序: " + lengthOrder);
        
        // 逆序排序
        TreeMap<Integer, String> reverseOrder = new TreeMap<>(Collections.reverseOrder());
        reverseOrder.put(1, "一");
        reverseOrder.put(3, "三");
        reverseOrder.put(2, "二");
        reverseOrder.put(5, "五");
        System.out.println("逆序排序: " + reverseOrder);
    }
    
    public static void rangeOperations() {
        System.out.println("\n--- 范围操作 ---");
        
        TreeMap<Integer, String> map = new TreeMap<>();
        for (int i = 1; i <= 10; i++) {
            map.put(i, "Value" + i);
        }
        System.out.println("原Map: " + map);
        
        // 子Map操作
        System.out.println("键小于5的子Map: " + map.headMap(5));
        System.out.println("键大于等于7的子Map: " + map.tailMap(7));
        System.out.println("键在3到8之间的子Map: " + map.subMap(3, 8));
        
        // 包含边界的子Map
        System.out.println("键在3到8之间（包含8）: " + map.subMap(3, true, 8, true));
    }
    
    public static void navigationMethods() {
        System.out.println("\n--- 导航方法 ---");
        
        TreeMap<Integer, String> map = new TreeMap<>();
        int[] keys = {1, 3, 5, 7, 9, 11, 13, 15};
        for (int key : keys) {
            map.put(key, "Value" + key);
        }
        System.out.println("原Map: " + map);
        
        int searchKey = 8;
        System.out.println("\n查找键: " + searchKey);
        
        // 查找操作
        System.out.println("小于等于" + searchKey + "的最大键: " + map.floorKey(searchKey));
        System.out.println("大于等于" + searchKey + "的最小键: " + map.ceilingKey(searchKey));
        System.out.println("小于" + searchKey + "的最大键: " + map.lowerKey(searchKey));
        System.out.println("大于" + searchKey + "的最小键: " + map.higherKey(searchKey));
        
        // 对应的Entry操作
        System.out.println("\n对应的Entry操作:");
        System.out.println("floorEntry: " + map.floorEntry(searchKey));
        System.out.println("ceilingEntry: " + map.ceilingEntry(searchKey));
        System.out.println("lowerEntry: " + map.lowerEntry(searchKey));
        System.out.println("higherEntry: " + map.higherEntry(searchKey));
        
        // 删除并返回第一个和最后一个
        System.out.println("\n删除操作:");
        System.out.println("删除并返回第一个: " + map.pollFirstEntry());
        System.out.println("删除并返回最后一个: " + map.pollLastEntry());
        System.out.println("删除后: " + map);
    }
}
```

## 五、集合选择指南

### 5.1 集合选择决策树

```java
import java.util.*;
import java.util.concurrent.CopyOnWriteArrayList;

public class CollectionSelectionGuide {
    public static void main(String[] args) {
        System.out.println("=== 集合选择指南 ===");
        
        // 演示不同场景下的集合选择
        demonstrateListSelection();
        demonstrateSetSelection();
        demonstrateMapSelection();
        demonstrateQueueSelection();
        
        // 性能对比
        performanceComparison();
    }
    
    public static void demonstrateListSelection() {
        System.out.println("\n--- List 选择指南 ---");
        
        // 场景1：频繁随机访问
        System.out.println("场景1：频繁随机访问 -> 选择ArrayList");
        List<Integer> arrayList = new ArrayList<>();
        // ArrayList 提供 O(1) 的随机访问
        
        // 场景2：频繁在开头/中间插入删除
        System.out.println("场景2：频繁在开头/中间插入删除 -> 选择LinkedList");
        List<Integer> linkedList = new LinkedList<>();
        // LinkedList 提供 O(1) 的插入删除（如果有引用）
        
        // 场景3：线程安全需求
        System.out.println("场景3：线程安全 -> 选择Vector或Collections.synchronizedList");
        List<Integer> syncList = Collections.synchronizedList(new ArrayList<>());
        Vector<Integer> vector = new Vector<>();
        
        // 场景4：读多写少的并发场景
        System.out.println("场景4：读多写少并发 -> 选择CopyOnWriteArrayList");
        List<Integer> cowList = new CopyOnWriteArrayList<>();
    }
    
    public static void demonstrateSetSelection() {
        System.out.println("\n--- Set 选择指南 ---");
        
        // 场景1：快速查找，不需要排序
        System.out.println("场景1：快速查找，无序 -> 选择HashSet");
        Set<String> hashSet = new HashSet<>();
        // HashSet 提供 O(1) 的查找性能
        
        // 场景2：需要保持插入顺序
        System.out.println("场景2：保持插入顺序 -> 选择LinkedHashSet");
        Set<String> linkedHashSet = new LinkedHashSet<>();
        
        // 场景3：需要排序
        System.out.println("场景3：需要排序 -> 选择TreeSet");
        Set<String> treeSet = new TreeSet<>();
        // TreeSet 提供 O(log n) 的操作，但元素有序
        
        // 场景4：枚举类型
        System.out.println("场景4：枚举类型 -> 选择EnumSet");
        Set<DayOfWeek> enumSet = EnumSet.allOf(DayOfWeek.class);
    }
    
    public static void demonstrateMapSelection() {
        System.out.println("\n--- Map 选择指南 ---");
        
        // 场景1：一般用途，高性能
        System.out.println("场景1：一般用途，高性能 -> 选择HashMap");
        Map<String, Integer> hashMap = new HashMap<>();
        
        // 场景2：需要保持插入顺序
        System.out.println("场景2：保持插入顺序 -> 选择LinkedHashMap");
        Map<String, Integer> linkedHashMap = new LinkedHashMap<>();
        
        // 场景3：需要排序
        System.out.println("场景3：需要排序 -> 选择TreeMap");
        Map<String, Integer> treeMap = new TreeMap<>();
        
        // 场景4：线程安全
        System.out.println("场景4：线程安全 -> 选择ConcurrentHashMap");
        // Map<String, Integer> concurrentMap = new ConcurrentHashMap<>();
        
        // 场景5：枚举键
        System.out.println("场景5：枚举键 -> 选择EnumMap");
        Map<DayOfWeek, String> enumMap = new EnumMap<>(DayOfWeek.class);
    }
    
    public static void demonstrateQueueSelection() {
        System.out.println("\n--- Queue 选择指南 ---");
        
        // 场景1：FIFO队列
        System.out.println("场景1：FIFO队列 -> 选择LinkedList或ArrayDeque");
        Queue<String> fifoQueue = new LinkedList<>();
        Queue<String> arrayDeque = new ArrayDeque<>();
        
        // 场景2：优先级队列
        System.out.println("场景2：优先级队列 -> 选择PriorityQueue");
        Queue<Integer> priorityQueue = new PriorityQueue<>();
        
        // 场景3：双端队列
        System.out.println("场景3：双端队列 -> 选择ArrayDeque");
        Deque<String> deque = new ArrayDeque<>();
    }
    
    public static void performanceComparison() {
        System.out.println("\n--- 性能对比 ---");
        
        int size = 100000;
        
        // List 性能对比
        System.out.println("\nList 添加性能对比（在末尾添加）:");
        testListAddPerformance(new ArrayList<>(), "ArrayList", size);
        testListAddPerformance(new LinkedList<>(), "LinkedList", size);
        testListAddPerformance(new Vector<>(), "Vector", size);
        
        // Set 性能对比
        System.out.println("\nSet 添加性能对比:");
        testSetAddPerformance(new HashSet<>(), "HashSet", size);
        testSetAddPerformance(new LinkedHashSet<>(), "LinkedHashSet", size);
        testSetAddPerformance(new TreeSet<>(), "TreeSet", size);
        
        // Map 性能对比
        System.out.println("\nMap 添加性能对比:");
        testMapPutPerformance(new HashMap<>(), "HashMap", size);
        testMapPutPerformance(new LinkedHashMap<>(), "LinkedHashMap", size);
        testMapPutPerformance(new TreeMap<>(), "TreeMap", size);
    }
    
    private static void testListAddPerformance(List<Integer> list, String name, int size) {
        long startTime = System.nanoTime();
        for (int i = 0; i < size; i++) {
            list.add(i);
        }
        long endTime = System.nanoTime();
        System.out.println(name + ": " + (endTime - startTime) / 1000000 + "ms");
    }
    
    private static void testSetAddPerformance(Set<Integer> set, String name, int size) {
        long startTime = System.nanoTime();
        for (int i = 0; i < size; i++) {
            set.add(i);
        }
        long endTime = System.nanoTime();
        System.out.println(name + ": " + (endTime - startTime) / 1000000 + "ms");
    }
    
    private static void testMapPutPerformance(Map<Integer, String> map, String name, int size) {
        long startTime = System.nanoTime();
        for (int i = 0; i < size; i++) {
            map.put(i, "Value" + i);
        }
        long endTime = System.nanoTime();
        System.out.println(name + ": " + (endTime - startTime) / 1000000 + "ms");
    }
}

// 示例枚举
enum DayOfWeek {
    MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY
}
```

### 5.2 集合选择决策表

```java
public class CollectionDecisionTable {
    public static void main(String[] args) {
        printCollectionDecisionTable();
    }
    
    public static void printCollectionDecisionTable() {
        System.out.println("=== 集合选择决策表 ===");
        
        System.out.println("\n【List 选择】");
        System.out.println("需求场景                    | 推荐选择        | 时间复杂度     | 说明");
        System.out.println("---------------------------|---------------|-------------|------------------");
        System.out.println("频繁随机访问                 | ArrayList     | get: O(1)   | 基于数组实现");
        System.out.println("频繁在开头/中间插入删除        | LinkedList    | add: O(1)*  | 基于链表实现");
        System.out.println("需要线程安全                 | Vector        | 同ArrayList  | 同步方法");
        System.out.println("读多写少的并发场景            | CopyOnWrite   | read: O(1)  | 写时复制");
        
        System.out.println("\n【Set 选择】");
        System.out.println("需求场景                    | 推荐选择        | 时间复杂度     | 说明");
        System.out.println("---------------------------|---------------|-------------|------------------");
        System.out.println("快速查找，无序要求            | HashSet       | O(1)        | 基于哈希表");
        System.out.println("保持插入顺序                 | LinkedHashSet | O(1)        | 哈希表+链表");
        System.out.println("需要排序                    | TreeSet       | O(log n)    | 基于红黑树");
        System.out.println("枚举类型                    | EnumSet       | O(1)        | 位向量实现");
        
        System.out.println("\n【Map 选择】");
        System.out.println("需求场景                    | 推荐选择        | 时间复杂度     | 说明");
        System.out.println("---------------------------|---------------|-------------|------------------");
        System.out.println("一般用途，高性能              | HashMap       | O(1)        | 基于哈希表");
        System.out.println("保持插入顺序                 | LinkedHashMap | O(1)        | 哈希表+链表");
        System.out.println("需要排序                    | TreeMap       | O(log n)    | 基于红黑树");
        System.out.println("线程安全                    | ConcurrentMap | O(1)        | 分段锁");
        System.out.println("枚举键                      | EnumMap       | O(1)        | 数组实现");
        
        System.out.println("\n【Queue 选择】");
        System.out.println("需求场景                    | 推荐选择        | 时间复杂度     | 说明");
        System.out.println("---------------------------|---------------|-------------|------------------");
        System.out.println("FIFO队列                   | ArrayDeque    | O(1)        | 循环数组");
        System.out.println("双端队列                    | ArrayDeque    | O(1)        | 两端操作");
        System.out.println("优先级队列                  | PriorityQueue | O(log n)    | 基于堆");
        System.out.println("线程安全队列                | BlockingQueue | varies      | 阻塞队列");
        
        System.out.println("\n【内存使用对比】");
        System.out.println("集合类型        | 内存开销    | 说明");
        System.out.println("---------------|-----------|---------------------------");
        System.out.println("ArrayList      | 低        | 只存储元素数组");
        System.out.println("LinkedList     | 高        | 每个节点额外存储前后指针");
        System.out.println("HashSet        | 中        | 基于HashMap实现");
        System.out.println("TreeSet        | 中        | 红黑树节点开销");
        System.out.println("HashMap        | 中        | 哈希表+链表/红黑树");
        System.out.println("TreeMap        | 高        | 红黑树节点开销较大");
    }
}
```

## 六、集合遍历方法

### 6.1 传统遍历方式

```java
import java.util.*;

public class CollectionIterationDemo {
    public static void main(String[] args) {
        System.out.println("=== 集合遍历方法 ===");
        
        // List 遍历
        demonstrateListIteration();
        
        // Set 遍历
        demonstrateSetIteration();
        
        // Map 遍历
        demonstrateMapIteration();
        
        // Iterator 的高级用法
        demonstrateIteratorAdvanced();
    }
    
    public static void demonstrateListIteration() {
        System.out.println("\n--- List 遍历方式 ---");
        
        List<String> list = Arrays.asList("Apple", "Banana", "Cherry", "Date");
        
        // 1. 传统for循环
        System.out.println("1. 传统for循环:");
        for (int i = 0; i < list.size(); i++) {
            System.out.println("Index " + i + ": " + list.get(i));
        }
        
        // 2. 增强for循环（for-each）
        System.out.println("\n2. 增强for循环:");
        for (String item : list) {
            System.out.println("Item: " + item);
        }
        
        // 3. Iterator
        System.out.println("\n3. Iterator:");
        Iterator<String> iterator = list.iterator();
        while (iterator.hasNext()) {
            String item = iterator.next();
            System.out.println("Item: " + item);
        }
        
        // 4. ListIterator（双向遍历）
        System.out.println("\n4. ListIterator（反向遍历）:");
        ListIterator<String> listIterator = list.listIterator(list.size());
        while (listIterator.hasPrevious()) {
            String item = listIterator.previous();
            System.out.println("Item: " + item);
        }
        
        // 5. Stream API（Java 8+）
        System.out.println("\n5. Stream API:");
        list.stream().forEach(item -> System.out.println("Item: " + item));
    }
    
    public static void demonstrateSetIteration() {
        System.out.println("\n--- Set 遍历方式 ---");
        
        Set<String> set = new HashSet<>(Arrays.asList("Apple", "Banana", "Cherry", "Date"));
        
        // 1. 增强for循环
        System.out.println("1. 增强for循环:");
        for (String item : set) {
            System.out.println("Item: " + item);
        }
        
        // 2. Iterator
        System.out.println("\n2. Iterator:");
        Iterator<String> iterator = set.iterator();
        while (iterator.hasNext()) {
            String item = iterator.next();
            System.out.println("Item: " + item);
        }
        
        // 3. Stream API
        System.out.println("\n3. Stream API:");
        set.stream().forEach(item -> System.out.println("Item: " + item));
        
        // 4. 过滤遍历
        System.out.println("\n4. 过滤遍历（以A开头）:");
        set.stream()
           .filter(item -> item.startsWith("A"))
           .forEach(item -> System.out.println("Filtered: " + item));
    }
    
    public static void demonstrateMapIteration() {
        System.out.println("\n--- Map 遍历方式 ---");
        
        Map<String, Integer> map = new HashMap<>();
        map.put("Apple", 10);
        map.put("Banana", 20);
        map.put("Cherry", 15);
        map.put("Date", 25);
        
        // 1. 遍历键
        System.out.println("1. 遍历键:");
        for (String key : map.keySet()) {
            System.out.println("Key: " + key + ", Value: " + map.get(key));
        }
        
        // 2. 遍历值
        System.out.println("\n2. 遍历值:");
        for (Integer value : map.values()) {
            System.out.println("Value: " + value);
        }
        
        // 3. 遍历键值对
        System.out.println("\n3. 遍历键值对:");
        for (Map.Entry<String, Integer> entry : map.entrySet()) {
            System.out.println("Key: " + entry.getKey() + ", Value: " + entry.getValue());
        }
        
        // 4. 使用Iterator遍历键值对
        System.out.println("\n4. 使用Iterator遍历键值对:");
        Iterator<Map.Entry<String, Integer>> iterator = map.entrySet().iterator();
        while (iterator.hasNext()) {
            Map.Entry<String, Integer> entry = iterator.next();
            System.out.println("Key: " + entry.getKey() + ", Value: " + entry.getValue());
        }
        
        // 5. Lambda表达式（Java 8+）
        System.out.println("\n5. Lambda表达式:");
        map.forEach((key, value) -> System.out.println(key + " -> " + value));
        
        // 6. Stream API 复杂操作
        System.out.println("\n6. Stream API 复杂操作（值大于15）:");
        map.entrySet().stream()
           .filter(entry -> entry.getValue() > 15)
           .sorted(Map.Entry.comparingByValue())
           .forEach(entry -> System.out.println(entry.getKey() + ": " + entry.getValue()));
    }
    
    public static void demonstrateIteratorAdvanced() {
        System.out.println("\n--- Iterator 高级用法 ---");
        
        // 安全删除元素
        List<String> list = new ArrayList<>(Arrays.asList("A", "B", "C", "D", "E"));
        System.out.println("原列表: " + list);
        
        // 错误的删除方式（会抛出ConcurrentModificationException）
        // for (String item : list) {
        //     if (item.equals("C")) {
        //         list.remove(item);  // 错误！
        //     }
        // }
        
        // 正确的删除方式
        Iterator<String> iterator = list.iterator();
        while (iterator.hasNext()) {
            String item = iterator.next();
            if (item.equals("C")) {
                iterator.remove();  // 正确！
            }
        }
        System.out.println("删除C后: " + list);
        
        // ListIterator 的双向遍历和修改
        List<Integer> numbers = new ArrayList<>(Arrays.asList(1, 2, 3, 4, 5));
        System.out.println("\n原数字列表: " + numbers);
        
        ListIterator<Integer> listIterator = numbers.listIterator();
        while (listIterator.hasNext()) {
            Integer num = listIterator.next();
            if (num % 2 == 0) {
                listIterator.set(num * 10);  // 偶数乘以10
            }
            if (num == 3) {
                listIterator.add(99);  // 在3后面添加99
            }
        }
        System.out.println("修改后: " + numbers);
        
        // 反向遍历
        System.out.println("\n反向遍历:");
        while (listIterator.hasPrevious()) {
            System.out.println("Previous: " + listIterator.previous());
        }
    }
}
```

## 总结

Java 集合框架是 Java 编程的核心组件，掌握其使用方法和最佳实践对于编写高效、可维护的代码至关重要。

### 关键要点

1. **选择合适的集合类型**：根据具体需求选择 List、Set、Map 或 Queue
2. **性能考虑**：了解不同实现的时间复杂度和适用场景
3. **线程安全**：在多线程环境中选择合适的并发集合
4. **内存优化**：合理设置初始容量，避免频繁扩容
5. **遍历方式**：选择合适的遍历方法，善用 Stream API
6. **避免陷阱**：注意 equals/hashCode 的重写，避免在遍历时修改集合

通过深入理解和实践这些概念，你将能够更好地利用 Java 集合框架来解决实际编程问题。