---
icon: material/code-braces
comments: true
---

# Java 基础语法

!!! note "本章内容"
    本章介绍 Java 的基础语法，包括变量、数据类型、运算符和控制流程等核心概念。

## 一、变量与数据类型

### 1.1 变量声明

在 Java 中，变量必须先声明后使用：

```java
// 声明变量
int age;
String name;

// 声明并初始化
int score = 85;
String message = "Hello World";
```

### 1.2 基本数据类型

Java 有 8 种基本数据类型：

| 类型 | 大小 | 范围 | 默认值 |
|------|------|------|--------|
| `byte` | 1字节 | -128 ~ 127 | 0 |
| `short` | 2字节 | -32,768 ~ 32,767 | 0 |
| `int` | 4字节 | -2^31 ~ 2^31-1 | 0 |
| `long` | 8字节 | -2^63 ~ 2^63-1 | 0L |
| `float` | 4字节 | IEEE 754 | 0.0f |
| `double` | 8字节 | IEEE 754 | 0.0d |
| `char` | 2字节 | 0 ~ 65,535 | '\u0000' |
| `boolean` | 1位 | true/false | false |

```java
// 基本数据类型示例
byte b = 100;
short s = 1000;
int i = 100000;
long l = 100000L;  // 注意L后缀

float f = 3.14f;   // 注意f后缀
double d = 3.14159;

char c = 'A';
boolean flag = true;
```

### 1.3 引用数据类型

除了基本数据类型，其他都是引用数据类型：

```java
// 字符串
String str = "Hello Java";

// 数组
int[] numbers = {1, 2, 3, 4, 5};

// 对象
Scanner scanner = new Scanner(System.in);
```

### 1.4 类型转换

#### 自动类型转换（隐式）

```java
// 小范围 → 大范围，自动转换
int i = 100;
long l = i;        // int → long
double d = l;      // long → double
```

#### 强制类型转换（显式）

```java
// 大范围 → 小范围，需要强制转换
double d = 3.14;
int i = (int) d;   // 结果：3（小数部分丢失）

// 注意精度丢失
long l = 123456789L;
int i2 = (int) l;  // 可能溢出
```

## 二、运算符

### 2.1 算术运算符

```java
int a = 10, b = 3;

System.out.println(a + b);  // 13 加法
System.out.println(a - b);  // 7  减法
System.out.println(a * b);  // 30 乘法
System.out.println(a / b);  // 3  除法（整数除法）
System.out.println(a % b);  // 1  取余

// 自增自减
int x = 5;
System.out.println(++x);    // 6 先自增再使用
System.out.println(x++);    // 6 先使用再自增
System.out.println(x);      // 7
```

### 2.2 关系运算符

```java
int a = 5, b = 3;

System.out.println(a > b);   // true
System.out.println(a < b);   // false
System.out.println(a >= b);  // true
System.out.println(a <= b);  // false
System.out.println(a == b);  // false
System.out.println(a != b);  // true
```

### 2.3 逻辑运算符

```java
boolean x = true, y = false;

System.out.println(x && y);  // false 逻辑与
System.out.println(x || y);  // true  逻辑或
System.out.println(!x);      // false 逻辑非

// 短路运算
int a = 5, b = 0;
if (b != 0 && a / b > 2) {   // b != 0 为 false，不会执行 a / b
    System.out.println("条件成立");
}
```

### 2.4 赋值运算符

```java
int a = 10;

a += 5;  // a = a + 5;  结果：15
a -= 3;  // a = a - 3;  结果：12
a *= 2;  // a = a * 2;  结果：24
a /= 4;  // a = a / 4;  结果：6
a %= 5;  // a = a % 5;  结果：1
```

### 2.5 三元运算符

```java
// 语法：条件 ? 值1 : 值2
int a = 10, b = 20;
int max = a > b ? a : b;  // 结果：20

String result = (score >= 60) ? "及格" : "不及格";
```

## 三、控制流程

### 3.1 条件语句

#### if 语句

```java
int score = 85;

// 单分支
if (score >= 60) {
    System.out.println("及格");
}

// 双分支
if (score >= 60) {
    System.out.println("及格");
} else {
    System.out.println("不及格");
}

// 多分支
if (score >= 90) {
    System.out.println("优秀");
} else if (score >= 80) {
    System.out.println("良好");
} else if (score >= 60) {
    System.out.println("及格");
} else {
    System.out.println("不及格");
}
```

#### switch 语句

```java
int dayOfWeek = 3;

switch (dayOfWeek) {
    case 1:
        System.out.println("星期一");
        break;
    case 2:
        System.out.println("星期二");
        break;
    case 3:
        System.out.println("星期三");
        break;
    case 4:
        System.out.println("星期四");
        break;
    case 5:
        System.out.println("星期五");
        break;
    case 6:
    case 7:
        System.out.println("周末");
        break;
    default:
        System.out.println("无效的日期");
}

// Java 14+ 新语法
String dayName = switch (dayOfWeek) {
    case 1 -> "星期一";
    case 2 -> "星期二";
    case 3 -> "星期三";
    case 4 -> "星期四";
    case 5 -> "星期五";
    case 6, 7 -> "周末";
    default -> "无效日期";
};
```

### 3.2 循环语句

#### for 循环

```java
// 基本 for 循环
for (int i = 1; i <= 5; i++) {
    System.out.println("第 " + i + " 次循环");
}

// 增强 for 循环（for-each）
int[] numbers = {1, 2, 3, 4, 5};
for (int num : numbers) {
    System.out.println(num);
}

// 嵌套循环
for (int i = 1; i <= 3; i++) {
    for (int j = 1; j <= 3; j++) {
        System.out.print("(" + i + "," + j + ") ");
    }
    System.out.println();
}
```

#### while 循环

```java
// while 循环
int i = 1;
while (i <= 5) {
    System.out.println("第 " + i + " 次循环");
    i++;
}

// do-while 循环
int j = 1;
do {
    System.out.println("第 " + j + " 次循环");
    j++;
} while (j <= 5);
```

### 3.3 跳转语句

#### break 和 continue

```java
// break：跳出循环
for (int i = 1; i <= 10; i++) {
    if (i == 5) {
        break;  // 跳出循环
    }
    System.out.println(i);  // 输出：1 2 3 4
}

// continue：跳过本次循环
for (int i = 1; i <= 5; i++) {
    if (i == 3) {
        continue;  // 跳过本次循环
    }
    System.out.println(i);  // 输出：1 2 4 5
}

// 标签跳转
outer: for (int i = 1; i <= 3; i++) {
    for (int j = 1; j <= 3; j++) {
        if (i == 2 && j == 2) {
            break outer;  // 跳出外层循环
        }
        System.out.println("i=" + i + ", j=" + j);
    }
}
```

## 四、输入输出

### 4.1 输出

```java
// 基本输出
System.out.print("不换行输出");
System.out.println("换行输出");

// 格式化输出
String name = "张三";
int age = 25;
double salary = 8500.5;

System.out.printf("姓名：%s，年龄：%d，工资：%.2f%n", name, age, salary);
// 输出：姓名：张三，年龄：25，工资：8500.50
```

### 4.2 输入

```java
import java.util.Scanner;

public class InputExample {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        
        System.out.print("请输入姓名：");
        String name = scanner.nextLine();
        
        System.out.print("请输入年龄：");
        int age = scanner.nextInt();
        
        System.out.print("请输入身高：");
        double height = scanner.nextDouble();
        
        System.out.println("姓名：" + name + "，年龄：" + age + "，身高：" + height);
        
        scanner.close();  // 关闭资源
    }
}
```

## 五、常见陷阱与注意事项

### 5.1 整数除法

```java
int a = 5, b = 2;
System.out.println(a / b);        // 2（整数除法）
System.out.println(5.0 / 2);      // 2.5（浮点除法）
System.out.println((double)a / b); // 2.5（强制转换）
```

### 5.2 浮点数比较

```java
// 错误的比较方式
double d1 = 0.1 + 0.2;
double d2 = 0.3;
System.out.println(d1 == d2);  // false！

// 正确的比较方式
double epsilon = 1e-10;
System.out.println(Math.abs(d1 - d2) < epsilon);  // true
```

### 5.3 字符串比较

```java
// 错误的比较方式
String s1 = "hello";
String s2 = "hello";
String s3 = new String("hello");

System.out.println(s1 == s2);     // true（字符串常量池）
System.out.println(s1 == s3);     // false（不同对象）

// 正确的比较方式
System.out.println(s1.equals(s3)); // true（内容相同）
```

### 5.4 Scanner 的 nextLine() 问题

```java
Scanner scanner = new Scanner(System.in);

System.out.print("输入数字：");
int num = scanner.nextInt();

System.out.print("输入字符串：");
scanner.nextLine();  // 消费换行符
String str = scanner.nextLine();
```

## 六、编程规范

### 6.1 命名规范

```java
// 类名：大驼峰命名法
class StudentManager { }

// 方法名和变量名：小驼峰命名法
int studentAge;
void calculateScore() { }

// 常量：全大写，下划线分隔
final int MAX_SIZE = 100;
final String DEFAULT_NAME = "Unknown";
```

### 6.2 代码风格

```java
// 良好的代码风格
public class Calculator {
    private static final double PI = 3.14159;
    
    public double calculateArea(double radius) {
        if (radius <= 0) {
            throw new IllegalArgumentException("半径必须大于0");
        }
        
        return PI * radius * radius;
    }
}
```

## 总结

Java 基础语法是学习 Java 编程的基石，主要包括：

1. **数据类型**：8种基本类型 + 引用类型
2. **运算符**：算术、关系、逻辑、赋值、三元
3. **控制流程**：if/switch 条件语句，for/while 循环语句
4. **输入输出**：System.out 输出，Scanner 输入

> **学习建议**：多练习编程，熟练掌握基础语法，为后续学习面向对象编程打下坚实基础。