---
icon: material/cube-send
comments: true
---

# 高级面向对象特性

!!! note "本章内容"
    本章介绍 Java 的高级面向对象特性：抽象类、接口、枚举、匿名内部类和 Java Bean 规范。

## 一、抽象类（Abstract Class）

### 1.1 抽象类的概念

抽象类是不能被实例化的类，通常包含一个或多个抽象方法：

```java
// 抽象类
public abstract class Animal {
    protected String name;
    protected int age;
    
    // 构造方法
    public Animal(String name, int age) {
        this.name = name;
        this.age = age;
    }
    
    // 抽象方法：子类必须实现
    public abstract void makeSound();
    public abstract void move();
    
    // 具体方法：子类可以直接使用
    public void eat() {
        System.out.println(name + "正在吃东西");
    }
    
    public void sleep() {
        System.out.println(name + "正在睡觉");
    }
    
    public void showInfo() {
        System.out.println("动物：" + name + "，年龄：" + age);
    }
}

// 具体子类必须实现所有抽象方法
public class Dog extends Animal {
    private String breed;
    
    public Dog(String name, int age, String breed) {
        super(name, age);
        this.breed = breed;
    }
    
    @Override
    public void makeSound() {
        System.out.println(name + "汪汪叫");
    }
    
    @Override
    public void move() {
        System.out.println(name + "在地上跑");
    }
    
    public void wagTail() {
        System.out.println(name + "摇尾巴");
    }
}

public class Bird extends Animal {
    private double wingspan;
    
    public Bird(String name, int age, double wingspan) {
        super(name, age);
        this.wingspan = wingspan;
    }
    
    @Override
    public void makeSound() {
        System.out.println(name + "叽叽喳喳");
    }
    
    @Override
    public void move() {
        System.out.println(name + "在天空飞翔，翼展：" + wingspan + "米");
    }
}
```

### 1.2 抽象类的特点

```java
public abstract class Shape {
    protected String color;
    protected static int count = 0;
    
    // 抽象类可以有构造方法
    public Shape(String color) {
        this.color = color;
        count++;
    }
    
    // 抽象类可以有静态方法
    public static int getCount() {
        return count;
    }
    
    // 抽象方法
    public abstract double calculateArea();
    public abstract double calculatePerimeter();
    
    // 具体方法
    public void displayInfo() {
        System.out.println("颜色：" + color + "，面积：" + calculateArea());
    }
    
    // 抽象类可以有 final 方法
    public final void printType() {
        System.out.println("这是一个几何图形");
    }
}
```

## 二、接口（Interface）

### 2.1 接口的基本概念

接口定义了类必须实现的方法规范：

```java
// 接口定义
public interface Drawable {
    // 接口中的变量默认是 public static final
    int MAX_SIZE = 1000;
    String DEFAULT_COLOR = "black";
    
    // 抽象方法（默认 public abstract）
    void draw();
    void erase();
    
    // Java 8+ 默认方法
    default void display() {
        System.out.println("显示图形");
    }
    
    // Java 8+ 静态方法
    static void printInfo() {
        System.out.println("这是一个可绘制的接口");
    }
    
    // Java 9+ 私有方法
    private void helper() {
        System.out.println("辅助方法");
    }
}

// 实现接口
public class Circle implements Drawable {
    private double radius;
    
    public Circle(double radius) {
        this.radius = radius;
    }
    
    @Override
    public void draw() {
        System.out.println("绘制半径为 " + radius + " 的圆形");
    }
    
    @Override
    public void erase() {
        System.out.println("擦除圆形");
    }
    
    // 可以重写默认方法
    @Override
    public void display() {
        System.out.println("显示圆形，半径：" + radius);
    }
}
```

### 2.2 多接口实现

```java
interface Flyable {
    void fly();
    
    default void takeOff() {
        System.out.println("起飞");
    }
}

interface Swimmable {
    void swim();
    
    default void dive() {
        System.out.println("潜水");
    }
}

// 一个类可以实现多个接口
public class Duck implements Flyable, Swimmable {
    private String name;
    
    public Duck(String name) {
        this.name = name;
    }
    
    @Override
    public void fly() {
        System.out.println(name + "在天空中飞翔");
    }
    
    @Override
    public void swim() {
        System.out.println(name + "在水中游泳");
    }
    
    // 如果多个接口有相同的默认方法，必须重写
    public void move() {
        System.out.println(name + "可以飞行和游泳");
    }
}
```

### 2.3 接口继承

```java
// 基础接口
interface Vehicle {
    void start();
    void stop();
}

// 接口可以继承接口
interface Car extends Vehicle {
    void drive();
    
    default void honk() {
        System.out.println("按喇叭");
    }
}

interface ElectricVehicle extends Vehicle {
    void charge();
    
    default void showBatteryLevel() {
        System.out.println("显示电量");
    }
}

// 接口可以继承多个接口
interface ElectricCar extends Car, ElectricVehicle {
    void enableAutoPilot();
}

// 实现类
public class Tesla implements ElectricCar {
    @Override
    public void start() {
        System.out.println("特斯拉启动");
    }
    
    @Override
    public void stop() {
        System.out.println("特斯拉停止");
    }
    
    @Override
    public void drive() {
        System.out.println("特斯拉行驶");
    }
    
    @Override
    public void charge() {
        System.out.println("特斯拉充电");
    }
    
    @Override
    public void enableAutoPilot() {
        System.out.println("启用自动驾驶");
    }
}
```

### 2.4 抽象类 vs 接口

| 特性 | 抽象类 | 接口 |
|------|--------|------|
| 关键字 | `abstract class` | `interface` |
| 继承 | 单继承 | 多实现 |
| 构造方法 | 可以有 | 不能有 |
| 成员变量 | 任意访问修饰符 | `public static final` |
| 方法类型 | 抽象方法 + 具体方法 | 抽象方法 + 默认方法 + 静态方法 |
| 实例化 | 不能直接实例化 | 不能实例化 |
| 使用场景 | 有共同实现的相关类 | 定义行为规范 |

```java
// 使用场景示例

// 抽象类：适用于有共同实现的相关类
abstract class DatabaseConnection {
    protected String url;
    protected String username;
    
    public DatabaseConnection(String url, String username) {
        this.url = url;
        this.username = username;
    }
    
    // 共同的连接逻辑
    public void connect() {
        System.out.println("连接到数据库：" + url);
    }
    
    // 不同数据库的具体实现
    public abstract void executeQuery(String sql);
}

// 接口：适用于定义行为规范
interface Serializable {
    void serialize();
    void deserialize();
}

interface Cacheable {
    void cache();
    void evict();
}
```

## 三、枚举（Enum）

### 3.1 基本枚举

```java
// 简单枚举
public enum Day {
    MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY
}

// 使用枚举
public class EnumDemo {
    public static void main(String[] args) {
        Day today = Day.MONDAY;
        
        System.out.println("今天是：" + today);
        System.out.println("序号：" + today.ordinal());
        System.out.println("名称：" + today.name());
        
        // 枚举比较
        if (today == Day.MONDAY) {
            System.out.println("今天是星期一");
        }
        
        // switch 语句
        switch (today) {
            case MONDAY:
                System.out.println("周一，新的开始");
                break;
            case FRIDAY:
                System.out.println("周五，快到周末了");
                break;
            case SATURDAY:
            case SUNDAY:
                System.out.println("周末，休息时间");
                break;
            default:
                System.out.println("工作日");
        }
        
        // 遍历所有枚举值
        for (Day day : Day.values()) {
            System.out.println(day + " (" + day.ordinal() + ")");
        }
    }
}
```

### 3.2 带属性和方法的枚举

```java
public enum Planet {
    // 枚举常量，带参数
    MERCURY(3.303e+23, 2.4397e6),
    VENUS(4.869e+24, 6.0518e6),
    EARTH(5.976e+24, 6.37814e6),
    MARS(6.421e+23, 3.3972e6);
    
    // 枚举属性
    private final double mass;   // 质量（千克）
    private final double radius; // 半径（米）
    
    // 枚举构造方法（必须是私有的）
    private Planet(double mass, double radius) {
        this.mass = mass;
        this.radius = radius;
    }
    
    // 枚举方法
    public double getMass() {
        return mass;
    }
    
    public double getRadius() {
        return radius;
    }
    
    // 计算表面重力
    public double surfaceGravity() {
        final double G = 6.67300E-11;
        return G * mass / (radius * radius);
    }
    
    // 计算在该星球上的重量
    public double surfaceWeight(double otherMass) {
        return otherMass * surfaceGravity();
    }
}

// 使用示例
public class PlanetDemo {
    public static void main(String[] args) {
        double earthWeight = 70.0; // 地球上的重量（千克）
        
        for (Planet planet : Planet.values()) {
            double weight = planet.surfaceWeight(earthWeight);
            System.out.printf("在 %s 上的重量：%.2f kg%n", planet, weight);
        }
    }
}
```

### 3.3 实现接口的枚举

```java
interface Operation {
    double apply(double x, double y);
}

public enum BasicOperation implements Operation {
    PLUS("+") {
        @Override
        public double apply(double x, double y) {
            return x + y;
        }
    },
    MINUS("-") {
        @Override
        public double apply(double x, double y) {
            return x - y;
        }
    },
    TIMES("*") {
        @Override
        public double apply(double x, double y) {
            return x * y;
        }
    },
    DIVIDE("/") {
        @Override
        public double apply(double x, double y) {
            return x / y;
        }
    };
    
    private final String symbol;
    
    private BasicOperation(String symbol) {
        this.symbol = symbol;
    }
    
    @Override
    public String toString() {
        return symbol;
    }
}

// 使用示例
public class OperationDemo {
    public static void main(String[] args) {
        double x = 10.0;
        double y = 3.0;
        
        for (BasicOperation op : BasicOperation.values()) {
            System.out.printf("%.1f %s %.1f = %.2f%n", x, op, y, op.apply(x, y));
        }
    }
}
```

## 四、内部类

### 4.1 成员内部类

```java
public class OuterClass {
    private String outerField = "外部类字段";
    private static String staticField = "静态字段";
    
    // 成员内部类
    public class InnerClass {
        private String innerField = "内部类字段";
        
        public void innerMethod() {
            // 内部类可以访问外部类的所有成员
            System.out.println("访问外部类字段：" + outerField);
            System.out.println("访问静态字段：" + staticField);
            System.out.println("内部类字段：" + innerField);
            
            // 调用外部类方法
            outerMethod();
        }
        
        public void accessOuter() {
            // 明确指定外部类实例
            System.out.println("外部类字段：" + OuterClass.this.outerField);
        }
    }
    
    public void outerMethod() {
        System.out.println("外部类方法");
        
        // 外部类访问内部类
        InnerClass inner = new InnerClass();
        inner.innerMethod();
    }
    
    public static void main(String[] args) {
        // 创建外部类实例
        OuterClass outer = new OuterClass();
        
        // 创建内部类实例
        OuterClass.InnerClass inner = outer.new InnerClass();
        inner.innerMethod();
    }
}
```

### 4.2 静态内部类

```java
public class OuterClass2 {
    private String outerField = "外部类字段";
    private static String staticField = "静态字段";
    
    // 静态内部类
    public static class StaticInnerClass {
        private String innerField = "静态内部类字段";
        
        public void innerMethod() {
            // 静态内部类只能访问外部类的静态成员
            System.out.println("访问静态字段：" + staticField);
            System.out.println("内部类字段：" + innerField);
            
            // System.out.println(outerField); // 编译错误
        }
        
        public void accessOuter(OuterClass2 outer) {
            // 通过外部类实例访问非静态成员
            System.out.println("外部类字段：" + outer.outerField);
        }
    }
    
    public static void main(String[] args) {
        // 直接创建静态内部类实例
        StaticInnerClass staticInner = new StaticInnerClass();
        staticInner.innerMethod();
        
        // 访问外部类非静态成员
        OuterClass2 outer = new OuterClass2();
        staticInner.accessOuter(outer);
    }
}
```

### 4.3 局部内部类

```java
public class LocalInnerClassDemo {
    private String outerField = "外部类字段";
    
    public void method() {
        final String localVar = "局部变量";
        int count = 10;
        
        // 局部内部类
        class LocalInnerClass {
            public void localMethod() {
                System.out.println("外部类字段：" + outerField);
                System.out.println("局部变量：" + localVar);
                System.out.println("count：" + count); // Java 8+ 可以访问 effectively final 变量
            }
        }
        
        // 在方法内使用局部内部类
        LocalInnerClass local = new LocalInnerClass();
        local.localMethod();
    }
    
    public static void main(String[] args) {
        LocalInnerClassDemo demo = new LocalInnerClassDemo();
        demo.method();
    }
}
```

### 4.4 匿名内部类

```java
interface Greeting {
    void sayHello(String name);
}

abstract class AbstractGreeting {
    public abstract void greet();
    
    public void commonMethod() {
        System.out.println("通用方法");
    }
}

public class AnonymousClassDemo {
    public static void main(String[] args) {
        // 匿名内部类实现接口
        Greeting greeting1 = new Greeting() {
            @Override
            public void sayHello(String name) {
                System.out.println("Hello, " + name + "!");
            }
        };
        greeting1.sayHello("张三");
        
        // 匿名内部类继承抽象类
        AbstractGreeting greeting2 = new AbstractGreeting() {
            @Override
            public void greet() {
                System.out.println("匿名类的问候");
            }
        };
        greeting2.greet();
        greeting2.commonMethod();
        
        // 匿名内部类继承具体类
        Thread thread = new Thread() {
            @Override
            public void run() {
                System.out.println("匿名线程运行");
            }
        };
        thread.start();
        
        // 使用 Lambda 表达式（Java 8+）
        Greeting greeting3 = name -> System.out.println("Hi, " + name + "!");
        greeting3.sayHello("李四");
    }
}
```

## 五、Java Bean 规范

### 5.1 标准 Java Bean

```java
import java.io.Serializable;

// 标准 Java Bean
public class Person implements Serializable {
    private static final long serialVersionUID = 1L;
    
    // 私有属性
    private String name;
    private int age;
    private String email;
    private boolean married;
    
    // 无参构造方法（必须）
    public Person() {
    }
    
    // 有参构造方法（可选）
    public Person(String name, int age, String email, boolean married) {
        this.name = name;
        this.age = age;
        this.email = email;
        this.married = married;
    }
    
    // getter 方法
    public String getName() {
        return name;
    }
    
    public int getAge() {
        return age;
    }
    
    public String getEmail() {
        return email;
    }
    
    // boolean 类型的 getter 方法可以用 is 开头
    public boolean isMarried() {
        return married;
    }
    
    // setter 方法
    public void setName(String name) {
        this.name = name;
    }
    
    public void setAge(int age) {
        if (age >= 0 && age <= 150) {
            this.age = age;
        }
    }
    
    public void setEmail(String email) {
        this.email = email;
    }
    
    public void setMarried(boolean married) {
        this.married = married;
    }
    
    // toString 方法（推荐）
    @Override
    public String toString() {
        return "Person{" +
                "name='" + name + '\'' +
                ", age=" + age +
                ", email='" + email + '\'' +
                ", married=" + married +
                '}';
    }
    
    // equals 和 hashCode 方法（推荐）
    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        
        Person person = (Person) obj;
        return age == person.age &&
               married == person.married &&
               name.equals(person.name) &&
               email.equals(person.email);
    }
    
    @Override
    public int hashCode() {
        int result = name.hashCode();
        result = 31 * result + age;
        result = 31 * result + email.hashCode();
        result = 31 * result + (married ? 1 : 0);
        return result;
    }
}
```

### 5.2 Java Bean 的使用

```java
import java.beans.*;
import java.lang.reflect.Method;

public class JavaBeanDemo {
    public static void main(String[] args) {
        // 创建 Java Bean 实例
        Person person = new Person();
        
        // 使用 setter 方法设置属性
        person.setName("张三");
        person.setAge(25);
        person.setEmail("zhangsan@example.com");
        person.setMarried(false);
        
        // 使用 getter 方法获取属性
        System.out.println("姓名：" + person.getName());
        System.out.println("年龄：" + person.getAge());
        System.out.println("邮箱：" + person.getEmail());
        System.out.println("已婚：" + person.isMarried());
        
        System.out.println(person);
        
        // 使用反射和内省 API
        try {
            BeanInfo beanInfo = Introspector.getBeanInfo(Person.class);
            PropertyDescriptor[] properties = beanInfo.getPropertyDescriptors();
            
            System.out.println("\nBean 属性：");
            for (PropertyDescriptor property : properties) {
                String name = property.getName();
                if (!"class".equals(name)) {  // 排除 class 属性
                    Method readMethod = property.getReadMethod();
                    if (readMethod != null) {
                        Object value = readMethod.invoke(person);
                        System.out.println(name + ": " + value);
                    }
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

### 5.3 Java Bean 规范总结

1. **类必须是公共的**：使用 `public` 修饰符
2. **必须有无参构造方法**：用于框架实例化
3. **属性必须是私有的**：使用 `private` 修饰符
4. **提供 getter 和 setter 方法**：遵循命名规范
5. **实现 Serializable 接口**：支持序列化
6. **重写 toString、equals、hashCode**：提供完整的对象行为

```java
// 命名规范示例
public class NamingConventionExample {
    private String firstName;     // getter: getFirstName(), setter: setFirstName()
    private boolean active;       // getter: isActive(), setter: setActive()
    private int age;             // getter: getAge(), setter: setAge()
    private double salary;       // getter: getSalary(), setter: setSalary()
    
    // 正确的命名
    public String getFirstName() { return firstName; }
    public void setFirstName(String firstName) { this.firstName = firstName; }
    
    public boolean isActive() { return active; }
    public void setActive(boolean active) { this.active = active; }
    
    public int getAge() { return age; }
    public void setAge(int age) { this.age = age; }
    
    public double getSalary() { return salary; }
    public void setSalary(double salary) { this.salary = salary; }
}
```

## 六、作用域和静态上下文

### 6.1 变量作用域

```java
public class ScopeDemo {
    // 类变量（静态变量）
    private static int classVar = 1;
    
    // 实例变量
    private int instanceVar = 2;
    
    public void method(int paramVar) {  // 参数变量
        int localVar = 4;  // 局部变量
        
        System.out.println("类变量：" + classVar);
        System.out.println("实例变量：" + instanceVar);
        System.out.println("参数变量：" + paramVar);
        System.out.println("局部变量：" + localVar);
        
        // 作用域范围：局部变量 > 参数变量 > 实例变量 > 类变量
        
        if (true) {
            int blockVar = 5;  // 块级变量
            System.out.println("块级变量：" + blockVar);
        }
        // System.out.println(blockVar);  // 编译错误：超出作用域
    }
    
    public static void staticMethod() {
        System.out.println("类变量：" + classVar);
        // System.out.println(instanceVar);  // 编译错误：静态方法不能访问实例变量
    }
}
```

### 6.2 静态上下文限制

```java
public class StaticContextDemo {
    private String instanceField = "实例字段";
    private static String staticField = "静态字段";
    
    public void instanceMethod() {
        System.out.println("实例方法");
    }
    
    public static void staticMethod() {
        System.out.println("静态方法");
    }
    
    // 静态方法的限制
    public static void restrictedStaticMethod() {
        // 1. 不能直接访问实例变量
        // System.out.println(instanceField);  // 编译错误
        
        // 2. 不能直接调用实例方法
        // instanceMethod();  // 编译错误
        
        // 3. 不能使用 this 和 super 关键字
        // System.out.println(this.staticField);  // 编译错误
        
        // 4. 可以访问静态成员
        System.out.println(staticField);  // 正确
        staticMethod();  // 正确
        
        // 5. 可以通过对象实例访问实例成员
        StaticContextDemo obj = new StaticContextDemo();
        System.out.println(obj.instanceField);  // 正确
        obj.instanceMethod();  // 正确
    }
    
    // 静态代码块的限制
    static {
        System.out.println("静态代码块");
        System.out.println(staticField);  // 可以访问静态字段
        staticMethod();  // 可以调用静态方法
        
        // System.out.println(instanceField);  // 编译错误
        // instanceMethod();  // 编译错误
    }
}
```

## 总结

高级面向对象特性的核心要点：

1. **抽象类**：部分实现的类，用于代码复用和规范定义
2. **接口**：行为规范的定义，支持多实现
3. **枚举**：类型安全的常量集合，可以有属性和方法
4. **内部类**：类的嵌套定义，提供更好的封装性
5. **Java Bean**：遵循特定规范的类，便于框架使用
6. **作用域**：变量的可见性范围，静态上下文的限制

> **设计建议**：合理使用这些特性可以提高代码的可读性、可维护性和可扩展性。