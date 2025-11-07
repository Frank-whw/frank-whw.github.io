# Java 异常与泛型

## 异常体系

### 异常分类
```
Throwable (所有错误和异常的父类)
├── Error (系统级别错误，程序无法处理)
│   ├── OutOfMemoryError
│   ├── StackOverflowError
│   └── VirtualMachineError
└── Exception (程序可以处理的异常)
    ├── RuntimeException (运行时异常，编译时不检查)
    │   ├── NullPointerException
    │   ├── IndexOutOfBoundsException
    │   ├── IllegalArgumentException
    │   └── ClassCastException
    └── 其他异常 (编译时异常，必须处理)
        ├── IOException
        ├── SQLException
        └── FileNotFoundException
```

### 异常的作用
- **调试工具**：帮助定位和修复bug
- **通信机制**：作为方法内部的特殊返回值，通知上层调用者执行情况

### 异常处理方案

#### 方案1：向上抛出并最终处理
```java
public void processFile() throws IOException {
    // 底层代码
    FileInputStream fis = new FileInputStream("file.txt");
}

// 最外层捕获
public static void main(String[] args) {
    try {
        processFile();
    } catch (IOException e) {
        // 记录异常信息（用于调试）
        e.printStackTrace();
        // 用户友好提示
        System.out.println("文件处理失败，请检查文件是否存在");
    }
}
```

#### 方案2：尝试修复
```java
public void connectToDatabase() {
    int retryCount = 0;
    while (retryCount < 3) {
        try {
            // 尝试连接数据库
            establishConnection();
            break;
        } catch (SQLException e) {
            retryCount++;
            if (retryCount == 3) {
                System.out.println("数据库连接失败，请检查网络");
            }
        }
    }
}
```

## 泛型

### 基本概念
- **作用**：编译期类型安全检查，避免强制类型转换和类型转换异常
- **本质**：将具体数据类型作为参数传递给类型变量

### 泛型类
```java
// 定义泛型类
public class Box<T> {
    private T content;
    
    public void setContent(T content) {
        this.content = content;
    }
    
    public T getContent() {
        return content;
    }
}

// 使用
Box<String> stringBox = new Box<>();
Box<Integer> integerBox = new Box<>();
```

### 常用类型变量约定
- `E` - Element (集合元素类型)
- `T` - Type (返回值类型)
- `K` - Key (键类型)
- `V` - Value (值类型)
- `N` - Number (数值类型)

### 泛型接口
```java
public interface Repository<T> {
    void save(T entity);
    T findById(Long id);
    List<T> findAll();
}

// 实现
public class UserRepository implements Repository<User> {
    @Override
    public void save(User entity) { ... }
    
    @Override
    public User findById(Long id) { ... }
    
    @Override
    public List<User> findAll() { ... }
}
```

### 泛型方法
```java
public class Utility {
    // 泛型方法
    public static <T> T processItem(T item) {
        // 处理逻辑
        return item;
    }
    
    // 多个类型参数
    public static <T, U> Pair<T, U> createPair(T first, U second) {
        return new Pair<>(first, second);
    }
}
```

### 通配符和上下限

#### 无界通配符
```java
public void processList(List<?> list) {
    // 可以接受任何类型的List
    for (Object item : list) {
        System.out.println(item);
    }
}
```

#### 上限通配符 (extends)
```java
// 接受Car及其子类的List
public void processCars(List<? extends Car> cars) {
    for (Car car : cars) {
        car.drive();
    }
}
```

#### 下限通配符 (super)
```java
// 接受Car及其父类的List
public void addCars(List<? super Car> list) {
    list.add(new Car());
    list.add(new SportsCar()); // SportsCar是Car的子类
}
```

### 泛型的限制和特性

#### 不支持基本数据类型
```java
// ❌ 错误写法
// List<int> intList = new ArrayList<>();

// ✅ 正确写法 - 使用包装类
List<Integer> intList = new ArrayList<>();
```

#### 类型擦除
泛型只在编译阶段有效，编译后泛型信息会被擦除，所有类型都变为Object类型。

```java
// 编译前
List<String> stringList = new ArrayList<>();

// 编译后（类型擦除）
List stringList = new ArrayList();
```

### 包装类

#### 基本类型与包装类对应关系
| 基本类型 | 包装类    |
|----------|-----------|
| byte     | Byte      |
| short    | Short     |
| int      | Integer   |
| long     | Long      |
| float    | Float     |
| double   | Double    |
| char     | Character |
| boolean  | Boolean   |

#### 包装类的使用
```java
// 手动装箱拆箱
Integer it = Integer.valueOf(100);  // 装箱
int value = it.intValue();          // 拆箱

// 自动装箱拆箱 (Java 5+)
Integer it11 = 100;                 // 自动装箱
int value2 = it11;                  // 自动拆箱
```

#### 包装类的常用方法
```java
// 字符串转换
String numStr = "123";
int num = Integer.parseInt(numStr);        // String -> int
Integer numObj = Integer.valueOf(numStr);  // String -> Integer

// 进制转换
String binary = Integer.toBinaryString(10); // "1010"
String hex = Integer.toHexString(255);      // "ff"

// 类型比较
Integer a = 100;
Integer b = 100;
System.out.println(a.equals(b));           // true
System.out.println(a.compareTo(200));      // -1 (a < 200)

// 常量值
System.out.println(Integer.MAX_VALUE);     // 2147483647
System.out.println(Integer.MIN_VALUE);     // -2147483648
```

### 最佳实践

#### 异常处理最佳实践
1. 具体异常具体处理，不要捕获通用Exception
2. 在合适的层级处理异常
3. 记录完整的异常信息
4. 为用户提供友好的错误提示

#### 泛型使用最佳实践
1. 在编译期充分利用类型安全检查
2. 使用有意义的类型参数名称
3. 合理使用上下限通配符提高API灵活性
4. 注意类型擦除对重载的影响


# Collection集合
list
set
接口
实现类
ArrayList HashSet
list：添加的元素是有序 可重复 有索引
set：无需 不重复 无索引

collection的常用功能：
add clear remove contain isEmpty size toArray
把集合转换为字符串数组
`String[] arr2 = list.toArray(String[]::new);`构造器引用

遍历方式
1. 迭代器
	iterator
	hasNext
	next 
2. 增强for循环
	for each
	for(类型 变量名 ： 数组或则和集合)
3. lambda表达式
	forEach 结合lambda遍历集合
	但是源码本质就是for each

三种遍历的区别
遍历集合的同时有存在增删集合元素的行为时可能出现业务异常，并发修改异常问题
迭代器遍历并删除默认存在并发修改异常问题
解决方法时用迭代器自己的方法去删除 it.remove

用增强for和lambda都没有办法解决并发修改异常问题   

如果有索引的话 可以用索引去解决