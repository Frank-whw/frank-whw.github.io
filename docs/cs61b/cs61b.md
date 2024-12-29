# 9. Disjointed set
## 9.1 introduction
1. 互斥
2. 有2种运算：
	1. `connect(x, y)`或者说是`union`
	2. `isConnected(x, y)`
3. an **interface** determines _what_ behaviors a data structure should have (but not _how_ to accomplish it)  接口
4. **design decisions greatly affect asymptotic runtime and code complexity.**
```java
public interface DisjointSets {
    /** connects two items P and Q */
    void connect(int p, int q);

    /** checks to see if two items are connected */
    boolean isConnected(int p, int q); 
}
```
## 9.2 Quick Find
1. 同一个set的元素的id相同
![image.png](https://raw.githubusercontent.com/Frank-whw/img/main/blog/202411111421.png)
2. 判断isConnected（x, y)可以直接判断id是否相同，时间复杂度O(1)
```java
public class QuickFindDS implements DisjointSets {

    private int[] id;

    /* Θ(N) */
    public QuickFindDS(int N){
        id = new int[N];
        for (int i = 0; i < N; i++){
            id[i] = i;
        }
    }

    /* need to iterate through the array => Θ(N) */
    public void connect(int p, int q){
        int pid = id[p];
        int qid = id[q];
        for (int i = 0; i < id.length; i++){
            if (id[i] == pid){
                id[i] = qid;
            }
        }
    }

    /* Θ(1) */
    public boolean isConnected(int p, int q){
        return (id[p] == id[q]);
    }
}
```
## 9.3 Quick Union
1. 辅助函数`find(int item)` 返回`item`所在的根
![image.png](https://raw.githubusercontent.com/Frank-whw/img/main/blog/202411111426.png)
	- find(4) = 0   find(5) = 3
```java
public class QuickUnionDS implements DisjointSets {
    private int[] parent;
    public QuickUnionDS(int num) {
        parent = new int[num];
        for (int i = 0; i < num; i++) {
            parent[i] = i;
        }
    }

    private int find(int p) {
        while (parent[p] >= 0) {
            p = parent[p];
        }
        return p;
    }

    @Override
    public void connect(int p, int q) {
        int i = find(p);
        int j= find(q);
        parent[i] = j;
    }

    @Override
    public boolean isConnected(int p, int q) {
        return find(p) == find(q);
    }
}
```
## 9.4 Weighted Quick Union(WQU)
1. 优化QU，针对`find`函数在运行是要climb to the root of a tree，显然是低效的，为了解决这个问题，提出了个关键思路：**在每次connect时，判断2个trees的高度，把高度小的tree links to 高的**。
2. 树的maximum height可以控制在logN内
## 9.5 WQU with Path Compression
1. 有点抽象，让所有的`item`都连接到根
2. 理解了
3. 核心思路是在find操作时，在经过沿途的`item`时把它直接连接到根节点，使得后续的查找路径更短
4. 为什么不会增加额外的渐进复杂度：
	1. **顺路**
	2. 摊还分析（Amortized Analysis）
---
# 10. ADT
## 10.1 intro
- Abstract Data Type抽象数据类型
- 仅由其操作定义，而不由其实现定义
- 常见的：Stacks、Lists、Sets、Maps
## 10.2 trees
- BST: Binary Search Tree
- **Hibbard deletion
	1. 找到该节点的**直接后继节点**（即右子树中最小的节点）或**直接前驱节点**（即左子树中最大的节点）。
	2.  用该后继节点或前驱节点的值替换待删除节点的值。
	3. 然后删除这个后继或前驱节点（注意它必然是前两种情况之一：要么是叶子节点，要么只有一个子节点）

---

# 11. Balanced Trees
## 11.1 Intro
- **BigO** is not synonymous to the Worst-case
- **depth**: the number of links between a node and the root.
- **height**: the lowest depth of a tree.
- **average depth**: average of the total depths in the tree. 
## 11.2 B-Trees
- problem：每次insert一个数据时都会增加树的高度
- 为改变这点，引入一个crazy idea：**let's just never add a leaf node! **
- When we insert, let's just add to a current leaf node. This way, the height will never increase.
![image.png](https://raw.githubusercontent.com/Frank-whw/img/main/blog/202411161829.png)
![image.png](https://raw.githubusercontent.com/Frank-whw/img/main/blog/202411171423.png)

- 我本人是不太喜欢或者理解这一个idea，原因在于这增加了find的时间复杂度，在16 17 18 19这一个叶子中find数据还是需要traverse，时间复杂度取决于叶子的大小
## 11.3 B-Tree invariants
- 同样一组数据，插入的顺序会决定树的高度
- B-Trees的特点（invarants）：
	1. All leaves must be the same distance from the source.
	2. A non-leaf node with `k`items must have exactly `k+1` children.
## 11.4 Rotating Trees
- 存在的原因在于通过rotating去维持树的invariant
```java
private Node rotateRight(Node h) {
    // assert (h != null) && isRed(h.left);
    Node x = h.left;
    h.left = x.right;
    x.right = h;
    return x;
}

// make a right-leaning link lean to the left
private Node rotateLeft(Node h) {
    // assert (h != null) && isRed(h.right);
    Node x = h.right;
    h.right = x.left;
    x.left = h;
    return x;
}
```
## 11.5 Red-Black Trees
- 略

---
# 12 Hashing
## 12.1 attempt
- limitation：
	1. item需要可以被比较
	2. 最优只有logn的复杂度，能不能更加优秀
- 针对limitation2提出DataIndexedIntergerSet
## 12.2 Inserting words
- 其实就是引出了**哈希表**的核心：input一个什么东西，把它转为成唯一且对应的hash值，根据这个hash值可以判断这个东西是不是存在
- 解决了item可以不需要被比较的问题以及复杂度变为O(1)
- 但是新问题：浪费
## 12.3 Inserting String and Overflow
- overflow会导致2种不同的string有相同的表示
- 因为java中最大的数据是2,147,483,647
- java中最多有4,294,967,296个整数，但是object的数量比这多
- 所以**collision不可避免**，但是这并不会阻止我们将string转换成int
- 以上这种转换称之为"Computing the **hash code** of the object"
- java的每一个object都内置了一个函数`.hashcode()`，这是通过object的地址（地址显然是唯一且对应的）生成hash值
- 有时我们也自己create `hashcode` method
- properties of `hashCodes`:
	1. 必须是整数
	2. 对同一个object运行`.hashCode`，**返回值必须相同**
	3. 2个Object被认为`.equal()`必须有相同的hash code
- pending issues：
	- a lot of space
	- hash collisions
## 12.4 handling collisions
- 主要的想法是一个hash值对应一个LinkedList，so that如果在添加一个item时，它的hash值已经存在在map中说明hash collision，那么将这个item放在hash值对应的LinkedList中（因为List显然是可以存多个item的）
- create workflow：
	- `add`item
	- `contains `item
- 于是可以减少容量，同时使用mod运算
- 目前的情况：
	- space问题解决了
	- collision解决了
	- runtime complexity有问题了
## 12.5 Hash Table and Fixing Runtime
- 最终的数据结构：`HashTable`
	- Inputs are converted by a hash function (`hashcode`) into an integer. Then, they're converted to a valid index using the modulus operator. Then, they're added at that index (dealing with collisions using LinkedList).
	- `contains` works in a similar fashion by figuring out the valid index, and looking in the corresponding LinkedList for the item.
- 如何解决runtime问题：
	1. 动态增长哈希表
	2. 改进哈希码

---
# Lab 7
- 以**树**为基础创建一个Map
- 创建完之后与ULLMap和TreeMap比较
- 需要完成的method：除了`remove、iterator、keySet`都要 + `printInOrder`()
- K应该继承Comparable：assume that generic keys `K` have a `compareTo` method.
-  use a private nested `BSTNode` class to help facilitate your implementation. （recommend）
finish at 2024年11月19日
---
# 13 Heaps and Priority Queues
## 13.1 PQ interface
- 引入：如何找到最大或者最小的元素而不只是快速搜索
- 引出：Priority Queue（优先队列）
	- 如何理解：想象一个包，可以加东西 可以减东西，但是只能`interact with the smallest items of this bag`
	```java
/** (Min) Priority Queue: Allowing tracking and removal of 
* the smallest item in a priority queue. */
public interface MinPQ<Item> {
	/** Adds the item to the priority queue. */
	public void add(Item x);
	/** Returns the smallest item in the priority queue. */
	public Item getSmallest();
	/** Removes the smallest item from the priority queue. */
	public Item removeSmallest();
	/** Returns the size of the priority queue. */
	public int size();
}
	```

![image.png](https://raw.githubusercontent.com/Frank-whw/img/main/blog/202411200928434.png)

- 显然BST的效率最高
## 13.2 Heaps
- 根据BST引出min-heap，有如下特性：
	- 每个节点都小于等于它的孩子
	- 如果有缺失，只会出现在bottom level
- 有如下操作：
	1. `add`: Add to the end of heap temporarily. Swim up the hierarchy to the proper place
	2.  `getSmallest`: Return the root of the heap (This is guaranteed to be the minimum by our _min-heap_ property
	3. `removeSmallest`: Swap the last item in the heap into the root. Sink down the hierarchy to the proper place.
## 13.3 The Implementation
- 通过在一个数组的开头留一个空位以简化计算!
![image.png](https://raw.githubusercontent.com/Frank-whw/img/main/blog/202411201039200.png)
- `leftChild(k)`=k∗2=k∗2
- `rightChild(k)`=k∗2+1=k∗2+1
- `parent(k)` =k/2=k/2

| Methods          | Ordered Array | Bushy BST | Hash Table | Heap    |
| ---------------- | ------------- | --------- | ---------- | ------- |
| `add`            | Θ(N)          | Θ(logN)   | Θ(1)       | Θ(logN) |
| `getSmallest`    | Θ(1)          | Θ(logN)   | Θ(N)       | Θ(1)    |
| `removeSmallest` | Θ(N)          | Θ(logN)   | Θ(N)       | Θ(logN) |
**problem**：
1. PQ怎么知道如何排序
2. 有什么允许灵活排序的方法吗
3. 怎么样才能将MinPQ变为MaxPQ

---
# 14 Data Structures Summary
|Name|Store Operation(s)|Primary Retrieval Operation|Retrieve By|
|---|---|---|---|
|List|`add(key)`, `insert(key, index)`|`get(index)`|index|
|Map|`put(key, value)`|`get(key)`|key identity|
|Set|`add(key)`|`containsKey(key)`|key identity|
|PQ|`add(key)`|`getSmallest()`|key order (aka key size)|
|Disjoint Sets|`connect(int1, int2)`|`isConnected(int1, int2)`|two integer values|

![image.png](https://raw.githubusercontent.com/Frank-whw/img/main/blog/202411201057311.png)

- we can often think of an ADT by the use of another ADT. 
- And that Abstract Data Types have layers of abstraction, each defining a behavior that is more specific than the idea that came before it.

---

# 17 Tree Traversals and Graphs
## 17.1 Tree recap
- 树的作用：
`speeding up searching for items, allowing prefixing, checking connectedness, and so on`
- 树的应用在生活中很普遍
## 17.2 Tree Traversal
- 层遍历 + 深度优先遍历（前序、中序和后序）
- 前序遍历
```java
preOrder(BSTNode x) {
    if (x == null) return;
    print(x.key)
    preOrder(x.left)
    preOrder(x.right)
}
```
## 17.3 Graphs
- 树的局限：2个节点之间只能有一条路径
- 图的组成：点+边
- 树 真包含于 图
- Graphs can be divided into two categories: **_simple_ graphs** and _multigraphs_ (or complicated graphs, a term I invented, because that's how I like to think of them.)
- 本节课研究simple graphs，简单图又分为无向+有向
## 17.4 Graph Problems
- **s-t Path**: Is there a path between vertices s and t?
- **Connectivity**: Is the graph connected, i.e. is there a path between all vertices?
- **Biconnectivity**: Is there a vertex whose removal disconnects the graph?
- **Shortest s-t Path**: What is the shortest path between vertices s and t?
- **Cycle Detection**: Does the graph contain any cycles?
- **Euler Tour**: Is there a cycle that uses every edge exactly once?
- **Hamilton Tour**: Is there a cycle that uses every vertex exactly once?
- **Planarity**: Can you draw the graph on paper with no crossing edges?
- **Isomorphism**: Are two graphs isomorphic (the same graph in disguise)?

---
# 18. BFS
## 18.1 BFS
- Breadth First Search(also known as Level Order Traversal)
- The pseudocode for BFS is as follows:
```
Initialize the fringe (a queue with the starting vertex) and mark that vertex.
Repeat until fringe is empty:
Remove vertex v from the fringe.
For each unmarked neighbor n of v:
Mark n.
Add n to fringe.
Set edgeTo[n] = v.
Set distTo[n] = distTo[v] + 1.
```

fringe在这边指一个队列，先入先出

- dfs和bfs的区别：
	- dfs是一个方向去搜，不到黄河不回头，直到遇到绝境
	- bfs是先把本节点所连接的所有节点都遍历一遍，走到下一个节点的时候，再把连接节点的所有节点遍历一遍
## 18.2 Representing Graphs
- 有个难点：
	- 原话：For our Graph API, let's use **the common convention** of assigning each unique node to an **integer** number. This can be done by maintaining a map which can tell us the integer assigned to each original node label. Doing so allows us to define our API to work with integers specifically, rather than introducing the need for generic types.
	- 我的理解：用唯一对应的整数表示节点，而不是节点的原始标签，有点像Hash算法

---
# Lab 8
## key things
- 与lab7很像，不同点在于这次将建造一个Hash Map而不是Tree Map
- 完成后 需要与基于列表的Map 以及 内置的Java HashMap进行比较，另外要和基于不同数据结构的map对比
- 新建一个class MyHashMap，完成Map61B中所有的methods，其中remove用报错代替，iterator返回迭代器，建议新建一个HashSet实例属性
- 那么如何让hash table基于不同的数据结构呢？如果只是使用 Find + Replace 需要付出很多努力才能将存储桶类型更改为不同的存储桶类型。所以我们这边要使用**polymorphism和inheritance**
- 继承结构如下：
![image.png](https://raw.githubusercontent.com/Frank-whw/img/main/blog/202411242047029.png)
- In the starter code, we give the **instance variable** `private Collection<Node>[] buckets`, which is the underlying data structure of the hash table.
	解读
	- buckets是MyHashMap的一个private变量
	- 这是Collection对象的数组，其中每一个Collection代表一个bucket
	- Node是个private辅助的类，用来存储单个key-value对。starter code应该易于理解且不需要任何修改
	- java.util.Collection是大多数据结构继承自的接口，该接口支持很多methods，如add、remove、iterate。有以下数据结构继承了该接口：ArrayList、LinkedList、TreeSet、HashSet、PriorityQueue等。所以我们可以assign them to a variable of static type Collection with **polymorphism**（多态）
	- 由于 Java 的限制，不能直接创建参数化类型（例如 `Collection<Node>`)的数组。为了实现类似功能，可以创建原始类型的 `Collection[]` 数组，并通过编程约定，确保数组中只存储特定类型（如 `Collection<Node>`）的元素。 **不太理解**
		- **不能创建参数化类型的数组**：  
		    在 Java 中，不能直接创建一个参数化类型（Parameterized Type，例如 `Collection<Node>`）的数组。比如，以下代码是不合法的：
		    `Collection<Node>[] buckets = new Collection<Node>[size];`     这是因为 Java 的泛型是通过**类型擦除**（Type Erasure）实现的，在运行时，`Collection<Node>` 其实只被当作一个普通的 `Collection`。如果允许直接创建参数化类型数组，会导致类型安全问题，无法保证数组中存储的元素类型一致。
		- **解决方法：**  
		    为了绕过这个限制，可以创建一个没有指定具体类型的 `Collection[]` 数组（即原始类型的数组），然后在使用时只向数组中添加类型为 `Collection<Node>` 的元素。代码示例如下：`Collection<Node>[] buckets = new Collection[size];`
		    这里的 `new Collection[size]` 创建了一个只能存储 `Collection` 的数组，但这个数组中的每个元素可以是任何类型的 `Collection`（例如 `Collection<Integer>` 或 `Collection<Node>`）。通过编程约定，我们只往其中添加 `Collection<Node>`。
		- **保证类型安全：**  
		    在实际操作中，尽管数组允许存储任意类型的集合（`Collection`），但我们要确保只将 `Collection<Node>` 存入数组，以保持逻辑上的类型一致性。
	- 为了代码便捷性，我们要使用createBucket这个方法：
```java
protected Collection<Node> createBucket() {
	return new LinkedList<>();
}
```
这个方法允许`MyHashMap*Buckets.java` 覆盖 `createBucket`
## implementation Requirements
- 使用3种constructors
```java
public MyHashMap();
public MyHashMap(int initialSize);
public MyHashMap(int initialSize, double loadFactor);
```
- 负载因子（load factor）= N / M，N是元素的数量，M是存储桶数
- 当负载因子超过loadFactor时，我们应该增加size（使用乘法调整大小，不需要调小）
- 默认值initialSize = 16， loadFactor = 0.75
- 每个bucket不是一个单独的对象，而是可以存储多个键值对的数据结构

# 19 Shortest Paths
## 19.1 Recap
- DFS不适用细长的图，因为每次递归调用会占用很大的空间
- BFS不适用bushy的图，因为队列会被大量使用
- 但是这些只适用于“边”没有**权重**的图
## 19.2 Dijkstra's Algorithm
- 迪杰斯特拉算法
- 通过优先级队列，当队列不为空时，弹出一个顶点并**relax**到从这个点出发的所有边
