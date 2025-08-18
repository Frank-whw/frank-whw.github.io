---
icon: material/cube-outline
comments: true
---

# 面向对象编程

!!! note "本章内容"
    本章介绍 Java 面向对象编程的核心概念：类与对象、继承、多态、封装，以及访问修饰符和 final 关键字。

## 一、类与对象

### 1.1 类的定义

类是对象的模板，定义了对象的属性和行为：

```java
public class Student {
    // 属性（成员变量）
    private String name;
    private int age;
    private double score;
    
    // 构造方法
    public Student() {
        // 无参构造方法
    }
    
    public Student(String name, int age, double score) {
        this.name = name;
        this.age = age;
        this.score = score;
    }
    
    // 方法（成员方法）
    public void study() {
        System.out.println(name + "正在学习");
    }
    
    public void showInfo() {
        System.out.println("姓名：" + name + "，年龄：" + age + "，成绩：" + score);
    }
    
    // getter 和 setter 方法
    public String getName() {
        return name;
    }
    
    public void setName(String name) {
        this.name = name;
    }
    
    public int getAge() {
        return age;
    }
    
    public void setAge(int age) {
        if (age > 0 && age < 150) {
            this.age = age;
        }
    }
    
    public double getScore() {
        return score;
    }
    
    public void setScore(double score) {
        if (score >= 0 && score <= 100) {
            this.score = score;
        }
    }
}
```

### 1.2 对象的创建和使用

```java
public class TestStudent {
    public static void main(String[] args) {
        // 创建对象
        Student student1 = new Student();
        Student student2 = new Student("张三", 20, 85.5);
        
        // 使用对象
        student1.setName("李四");
        student1.setAge(19);
        student1.setScore(92.0);
        
        student1.showInfo();
        student1.study();
        
        student2.showInfo();
        student2.study();
    }
}
```

### 1.3 this 关键字

`this` 关键字代表当前对象的引用：

```java
public class Person {
    private String name;
    private int age;
    
    public Person(String name, int age) {
        this.name = name;  // this.name 指当前对象的 name 属性
        this.age = age;    // this.age 指当前对象的 age 属性
    }
    
    public void setName(String name) {
        this.name = name;  // 区分参数 name 和属性 name
    }
    
    public Person getOlder(Person other) {
        return this.age > other.age ? this : other;
    }
    
    public void introduce() {
        System.out.println("我是 " + this.name);  // this 可以省略
        this.showAge();  // 调用当前对象的方法
    }
    
    private void showAge() {
        System.out.println("我今年 " + age + " 岁");
    }
}
```

## 二、封装（Encapsulation）

### 2.1 封装的概念

封装是将数据和操作数据的方法绑定在一起，并隐藏内部实现细节：

```java
public class BankAccount {
    private double balance;  // 私有属性，外部无法直接访问
    private String accountNumber;
    
    public BankAccount(String accountNumber, double initialBalance) {
        this.accountNumber = accountNumber;
        this.balance = initialBalance;
    }
    
    // 提供公共方法来操作私有数据
    public void deposit(double amount) {
        if (amount > 0) {
            balance += amount;
            System.out.println("存款成功，余额：" + balance);
        } else {
            System.out.println("存款金额必须大于0");
        }
    }
    
    public void withdraw(double amount) {
        if (amount > 0 && amount <= balance) {
            balance -= amount;
            System.out.println("取款成功，余额：" + balance);
        } else {
            System.out.println("取款失败：金额无效或余额不足");
        }
    }
    
    public double getBalance() {
        return balance;  // 只读访问
    }
    
    public String getAccountNumber() {
        return accountNumber;
    }
}
```

### 2.2 访问修饰符

| 修饰符 | 同一类 | 同一包 | 不同包子类 | 不同包非子类 |
|--------|--------|--------|------------|-------------|
| `private` | ✓ | ✗ | ✗ | ✗ |
| 默认（包访问） | ✓ | ✓ | ✗ | ✗ |
| `protected` | ✓ | ✓ | ✓ | ✗ |
| `public` | ✓ | ✓ | ✓ | ✓ |

```java
public class AccessExample {
    private int privateField = 1;      // 只能在本类中访问
    int packageField = 2;              // 包访问权限
    protected int protectedField = 3;   // 受保护访问权限
    public int publicField = 4;        // 公共访问权限
    
    private void privateMethod() {
        System.out.println("私有方法");
    }
    
    void packageMethod() {
        System.out.println("包访问方法");
    }
    
    protected void protectedMethod() {
        System.out.println("受保护方法");
    }
    
    public void publicMethod() {
        System.out.println("公共方法");
        privateMethod();  // 在同一类中可以访问私有方法
    }
}
```

## 三、继承（Inheritance）

### 3.1 继承的基本概念

继承允许一个类获得另一个类的属性和方法：

```java
// 父类（基类、超类）
public class Animal {
    protected String name;
    protected int age;
    
    public Animal(String name, int age) {
        this.name = name;
        this.age = age;
    }
    
    public void eat() {
        System.out.println(name + "正在吃东西");
    }
    
    public void sleep() {
        System.out.println(name + "正在睡觉");
    }
    
    public void showInfo() {
        System.out.println("名字：" + name + "，年龄：" + age);
    }
}

// 子类（派生类）
public class Dog extends Animal {
    private String breed;  // 子类特有属性
    
    public Dog(String name, int age, String breed) {
        super(name, age);  // 调用父类构造方法
        this.breed = breed;
    }
    
    // 子类特有方法
    public void bark() {
        System.out.println(name + "正在汪汪叫");
    }
    
    // 重写父类方法
    @Override
    public void showInfo() {
        super.showInfo();  // 调用父类方法
        System.out.println("品种：" + breed);
    }
}

// 另一个子类
public class Cat extends Animal {
    public Cat(String name, int age) {
        super(name, age);
    }
    
    public void meow() {
        System.out.println(name + "正在喵喵叫");
    }
    
    @Override
    public void eat() {
        System.out.println(name + "正在优雅地吃猫粮");
    }
}
```

### 3.2 super 关键字

`super` 关键字用于访问父类的成员：

```java
public class Vehicle {
    protected String brand;
    protected double speed;
    
    public Vehicle(String brand) {
        this.brand = brand;
        this.speed = 0;
    }
    
    public void start() {
        System.out.println(brand + "启动了");
    }
    
    public void accelerate(double increment) {
        speed += increment;
        System.out.println("当前速度：" + speed + " km/h");
    }
}

public class Car extends Vehicle {
    private int doors;
    
    public Car(String brand, int doors) {
        super(brand);  // 调用父类构造方法
        this.doors = doors;
    }
    
    @Override
    public void start() {
        super.start();  // 调用父类的 start 方法
        System.out.println("汽车准备就绪");
    }
    
    @Override
    public void accelerate(double increment) {
        if (speed + increment <= 200) {  // 汽车限速
            super.accelerate(increment);  // 调用父类方法
        } else {
            System.out.println("超速警告！");
        }
    }
}
```

### 3.3 方法重写（Override）

子类可以重写父类的方法来提供特定的实现：

```java
public class Shape {
    protected double area;
    
    public void calculateArea() {
        System.out.println("计算图形面积");
    }
    
    public void display() {
        System.out.println("这是一个图形，面积：" + area);
    }
}

public class Circle extends Shape {
    private double radius;
    
    public Circle(double radius) {
        this.radius = radius;
    }
    
    @Override  // 注解，表示这是重写的方法
    public void calculateArea() {
        area = Math.PI * radius * radius;
        System.out.println("计算圆形面积");
    }
    
    @Override
    public void display() {
        System.out.println("这是一个圆形，半径：" + radius + "，面积：" + area);
    }
}

public class Rectangle extends Shape {
    private double width;
    private double height;
    
    public Rectangle(double width, double height) {
        this.width = width;
        this.height = height;
    }
    
    @Override
    public void calculateArea() {
        area = width * height;
        System.out.println("计算矩形面积");
    }
    
    @Override
    public void display() {
        System.out.println("这是一个矩形，宽：" + width + "，高：" + height + "，面积：" + area);
    }
}
```

## 四、多态（Polymorphism）

### 4.1 多态的概念

多态允许不同类的对象对同一消息做出不同的响应：

```java
public class PolymorphismDemo {
    public static void main(String[] args) {
        // 多态：父类引用指向子类对象
        Animal animal1 = new Dog("旺财", 3, "金毛");
        Animal animal2 = new Cat("咪咪", 2);
        
        // 调用重写的方法，表现出不同的行为
        animal1.eat();  // 输出：旺财正在吃东西
        animal2.eat();  // 输出：咪咪正在优雅地吃猫粮
        
        // 多态数组
        Animal[] animals = {
            new Dog("小黑", 2, "拉布拉多"),
            new Cat("小白", 1),
            new Dog("大黄", 4, "土狗")
        };
        
        // 统一处理不同类型的对象
        for (Animal animal : animals) {
            animal.showInfo();
            animal.eat();
            System.out.println("---");
        }
    }
}
```

### 4.2 instanceof 运算符

用于检查对象是否是特定类的实例：

```java
public class InstanceofDemo {
    public static void processAnimal(Animal animal) {
        animal.eat();  // 多态调用
        
        // 类型检查和向下转型
        if (animal instanceof Dog) {
            Dog dog = (Dog) animal;  // 向下转型
            dog.bark();  // 调用子类特有方法
        } else if (animal instanceof Cat) {
            Cat cat = (Cat) animal;
            cat.meow();
        }
    }
    
    public static void main(String[] args) {
        processAnimal(new Dog("旺财", 3, "金毛"));
        processAnimal(new Cat("咪咪", 2));
    }
}
```

### 4.3 抽象方法和抽象类

```java
// 抽象类
public abstract class Employee {
    protected String name;
    protected double baseSalary;
    
    public Employee(String name, double baseSalary) {
        this.name = name;
        this.baseSalary = baseSalary;
    }
    
    // 抽象方法，子类必须实现
    public abstract double calculateSalary();
    
    // 具体方法
    public void showInfo() {
        System.out.println("员工：" + name + "，工资：" + calculateSalary());
    }
}

// 具体子类
public class FullTimeEmployee extends Employee {
    private double bonus;
    
    public FullTimeEmployee(String name, double baseSalary, double bonus) {
        super(name, baseSalary);
        this.bonus = bonus;
    }
    
    @Override
    public double calculateSalary() {
        return baseSalary + bonus;
    }
}

public class PartTimeEmployee extends Employee {
    private int hoursWorked;
    private double hourlyRate;
    
    public PartTimeEmployee(String name, int hoursWorked, double hourlyRate) {
        super(name, 0);  // 兼职员工没有基本工资
        this.hoursWorked = hoursWorked;
        this.hourlyRate = hourlyRate;
    }
    
    @Override
    public double calculateSalary() {
        return hoursWorked * hourlyRate;
    }
}
```

## 五、final 关键字

### 5.1 final 变量

```java
public class FinalVariableDemo {
    // final 实例变量必须初始化
    private final String name = "张三";
    private final int id;
    
    // final 静态变量（常量）
    public static final double PI = 3.14159;
    public static final String COMPANY_NAME = "ABC公司";
    
    public FinalVariableDemo(int id) {
        this.id = id;  // 在构造方法中初始化 final 变量
    }
    
    public void method() {
        final int localVar = 100;  // final 局部变量
        // localVar = 200;  // 编译错误：无法修改 final 变量
        
        System.out.println("ID: " + id + ", Name: " + name);
    }
}
```

### 5.2 final 方法

```java
public class Parent {
    // final 方法不能被重写
    public final void finalMethod() {
        System.out.println("这是一个 final 方法");
    }
    
    public void normalMethod() {
        System.out.println("这是一个普通方法");
    }
}

public class Child extends Parent {
    // @Override
    // public void finalMethod() {  // 编译错误：无法重写 final 方法
    //     System.out.println("尝试重写 final 方法");
    // }
    
    @Override
    public void normalMethod() {
        System.out.println("重写普通方法");
    }
}
```

### 5.3 final 类

```java
// final 类不能被继承
public final class FinalClass {
    public void method() {
        System.out.println("final 类的方法");
    }
}

// public class SubClass extends FinalClass {  // 编译错误：无法继承 final 类
// }

// Java 中的 final 类示例
// String、Integer、Double 等包装类都是 final 类
String str = "Hello";  // String 是 final 类
Integer num = 100;     // Integer 是 final 类
```

## 六、对象的生命周期

### 6.1 对象的创建过程

```java
public class ObjectLifecycle {
    private String name;
    private static int count = 0;
    
    // 静态代码块：类加载时执行
    static {
        System.out.println("静态代码块执行");
    }
    
    // 实例代码块：每次创建对象时执行
    {
        System.out.println("实例代码块执行");
        count++;
    }
    
    // 构造方法
    public ObjectLifecycle(String name) {
        System.out.println("构造方法执行");
        this.name = name;
    }
    
    public static int getCount() {
        return count;
    }
}

// 执行顺序：静态代码块 → 实例代码块 → 构造方法
```

### 6.2 垃圾回收

```java
public class GarbageCollectionDemo {
    private String name;
    
    public GarbageCollectionDemo(String name) {
        this.name = name;
    }
    
    // finalize 方法（不推荐使用）
    @Override
    protected void finalize() throws Throwable {
        System.out.println(name + " 对象被回收");
        super.finalize();
    }
    
    public static void main(String[] args) {
        GarbageCollectionDemo obj1 = new GarbageCollectionDemo("对象1");
        GarbageCollectionDemo obj2 = new GarbageCollectionDemo("对象2");
        
        obj1 = null;  // 取消引用
        obj2 = null;
        
        System.gc();  // 建议进行垃圾回收（不保证立即执行）
        
        try {
            Thread.sleep(1000);  // 等待垃圾回收
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}
```

## 七、设计原则

### 7.1 单一职责原则

```java
// 不好的设计：一个类承担多个职责
class BadEmployee {
    private String name;
    private double salary;
    
    public void calculateSalary() { /* 计算工资 */ }
    public void saveToDatabase() { /* 保存到数据库 */ }
    public void sendEmail() { /* 发送邮件 */ }
}

// 好的设计：职责分离
class Employee {
    private String name;
    private double salary;
    
    public void calculateSalary() { /* 只负责计算工资 */ }
    // getter 和 setter 方法
}

class EmployeeDAO {
    public void save(Employee employee) { /* 负责数据持久化 */ }
}

class EmailService {
    public void sendEmail(Employee employee) { /* 负责发送邮件 */ }
}
```

### 7.2 开闭原则

```java
// 对扩展开放，对修改关闭
abstract class Shape {
    public abstract double calculateArea();
}

class Circle extends Shape {
    private double radius;
    
    public Circle(double radius) {
        this.radius = radius;
    }
    
    @Override
    public double calculateArea() {
        return Math.PI * radius * radius;
    }
}

class Rectangle extends Shape {
    private double width, height;
    
    public Rectangle(double width, double height) {
        this.width = width;
        this.height = height;
    }
    
    @Override
    public double calculateArea() {
        return width * height;
    }
}

// 添加新图形时，不需要修改现有代码
class Triangle extends Shape {
    private double base, height;
    
    public Triangle(double base, double height) {
        this.base = base;
        this.height = height;
    }
    
    @Override
    public double calculateArea() {
        return 0.5 * base * height;
    }
}
```

## 总结

面向对象编程的核心概念：

1. **封装**：隐藏内部实现，提供公共接口
2. **继承**：代码复用，建立类之间的层次关系
3. **多态**：同一接口，不同实现，提高代码灵活性
4. **抽象**：提取共同特征，定义规范

> **设计原则**：高内聚、低耦合，遵循 SOLID 原则，编写可维护、可扩展的代码。