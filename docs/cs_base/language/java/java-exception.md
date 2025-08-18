---
icon: material/alert-circle
comments: true
---

# Java 异常处理

!!! note "本章内容"
    本章介绍 Java 的异常处理机制：异常体系、处理语法、自定义异常和最佳实践。

## 一、异常体系概述

### 1.1 异常层次结构

```java
/*
异常层次结构：

Throwable
├── Error (错误)
│   ├── OutOfMemoryError
│   ├── StackOverflowError
│   └── VirtualMachineError
└── Exception (异常)
    ├── RuntimeException (运行时异常/非检查异常)
    │   ├── NullPointerException
    │   ├── IndexOutOfBoundsException
    │   ├── IllegalArgumentException
    │   └── ClassCastException
    └── 检查异常 (Checked Exception)
        ├── IOException
        ├── SQLException
        ├── ClassNotFoundException
        └── ParseException
*/

public class ExceptionHierarchyDemo {
    public static void main(String[] args) {
        System.out.println("=== 异常层次结构演示 ===");
        
        // Error 示例（通常不应该被捕获）
        try {
            // 模拟栈溢出
            // recursiveMethod();
        } catch (StackOverflowError e) {
            System.out.println("捕获到 Error: " + e.getClass().getSimpleName());
        }
        
        // RuntimeException 示例
        try {
            String str = null;
            int length = str.length();  // NullPointerException
        } catch (RuntimeException e) {
            System.out.println("捕获到运行时异常: " + e.getClass().getSimpleName());
        }
        
        // 检查异常示例
        try {
            Class.forName("com.nonexistent.Class");  // ClassNotFoundException
        } catch (ClassNotFoundException e) {
            System.out.println("捕获到检查异常: " + e.getClass().getSimpleName());
        }
    }
    
    // 递归方法导致栈溢出
    public static void recursiveMethod() {
        recursiveMethod();
    }
}
```

### 1.2 常见运行时异常

```java
import java.util.ArrayList;
import java.util.List;

public class CommonRuntimeExceptionsDemo {
    public static void main(String[] args) {
        System.out.println("=== 常见运行时异常 ===");
        
        // 1. NullPointerException
        demonstrateNullPointerException();
        
        // 2. IndexOutOfBoundsException
        demonstrateIndexOutOfBoundsException();
        
        // 3. IllegalArgumentException
        demonstrateIllegalArgumentException();
        
        // 4. ClassCastException
        demonstrateClassCastException();
        
        // 5. NumberFormatException
        demonstrateNumberFormatException();
        
        // 6. ArithmeticException
        demonstrateArithmeticException();
    }
    
    public static void demonstrateNullPointerException() {
        System.out.println("\n--- NullPointerException ---");
        try {
            String str = null;
            System.out.println(str.length());  // 空指针异常
        } catch (NullPointerException e) {
            System.out.println("捕获异常: " + e.getMessage());
        }
    }
    
    public static void demonstrateIndexOutOfBoundsException() {
        System.out.println("\n--- IndexOutOfBoundsException ---");
        try {
            List<String> list = new ArrayList<>();
            list.add("item1");
            System.out.println(list.get(5));  // 索引越界
        } catch (IndexOutOfBoundsException e) {
            System.out.println("捕获异常: " + e.getMessage());
        }
        
        try {
            int[] array = {1, 2, 3};
            System.out.println(array[10]);  // 数组越界
        } catch (ArrayIndexOutOfBoundsException e) {
            System.out.println("捕获异常: " + e.getMessage());
        }
    }
    
    public static void demonstrateIllegalArgumentException() {
        System.out.println("\n--- IllegalArgumentException ---");
        try {
            Thread.sleep(-1000);  // 负数参数
        } catch (IllegalArgumentException e) {
            System.out.println("捕获异常: " + e.getMessage());
        } catch (InterruptedException e) {
            System.out.println("线程中断异常");
        }
    }
    
    public static void demonstrateClassCastException() {
        System.out.println("\n--- ClassCastException ---");
        try {
            Object obj = "Hello";
            Integer num = (Integer) obj;  // 类型转换异常
        } catch (ClassCastException e) {
            System.out.println("捕获异常: " + e.getMessage());
        }
    }
    
    public static void demonstrateNumberFormatException() {
        System.out.println("\n--- NumberFormatException ---");
        try {
            int num = Integer.parseInt("abc");  // 数字格式异常
        } catch (NumberFormatException e) {
            System.out.println("捕获异常: " + e.getMessage());
        }
    }
    
    public static void demonstrateArithmeticException() {
        System.out.println("\n--- ArithmeticException ---");
        try {
            int result = 10 / 0;  // 除零异常
        } catch (ArithmeticException e) {
            System.out.println("捕获异常: " + e.getMessage());
        }
    }
}
```

## 二、异常处理语法

### 2.1 try-catch-finally 语句

```java
import java.io.*;
import java.util.Scanner;

public class TryCatchFinallyDemo {
    public static void main(String[] args) {
        // 基本 try-catch
        basicTryCatch();
        
        // 多个 catch 块
        multipleCatch();
        
        // try-catch-finally
        tryCatchFinally();
        
        // finally 的执行时机
        finallyExecutionOrder();
    }
    
    public static void basicTryCatch() {
        System.out.println("=== 基本 try-catch ===");
        try {
            int[] array = {1, 2, 3};
            System.out.println(array[5]);
        } catch (ArrayIndexOutOfBoundsException e) {
            System.out.println("数组越界: " + e.getMessage());
        }
        System.out.println("程序继续执行");
    }
    
    public static void multipleCatch() {
        System.out.println("\n=== 多个 catch 块 ===");
        Scanner scanner = new Scanner(System.in);
        
        try {
            System.out.print("请输入一个数字: ");
            String input = "abc";  // 模拟输入
            int number = Integer.parseInt(input);
            int result = 100 / number;
            System.out.println("结果: " + result);
        } catch (NumberFormatException e) {
            System.out.println("输入格式错误: " + e.getMessage());
        } catch (ArithmeticException e) {
            System.out.println("算术错误: " + e.getMessage());
        } catch (Exception e) {
            System.out.println("其他异常: " + e.getMessage());
        }
    }
    
    public static void tryCatchFinally() {
        System.out.println("\n=== try-catch-finally ===");
        FileInputStream fis = null;
        try {
            fis = new FileInputStream("nonexistent.txt");
            System.out.println("文件打开成功");
        } catch (FileNotFoundException e) {
            System.out.println("文件未找到: " + e.getMessage());
        } finally {
            System.out.println("finally 块执行");
            if (fis != null) {
                try {
                    fis.close();
                    System.out.println("文件已关闭");
                } catch (IOException e) {
                    System.out.println("关闭文件时出错: " + e.getMessage());
                }
            }
        }
    }
    
    public static void finallyExecutionOrder() {
        System.out.println("\n=== finally 执行顺序 ===");
        System.out.println("返回值: " + testFinally());
    }
    
    public static int testFinally() {
        try {
            System.out.println("try 块执行");
            return 1;
        } catch (Exception e) {
            System.out.println("catch 块执行");
            return 2;
        } finally {
            System.out.println("finally 块执行");
            // 注意：finally 中的 return 会覆盖 try/catch 中的 return
            // return 3;  // 不推荐在 finally 中使用 return
        }
    }
}
```

### 2.2 try-with-resources 语句（Java 7+）

```java
import java.io.*;
import java.util.Scanner;

public class TryWithResourcesDemo {
    public static void main(String[] args) {
        // 传统方式
        traditionalWay();
        
        // try-with-resources 方式
        tryWithResources();
        
        // 多个资源
        multipleResources();
        
        // 自定义资源类
        customResource();
    }
    
    public static void traditionalWay() {
        System.out.println("=== 传统方式 ===");
        FileInputStream fis = null;
        BufferedReader reader = null;
        try {
            fis = new FileInputStream("test.txt");
            reader = new BufferedReader(new InputStreamReader(fis));
            String line = reader.readLine();
            System.out.println("读取内容: " + line);
        } catch (IOException e) {
            System.out.println("IO异常: " + e.getMessage());
        } finally {
            // 手动关闭资源
            if (reader != null) {
                try {
                    reader.close();
                } catch (IOException e) {
                    System.out.println("关闭 reader 失败");
                }
            }
            if (fis != null) {
                try {
                    fis.close();
                } catch (IOException e) {
                    System.out.println("关闭 fis 失败");
                }
            }
        }
    }
    
    public static void tryWithResources() {
        System.out.println("\n=== try-with-resources 方式 ===");
        // 资源会自动关闭
        try (FileInputStream fis = new FileInputStream("test.txt");
             BufferedReader reader = new BufferedReader(new InputStreamReader(fis))) {
            
            String line = reader.readLine();
            System.out.println("读取内容: " + line);
            
        } catch (IOException e) {
            System.out.println("IO异常: " + e.getMessage());
        }
        // 不需要 finally 块，资源自动关闭
    }
    
    public static void multipleResources() {
        System.out.println("\n=== 多个资源 ===");
        try (Scanner scanner = new Scanner(System.in);
             FileWriter writer = new FileWriter("output.txt")) {
            
            // 使用多个资源
            writer.write("Hello, World!");
            System.out.println("写入完成");
            
        } catch (IOException e) {
            System.out.println("IO异常: " + e.getMessage());
        }
    }
    
    public static void customResource() {
        System.out.println("\n=== 自定义资源类 ===");
        try (MyResource resource = new MyResource("测试资源")) {
            resource.doSomething();
        } catch (Exception e) {
            System.out.println("异常: " + e.getMessage());
        }
    }
}

// 自定义资源类，实现 AutoCloseable 接口
class MyResource implements AutoCloseable {
    private String name;
    
    public MyResource(String name) {
        this.name = name;
        System.out.println("资源 " + name + " 已创建");
    }
    
    public void doSomething() {
        System.out.println("使用资源 " + name);
    }
    
    @Override
    public void close() throws Exception {
        System.out.println("资源 " + name + " 已关闭");
    }
}
```

## 三、异常声明和抛出

### 3.1 throws 声明异常

```java
import java.io.*;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;

public class ThrowsDemo {
    public static void main(String[] args) {
        try {
            // 调用声明异常的方法
            readFile("test.txt");
            parseDate("2024-01-01");
            processData(null);
        } catch (IOException e) {
            System.out.println("IO异常: " + e.getMessage());
        } catch (ParseException e) {
            System.out.println("解析异常: " + e.getMessage());
        } catch (IllegalArgumentException e) {
            System.out.println("参数异常: " + e.getMessage());
        }
    }
    
    // 声明可能抛出的检查异常
    public static void readFile(String filename) throws IOException {
        FileReader reader = new FileReader(filename);
        // 读取文件内容
        reader.close();
    }
    
    // 声明多个异常
    public static Date parseDate(String dateStr) throws ParseException, IllegalArgumentException {
        if (dateStr == null || dateStr.trim().isEmpty()) {
            throw new IllegalArgumentException("日期字符串不能为空");
        }
        
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
        return sdf.parse(dateStr);
    }
    
    // 运行时异常不需要声明，但可以声明
    public static void processData(String data) throws IllegalArgumentException {
        if (data == null) {
            throw new IllegalArgumentException("数据不能为null");
        }
        System.out.println("处理数据: " + data);
    }
    
    // 方法重写时的异常声明规则
    public static void demonstrateOverrideRules() {
        // 子类重写方法时，不能声明比父类更多的检查异常
    }
}

// 演示方法重写时的异常规则
class Parent {
    public void method1() throws IOException {
        // 父类方法声明 IOException
    }
    
    public void method2() {
        // 父类方法不声明异常
    }
}

class Child extends Parent {
    @Override
    public void method1() throws FileNotFoundException {
        // 正确：FileNotFoundException 是 IOException 的子类
    }
    
    @Override
    public void method2() throws RuntimeException {
        // 正确：可以声明运行时异常
    }
    
    // 错误示例（编译错误）：
    // public void method2() throws IOException {
    //     // 错误：不能声明比父类更多的检查异常
    // }
}
```

### 3.2 throw 抛出异常

```java
public class ThrowDemo {
    public static void main(String[] args) {
        try {
            validateAge(150);
            divide(10, 0);
            processUser(null);
        } catch (IllegalArgumentException e) {
            System.out.println("参数异常: " + e.getMessage());
        } catch (ArithmeticException e) {
            System.out.println("算术异常: " + e.getMessage());
        } catch (NullPointerException e) {
            System.out.println("空指针异常: " + e.getMessage());
        }
    }
    
    // 抛出运行时异常
    public static void validateAge(int age) {
        if (age < 0 || age > 120) {
            throw new IllegalArgumentException("年龄必须在 0-120 之间，当前值: " + age);
        }
        System.out.println("年龄验证通过: " + age);
    }
    
    // 抛出算术异常
    public static int divide(int a, int b) {
        if (b == 0) {
            throw new ArithmeticException("除数不能为零");
        }
        return a / b;
    }
    
    // 抛出空指针异常
    public static void processUser(User user) {
        if (user == null) {
            throw new NullPointerException("用户对象不能为null");
        }
        System.out.println("处理用户: " + user.getName());
    }
    
    // 重新抛出异常
    public static void rethrowException() {
        try {
            riskyOperation();
        } catch (Exception e) {
            System.out.println("记录异常日志: " + e.getMessage());
            // 重新抛出异常
            throw e;
        }
    }
    
    public static void riskyOperation() {
        throw new RuntimeException("操作失败");
    }
}

class User {
    private String name;
    
    public User(String name) {
        this.name = name;
    }
    
    public String getName() {
        return name;
    }
}
```

## 四、自定义异常

### 4.1 创建自定义异常类

```java
// 自定义检查异常
class BusinessException extends Exception {
    private int errorCode;
    
    public BusinessException(String message) {
        super(message);
    }
    
    public BusinessException(String message, Throwable cause) {
        super(message, cause);
    }
    
    public BusinessException(int errorCode, String message) {
        super(message);
        this.errorCode = errorCode;
    }
    
    public BusinessException(int errorCode, String message, Throwable cause) {
        super(message, cause);
        this.errorCode = errorCode;
    }
    
    public int getErrorCode() {
        return errorCode;
    }
}

// 自定义运行时异常
class ValidationException extends RuntimeException {
    private String field;
    private Object value;
    
    public ValidationException(String field, Object value, String message) {
        super(String.format("字段 '%s' 的值 '%s' 验证失败: %s", field, value, message));
        this.field = field;
        this.value = value;
    }
    
    public String getField() {
        return field;
    }
    
    public Object getValue() {
        return value;
    }
}

// 具体的业务异常
class UserNotFoundException extends BusinessException {
    public UserNotFoundException(String userId) {
        super(1001, "用户不存在: " + userId);
    }
}

class InsufficientBalanceException extends BusinessException {
    private double currentBalance;
    private double requiredAmount;
    
    public InsufficientBalanceException(double currentBalance, double requiredAmount) {
        super(1002, String.format("余额不足，当前余额: %.2f，需要金额: %.2f", 
                                  currentBalance, requiredAmount));
        this.currentBalance = currentBalance;
        this.requiredAmount = requiredAmount;
    }
    
    public double getCurrentBalance() {
        return currentBalance;
    }
    
    public double getRequiredAmount() {
        return requiredAmount;
    }
}
```

### 4.2 使用自定义异常

```java
import java.util.HashMap;
import java.util.Map;

public class CustomExceptionDemo {
    private static Map<String, User> userDatabase = new HashMap<>();
    private static Map<String, Double> accountBalance = new HashMap<>();
    
    static {
        // 初始化测试数据
        userDatabase.put("user001", new User("张三"));
        userDatabase.put("user002", new User("李四"));
        accountBalance.put("user001", 1000.0);
        accountBalance.put("user002", 500.0);
    }
    
    public static void main(String[] args) {
        // 测试用户查找
        testUserLookup();
        
        // 测试转账操作
        testTransfer();
        
        // 测试数据验证
        testValidation();
    }
    
    public static void testUserLookup() {
        System.out.println("=== 测试用户查找 ===");
        try {
            User user = findUser("user001");
            System.out.println("找到用户: " + user.getName());
            
            User nonExistentUser = findUser("user999");
        } catch (UserNotFoundException e) {
            System.out.println("异常代码: " + e.getErrorCode());
            System.out.println("异常信息: " + e.getMessage());
        }
    }
    
    public static void testTransfer() {
        System.out.println("\n=== 测试转账操作 ===");
        try {
            transfer("user001", "user002", 500.0);
            System.out.println("转账成功");
            
            transfer("user002", "user001", 1000.0);  // 余额不足
        } catch (BusinessException e) {
            System.out.println("业务异常: " + e.getMessage());
            if (e instanceof InsufficientBalanceException) {
                InsufficientBalanceException ibe = (InsufficientBalanceException) e;
                System.out.println("当前余额: " + ibe.getCurrentBalance());
                System.out.println("需要金额: " + ibe.getRequiredAmount());
            }
        }
    }
    
    public static void testValidation() {
        System.out.println("\n=== 测试数据验证 ===");
        try {
            validateUser("张三", 25, "zhangsan@example.com");
            System.out.println("用户验证通过");
            
            validateUser("", -5, "invalid-email");  // 多个验证错误
        } catch (ValidationException e) {
            System.out.println("验证异常: " + e.getMessage());
            System.out.println("错误字段: " + e.getField());
            System.out.println("错误值: " + e.getValue());
        }
    }
    
    // 查找用户
    public static User findUser(String userId) throws UserNotFoundException {
        User user = userDatabase.get(userId);
        if (user == null) {
            throw new UserNotFoundException(userId);
        }
        return user;
    }
    
    // 转账操作
    public static void transfer(String fromUserId, String toUserId, double amount) 
            throws BusinessException {
        // 检查用户是否存在
        findUser(fromUserId);
        findUser(toUserId);
        
        // 检查余额
        double currentBalance = accountBalance.getOrDefault(fromUserId, 0.0);
        if (currentBalance < amount) {
            throw new InsufficientBalanceException(currentBalance, amount);
        }
        
        // 执行转账
        accountBalance.put(fromUserId, currentBalance - amount);
        accountBalance.put(toUserId, accountBalance.getOrDefault(toUserId, 0.0) + amount);
    }
    
    // 用户数据验证
    public static void validateUser(String name, int age, String email) {
        if (name == null || name.trim().isEmpty()) {
            throw new ValidationException("name", name, "姓名不能为空");
        }
        
        if (age < 0 || age > 120) {
            throw new ValidationException("age", age, "年龄必须在0-120之间");
        }
        
        if (email == null || !email.contains("@")) {
            throw new ValidationException("email", email, "邮箱格式不正确");
        }
    }
}
```

## 五、异常处理最佳实践

### 5.1 异常处理原则

```java
import java.io.*;
import java.util.logging.Logger;

public class ExceptionBestPracticesDemo {
    private static final Logger logger = Logger.getLogger(ExceptionBestPracticesDemo.class.getName());
    
    public static void main(String[] args) {
        // 1. 具体异常处理
        specificExceptionHandling();
        
        // 2. 异常信息记录
        exceptionLogging();
        
        // 3. 资源清理
        resourceCleanup();
        
        // 4. 异常转换
        exceptionTranslation();
    }
    
    // 1. 具体异常处理 - 好的做法
    public static void specificExceptionHandling() {
        System.out.println("=== 具体异常处理 ===");
        
        // 好的做法：捕获具体异常
        try {
            int[] array = {1, 2, 3};
            System.out.println(array[5]);
        } catch (ArrayIndexOutOfBoundsException e) {
            System.out.println("数组索引越界: " + e.getMessage());
            // 具体的处理逻辑
        }
        
        // 避免的做法：捕获过于宽泛的异常
        try {
            // 一些操作
        } catch (Exception e) {
            // 这样做会掩盖具体的异常类型
            System.out.println("发生异常: " + e.getMessage());
        }
    }
    
    // 2. 异常信息记录
    public static void exceptionLogging() {
        System.out.println("\n=== 异常信息记录 ===");
        
        try {
            riskyOperation();
        } catch (Exception e) {
            // 记录完整的异常信息
            logger.severe("操作失败: " + e.getMessage());
            
            // 打印堆栈跟踪（开发环境）
            e.printStackTrace();
            
            // 记录异常上下文信息
            System.out.println("异常发生时间: " + java.time.LocalDateTime.now());
            System.out.println("异常类型: " + e.getClass().getSimpleName());
            System.out.println("异常消息: " + e.getMessage());
        }
    }
    
    // 3. 资源清理
    public static void resourceCleanup() {
        System.out.println("\n=== 资源清理 ===");
        
        // 推荐：使用 try-with-resources
        try (FileInputStream fis = new FileInputStream("test.txt");
             BufferedReader reader = new BufferedReader(new InputStreamReader(fis))) {
            
            // 使用资源
            String line = reader.readLine();
            
        } catch (IOException e) {
            System.out.println("IO异常: " + e.getMessage());
        }
        // 资源自动关闭
    }
    
    // 4. 异常转换
    public static void exceptionTranslation() {
        System.out.println("\n=== 异常转换 ===");
        
        try {
            lowLevelOperation();
        } catch (IOException e) {
            // 将低级异常转换为业务异常
            throw new BusinessException("业务操作失败", e);
        }
    }
    
    public static void riskyOperation() {
        throw new RuntimeException("模拟异常");
    }
    
    public static void lowLevelOperation() throws IOException {
        throw new IOException("低级IO异常");
    }
}
```

### 5.2 异常处理反模式（应避免的做法）

```java
public class ExceptionAntiPatternsDemo {
    public static void main(String[] args) {
        // 演示应该避免的异常处理方式
        demonstrateAntiPatterns();
    }
    
    public static void demonstrateAntiPatterns() {
        System.out.println("=== 异常处理反模式 ===");
        
        // 反模式1：忽略异常
        badPattern1_IgnoreException();
        
        // 反模式2：捕获异常但不处理
        badPattern2_CatchAndIgnore();
        
        // 反模式3：过度使用异常
        badPattern3_OveruseException();
        
        // 反模式4：异常信息不明确
        badPattern4_VagueExceptionMessage();
    }
    
    // 反模式1：忽略异常（非常危险）
    public static void badPattern1_IgnoreException() {
        System.out.println("\n--- 反模式1：忽略异常 ---");
        
        // 错误做法：不处理可能的异常
        try {
            int result = Integer.parseInt("abc");
        } catch (NumberFormatException e) {
            // 什么都不做 - 这是危险的！
        }
        
        // 正确做法：至少记录异常
        try {
            int result = Integer.parseInt("abc");
        } catch (NumberFormatException e) {
            System.out.println("数字格式错误: " + e.getMessage());
            // 或者重新抛出异常
        }
    }
    
    // 反模式2：捕获异常但不处理
    public static void badPattern2_CatchAndIgnore() {
        System.out.println("\n--- 反模式2：捕获异常但不处理 ---");
        
        // 错误做法：捕获所有异常
        try {
            // 复杂的操作
            complexOperation();
        } catch (Exception e) {
            // 只是简单打印，没有具体处理
            System.out.println("出错了: " + e.getMessage());
        }
        
        // 正确做法：针对不同异常进行不同处理
        try {
            complexOperation();
        } catch (IllegalArgumentException e) {
            System.out.println("参数错误: " + e.getMessage());
            // 具体的参数错误处理
        } catch (RuntimeException e) {
            System.out.println("运行时错误: " + e.getMessage());
            // 具体的运行时错误处理
        }
    }
    
    // 反模式3：过度使用异常进行流程控制
    public static void badPattern3_OveruseException() {
        System.out.println("\n--- 反模式3：过度使用异常 ---");
        
        // 错误做法：使用异常控制正常流程
        try {
            for (int i = 0; ; i++) {
                System.out.println(getArrayElement(new int[]{1, 2, 3}, i));
            }
        } catch (ArrayIndexOutOfBoundsException e) {
            // 使用异常来结束循环 - 这是错误的！
            System.out.println("数组遍历结束");
        }
        
        // 正确做法：使用正常的流程控制
        int[] array = {1, 2, 3};
        for (int i = 0; i < array.length; i++) {
            System.out.println(array[i]);
        }
    }
    
    // 反模式4：异常信息不明确
    public static void badPattern4_VagueExceptionMessage() {
        System.out.println("\n--- 反模式4：异常信息不明确 ---");
        
        // 错误做法：异常信息不明确
        try {
            validateUserData("", -1);
        } catch (IllegalArgumentException e) {
            System.out.println("参数错误");  // 信息太模糊
        }
        
        // 正确做法：提供详细的异常信息
        try {
            validateUserDataCorrect("", -1);
        } catch (IllegalArgumentException e) {
            System.out.println("详细错误信息: " + e.getMessage());
        }
    }
    
    public static void complexOperation() {
        if (Math.random() > 0.5) {
            throw new IllegalArgumentException("随机参数错误");
        }
        throw new RuntimeException("随机运行时错误");
    }
    
    public static int getArrayElement(int[] array, int index) {
        return array[index];  // 可能抛出 ArrayIndexOutOfBoundsException
    }
    
    public static void validateUserData(String name, int age) {
        if (name.isEmpty()) {
            throw new IllegalArgumentException("错误");  // 信息不明确
        }
        if (age < 0) {
            throw new IllegalArgumentException("错误");  // 信息不明确
        }
    }
    
    public static void validateUserDataCorrect(String name, int age) {
        if (name.isEmpty()) {
            throw new IllegalArgumentException("用户名不能为空");
        }
        if (age < 0) {
            throw new IllegalArgumentException("年龄不能为负数，当前值: " + age);
        }
    }
}
```

### 5.3 Java 7+ 异常处理增强

```java
import java.io.*;
import java.sql.*;

public class Java7ExceptionEnhancementsDemo {
    public static void main(String[] args) {
        // 1. 多异常捕获
        multiCatchDemo();
        
        // 2. 重新抛出异常的类型推断
        rethrowDemo();
        
        // 3. try-with-resources 的抑制异常
        suppressedExceptionsDemo();
    }
    
    // 1. 多异常捕获（Java 7+）
    public static void multiCatchDemo() {
        System.out.println("=== 多异常捕获 ===");
        
        // Java 7 之前的写法
        try {
            riskyOperation();
        } catch (IOException e) {
            System.out.println("IO异常: " + e.getMessage());
            logException(e);
        } catch (SQLException e) {
            System.out.println("SQL异常: " + e.getMessage());
            logException(e);
        }
        
        // Java 7+ 的写法：多异常捕获
        try {
            riskyOperation();
        } catch (IOException | SQLException e) {
            System.out.println("IO或SQL异常: " + e.getMessage());
            logException(e);
            // 注意：e 是 final 的，不能重新赋值
        }
    }
    
    // 2. 重新抛出异常的类型推断（Java 7+）
    public static void rethrowDemo() throws IOException, SQLException {
        System.out.println("\n=== 重新抛出异常的类型推断 ===");
        
        try {
            riskyOperation();
        } catch (Exception e) {
            System.out.println("捕获异常: " + e.getClass().getSimpleName());
            // Java 7+ 可以推断出实际的异常类型
            throw e;  // 编译器知道这里只可能抛出 IOException 或 SQLException
        }
    }
    
    // 3. try-with-resources 的抑制异常
    public static void suppressedExceptionsDemo() {
        System.out.println("\n=== 抑制异常演示 ===");
        
        try (ProblematicResource resource = new ProblematicResource()) {
            resource.doSomething();
        } catch (Exception e) {
            System.out.println("主异常: " + e.getMessage());
            
            // 检查抑制的异常
            Throwable[] suppressed = e.getSuppressed();
            for (Throwable t : suppressed) {
                System.out.println("抑制异常: " + t.getMessage());
            }
        }
    }
    
    public static void riskyOperation() throws IOException, SQLException {
        double random = Math.random();
        if (random < 0.3) {
            throw new IOException("IO操作失败");
        } else if (random < 0.6) {
            throw new SQLException("数据库操作失败");
        }
        System.out.println("操作成功");
    }
    
    public static void logException(Exception e) {
        System.out.println("记录异常日志: " + e.getClass().getSimpleName());
    }
}

// 演示抑制异常的资源类
class ProblematicResource implements AutoCloseable {
    public void doSomething() throws Exception {
        throw new Exception("业务操作异常");
    }
    
    @Override
    public void close() throws Exception {
        throw new Exception("关闭资源异常");
    }
}
```

## 总结

Java 异常处理的核心要点：

1. **异常体系**：Error、RuntimeException、检查异常的区别
2. **处理语法**：try-catch-finally、try-with-resources
3. **异常声明**：throws 声明、throw 抛出
4. **自定义异常**：继承合适的异常类，提供有意义的信息
5. **最佳实践**：
   - 捕获具体异常而非 Exception
   - 提供有意义的异常信息
   - 正确清理资源
   - 不要忽略异常
   - 不要过度使用异常进行流程控制

> **设计原则**：异常应该用于处理真正的异常情况，而不是正常的程序流程控制。好的异常处理能够提高程序的健壮性和可维护性。