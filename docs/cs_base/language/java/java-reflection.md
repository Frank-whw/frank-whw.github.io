# Java 反射机制

## 概述

Java反射（Reflection）是Java语言的一个重要特性，它允许程序在运行时检查和操作类、接口、字段和方法的信息。反射提供了动态获取类信息和动态调用对象方法的能力，是许多框架（如Spring、Hibernate）的核心技术。

## 1. 反射基础

### 1.1 什么是反射

反射是指程序在运行时能够获取自身的信息。在Java中，反射机制允许程序在执行期间：

- 获取任意一个类的内部信息
- 获取任意一个对象的字段和方法
- 在运行时创建对象和调用方法
- 在运行时处理注解

### 1.2 反射的核心类

- **Class**：代表类的实体，在运行的Java应用程序中表示类和接口
- **Field**：代表类的成员变量（字段）
- **Method**：代表类的方法
- **Constructor**：代表类的构造方法

## 2. Class对象操作

### 2.1 获取Class对象的方式

```java
public class ClassExample {
    public static void main(String[] args) throws ClassNotFoundException {
        // 方式1：通过对象的getClass()方法
        String str = "Hello";
        Class<?> clazz1 = str.getClass();
        System.out.println("方式1: " + clazz1.getName());
        
        // 方式2：通过类的.class属性
        Class<?> clazz2 = String.class;
        System.out.println("方式2: " + clazz2.getName());
        
        // 方式3：通过Class.forName()方法
        Class<?> clazz3 = Class.forName("java.lang.String");
        System.out.println("方式3: " + clazz3.getName());
        
        // 验证三种方式获取的是同一个Class对象
        System.out.println("clazz1 == clazz2: " + (clazz1 == clazz2));
        System.out.println("clazz2 == clazz3: " + (clazz2 == clazz3));
    }
}
```

### 2.2 Class对象的常用方法

```java
import java.lang.reflect.*;
import java.util.Arrays;

public class ClassMethodsExample {
    public static void main(String[] args) {
        Class<?> clazz = String.class;
        
        // 获取类名
        System.out.println("类名: " + clazz.getName());
        System.out.println("简单类名: " + clazz.getSimpleName());
        
        // 获取包信息
        System.out.println("包名: " + clazz.getPackage().getName());
        
        // 获取父类
        System.out.println("父类: " + clazz.getSuperclass().getName());
        
        // 获取实现的接口
        Class<?>[] interfaces = clazz.getInterfaces();
        System.out.println("实现的接口: " + Arrays.toString(interfaces));
        
        // 获取修饰符
        int modifiers = clazz.getModifiers();
        System.out.println("是否为public: " + Modifier.isPublic(modifiers));
        System.out.println("是否为final: " + Modifier.isFinal(modifiers));
        
        // 判断类型
        System.out.println("是否为接口: " + clazz.isInterface());
        System.out.println("是否为数组: " + clazz.isArray());
        System.out.println("是否为枚举: " + clazz.isEnum());
    }
}
```

## 3. 字段操作

### 3.1 获取字段信息

```java
import java.lang.reflect.Field;

class Person {
    public String name;
    private int age;
    protected String address;
    static String country = "China";
    
    public Person(String name, int age) {
        this.name = name;
        this.age = age;
    }
}

public class FieldExample {
    public static void main(String[] args) throws Exception {
        Class<?> clazz = Person.class;
        
        System.out.println("=== 获取所有public字段 ===");
        Field[] publicFields = clazz.getFields();
        for (Field field : publicFields) {
            System.out.println(field.getName() + " - " + field.getType().getName());
        }
        
        System.out.println("\n=== 获取所有声明的字段 ===");
        Field[] declaredFields = clazz.getDeclaredFields();
        for (Field field : declaredFields) {
            System.out.println(field.getName() + " - " + field.getType().getName() + 
                " - " + Modifier.toString(field.getModifiers()));
        }
        
        System.out.println("\n=== 获取特定字段 ===");
        Field nameField = clazz.getField("name");
        System.out.println("name字段: " + nameField);
        
        Field ageField = clazz.getDeclaredField("age");
        System.out.println("age字段: " + ageField);
    }
}
```

### 3.2 字段值的读取和设置

```java
import java.lang.reflect.Field;

public class FieldAccessExample {
    public static void main(String[] args) throws Exception {
        Person person = new Person("张三", 25);
        Class<?> clazz = person.getClass();
        
        // 访问public字段
        Field nameField = clazz.getField("name");
        System.out.println("原始name: " + nameField.get(person));
        nameField.set(person, "李四");
        System.out.println("修改后name: " + nameField.get(person));
        
        // 访问private字段
        Field ageField = clazz.getDeclaredField("age");
        ageField.setAccessible(true); // 设置可访问
        System.out.println("原始age: " + ageField.get(person));
        ageField.set(person, 30);
        System.out.println("修改后age: " + ageField.get(person));
        
        // 访问static字段
        Field countryField = clazz.getDeclaredField("country");
        System.out.println("静态字段country: " + countryField.get(null));
        countryField.set(null, "USA");
        System.out.println("修改后country: " + countryField.get(null));
    }
}
```

## 4. 方法操作

### 4.1 获取方法信息

```java
import java.lang.reflect.Method;
import java.util.Arrays;

class Calculator {
    public int add(int a, int b) {
        return a + b;
    }
    
    private int subtract(int a, int b) {
        return a - b;
    }
    
    public static int multiply(int a, int b) {
        return a * b;
    }
    
    public void printResult(String operation, int result) {
        System.out.println(operation + " = " + result);
    }
}

public class MethodExample {
    public static void main(String[] args) throws Exception {
        Class<?> clazz = Calculator.class;
        
        System.out.println("=== 获取所有public方法 ===");
        Method[] publicMethods = clazz.getMethods();
        for (Method method : publicMethods) {
            if (method.getDeclaringClass() == clazz) { // 只显示当前类的方法
                System.out.println(method.getName() + " - 参数: " + 
                    Arrays.toString(method.getParameterTypes()) + 
                    " - 返回类型: " + method.getReturnType().getName());
            }
        }
        
        System.out.println("\n=== 获取所有声明的方法 ===");
        Method[] declaredMethods = clazz.getDeclaredMethods();
        for (Method method : declaredMethods) {
            System.out.println(method.getName() + " - " + 
                Modifier.toString(method.getModifiers()) + 
                " - 参数: " + Arrays.toString(method.getParameterTypes()));
        }
        
        System.out.println("\n=== 获取特定方法 ===");
        Method addMethod = clazz.getMethod("add", int.class, int.class);
        System.out.println("add方法: " + addMethod);
        
        Method subtractMethod = clazz.getDeclaredMethod("subtract", int.class, int.class);
        System.out.println("subtract方法: " + subtractMethod);
    }
}
```

### 4.2 动态调用方法

```java
import java.lang.reflect.Method;

public class MethodInvokeExample {
    public static void main(String[] args) throws Exception {
        Calculator calculator = new Calculator();
        Class<?> clazz = calculator.getClass();
        
        // 调用实例方法
        Method addMethod = clazz.getMethod("add", int.class, int.class);
        Object result = addMethod.invoke(calculator, 10, 5);
        System.out.println("add(10, 5) = " + result);
        
        // 调用private方法
        Method subtractMethod = clazz.getDeclaredMethod("subtract", int.class, int.class);
        subtractMethod.setAccessible(true);
        Object result2 = subtractMethod.invoke(calculator, 10, 5);
        System.out.println("subtract(10, 5) = " + result2);
        
        // 调用static方法
        Method multiplyMethod = clazz.getMethod("multiply", int.class, int.class);
        Object result3 = multiplyMethod.invoke(null, 10, 5);
        System.out.println("multiply(10, 5) = " + result3);
        
        // 调用void方法
        Method printMethod = clazz.getMethod("printResult", String.class, int.class);
        printMethod.invoke(calculator, "10 + 5", 15);
    }
}
```

## 5. 构造方法操作

### 5.1 获取和使用构造方法

```java
import java.lang.reflect.Constructor;
import java.util.Arrays;

class Student {
    private String name;
    private int age;
    private String major;
    
    public Student() {
        this.name = "Unknown";
        this.age = 0;
    }
    
    public Student(String name, int age) {
        this.name = name;
        this.age = age;
    }
    
    private Student(String name, int age, String major) {
        this.name = name;
        this.age = age;
        this.major = major;
    }
    
    @Override
    public String toString() {
        return "Student{name='" + name + "', age=" + age + ", major='" + major + "'}";
    }
}

public class ConstructorExample {
    public static void main(String[] args) throws Exception {
        Class<?> clazz = Student.class;
        
        System.out.println("=== 获取所有public构造方法 ===");
        Constructor<?>[] publicConstructors = clazz.getConstructors();
        for (Constructor<?> constructor : publicConstructors) {
            System.out.println("参数类型: " + Arrays.toString(constructor.getParameterTypes()));
        }
        
        System.out.println("\n=== 获取所有声明的构造方法 ===");
        Constructor<?>[] declaredConstructors = clazz.getDeclaredConstructors();
        for (Constructor<?> constructor : declaredConstructors) {
            System.out.println(Modifier.toString(constructor.getModifiers()) + 
                " - 参数类型: " + Arrays.toString(constructor.getParameterTypes()));
        }
        
        System.out.println("\n=== 使用构造方法创建对象 ===");
        
        // 使用无参构造方法
        Constructor<?> defaultConstructor = clazz.getConstructor();
        Object student1 = defaultConstructor.newInstance();
        System.out.println("无参构造: " + student1);
        
        // 使用有参构造方法
        Constructor<?> paramConstructor = clazz.getConstructor(String.class, int.class);
        Object student2 = paramConstructor.newInstance("张三", 20);
        System.out.println("有参构造: " + student2);
        
        // 使用private构造方法
        Constructor<?> privateConstructor = clazz.getDeclaredConstructor(
            String.class, int.class, String.class);
        privateConstructor.setAccessible(true);
        Object student3 = privateConstructor.newInstance("李四", 22, "计算机科学");
        System.out.println("私有构造: " + student3);
    }
}
```

## 6. 数组操作

### 6.1 动态创建和操作数组

```java
import java.lang.reflect.Array;

public class ArrayReflectionExample {
    public static void main(String[] args) {
        // 创建一维数组
        Object intArray = Array.newInstance(int.class, 5);
        
        // 设置数组元素
        for (int i = 0; i < 5; i++) {
            Array.set(intArray, i, i * 10);
        }
        
        // 获取数组元素
        System.out.println("一维数组:");
        for (int i = 0; i < Array.getLength(intArray); i++) {
            System.out.println("intArray[" + i + "] = " + Array.get(intArray, i));
        }
        
        // 创建二维数组
        Object stringArray2D = Array.newInstance(String.class, 3, 2);
        
        // 设置二维数组元素
        for (int i = 0; i < 3; i++) {
            Object row = Array.get(stringArray2D, i);
            for (int j = 0; j < 2; j++) {
                Array.set(row, j, "(" + i + "," + j + ")");
            }
        }
        
        // 获取二维数组元素
        System.out.println("\n二维数组:");
        for (int i = 0; i < Array.getLength(stringArray2D); i++) {
            Object row = Array.get(stringArray2D, i);
            for (int j = 0; j < Array.getLength(row); j++) {
                System.out.print(Array.get(row, j) + " ");
            }
            System.out.println();
        }
        
        // 获取数组类型信息
        Class<?> arrayClass = intArray.getClass();
        System.out.println("\n数组类型信息:");
        System.out.println("是否为数组: " + arrayClass.isArray());
        System.out.println("组件类型: " + arrayClass.getComponentType());
    }
}
```

## 7. 注解处理

### 7.1 自定义注解

```java
import java.lang.annotation.*;

// 定义注解
@Retention(RetentionPolicy.RUNTIME)
@Target({ElementType.TYPE, ElementType.FIELD, ElementType.METHOD})
@interface MyAnnotation {
    String value() default "";
    int priority() default 0;
}

@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.FIELD)
@interface FieldInfo {
    String description();
    boolean required() default false;
}

// 使用注解的类
@MyAnnotation(value = "这是一个测试类", priority = 1)
class AnnotatedClass {
    @FieldInfo(description = "用户名", required = true)
    private String username;
    
    @FieldInfo(description = "年龄")
    private int age;
    
    @MyAnnotation("这是一个测试方法")
    public void testMethod() {
        System.out.println("测试方法执行");
    }
}
```

### 7.2 读取注解信息

```java
import java.lang.reflect.Field;
import java.lang.reflect.Method;

public class AnnotationExample {
    public static void main(String[] args) throws Exception {
        Class<?> clazz = AnnotatedClass.class;
        
        // 读取类上的注解
        System.out.println("=== 类注解 ===");
        if (clazz.isAnnotationPresent(MyAnnotation.class)) {
            MyAnnotation classAnnotation = clazz.getAnnotation(MyAnnotation.class);
            System.out.println("类注解值: " + classAnnotation.value());
            System.out.println("类注解优先级: " + classAnnotation.priority());
        }
        
        // 读取字段上的注解
        System.out.println("\n=== 字段注解 ===");
        Field[] fields = clazz.getDeclaredFields();
        for (Field field : fields) {
            if (field.isAnnotationPresent(FieldInfo.class)) {
                FieldInfo fieldInfo = field.getAnnotation(FieldInfo.class);
                System.out.println("字段: " + field.getName());
                System.out.println("  描述: " + fieldInfo.description());
                System.out.println("  必需: " + fieldInfo.required());
            }
        }
        
        // 读取方法上的注解
        System.out.println("\n=== 方法注解 ===");
        Method[] methods = clazz.getDeclaredMethods();
        for (Method method : methods) {
            if (method.isAnnotationPresent(MyAnnotation.class)) {
                MyAnnotation methodAnnotation = method.getAnnotation(MyAnnotation.class);
                System.out.println("方法: " + method.getName());
                System.out.println("  注解值: " + methodAnnotation.value());
            }
        }
    }
}
```

## 8. 反射的应用场景

### 8.1 简单的依赖注入框架

```java
import java.lang.annotation.*;
import java.lang.reflect.Field;
import java.util.HashMap;
import java.util.Map;

// 依赖注入注解
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.FIELD)
@interface Inject {
}

// 服务接口和实现
interface UserService {
    void saveUser(String username);
}

class UserServiceImpl implements UserService {
    @Override
    public void saveUser(String username) {
        System.out.println("保存用户: " + username);
    }
}

// 控制器类
class UserController {
    @Inject
    private UserService userService;
    
    public void createUser(String username) {
        if (userService != null) {
            userService.saveUser(username);
        } else {
            System.out.println("UserService未注入");
        }
    }
}

// 简单的依赖注入容器
class SimpleContainer {
    private Map<Class<?>, Object> instances = new HashMap<>();
    
    public void register(Class<?> interfaceClass, Object implementation) {
        instances.put(interfaceClass, implementation);
    }
    
    public <T> T getInstance(Class<T> clazz) throws Exception {
        T instance = clazz.getDeclaredConstructor().newInstance();
        injectDependencies(instance);
        return instance;
    }
    
    private void injectDependencies(Object instance) throws Exception {
        Class<?> clazz = instance.getClass();
        Field[] fields = clazz.getDeclaredFields();
        
        for (Field field : fields) {
            if (field.isAnnotationPresent(Inject.class)) {
                Class<?> fieldType = field.getType();
                Object dependency = instances.get(fieldType);
                
                if (dependency != null) {
                    field.setAccessible(true);
                    field.set(instance, dependency);
                }
            }
        }
    }
}

public class DIExample {
    public static void main(String[] args) throws Exception {
        // 创建容器并注册服务
        SimpleContainer container = new SimpleContainer();
        container.register(UserService.class, new UserServiceImpl());
        
        // 获取控制器实例（自动注入依赖）
        UserController controller = container.getInstance(UserController.class);
        controller.createUser("张三");
    }
}
```

### 8.2 对象序列化工具

```java
import java.lang.reflect.Field;
import java.util.HashMap;
import java.util.Map;

class Person2 {
    private String name;
    private int age;
    private String email;
    
    public Person2(String name, int age, String email) {
        this.name = name;
        this.age = age;
        this.email = email;
    }
    
    // getter和setter方法省略
}

class ObjectSerializer {
    public static Map<String, Object> toMap(Object obj) throws Exception {
        Map<String, Object> map = new HashMap<>();
        Class<?> clazz = obj.getClass();
        
        Field[] fields = clazz.getDeclaredFields();
        for (Field field : fields) {
            field.setAccessible(true);
            Object value = field.get(obj);
            map.put(field.getName(), value);
        }
        
        return map;
    }
    
    public static <T> T fromMap(Map<String, Object> map, Class<T> clazz) throws Exception {
        T instance = clazz.getDeclaredConstructor().newInstance();
        
        Field[] fields = clazz.getDeclaredFields();
        for (Field field : fields) {
            field.setAccessible(true);
            Object value = map.get(field.getName());
            if (value != null) {
                field.set(instance, value);
            }
        }
        
        return instance;
    }
}

public class SerializationExample {
    public static void main(String[] args) throws Exception {
        Person2 person = new Person2("张三", 25, "zhangsan@example.com");
        
        // 对象转Map
        Map<String, Object> map = ObjectSerializer.toMap(person);
        System.out.println("对象转Map: " + map);
        
        // Map转对象
        Person2 newPerson = ObjectSerializer.fromMap(map, Person2.class);
        System.out.println("Map转对象成功");
    }
}
```

## 9. 反射的性能考虑

### 9.1 性能测试

```java
import java.lang.reflect.Method;

class PerformanceTest {
    public int add(int a, int b) {
        return a + b;
    }
}

public class ReflectionPerformanceExample {
    public static void main(String[] args) throws Exception {
        PerformanceTest test = new PerformanceTest();
        Method addMethod = test.getClass().getMethod("add", int.class, int.class);
        
        int iterations = 1000000;
        
        // 直接调用性能测试
        long startTime = System.currentTimeMillis();
        for (int i = 0; i < iterations; i++) {
            test.add(1, 2);
        }
        long directTime = System.currentTimeMillis() - startTime;
        
        // 反射调用性能测试
        startTime = System.currentTimeMillis();
        for (int i = 0; i < iterations; i++) {
            addMethod.invoke(test, 1, 2);
        }
        long reflectionTime = System.currentTimeMillis() - startTime;
        
        System.out.println("直接调用时间: " + directTime + "ms");
        System.out.println("反射调用时间: " + reflectionTime + "ms");
        System.out.println("性能差异: " + (reflectionTime / (double) directTime) + "倍");
    }
}
```

### 9.2 性能优化建议

```java
import java.lang.reflect.Method;
import java.util.concurrent.ConcurrentHashMap;

// 缓存反射对象
class ReflectionCache {
    private static final ConcurrentHashMap<String, Method> methodCache = 
        new ConcurrentHashMap<>();
    
    public static Method getMethod(Class<?> clazz, String methodName, Class<?>... paramTypes) 
            throws NoSuchMethodException {
        String key = clazz.getName() + "." + methodName;
        return methodCache.computeIfAbsent(key, k -> {
            try {
                return clazz.getMethod(methodName, paramTypes);
            } catch (NoSuchMethodException e) {
                throw new RuntimeException(e);
            }
        });
    }
}

public class ReflectionOptimizationExample {
    public static void main(String[] args) throws Exception {
        PerformanceTest test = new PerformanceTest();
        
        int iterations = 1000000;
        
        // 未缓存的反射调用
        long startTime = System.currentTimeMillis();
        for (int i = 0; i < iterations; i++) {
            Method method = test.getClass().getMethod("add", int.class, int.class);
            method.invoke(test, 1, 2);
        }
        long uncachedTime = System.currentTimeMillis() - startTime;
        
        // 缓存的反射调用
        startTime = System.currentTimeMillis();
        for (int i = 0; i < iterations; i++) {
            Method method = ReflectionCache.getMethod(test.getClass(), "add", int.class, int.class);
            method.invoke(test, 1, 2);
        }
        long cachedTime = System.currentTimeMillis() - startTime;
        
        System.out.println("未缓存反射时间: " + uncachedTime + "ms");
        System.out.println("缓存反射时间: " + cachedTime + "ms");
        System.out.println("性能提升: " + (uncachedTime / (double) cachedTime) + "倍");
    }
}
```

## 10. 反射的最佳实践

### 10.1 安全性考虑

```java
import java.lang.reflect.Field;

public class SecurityExample {
    private static final String SENSITIVE_DATA = "敏感信息";
    
    public static void safeReflectionAccess(Object obj, String fieldName) {
        try {
            Class<?> clazz = obj.getClass();
            Field field = clazz.getDeclaredField(fieldName);
            
            // 检查安全性
            if (field.getName().contains("password") || 
                field.getName().contains("secret")) {
                System.out.println("拒绝访问敏感字段: " + fieldName);
                return;
            }
            
            field.setAccessible(true);
            Object value = field.get(obj);
            System.out.println(fieldName + ": " + value);
            
        } catch (Exception e) {
            System.out.println("访问字段失败: " + e.getMessage());
        }
    }
}
```

### 10.2 异常处理

```java
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;

public class ExceptionHandlingExample {
    public static Object safeInvoke(Object obj, String methodName, Object... args) {
        try {
            Class<?> clazz = obj.getClass();
            Class<?>[] paramTypes = new Class[args.length];
            for (int i = 0; i < args.length; i++) {
                paramTypes[i] = args[i].getClass();
            }
            
            Method method = clazz.getMethod(methodName, paramTypes);
            return method.invoke(obj, args);
            
        } catch (NoSuchMethodException e) {
            System.err.println("方法不存在: " + methodName);
        } catch (IllegalAccessException e) {
            System.err.println("方法访问权限不足: " + methodName);
        } catch (InvocationTargetException e) {
            System.err.println("方法执行异常: " + e.getCause().getMessage());
        } catch (Exception e) {
            System.err.println("反射调用异常: " + e.getMessage());
        }
        return null;
    }
}
```

## 总结

Java反射机制是一个强大的特性，它提供了运行时检查和操作类、字段、方法的能力。掌握以下要点：

### 核心概念
1. **Class对象**：反射的入口点，代表类的元信息
2. **Field、Method、Constructor**：分别代表字段、方法和构造器
3. **动态操作**：运行时创建对象、调用方法、访问字段

### 主要用途
1. **框架开发**：Spring、Hibernate等框架的核心技术
2. **配置驱动**：根据配置文件动态创建对象
3. **注解处理**：读取和处理注解信息
4. **序列化**：对象与其他格式的转换

### 注意事项
1. **性能影响**：反射比直接调用慢，需要合理使用
2. **安全性**：可能破坏封装性，需要谨慎处理
3. **异常处理**：反射操作可能抛出多种异常
4. **缓存优化**：缓存反射对象以提高性能

反射是Java高级特性之一，合理使用可以大大提高程序的灵活性和可扩展性。