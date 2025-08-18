---
icon: material/library
comments: true
---

# Java 核心类库

!!! note "本章内容"
    本章介绍 Java 的核心类库：Object 类、String 类、包装类、日期时间类和 Arrays 工具类。

## 一、Object 类

### 1.1 Object 类概述

Object 类是所有 Java 类的根父类，位于 `java.lang` 包中：

```java
public class ObjectDemo {
    public static void main(String[] args) {
        // 所有类都隐式继承 Object
        String str = "Hello";
        Integer num = 42;
        int[] arr = {1, 2, 3};
        
        // 都可以调用 Object 的方法
        System.out.println(str.toString());
        System.out.println(num.hashCode());
        System.out.println(arr.getClass());
    }
}
```

### 1.2 Object 类的重要方法

```java
public class Person {
    private String name;
    private int age;
    
    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }
    
    // 重写 toString() 方法
    @Override
    public String toString() {
        return "Person{name='" + name + "', age=" + age + "}";
    }
    
    // 重写 equals() 方法
    @Override
    public boolean equals(Object obj) {
        // 1. 检查是否是同一个对象
        if (this == obj) {
            return true;
        }
        
        // 2. 检查是否为 null
        if (obj == null) {
            return false;
        }
        
        // 3. 检查类型是否相同
        if (getClass() != obj.getClass()) {
            return false;
        }
        
        // 4. 强制类型转换并比较属性
        Person person = (Person) obj;
        return age == person.age && 
               (name != null ? name.equals(person.name) : person.name == null);
    }
    
    // 重写 hashCode() 方法
    @Override
    public int hashCode() {
        int result = name != null ? name.hashCode() : 0;
        result = 31 * result + age;
        return result;
    }
    
    // getter 方法
    public String getName() { return name; }
    public int getAge() { return age; }
}

// 使用示例
public class ObjectMethodsDemo {
    public static void main(String[] args) {
        Person p1 = new Person("张三", 25);
        Person p2 = new Person("张三", 25);
        Person p3 = new Person("李四", 30);
        
        // toString() 方法
        System.out.println("p1: " + p1.toString());
        System.out.println("p1: " + p1);  // 自动调用 toString()
        
        // equals() 方法
        System.out.println("p1.equals(p2): " + p1.equals(p2));  // true
        System.out.println("p1.equals(p3): " + p1.equals(p3));  // false
        System.out.println("p1 == p2: " + (p1 == p2));          // false
        
        // hashCode() 方法
        System.out.println("p1.hashCode(): " + p1.hashCode());
        System.out.println("p2.hashCode(): " + p2.hashCode());
        System.out.println("p3.hashCode(): " + p3.hashCode());
        
        // getClass() 方法
        System.out.println("p1.getClass(): " + p1.getClass());
        System.out.println("p1.getClass().getName(): " + p1.getClass().getName());
        System.out.println("p1.getClass().getSimpleName(): " + p1.getClass().getSimpleName());
    }
}
```

### 1.3 Object 类的其他方法

```java
public class ObjectOtherMethodsDemo {
    public static void main(String[] args) throws CloneNotSupportedException {
        // clone() 方法示例
        CloneableExample original = new CloneableExample("原始对象", 100);
        CloneableExample cloned = (CloneableExample) original.clone();
        
        System.out.println("原始对象: " + original);
        System.out.println("克隆对象: " + cloned);
        System.out.println("是否为同一对象: " + (original == cloned));
        
        // finalize() 方法（已废弃，不推荐使用）
        // 由垃圾回收器调用，用于清理资源
        
        // wait(), notify(), notifyAll() 方法
        // 用于线程间通信，在同步代码块中使用
    }
}

// 实现 Cloneable 接口的示例
class CloneableExample implements Cloneable {
    private String name;
    private int value;
    
    public CloneableExample(String name, int value) {
        this.name = name;
        this.value = value;
    }
    
    @Override
    protected Object clone() throws CloneNotSupportedException {
        return super.clone();  // 浅拷贝
    }
    
    @Override
    public String toString() {
        return "CloneableExample{name='" + name + "', value=" + value + "}";
    }
}
```

## 二、String 类

### 2.1 String 类的特性

```java
public class StringBasicsDemo {
    public static void main(String[] args) {
        // String 的不可变性
        String str1 = "Hello";
        String str2 = str1;
        str1 = str1 + " World";  // 创建新的 String 对象
        
        System.out.println("str1: " + str1);  // "Hello World"
        System.out.println("str2: " + str2);  // "Hello"
        
        // 字符串字面量池
        String s1 = "Java";
        String s2 = "Java";
        String s3 = new String("Java");
        
        System.out.println("s1 == s2: " + (s1 == s2));        // true（同一对象）
        System.out.println("s1 == s3: " + (s1 == s3));        // false（不同对象）
        System.out.println("s1.equals(s3): " + s1.equals(s3)); // true（内容相同）
        
        // intern() 方法
        String s4 = s3.intern();
        System.out.println("s1 == s4: " + (s1 == s4));        // true
    }
}
```

### 2.2 String 类的常用方法

```java
public class StringMethodsDemo {
    public static void main(String[] args) {
        String str = "  Hello Java World  ";
        
        // 长度和字符访问
        System.out.println("长度: " + str.length());
        System.out.println("第6个字符: " + str.charAt(6));
        
        // 大小写转换
        System.out.println("大写: " + str.toUpperCase());
        System.out.println("小写: " + str.toLowerCase());
        
        // 去除空白
        System.out.println("去除首尾空白: '" + str.trim() + "'");
        System.out.println("去除所有空白: '" + str.strip() + "'");  // Java 11+
        
        // 查找和判断
        System.out.println("包含 'Java': " + str.contains("Java"));
        System.out.println("以 '  Hello' 开头: " + str.startsWith("  Hello"));
        System.out.println("以 'World  ' 结尾: " + str.endsWith("World  "));
        System.out.println("'Java' 的位置: " + str.indexOf("Java"));
        System.out.println("最后一个 'o' 的位置: " + str.lastIndexOf("o"));
        
        // 字符串截取
        System.out.println("从索引7开始: '" + str.substring(7) + "'");
        System.out.println("索引7到12: '" + str.substring(7, 12) + "'");
        
        // 字符串替换
        System.out.println("替换 'Java' 为 'Python': " + str.replace("Java", "Python"));
        System.out.println("替换所有空格: " + str.replaceAll("\\s+", "-"));
        
        // 字符串分割
        String[] words = str.trim().split(" ");
        System.out.println("分割结果: " + java.util.Arrays.toString(words));
        
        // 字符串比较
        String str2 = "hello java world";
        System.out.println("忽略大小写比较: " + str.trim().equalsIgnoreCase(str2));
        System.out.println("字典序比较: " + str.trim().compareTo(str2));
        
        // 字符串格式化
        String formatted = String.format("姓名: %s, 年龄: %d, 分数: %.2f", "张三", 25, 89.567);
        System.out.println("格式化字符串: " + formatted);
    }
}
```

### 2.3 StringBuilder 和 StringBuffer

```java
public class StringBuilderDemo {
    public static void main(String[] args) {
        // StringBuilder（非线程安全，性能更好）
        StringBuilder sb = new StringBuilder();
        sb.append("Hello");
        sb.append(" ");
        sb.append("World");
        sb.insert(5, " Java");
        sb.delete(11, 17);  // 删除 " World"
        
        System.out.println("StringBuilder 结果: " + sb.toString());
        System.out.println("长度: " + sb.length());
        System.out.println("容量: " + sb.capacity());
        
        // 链式调用
        StringBuilder sb2 = new StringBuilder()
            .append("Java")
            .append(" is")
            .append(" awesome!");
        System.out.println("链式调用结果: " + sb2);
        
        // StringBuffer（线程安全）
        StringBuffer sbf = new StringBuffer("Thread Safe");
        sbf.append(" String");
        System.out.println("StringBuffer 结果: " + sbf);
        
        // 性能比较
        performanceComparison();
    }
    
    public static void performanceComparison() {
        int iterations = 10000;
        
        // String 拼接（性能最差）
        long start = System.currentTimeMillis();
        String str = "";
        for (int i = 0; i < iterations; i++) {
            str += "a";
        }
        long stringTime = System.currentTimeMillis() - start;
        
        // StringBuilder 拼接（性能最好）
        start = System.currentTimeMillis();
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < iterations; i++) {
            sb.append("a");
        }
        String sbResult = sb.toString();
        long sbTime = System.currentTimeMillis() - start;
        
        System.out.println("\n性能比较（" + iterations + " 次拼接）:");
        System.out.println("String 拼接耗时: " + stringTime + "ms");
        System.out.println("StringBuilder 拼接耗时: " + sbTime + "ms");
        System.out.println("StringBuilder 比 String 快 " + (stringTime / (double) sbTime) + " 倍");
    }
}
```

## 三、包装类（Wrapper Classes）

### 3.1 基本类型与包装类

```java
public class WrapperClassDemo {
    public static void main(String[] args) {
        // 基本类型与对应的包装类
        byte b = 1;           // Byte
        short s = 2;          // Short
        int i = 3;            // Integer
        long l = 4L;          // Long
        float f = 5.0f;       // Float
        double d = 6.0;       // Double
        char c = 'A';         // Character
        boolean bool = true;  // Boolean
        
        // 装箱（基本类型 -> 包装类）
        Integer intObj1 = Integer.valueOf(i);  // 手动装箱
        Integer intObj2 = i;                   // 自动装箱（Java 5+）
        
        // 拆箱（包装类 -> 基本类型）
        int intValue1 = intObj1.intValue();    // 手动拆箱
        int intValue2 = intObj1;               // 自动拆箱（Java 5+）
        
        System.out.println("装箱结果: " + intObj1);
        System.out.println("拆箱结果: " + intValue1);
        
        // 包装类的缓存机制
        Integer a1 = 127;
        Integer a2 = 127;
        Integer b1 = 128;
        Integer b2 = 128;
        
        System.out.println("a1 == a2: " + (a1 == a2));  // true（缓存范围内）
        System.out.println("b1 == b2: " + (b1 == b2));  // false（超出缓存范围）
        
        // 正确的比较方式
        System.out.println("b1.equals(b2): " + b1.equals(b2));  // true
    }
}
```

### 3.2 包装类的常用方法

```java
public class WrapperMethodsDemo {
    public static void main(String[] args) {
        // Integer 类的常用方法
        System.out.println("=== Integer 类方法 ===");
        System.out.println("最大值: " + Integer.MAX_VALUE);
        System.out.println("最小值: " + Integer.MIN_VALUE);
        System.out.println("字节数: " + Integer.BYTES);
        
        // 字符串转换
        String numStr = "123";
        int num = Integer.parseInt(numStr);
        Integer numObj = Integer.valueOf(numStr);
        System.out.println("字符串转int: " + num);
        System.out.println("字符串转Integer: " + numObj);
        
        // 进制转换
        int decimal = 255;
        System.out.println("十进制 " + decimal + " 转二进制: " + Integer.toBinaryString(decimal));
        System.out.println("十进制 " + decimal + " 转八进制: " + Integer.toOctalString(decimal));
        System.out.println("十进制 " + decimal + " 转十六进制: " + Integer.toHexString(decimal));
        
        // 其他进制转十进制
        System.out.println("二进制 '1111' 转十进制: " + Integer.parseInt("1111", 2));
        System.out.println("十六进制 'FF' 转十进制: " + Integer.parseInt("FF", 16));
        
        // Double 类的特殊值
        System.out.println("\n=== Double 类特殊值 ===");
        System.out.println("正无穷: " + Double.POSITIVE_INFINITY);
        System.out.println("负无穷: " + Double.NEGATIVE_INFINITY);
        System.out.println("非数字: " + Double.NaN);
        
        double result1 = 1.0 / 0.0;
        double result2 = 0.0 / 0.0;
        System.out.println("1.0/0.0 = " + result1);
        System.out.println("0.0/0.0 = " + result2);
        System.out.println("是否为无穷: " + Double.isInfinite(result1));
        System.out.println("是否为NaN: " + Double.isNaN(result2));
        
        // Character 类的方法
        System.out.println("\n=== Character 类方法 ===");
        char ch = 'A';
        System.out.println("是否为字母: " + Character.isLetter(ch));
        System.out.println("是否为数字: " + Character.isDigit(ch));
        System.out.println("是否为大写: " + Character.isUpperCase(ch));
        System.out.println("转小写: " + Character.toLowerCase(ch));
        System.out.println("Unicode值: " + (int) ch);
        
        // Boolean 类的方法
        System.out.println("\n=== Boolean 类方法 ===");
        System.out.println("字符串转boolean: " + Boolean.parseBoolean("true"));
        System.out.println("字符串转boolean: " + Boolean.parseBoolean("false"));
        System.out.println("字符串转boolean: " + Boolean.parseBoolean("yes"));  // false
    }
}
```

### 3.3 包装类的注意事项

```java
public class WrapperPitfallsDemo {
    public static void main(String[] args) {
        // 1. 缓存范围
        System.out.println("=== 缓存范围 ===");
        // Integer 缓存 -128 到 127
        Integer i1 = 100;
        Integer i2 = 100;
        Integer i3 = 200;
        Integer i4 = 200;
        
        System.out.println("i1 == i2: " + (i1 == i2));  // true
        System.out.println("i3 == i4: " + (i3 == i4));  // false
        
        // 2. 空指针异常
        System.out.println("\n=== 空指针异常 ===");
        Integer nullInt = null;
        try {
            int value = nullInt;  // 自动拆箱时抛出 NullPointerException
        } catch (NullPointerException e) {
            System.out.println("空指针异常: " + e.getMessage());
        }
        
        // 3. 性能考虑
        System.out.println("\n=== 性能比较 ===");
        long start, end;
        int iterations = 1000000;
        
        // 基本类型运算
        start = System.currentTimeMillis();
        int sum1 = 0;
        for (int i = 0; i < iterations; i++) {
            sum1 += i;
        }
        end = System.currentTimeMillis();
        System.out.println("基本类型运算耗时: " + (end - start) + "ms");
        
        // 包装类运算（频繁装箱拆箱）
        start = System.currentTimeMillis();
        Integer sum2 = 0;
        for (int i = 0; i < iterations; i++) {
            sum2 += i;  // 自动装箱拆箱
        }
        end = System.currentTimeMillis();
        System.out.println("包装类运算耗时: " + (end - start) + "ms");
        
        // 4. 比较陷阱
        System.out.println("\n=== 比较陷阱 ===");
        Integer a = new Integer(1);
        Integer b = new Integer(1);
        System.out.println("new Integer(1) == new Integer(1): " + (a == b));  // false
        System.out.println("new Integer(1).equals(new Integer(1)): " + a.equals(b));  // true
        
        // 混合比较
        Integer c = 1;
        int d = 1;
        System.out.println("Integer(1) == int(1): " + (c == d));  // true（自动拆箱）
    }
}
```

## 四、日期时间类

### 4.1 传统日期时间类（Java 8 之前）

```java
import java.util.Date;
import java.util.Calendar;
import java.text.SimpleDateFormat;
import java.text.ParseException;

public class LegacyDateDemo {
    public static void main(String[] args) throws ParseException {
        // Date 类（已过时，不推荐使用）
        System.out.println("=== Date 类 ===");
        Date now = new Date();
        System.out.println("当前时间: " + now);
        System.out.println("时间戳: " + now.getTime());
        
        // 创建指定时间
        Date specificDate = new Date(2024, 0, 1);  // 已废弃
        System.out.println("指定时间: " + specificDate);
        
        // SimpleDateFormat 格式化
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        String formatted = sdf.format(now);
        System.out.println("格式化时间: " + formatted);
        
        // 解析字符串为日期
        Date parsed = sdf.parse("2024-01-01 12:30:45");
        System.out.println("解析的日期: " + parsed);
        
        // Calendar 类
        System.out.println("\n=== Calendar 类 ===");
        Calendar cal = Calendar.getInstance();
        System.out.println("当前年份: " + cal.get(Calendar.YEAR));
        System.out.println("当前月份: " + (cal.get(Calendar.MONTH) + 1));  // 月份从0开始
        System.out.println("当前日期: " + cal.get(Calendar.DAY_OF_MONTH));
        System.out.println("当前小时: " + cal.get(Calendar.HOUR_OF_DAY));
        System.out.println("当前分钟: " + cal.get(Calendar.MINUTE));
        System.out.println("当前秒数: " + cal.get(Calendar.SECOND));
        
        // 设置时间
        cal.set(2024, Calendar.JANUARY, 1, 0, 0, 0);
        System.out.println("设置的时间: " + cal.getTime());
        
        // 时间运算
        cal.add(Calendar.DAY_OF_MONTH, 30);
        System.out.println("30天后: " + cal.getTime());
        
        cal.add(Calendar.MONTH, -1);
        System.out.println("1个月前: " + cal.getTime());
    }
}
```

### 4.2 新日期时间 API（Java 8+）

```java
import java.time.*;
import java.time.format.DateTimeFormatter;
import java.time.temporal.ChronoUnit;

public class ModernDateTimeDemo {
    public static void main(String[] args) {
        // LocalDate - 日期（年月日）
        System.out.println("=== LocalDate ===");
        LocalDate today = LocalDate.now();
        LocalDate specificDate = LocalDate.of(2024, 1, 1);
        LocalDate parsedDate = LocalDate.parse("2024-12-25");
        
        System.out.println("今天: " + today);
        System.out.println("指定日期: " + specificDate);
        System.out.println("解析日期: " + parsedDate);
        
        System.out.println("年份: " + today.getYear());
        System.out.println("月份: " + today.getMonthValue());
        System.out.println("日期: " + today.getDayOfMonth());
        System.out.println("星期: " + today.getDayOfWeek());
        
        // LocalTime - 时间（时分秒）
        System.out.println("\n=== LocalTime ===");
        LocalTime now = LocalTime.now();
        LocalTime specificTime = LocalTime.of(14, 30, 45);
        LocalTime parsedTime = LocalTime.parse("09:15:30");
        
        System.out.println("现在时间: " + now);
        System.out.println("指定时间: " + specificTime);
        System.out.println("解析时间: " + parsedTime);
        
        // LocalDateTime - 日期时间
        System.out.println("\n=== LocalDateTime ===");
        LocalDateTime nowDateTime = LocalDateTime.now();
        LocalDateTime specificDateTime = LocalDateTime.of(2024, 1, 1, 12, 0, 0);
        
        System.out.println("现在: " + nowDateTime);
        System.out.println("指定日期时间: " + specificDateTime);
        
        // 组合 LocalDate 和 LocalTime
        LocalDateTime combined = LocalDate.now().atTime(LocalTime.now());
        System.out.println("组合日期时间: " + combined);
        
        // ZonedDateTime - 带时区的日期时间
        System.out.println("\n=== ZonedDateTime ===");
        ZonedDateTime zonedNow = ZonedDateTime.now();
        ZonedDateTime tokyoTime = ZonedDateTime.now(ZoneId.of("Asia/Tokyo"));
        ZonedDateTime newYorkTime = ZonedDateTime.now(ZoneId.of("America/New_York"));
        
        System.out.println("本地时区: " + zonedNow);
        System.out.println("东京时间: " + tokyoTime);
        System.out.println("纽约时间: " + newYorkTime);
        
        // Instant - 时间戳
        System.out.println("\n=== Instant ===");
        Instant instant = Instant.now();
        System.out.println("当前时间戳: " + instant);
        System.out.println("毫秒数: " + instant.toEpochMilli());
        System.out.println("秒数: " + instant.getEpochSecond());
    }
}
```

### 4.3 日期时间操作和格式化

```java
import java.time.*;
import java.time.format.DateTimeFormatter;
import java.time.temporal.ChronoUnit;
import java.time.temporal.TemporalAdjusters;

public class DateTimeOperationsDemo {
    public static void main(String[] args) {
        LocalDateTime now = LocalDateTime.now();
        
        // 日期时间运算
        System.out.println("=== 日期时间运算 ===");
        System.out.println("现在: " + now);
        System.out.println("1年后: " + now.plusYears(1));
        System.out.println("3个月后: " + now.plusMonths(3));
        System.out.println("10天后: " + now.plusDays(10));
        System.out.println("2小时后: " + now.plusHours(2));
        System.out.println("30分钟前: " + now.minusMinutes(30));
        
        // 使用 TemporalAdjusters
        System.out.println("\n=== TemporalAdjusters ===");
        LocalDate today = LocalDate.now();
        System.out.println("今天: " + today);
        System.out.println("本月第一天: " + today.with(TemporalAdjusters.firstDayOfMonth()));
        System.out.println("本月最后一天: " + today.with(TemporalAdjusters.lastDayOfMonth()));
        System.out.println("下个周一: " + today.with(TemporalAdjusters.next(DayOfWeek.MONDAY)));
        System.out.println("本月第一个周五: " + today.with(TemporalAdjusters.firstInMonth(DayOfWeek.FRIDAY)));
        
        // 时间间隔计算
        System.out.println("\n=== 时间间隔 ===");
        LocalDate startDate = LocalDate.of(2024, 1, 1);
        LocalDate endDate = LocalDate.of(2024, 12, 31);
        
        long daysBetween = ChronoUnit.DAYS.between(startDate, endDate);
        long monthsBetween = ChronoUnit.MONTHS.between(startDate, endDate);
        
        System.out.println("开始日期: " + startDate);
        System.out.println("结束日期: " + endDate);
        System.out.println("相差天数: " + daysBetween);
        System.out.println("相差月数: " + monthsBetween);
        
        // Period 和 Duration
        Period period = Period.between(startDate, endDate);
        System.out.println("Period: " + period);
        System.out.println("年数: " + period.getYears());
        System.out.println("月数: " + period.getMonths());
        System.out.println("天数: " + period.getDays());
        
        LocalTime startTime = LocalTime.of(9, 0);
        LocalTime endTime = LocalTime.of(17, 30);
        Duration duration = Duration.between(startTime, endTime);
        System.out.println("Duration: " + duration);
        System.out.println("小时数: " + duration.toHours());
        System.out.println("分钟数: " + duration.toMinutes());
        
        // 格式化
        System.out.println("\n=== 格式化 ===");
        LocalDateTime dateTime = LocalDateTime.now();
        
        // 预定义格式
        System.out.println("ISO格式: " + dateTime.format(DateTimeFormatter.ISO_LOCAL_DATE_TIME));
        
        // 自定义格式
        DateTimeFormatter formatter1 = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
        DateTimeFormatter formatter2 = DateTimeFormatter.ofPattern("yyyy年MM月dd日 HH时mm分ss秒");
        DateTimeFormatter formatter3 = DateTimeFormatter.ofPattern("E, MMM dd, yyyy");
        
        System.out.println("自定义格式1: " + dateTime.format(formatter1));
        System.out.println("自定义格式2: " + dateTime.format(formatter2));
        System.out.println("自定义格式3: " + dateTime.format(formatter3));
        
        // 解析字符串
        String dateStr = "2024-01-01 12:30:45";
        LocalDateTime parsed = LocalDateTime.parse(dateStr, formatter1);
        System.out.println("解析结果: " + parsed);
    }
}
```

## 五、Arrays 工具类

### 5.1 Arrays 类的基本方法

```java
import java.util.Arrays;
import java.util.Comparator;

public class ArraysDemo {
    public static void main(String[] args) {
        // 数组转字符串
        System.out.println("=== 数组转字符串 ===");
        int[] intArray = {3, 1, 4, 1, 5, 9, 2, 6};
        String[] strArray = {"apple", "banana", "cherry", "date"};
        
        System.out.println("int数组: " + Arrays.toString(intArray));
        System.out.println("String数组: " + Arrays.toString(strArray));
        
        // 二维数组
        int[][] matrix = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};
        System.out.println("二维数组: " + Arrays.deepToString(matrix));
        
        // 数组排序
        System.out.println("\n=== 数组排序 ===");
        int[] sortArray = intArray.clone();
        Arrays.sort(sortArray);
        System.out.println("排序前: " + Arrays.toString(intArray));
        System.out.println("排序后: " + Arrays.toString(sortArray));
        
        // 字符串数组排序
        String[] sortStrArray = strArray.clone();
        Arrays.sort(sortStrArray);
        System.out.println("字符串排序: " + Arrays.toString(sortStrArray));
        
        // 自定义排序（降序）
        String[] customSortArray = strArray.clone();
        Arrays.sort(customSortArray, Comparator.reverseOrder());
        System.out.println("降序排序: " + Arrays.toString(customSortArray));
        
        // 部分排序
        int[] partialSort = {5, 2, 8, 1, 9, 3};
        Arrays.sort(partialSort, 1, 4);  // 排序索引1到3的元素
        System.out.println("部分排序: " + Arrays.toString(partialSort));
        
        // 数组查找
        System.out.println("\n=== 数组查找 ===");
        int[] searchArray = {1, 2, 3, 4, 5, 6, 7, 8, 9};
        int index = Arrays.binarySearch(searchArray, 5);
        System.out.println("查找元素5的索引: " + index);
        
        int notFoundIndex = Arrays.binarySearch(searchArray, 10);
        System.out.println("查找不存在元素10: " + notFoundIndex);  // 负数表示插入位置
        
        // 数组比较
        System.out.println("\n=== 数组比较 ===");
        int[] array1 = {1, 2, 3, 4, 5};
        int[] array2 = {1, 2, 3, 4, 5};
        int[] array3 = {1, 2, 3, 4, 6};
        
        System.out.println("array1 equals array2: " + Arrays.equals(array1, array2));
        System.out.println("array1 equals array3: " + Arrays.equals(array1, array3));
        
        // 数组填充
        System.out.println("\n=== 数组填充 ===");
        int[] fillArray = new int[5];
        Arrays.fill(fillArray, 42);
        System.out.println("填充数组: " + Arrays.toString(fillArray));
        
        // 部分填充
        Arrays.fill(fillArray, 1, 4, 99);
        System.out.println("部分填充: " + Arrays.toString(fillArray));
        
        // 数组复制
        System.out.println("\n=== 数组复制 ===");
        int[] original = {1, 2, 3, 4, 5};
        int[] copy1 = Arrays.copyOf(original, original.length);
        int[] copy2 = Arrays.copyOf(original, 8);  // 扩展长度
        int[] copy3 = Arrays.copyOfRange(original, 1, 4);  // 复制部分
        
        System.out.println("原数组: " + Arrays.toString(original));
        System.out.println("完整复制: " + Arrays.toString(copy1));
        System.out.println("扩展复制: " + Arrays.toString(copy2));
        System.out.println("部分复制: " + Arrays.toString(copy3));
    }
}
```

### 5.2 Arrays 类的高级用法

```java
import java.util.Arrays;
import java.util.Comparator;
import java.util.List;

public class AdvancedArraysDemo {
    public static void main(String[] args) {
        // 自定义对象排序
        System.out.println("=== 自定义对象排序 ===");
        Student[] students = {
            new Student("张三", 85),
            new Student("李四", 92),
            new Student("王五", 78),
            new Student("赵六", 95)
        };
        
        System.out.println("原始顺序:");
        printStudents(students);
        
        // 按分数排序
        Arrays.sort(students, Comparator.comparingInt(Student::getScore));
        System.out.println("\n按分数升序:");
        printStudents(students);
        
        // 按分数降序
        Arrays.sort(students, Comparator.comparingInt(Student::getScore).reversed());
        System.out.println("\n按分数降序:");
        printStudents(students);
        
        // 按姓名排序
        Arrays.sort(students, Comparator.comparing(Student::getName));
        System.out.println("\n按姓名排序:");
        printStudents(students);
        
        // 多条件排序
        Student[] moreStudents = {
            new Student("张三", 85),
            new Student("李四", 85),
            new Student("王五", 92),
            new Student("赵六", 85)
        };
        
        Arrays.sort(moreStudents, 
            Comparator.comparingInt(Student::getScore)
                     .thenComparing(Student::getName));
        System.out.println("\n多条件排序（分数升序，姓名升序）:");
        printStudents(moreStudents);
        
        // 数组转List
        System.out.println("\n=== 数组转List ===");
        String[] strArray = {"apple", "banana", "cherry"};
        List<String> list = Arrays.asList(strArray);
        System.out.println("转换的List: " + list);
        
        // 注意：Arrays.asList() 返回的是固定大小的List
        try {
            list.add("date");  // 会抛出 UnsupportedOperationException
        } catch (UnsupportedOperationException e) {
            System.out.println("不能添加元素: " + e.getMessage());
        }
        
        // 修改原数组会影响List
        strArray[0] = "apricot";
        System.out.println("修改原数组后的List: " + list);
        
        // 并行排序（Java 8+）
        System.out.println("\n=== 并行排序 ===");
        int[] largeArray = new int[1000000];
        for (int i = 0; i < largeArray.length; i++) {
            largeArray[i] = (int) (Math.random() * 1000000);
        }
        
        int[] copy1 = largeArray.clone();
        int[] copy2 = largeArray.clone();
        
        long start = System.currentTimeMillis();
        Arrays.sort(copy1);
        long serialTime = System.currentTimeMillis() - start;
        
        start = System.currentTimeMillis();
        Arrays.parallelSort(copy2);
        long parallelTime = System.currentTimeMillis() - start;
        
        System.out.println("串行排序耗时: " + serialTime + "ms");
        System.out.println("并行排序耗时: " + parallelTime + "ms");
        System.out.println("并行排序提升: " + (serialTime / (double) parallelTime) + "倍");
    }
    
    private static void printStudents(Student[] students) {
        for (Student student : students) {
            System.out.println(student);
        }
    }
}

// 学生类
class Student {
    private String name;
    private int score;
    
    public Student(String name, int score) {
        this.name = name;
        this.score = score;
    }
    
    public String getName() {
        return name;
    }
    
    public int getScore() {
        return score;
    }
    
    @Override
    public String toString() {
        return "Student{name='" + name + "', score=" + score + "}";
    }
}
```

## 总结

Java 核心类库的关键要点：

1. **Object 类**：所有类的根父类，提供基础方法
2. **String 类**：不可变字符串，字符串池优化
3. **StringBuilder/StringBuffer**：可变字符串，性能优化
4. **包装类**：基本类型的对象封装，自动装箱拆箱
5. **日期时间**：传统 Date/Calendar vs 新 API（Java 8+）
6. **Arrays 工具类**：数组操作的实用方法集合

> **最佳实践**：
> - 重写 equals() 时必须重写 hashCode()
> - 大量字符串拼接使用 StringBuilder
> - 优先使用新的日期时间 API
> - 注意包装类的缓存机制和性能影响