# TypeScript 基础类型系统示例
```typescript
// TypeScript 基础类型系统示例

     // 1. 基本类型
     let username: string = "张三";
     let age: number = 20;
     let isStudent: boolean = true;
     let hobbies: string[] = ["编程", "游戏", "音乐"];

     // 2. 对象类型
     let user: {
       name: string;
       age: number;
       email?: string; // ? 表示可选属性
     } = {
       name: "李四",
       age: 22
     };

     // 3. 交叉类型 (Intersection Types) - 用 & 表示"和"
     // 意思是一个值必须同时满足多个类型的要求

     // 基础交叉类型
     type Person = {
       name: string;
       age: number;
     };

     type Employee = {
       employeeId: string;
       department: string;
     };

     // 交叉类型：既是Person又是Employee
     type PersonEmployee = Person & Employee;

     const worker: PersonEmployee = {
       name: "张三",
       age: 28,
       employeeId: "E001",
       department: "技术部"
       // 必须包含两个类型的所有属性
     };

     // 函数能力的组合
     type Flyable = {
       fly(): void;
     };

     type Swimmable = {
       swim(): void;
     };

     // 既会飞又会游泳
     type Duck = Flyable & Swimmable;

     const duck: Duck = {
       fly() {
         console.log("鸭子在飞");
       },
       swim() {
         console.log("鸭子在游泳");
       }
     };

     // 实际应用：混合不同的配置
     type DatabaseConfig = {
       host: string;
       port: number;
     };

     type AuthConfig = {
       apiKey: string;
       secret: string;
     };

     type CacheConfig = {
       ttl: number;
       maxSize: number;
     };

     // 完整应用配置
     type AppConfig = DatabaseConfig & AuthConfig &
     CacheConfig;

     const config: AppConfig = {
       // 数据库配置
       host: "localhost",
       port: 5432,

       // 认证配置
       apiKey: "your-api-key",
       secret: "your-secret",

       // 缓存配置
       ttl: 3600,
       maxSize: 100
     };

     // 与联合类型的对比
     type A = { x: number };
     type B = { y: string };

     // 联合类型：A或B
     type AorB = A | B;
     let unionExample: AorB;
     unionExample = { x: 1 };           // ✅ 只需要A
     unionExample = { y: "hello" };     // ✅ 只需要B
     // unionExample = { x: 1, y: "hello" }; // ✅
     也可以两个都有

     // 交叉类型：A和B
     type AandB = A & B;
     let intersectionExample: AandB;
     intersectionExample = { x: 1, y: "hello" }; // ✅
     必须两个都有
     // intersectionExample = { x: 1 };          // ❌
     缺少y
     // intersectionExample = { y: "hello" };    // ❌
     缺少x

     // 实际项目中的使用：Mixin模式
     function withTimestamp<T extends {}>(obj: T): T & {
     timestamp: number } {
       return {
         ...obj,
         timestamp: Date.now()
       };
     }

     const user = { name: "李四", email:
     "lisi@example.com" };
     const userWithTimestamp = withTimestamp(user);
     // userWithTimestamp 现在有: name, email, timestamp

     // API响应的组合
     type BaseResponse = {
       success: boolean;
       message: string;
     };

     type DataResponse<T> = {
       data: T;
     };

     type ErrorResponse = {
       error: string;
       code: number;
     };

     // 成功响应
     type SuccessResponse<T> = BaseResponse &
     DataResponse<T>;

     // 错误响应
     type FailResponse = BaseResponse & ErrorResponse;

     // 使用示例
     const successResponse: SuccessResponse<User[]> = {
       success: true,
       message: "获取用户列表成功",
       data: [
         { id: "1", name: "用户1", email:
     "user1@example.com", age: 25 }
       ]
     };

     const errorResponse: FailResponse = {
       success: false,
       message: "获取用户列表失败",
       error: "数据库连接失败",
       code: 500
     };

     // 从types/index.ts导入User类型
     type User = {
       id: string;
       name: string;
       email: string;
       age: number;
     };

     export { };

     // 4. 函数类型
     function calculateTotal(price: number, tax: number):
     number {
       return price * (1 + tax);
     }

     // 箭头函数
     const greet = (name: string): string => {
       return `Hello, ${name}!`;
     };

     // 5. 数组的不同写法
     let numbers1: number[] = [1, 2, 3];
     let numbers2: Array<number> = [1, 2, 3];

     console.log("TypeScript基础类型演示完成！");
```

```javascript
// Interface vs Type 详解

     // 1. Interface - 描述对象的形状
     interface User {
       id: string;
       name: string;
       email: string;
       age: number;
       avatar?: string; // 可选属性
     }

     // Interface 可以扩展
     interface AdminUser extends User {
       role: "admin" | "super_admin";
       permissions: string[];
     }

     // Interface 可以合并声明
     interface User {
       lastLoginAt?: Date;
     }

     // 2. Type - 更灵活的类型别名
     type Status = "loading" | "success" | "error" |
     "idle";
     type ApiResponse<T> = {
       data: T;
       status: Status;
       message?: string;
     };

     // Type 可以使用联合类型、交叉类型
     type UserWithStatus = User & {
       status: Status;
     };

     // 3. 实际使用示例
     const createUser = (userData: Omit<User, "id">): User
      => {
       return {
         id: `user_${Date.now()}`,
         ...userData
       };
     };

      // 4. 泛型 (Generics) - 用 <T> 表示类型参数
     // 让函数、类、接口可以处理多种类型，同时保持类型安全

     // 最简单的泛型函数
     function identity<T>(arg: T): T {
       return arg;
     }

     // 使用时可以指定类型
     let stringResult = identity<string>("hello");   //
     string类型
     let numberResult = identity<number>(123);       //
     number类型
     let autoResult = identity("world");             //
     自动推断为string

     // 泛型数组操作
     function getFirstElement<T>(arr: T[]): T | undefined
     {
       return arr[0];
     }

     const firstNumber = getFirstElement([1, 2, 3]);
     // number | undefined
     const firstString = getFirstElement(["a", "b"]);
     // string | undefined

     // 多个泛型参数
     function pair<T, U>(first: T, second: U): [T, U] {
       return [first, second];
     }

     const stringNumberPair = pair("hello", 42);        //
      [string, number]
     const booleanStringPair = pair(true, "world");     //
      [boolean, string]

     // 泛型接口
     interface Container<T> {
       value: T;
       getValue(): T;
       setValue(newValue: T): void;
     }

     // 实现泛型接口
     class Box<T> implements Container<T> {
       constructor(public value: T) {}

       getValue(): T {
         return this.value;
       }

       setValue(newValue: T): void {
         this.value = newValue;
       }
     }

     const stringBox = new Box<string>("初始值");
     const numberBox = new Box<number>(100);

     // 泛型约束 - 限制T必须有某些属性
     interface HasLength {
       length: number;
     }

     function logLength<T extends HasLength>(arg: T): T {
       console.log(arg.length); //
     现在可以安全使用length属性
       return arg;
     }

     logLength("hello");        // ✅ string有length属性
     logLength([1, 2, 3]);      // ✅ array有length属性
     // logLength(123);         // ❌ number没有length属性

     // 实际项目中的API请求泛型
     interface ApiResponse<T> {
       success: boolean;
       data: T;
       message: string;
     }

     async function fetchData<T>(url: string):
     Promise<ApiResponse<T>> {
       const response = await fetch(url);
       return response.json() as ApiResponse<T>;
     }

     // 使用时指定数据类型
     interface User {
       id: string;
       name: string;
       email: string;
     }

     const userData = await
     fetchData<User[]>("/api/users");
     // userData.data 现在是 User[] 类型

     const singleUser = await
     fetchData<User>("/api/users/1");
     // singleUser.data 现在是 User 类型

     // 数据库操作的泛型类
     class Repository<T> {
       private items: T[] = [];

       add(item: T): void {
         this.items.push(item);
       }

       findById<K extends keyof T>(key: K, value: T[K]): T
      | undefined {
         return this.items.find(item => item[key] ===
     value);
       }

       getAll(): T[] {
         return [...this.items];
       }

       update(predicate: (item: T) => boolean, updates:
     Partial<T>): T | undefined {
         const item = this.items.find(predicate);
         if (item) {
           Object.assign(item, updates);
         }
         return item;
       }
     }

     // 使用泛型Repository
     const userRepo = new Repository<User>();
     userRepo.add({ id: "1", name: "张三", email:
     "zhangsan@example.com" });

     const user = userRepo.findById("id", "1");
     userRepo.update(user => user.id === "1", { name:
     "张三丰" });

     // 工具类型的泛型应用
     type Partial<T> = {
       [P in keyof T]?: T[P];
     };

     type Required<T> = {
       [P in keyof T]-?: T[P];
     };

     type Pick<T, K extends keyof T> = {
       [P in K]: T[P];
     };

     // React组件的泛型Props
     interface ListProps<T> {
       items: T[];
       renderItem: (item: T, index: number) =>
     React.ReactNode;
       keyExtractor: (item: T) => string;
     }

     function List<T>({ items, renderItem, keyExtractor }:
      ListProps<T>) {
       return (
         <ul>
           {items.map((item, index) => (
             <li key={keyExtractor(item)}>
               {renderItem(item, index)}
             </li>
           ))}
         </ul>
       );
     }

     // 使用泛型组件
     const UserList = () => (
       <List
         items={users}
         renderItem={(user) => <span>{user.name}</span>}
         keyExtractor={(user) => user.id}
       />
     );

     const users: User[] = [
       { id: "1", name: "用户1", email:
     "user1@example.com" }
     ];

     export { };

     // 使用泛型
     const userRepository: Repository<User> = {
       async findById(id: string) {
         // 实际实现会连接数据库
         return null;
       },
       async create(userData) {
         return createUser(userData);
       },
       async update(id: string, data: Partial<User>) {
         // 实现更新逻辑
         throw new Error("Not implemented");
       },
       async delete(id: string) {
         // 实现删除逻辑
       }
     };

     // 5. 实用工具类型
     type UserKeys = keyof User; // "id" | "name" |
     "email" | "age" | "avatar"
     type RequiredUser = Required<User>; //
     所有属性变为必需
     type PartialUser = Partial<User>; // 所有属性变为可选
     type UserEmail = Pick<User, "email">; //
     只选择email属性
     type UserWithoutId = Omit<User, "id">; // 排除id属性

     export type { User, AdminUser, Status, ApiResponse,
     Repository };
     
      // 6. async/await - 处理异步操作的现代语法
     // 让异步代码看起来像同步代码，避免回调地狱

     // 传统的Promise写法
     function fetchUserOld(id: string): Promise<User> {
       return fetch(‘/api/users/${id}’)
         .then(response => response.json())
         .then(data => data.user)
         .catch(error => {
           console.error('获取用户失败:', error);
           throw error;
         });
     }

     // 使用async/await的现代写法
     async function fetchUser(id: string): Promise<User> {
       try {
         const response = await fetch(`/api/users/${id}`);
         const data = await response.json();
         return data.user;
       } catch (error) {
         console.error('获取用户失败:', error);
         throw error;
       }
     }

     // 基础概念解释
     // async: 声明一个异步函数，自动返回Promise
     // await: 等待Promise完成，暂停函数执行直到结果返回

     // 简单示例：延时函数
     function delay(ms: number): Promise<void> {
       return new Promise(resolve => setTimeout(resolve,
     ms));
     }

     async function example() {
       console.log('开始');
       await delay(1000); // 等待1秒
       console.log('1秒后');
       await delay(2000); // 再等待2秒
       console.log('3秒后');
     }

     // 并行执行 vs 串行执行
     async function serialExample() {
       console.log('串行执行开始');
       const user1 = await fetchUser("1");    //
     等待第一个完成
       const user2 = await fetchUser("2");    //
     然后获取第二个
       const user3 = await fetchUser("3");    //
     最后获取第三个
       console.log('串行执行完成', [user1, user2, user3]);
     }

     async function parallelExample() {
       console.log('并行执行开始');
       // 同时发起三个请求
       const [user1, user2, user3] = await Promise.all([
         fetchUser("1"),
         fetchUser("2"),
         fetchUser("3")
       ]);
       console.log('并行执行完成', [user1, user2, user3]);
     }

     // 错误处理
     async function handleErrors() {
       try {
         const user = await fetchUser("nonexistent");
         console.log(user);
       } catch (error) {
         if (error instanceof Error) {
           console.error('捕获到错误:', error.message);
         }
       }
     }

     // 实际项目中的应用：表单提交
     async function handleSubmit(formData: FormData) {
       const submitButton =
     document.getElementById('submit') as
     HTMLButtonElement;

       try {
         // 禁用按钮，防止重复提交
         submitButton.disabled = true;
         submitButton.textContent = '提交中...';

         // 1. 验证表单
         const validationResult = await
     validateForm(formData);
         if (!validationResult.isValid) {
           throw new Error(validationResult.message);
         }

         // 2. 上传文件（如果有）
         let fileUrl = '';
         const file = formData.get('avatar') as File;
         if (file && file.size > 0) {
           fileUrl = await uploadFile(file);
         }

         // 3. 创建用户
         const userData = {
           name: formData.get('name') as string,
           email: formData.get('email') as string,
           avatar: fileUrl
         };

         const newUser = await createUser(userData);

         // 4. 显示成功消息
         showSuccessMessage('用户创建成功！');

         return newUser;

       } catch (error) {
         console.error('提交失败:', error);
         showErrorMessage(error instanceof Error ?
     error.message : '未知错误');
         throw error;

       } finally {
         // 无论成功或失败都会执行
         submitButton.disabled = false;
         submitButton.textContent = '提交';
       }
     }

     // 数据库操作示例
     class UserService {
       async createUser(userData: CreateUserData):
     Promise<User> {
         // 1. 检查邮箱是否已存在
         const existingUser = await
     this.findByEmail(userData.email);
         if (existingUser) {
           throw new Error('邮箱已被注册');
         }

         // 2. 哈希密码
         const hashedPassword = await
     this.hashPassword(userData.password);

         // 3. 保存到数据库
         const user = await this.database.insert('users',
     {
           ...userData,
           password: hashedPassword,
           createdAt: new Date()
         });

         // 4. 发送欢迎邮件
         await
     this.emailService.sendWelcomeEmail(user.email,
     user.name);

         return user;
       }

       async findByEmail(email: string): Promise<User |
     null> {
         const result = await this.database.query(
           'SELECT * FROM users WHERE email = ?',
           [email]
         );
         return result[0] || null;
       }

       private async hashPassword(password: string):
     Promise<string> {
         // 模拟密码哈希
         await delay(100);
         return `hashed_${password}`;
       }

       private database = {
         async insert(table: string, data: any):
     Promise<User> {
           // 模拟数据库插入
           await delay(200);
           return { id: Date.now().toString(), ...data };
         },

         async query(sql: string, params: any[]):
     Promise<any[]> {
           // 模拟数据库查询
           await delay(100);
           return [];
         }
       };

       private emailService = {
         async sendWelcomeEmail(email: string, name:
     string): Promise<void> {
           console.log(`发送欢迎邮件给 ${email}‘);
           await delay(500);
         }
       };
     }

     // React组件中的异步操作
     function UserProfile({ userId }: { userId: string })
     {
       const [user, setUser] = useState<User |
     null>(null);
       const [loading, setLoading] = useState(true);
       const [error, setError] = useState<string |
     null>(null);

       useEffect(() => {
         async function loadUser() {
           try {
             setLoading(true);
             setError(null);
             const userData = await fetchUser(userId);
             setUser(userData);
           } catch (err) {
             setError(err instanceof Error ? err.message :
      '加载失败');
           } finally {
             setLoading(false);
           }
         }

         loadUser();
       }, [userId]);

       if (loading) return <div>加载中...</div>;
       if (error) return <div>错误: {error}</div>;
       if (!user) return <div>未找到用户</div>;

       return <div>{user.name}</div>;
     }

     // 辅助函数类型定义
     interface User {
       id: string;
       name: string;
       email: string;
       avatar?: string;
       createdAt?: Date;
     }

     interface CreateUserData {
       name: string;
       email: string;
       password: string;
     }

     interface ValidationResult {
       isValid: boolean;
       message: string;
     }

     // 模拟函数实现
     async function validateForm(formData: FormData):
     Promise<ValidationResult> {
       await delay(100);
       return { isValid: true, message: '' };
     }

     async function uploadFile(file: File):
     Promise<string> {
       await delay(1000);
       return `https://example.com/uploads/${file.name}`;
     }

     async function createUser(userData: any):
     Promise<User> {
       await delay(500);
       return { id: Date.now().toString(), ...userData };
     }

     function showSuccessMessage(message: string) {
       console.log('✅', message);
     }

     function showErrorMessage(message: string) {
       console.log('❌', message);
     }

     // React hooks (简化版)
     function useState<T>(initial: T): [T, (value: T) =>
     void] {
       // 简化实现
       return [initial, () => {}];
     }

     function useEffect(fn: () => void, deps: any[]) {
       // 简化实现
       fn();
     }

     export { };
```

● 🎯 TypeScript关键点总结：

  1. 类型安全：编译时捕获错误，减少运行时bug
  2. Interface vs Type：
    - Interface：适合定义对象形状，可扩展
    - Type：更灵活，支持联合类型、交叉类型
  3. 泛型：让代码可重用，如Repository<T>
  4. 工具类型：Partial、Omit、Pick等提高开发效率
  5. 事件类型：React.FormEvent、React.ChangeEvent等
  6. 联合类型 (|) - "或者"
  let value: string | number = "hello"; //
  可以是字符串或数字

  7. 箭头函数 (=>) - 更简洁的函数写法
  const add = (a: number, b: number) => a + b;

  8. 交叉类型 (&) - "和"
  type Person = {name: string} & {age: number}; //
  必须同时有name和age

  9. 泛型 (<T>) - 类型参数，让代码可重用
  function identity<T>(arg: T): T { return arg; }

  10. async/await - 处理异步操作

async function getData() {
const result = await fetch('/api/data');
return result.json();
}
```