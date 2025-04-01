# CS61C Lab02 完善笔记

## 1. Makefiles 深入解析
### 问题解答
1. **删除所有编译文件的目标**：`clean`
2. **编译所有程序的目标**：`all`
3. **当前编译器**：`gcc`
4. **C标准版本**：C99（`-std=c99`）
5. **引用变量**：`$(FOO)`
6. **Darwin系统**：macOS/OS X
7. **LFSR构建行号**：通过分析应定位到`$(LFSR_PROG): $(LFSR_OBJS)`规则定义的行（具体行号需查看原始文件）

### 关键知识点
- **自动变量**：
  - `$<` 表示第一个依赖文件
  - `$@` 表示目标文件
  - `$^` 表示所有依赖文件
- **条件指令**：`ifeq/else/endif` 实现跨平台兼容
- **后缀规则**：`.c.o` 定义通用编译规则
- **内存调试**：
  ```makefile
  valgrind --leak-check=full  # 完整内存泄漏检查
  --track-origins=yes        # 追踪未初始化值的来源
  ```

### 常见陷阱
- 忘记在clean目标前加`-`忽略错误
- 头文件依赖缺失导致修改后不重新编译
- 跨平台编译时工具链差异（如macOS需要dsymutil）

---

## 2. 位操作核心技巧
### 代码优化分析
```c
// 获取第n位
unsigned get_bit(unsigned x, unsigned n) {
    return (x >> n) & 1;  // 右移后取最后一位
}

// 设置第n位
void set_bit(unsigned *x, unsigned n, unsigned v) {
    *x = (*x & ~(1 << n)) | (v << n);  // 经典位操作模式
}

// 翻转位
void flip_bit(unsigned *x, unsigned n) {
    *x ^= (1 << n);  // 更简洁的异或实现
}
```

### 位操作要点
- **掩码构建**：
  - 设置位：`mask = 1 << n`
  - 清除位：`~mask`
- **复合操作**：
  - 设置位：`|=`
  - 清除位：`&= ~mask`
  - 翻转位：`^= mask`
- **位移陷阱**：
  - 无符号数保证逻辑移位
  - 有符号数右移是算术移位（补符号位）

---

## 3. 线性反馈移位寄存器原理
### LFSR实现分析
```c
void lfsr_calculate(uint16_t *reg) {
    unsigned MSB = (*reg >> 0) ^ (*reg >> 2) ^ (*reg >> 3) ^ (*reg >> 5);
    *reg = (MSB << 15) | (*reg >> 1);
}
```

### 关键概念
- **反馈多项式**：x^16 + x^5 + x^3 + x^2 + 1
- **最大长度序列**：2^n -1 个不重复状态（本实现为65535）
- **应用场景**：
  - 伪随机数生成
  - 加密算法
  - 通信编码

### 不同抽头位置效果
| 抽头组合      | 周期长度  | 随机性 |
| --------- | ----- | --- |
| (0,2,3,5) | 65535 | 优   |
| (0,1)     | 短     | 差   |

---

## 4. 动态内存管理最佳实践
### 正确实现要点
```c
vector_t *vector_new() {
    vector_t *retval = malloc(sizeof(vector_t));  // 分配结构体
    retval->data = malloc(sizeof(int));           // 分配数据空间
    if (!retval || !retval->data) {
        free(retval);  // 关键：释放可能分配的部分内存
        allocation_failed();
    }
    // ...初始化...
}
```

### 内存操作对比
| 错误类型   | 问题   | 正确做法      |
| ------ | ---- | --------- |
| 返回栈地址  | 悬垂指针 | malloc堆内存 |
| 浅拷贝结构体 | 双重释放 | 深拷贝数据     |
| 忘记释放   | 内存泄漏 | 配对free    |

### realloc使用模式
```c
void vector_set(...) {
    if (loc >= v->size) {
        int *new_data = realloc(v->data, (loc+1)*sizeof(int));
        if (!new_data) { /* 处理失败 */ }
        v->data = new_data;
        // 初始化新增元素...
    }
}
```

