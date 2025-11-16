# CSAPP Attack Lab 踩坑记：Ubuntu 22.04 下 ctarget Segmentation fault

## Overview
CS:APP 第三实验（Attack Lab）提供的预编译二进制文件 `ctarget` 因版本较旧，在 Ubuntu 22.04 系统上无法正常运行，直接触发段错误（SIGSEGV）。本文记录完整调试过程与两种高效解决方案，帮大家快速避坑。
![image.png](https://raw.githubusercontent.com/Frank-whw/img/main/blog/202511161804102.png)
## 问题复现与调试分析
尝试运行实验指令时，`ctarget` 直接崩溃，借助 gdb 调试获取关键日志：
```bash
Starting program: /home/frank/learning/csapp/10245501488/target1/ctarget < level1_raw.txt -q
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
Cookie: 0x59b997fa

Program received signal SIGSEGV, Segmentation fault.
0x00007ffff7dfa0d0 in __vfprintf_internal (s=0x7ffff7fa0780 <_IO_2_1_stdout_>, format=0x4032b4 "Type string:", ap=ap@entry=0x5561dbd8, mode_flags=mode_flags@entry=2) at ./stdio-common/vfprintf-internal.c:1244
1244    ./stdio-common/vfprintf-internal.c: No such file or directory.
(gdb) bt
#0  0x00007ffff7dfa0d0 in __vfprintf_internal (s=0x7ffff7fa0780 <_IO_2_1_stdout_>,
    format=0x4032b4 "Type string:", ap=ap@entry=0x5561dbd8, mode_flags=mode_flags@entry=2)
    at ./stdio-common/vfprintf-internal.c:1244
#1  0x00007ffff7eb9cbb in ___printf_chk (flag=flag@entry=1, format=format@entry=0x4032b4 "Type string:")
    at ./debug/printf_chk.c:33
#2  0x0000000000401f10 in printf (__fmt=0x4032b4 "Type string:")
    at /usr/include/x86_64-linux-gnu/bits/stdio2.h:105
#3  launch (offset=<optimized out>) at support.c:293
#4  0x0000000000401ffa in stable_launch (offset=<optimized out>) at support.c:340
Backtrace stopped: Cannot access memory at address 0x55686000
```

### 关键结论
从调用栈可见，崩溃点并非 `ctarget` 自身逻辑，而是进入 glibc 底层打印函数 `__vfprintf_internal` 后触发的。完整调用链为：
`stable_launch → launch → printf → ___printf_chk → __vfprintf_internal`

这说明问题根源不在实验攻击代码，而是 `ctarget` 与系统 glibc 存在兼容性冲突。

## 问题本质：栈对齐要求不兼容
通过 Google 检索到 Stack Overflow 相关问题（[CSAPP Attack Lab Phase1 Segmentation Fault on Ubuntu22.04](https://stackoverflow.com/questions/77568098/csapp-attack-lab-phase1-segmentation-fault-on-ubuntu22-04)），解释如下：
>`Using gdb, I found that it is a movaps %xmm1, 0x10(%rsp) instruction in my glibc that causes the failure. I guess that the align requirement of movaps is not satisfied, because the glibc version when compiling the ctarget is so old that the requirement that the size of each frame shall be a multiple of 16 have not been standard. Then I force the rsp to be a multiple of 16 before the program enters __printf_chk@plt in gdb, and it works out and confirm my reasoning.`
- Ubuntu 22.04 搭载的新版 glibc 中，`__printf_chk` 函数会调用 `movaps %xmm1, 0x10(%rsp)` 指令，该指令要求栈指针 `rsp` 必须满足 16 字节对齐（低 4 位为 0）。
- `ctarget` 是基于旧版 glibc 编译的，当时尚未强制“栈帧大小为 16 字节倍数”的标准，导致其调用 `printf` 时 `rsp` 未满足对齐要求，最终触发段错误。

## 两种解决方案（二选一即可）
### 方案一：手动编译自定义共享库（理解底层逻辑）
通过自定义 `__printf_chk` 函数替换系统默认版本，手动保证栈对齐，步骤如下：

1. 新建 `printf.c` 文件，写入适配代码：
```c
#include <stdio.h>
#include <stdarg.h>

// 自定义__printf_chk，绕开系统对齐敏感逻辑
int __printf_chk(int flag, const char *fmt, ...) {
  va_list ap;
  int ret;
  va_start(ap, fmt);          // 初始化可变参数列表
  ret = vfprintf(stdout, fmt, ap);  // 调用底层打印函数
  va_end(ap);                 // 释放可变参数列表
  return ret;
}
```

2. 编译生成汇编文件并添加对齐逻辑：
```bash
# 生成汇编文件printf.s
gcc -shared -fPIC -S printf.c -O2
```
编辑 `printf.s`：
- 函数开头添加：`pushq %rbp; movq %rsp, %rbp; andq $-0x10, %rsp; subq $-0x8, %rsp`（强制 rsp 16 字节对齐）
- 函数结尾 `addq $216, %rsp` 后添加：`leave`（恢复栈帧）

3. 生成最终共享库 `printf.so`：
```bash
gcc -shared -fPIC -o printf.so printf.s
```

4. 一键编译脚本（直接复制执行）：
```bash
# One-click create printf.c with compatibility code and compile to shared library
cat > printf.c << 'EOF'
#include <stdio.h>
#include <stdarg.h>

int __printf_chk(int flag, const char *fmt, ...) {
  va_list ap;
  int ret;
  va_start(ap, fmt);
  ret = vfprintf(stdout, fmt, ap);
  va_end(ap);
  return ret;
}
EOF

# Compile to generate printf.so (shared library)
gcc -shared -fPIC -S printf.c -O2
gcc -shared -fPIC -o printf.so printf.s

# Verify successful generation
if [ -f "printf.so" ]; then
  echo "printf.so generated successfully!"
  echo "Next step: LD_PRELOAD=./printf.so ./ctarget < level1_raw.txt -q"
else
  echo "Generation failed. Check if gcc is installed (run: sudo apt install gcc)"
fi
```

### 方案二：直接下载现成共享库（快速上手）
NJU 大佬 [Rijuyuezhu](https://blog.rijuyuezhu.top/posts/db646f34/) 提供了预编译好的 `printf.so`，可直接下载使用，省去编写代码和修改汇编的步骤。

这边我提供懒人脚本：
```bash
#!/bin/bash
# One-click download, verify and prepare printf.so for CSAPP Attack Lab

PRINTF_SO_URL="https://blog.rijuyuezhu.top/posts/db646f34/printf.so" 

echo "🔄 Downloading printf.so from $PRINTF_SO_URL..."
wget -q --show-progress -O printf.so "$PRINTF_SO_URL"

# 检查下载是否成功
if [ ! -f "printf.so" ]; then
  echo "❌ Download failed! Please check the URL or network connection."
  exit 1
fi

echo -e "\n✅ Download completed. Verifying compatibility..."
FILE_INFO=$(file ./printf.so)
if echo "$FILE_INFO" | grep -q "ELF 64-bit LSB shared object, x86-64"; then
  echo "✅ Architecture check passed (x86_64 compatible)"
else
  echo "❌ Incompatible architecture! Expected x86_64, got: $FILE_INFO"
  rm -f printf.so  
  exit 1
fi

chmod +x printf.so

echo -e "\n🎉 Ready to use! Run ctarget with:"
echo "LD_PRELOAD=./printf.so ./ctarget < level1_raw.txt -q"
```

## 最终运行
无论选择哪种方案，生成/下载 `printf.so` 后，执行以下命令即可正常运行 `ctarget`：
```bash
LD_PRELOAD=./printf.so ./ctarget < level1_raw.txt -q
```

成功运行截图：
![ctarget运行成功](https://raw.githubusercontent.com/Frank-whw/img/main/blog/202511161847180.png)

