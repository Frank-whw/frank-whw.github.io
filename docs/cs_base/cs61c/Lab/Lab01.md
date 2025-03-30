# Lab01: Debugging Tools & C Programming

## Exercise 1: See what you can C
### 目标
学习C语言宏定义（Macro）的基础用法，理解预处理阶段的作用。
### 关键概念
- **宏定义**：通过 `#define` 替换文本，分为无参宏和带参宏。
  ```c
  #define PI 3.14              // 无参宏
  #define SQUARE(x) ((x)*(x))  // 带参宏（注意括号避免运算符优先级问题）
  ```
- **调试宏**：利用宏输出调试信息，结合条件编译控制是否启用：
  ```c
  #ifdef DEBUG
  #define LOG(msg) printf("DEBUG: %s\n", msg)
  #else
  #define LOG(msg)
  #endif
  ```
- **防止头文件重复包含**：
  ```c
  #ifndef HEADER_H
  #define HEADER_H
  // 头文件内容
  #endif
  ```

---

## Exercise 2: Catch those bugs (GDB/cgdb 实战)
### 目标
掌握GDB调试器核心命令，理解断点、单步执行、变量监控等操作。

### 核心命令对比表
| 操作                | GDB命令            | 简写 | 说明                         |
|---------------------|--------------------|------|------------------------------|
| 设置参数            | `set args <...>`   | -    | 程序启动参数                 |
| 设置断点            | `break <loc>`      | `b`  | 函数名/行号/文件:行号        |
| 单步执行（不进入函数）| `next`             | `n`  | 执行下一行代码               |
| 单步进入函数        | `step`             | `s`  | 进入函数内部                 |
| 继续运行            | `continue`         | `c`  | 运行到下一个断点             |
| 打印变量            | `print <expr>`     | `p`  | 支持表达式如 `p *(arr+5)`    |
| 自动显示变量        | `display <var>`    | -    | 每步后自动显示值             |
| 查看局部变量        | `info locals`      | -    | 当前栈帧所有局部变量         |
| 退出GDB             | `quit`             | `q`  | 退出调试器                   |

### 高级技巧
- **条件断点**：当变量满足条件时暂停
  ```gdb
  break 20 if i == 5
  ```
- **修改变量值**：动态调试时修改运行状态
  ```gdb
  set variable x = 10
  ```
- **查看内存布局**：
  ```gdb
  x/8wx &array  # 以16进制查看数组前8个字
  ```
- **cgdb优势**：分屏界面（上代码/下命令），支持Vi快捷键（按`Esc`进入代码窗口，方向键浏览）。

---

## Exercise 3: Debugging with User Input (输入重定向)
### 目标
避免调试交互式程序时手动输入，通过重定向预定义输入。
### 操作步骤
1. **创建输入文件** `input.txt`：
   ```
   John
   CS61C
   ```
2. **命令行重定向**：
   ```bash
   ./int_hello < input.txt
   ```
3. **在GDB中使用重定向**：
   ```gdb
   (gdb) run < input.txt
   # 或提前设置参数
   (gdb) set args < input.txt
   (gdb) run
   ```

### 原理
- **`<` 操作符**：将文件内容重定向到程序的标准输入（stdin）。
- **管道技巧**：结合 `echo` 快速测试
  ```bash
  echo -e "John\nCS61C" | ./int_hello
  ```

---

## Exercise 4: Valgrind'ing away (内存检测)
### 目标
使用Valgrind检测内存错误（如越界访问、内存泄漏）。
### 关键命令
```bash
valgrind --tool=memcheck --leak-check=full ./your_program
```
### 常见错误类型
1. **Invalid read/write**：越界访问内存
   ```c
   int arr[5];
   arr[5] = 10;  // 越界（合法索引0-4）
   ```
2. **Memory leak**：未释放动态分配的内存
   ```c
   int *p = malloc(10 * sizeof(int));
   // 忘记 free(p);
   ```
3. **Use of uninitialized value**：使用未初始化变量
   ```c
   int x;
   printf("%d", x);  // x未初始化
   ```

### Valgrind输出解读
- **Definitely lost**：明确的内存泄漏（需优先修复）。
- **Indirectly lost**：因结构体嵌套导致泄漏。
- **Suppression**：通过配置文件忽略第三方库的误报。

---

## Exercise 5: Pointers and Structures in C (链表环检测)
### 目标
实现快慢指针算法检测链表环。
### 算法思路
```c
bool ll_has_cycle(node *head) {
    node *fast = head, *slow = head;
    while (fast && fast->next) {
        slow = slow->next;
        fast = fast->next->next;
        if (slow == fast) {
            return true;
        }
    }
    return false;
}
```
### 测试技巧
- **编译命令**：
  ```bash
  gcc -g -o test_ll_cycle test_ll_cycle.c ll_cycle.c
  ```
- **GDB调试指针**：
  ```gdb
  (gdb) p *slow   # 查看节点内容
  (gdb) x/3x slow # 查看内存地址处的3个字（16进制）
  ```

---

## 附录：常用调试策略
1. **最小化复现**：将问题代码剥离到最小可编译示例。
2. **二分法排查**：通过注释代码逐步缩小问题范围。
3. **防御性编程**：使用 `assert()` 验证假设条件。
4. **日志输出**：在关键路径添加 `printf` 调试（提交前移除）。

