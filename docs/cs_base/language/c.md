# C
## 1.指针
### 1.1 基本知识

- pointer是用来存储**内存地址**的变量
- 内存地址直接指向存在该地址的对象的值
- 定义指针变量时必须带`*`，给指针变量赋值时不能带`*`
```c
#include <stdio.h>
int main(){
    int a = 15;
    int *p = &a;
    printf("%d, %d\n", a, *p);  //两种方式都可以输出a的值
    return 0;
}
```
### 1.2数组指针
```c
#include <stdio.h>
int main(){
    int arr[] = { 99, 15, 100, 888, 252 };
    int len = sizeof(arr) / sizeof(int);  //求数组长度
    int i;
    for(i=0; i<len; i++){
        printf("%d  ", *(arr+i) );  //*(arr+i)等价于arr[i]
    }
    printf("\n");
    return 0;
}
```
### 1.3字符串指针
```c
#include <stdio.h>
#include <string.h>
int main(){
    char *str = "http://c.biancheng.net";
    int len = strlen(str), i;
    //直接输出字符串
    printf("%s\n", str);
    //使用*(str+i)
    for(i=0; i<len; i++){
        printf("%c", *(str+i));
    }
    printf("\n");
    //使用str[i]
    for(i=0; i<len; i++){
        printf("%c", str[i]);
    }
    printf("\n");
    return 0;
}
```
- 区别是：字符数组和字符串指针(也叫**字符串常量**）在内存中的**存储区域**不同，前者在全局数据区或栈区，后者在常量区。前者有读取和写入的权限，而后者只有读取权限，没有写入权限
```c
#include <stdio.h>
int main(){
    char *str = "Hello World!";
    str = "I love C!";  //正确
    str[3] = 'P';  //错误

    return 0;
}
```
### 1.4指针变量作为函数参数
```c
#include <stdio.h>

void swap(int *p1, int *p2){ //传入的是指针变量，所以我可以修改这个内存上的值
    int temp;  //临时变量
    temp = *p1;
    *p1 = *p2;
    *p2 = temp;
}

int main(){
    int a = 66, b = 99;
    swap(&a, &b);
    printf("a = %d, b = %d\n", a, b);
    return 0;
}
```
- 数组是一系列数据的集合，**无法**通过参数将它们一次性传递到函数内部，如果希望在函数内部操作数组，必须传递数组指针
```c
#include <stdio.h>

//参数 intArr 仅仅是一个数组指针，在函数内部无法通过这个指针获得数组长度，必须将数组长度作为函数参数传递到函数内部。
int max(int *intArr, int len){
    int i, maxValue = intArr[0];  //假设第0个元素是最大值
    for(i=1; i<len; i++){
        if(maxValue < intArr[i]){
            maxValue = intArr[i];
        }
    }
   
    return maxValue;
}

int main(){
    int nums[6], i;
    int len = sizeof(nums)/sizeof(int);
    //读取用户输入的数据并赋值给数组元素
    for(i=0; i<len; i++){
        scanf("%d", nums+i);
    }
    printf("Max value is %d!\n", max(nums, len));

    return 0;
}
```
- C语言为什么不允许直接传递数组的所有元素，而必须传递数组指针呢？   
	**参数的传递本质上是一次赋值的过程**，赋值就是对内存进行拷贝。所谓内存拷贝，是指将一块内存上的数据复制到另一块内存上。数据的数量没有限制，可能很少，也可能成千上万，对它们进行内存拷贝有可能是一个漫长的过程，会严重拖慢程序的效率，为了防止技艺不佳的程序员写出低效的代码，C语言没有从**语法上**支持数据集合的直接赋值。
### 1.5指针函数
- 函数的返回值是一个**指针**（地址）
```c
#include <stdio.h>
#include <string.h>

char *strlong(char *str1, char *str2){
    if(strlen(str1) >= strlen(str2)){
        return str1;
    }else{
        return str2;
    }
}

int main(){
    char str1[30], str2[30], *str;
    gets(str1);
    gets(str2);
    str = strlong(str1, str2);
    printf("Longer string: %s\n", str);

    return 0;
}
```
- 用指针作为函数返回值时需要注意的一点是，函数运行结束后会**销毁在它内部定义的所有局部数据**，包括局部变量、局部数组和形式参数，函数返回的指针请尽量不要指向这些数据，C语言没有任何机制来保证这些数据会一直有效，它们在后续使用过程中可能会引发运行时错误。
- 这里所谓的销毁**并不是**将局部数据所占用的内存全部抹掉，而是**程序放弃对它的使用权限**，弃之不理，后面的代码可以随意使用这块内存。对于上面的两个例子，func() 运行结束后 n 的内存依然保持原样，值还是 100，如果使用及时也能够得到正确的数据，如果有其它函数被调用就会覆盖这块内存，得到的数据就失去了意义。
### 1.6二级指针
- 指向指针的指针
- 指针变量也是一种变量，也会占用存储空间，也可以使用`&`获取它的地址。C语言不限制指针的级数，每增加一级指针，在定义指针变量时就得增加一个星号`*`。p1 是一级指针，指向普通类型的数据，定义时有一个`*`；p2 是二级指针，指向一级指针 p1，定义时有两个`*`。
```c
#include <stdio.h>

int main(){
    int a =100;
    int *p1 = &a;
    int **p2 = &p1;
    int ***p3 = &p2;

    printf("%d, %d, %d, %d\n", a, *p1, **p2, ***p3);
    printf("&p2 = %#X, p3 = %#X\n", &p2, p3);
    printf("&p1 = %#X, p2 = %#X, *p3 = %#X\n", &p1, p2, *p3);
    printf(" &a = %#X, p1 = %#X, *p2 = %#X, **p3 = %#X\n", &a, p1, *p2, **p3);
    return 0;
}
```
### 1.7指针数组
- 如果一个数组中的所有元素保存的都是**指针**，即称之为**指针数组**。
```c
#include <stdio.h>
int main(){
    int a = 16, b = 932, c = 100;
    //定义一个指针数组
    int *arr[3] = {&a, &b, &c};//也可以不指定长度，直接写作 int *arr[]
    //定义一个指向指针数组的指针
    int **parr = arr;
    printf("%d, %d, %d\n", *arr[0], *arr[1], *arr[2]);
    printf("%d, %d, %d\n", **(parr+0), **(parr+1), **(parr+2));

    return 0;
}
```
### 1.8二维数组指针

为了更好的理解指针和二维数组的关系，我们先来定义一个指向 a 的指针变量 p：
`int (*p)[4] = a;`
括号中的`*`表明 p 是一个指针，它指向一个数组，数组的类型为`int [4]`，这正是 a 所包含的每个一维数组的类型。  
`[ ]`的优先级高于`*`，`( )`是必须要加的，如果赤裸裸地写作`int *p[4]`，那么应该理解为`int *(p[4])`，p 就成了一个指针数组，而不是二维数组指针。
- **数组名 a 在表达式中也会被转换为和 p 等价的指针！**
```c
#include <stdio.h>
int main(){
    int a[3][4] = { {0, 1, 2, 3}, {4, 5, 6, 7}, {8, 9, 10, 11} };
    int (*p)[4] = a;
    printf("%d\n", sizeof(*(p+1)));
	//运行结果：16
    return 0;
}
```
- 说明`*(p+1)`表示整个第一行的数据，4 * 4=16
- `*(*(p+1)+1)`表示第 1 行第 1 个元素的值。很明显，增加一个 * 表示取地址上的数据。
- 所以有以下等价关系：
```
a+i == p+i  
a[i] == p[i] == *(a+i) == *(p+i)  
a[i][j] == p[i][j] == *(a[i]+j) == *(p[i]+j) == *(*(a+i)+j) == *(*(p+i)+j)
```
- 使用指针遍历二维数组
```c
#include <stdio.h>
int main(){
    int a[3][4]={0,1,2,3,4,5,6,7,8,9,10,11};
    int(*p)[4];
    int i,j;
    p=a;
    for(i=0; i<3; i++){
        for(j=0; j<4; j++) printf("%2d  ",*(*(p+i)+j));
        printf("\n");
    }
    return 0;
}
```
- 指针数组和二维数组指针的区别：
	`1. int *(p1[5]); //指针数组，可以去掉括号直接写作 int *p1[5];`
	`2. int (*p2)[5]; //二维数组指针，不能去掉括号`
### 1.9函数指针
- 一个函数总是占用**一段连续的内存区域**，函数名在表达式中有时也会被转换为该函数所在内存区域的首地址，这和数组名非常类似。我们可以把函数的这个首地址（或称入口地址）赋予一个指针变量，使**指针变量指向函数所在的内存区域**，然后通过指针变量就可以找到并调用该函数。这种指针就是**函数指针**。
- 定义形式为`returnType (*pointerName)(param list)`
	- `( )`的优先级高于`*`，第一个括号不能省略，如果写作`returnType *pointerName(param list);`就成了函数原型，它表明函数的返回值类型`returnType *`。
	- 【实例】用指针来实现对函数的调用
```c
#include <stdio.h>
//返回两个数中较大的一个
int max(int a, int b){
    return a>b ? a : b;
}
int main(){
    int x, y, maxval;
    //定义函数指针
    int (*pmax)(int, int) = max;  //也可以写作int (*pmax)(int a, int b)
    printf("Input two numbers:");
    scanf("%d %d", &x, &y);
    maxval = (*pmax)(x, y);
    printf("Max value: %d\n", maxval);

    return 0;
}
```

### 1.10指针总结
- **指针**（Pointer）就是内存的地址，C语言允许用一个变量来存放指针，这种变量称为指针变量。指针变量可以存放基本类型数据的地址，也可以存放数组、函数以及其他指针变量的地址。  
- 程序在运行过程中需要的是**数据和指令的地址**，变量名、函数名、字符串名和数组名在本质上是一样的，它们都是地址的助记符：在编写代码的过程中，我们认为变量名表示的是数据本身，而函数名、字符串名和数组名表示的是代码块或数据块的首地址；程序被编译和链接后，这些名字都会消失，取而代之的是它们**对应的地址**。

- 常见指针变量的定义

| 定  义         | 含  义                                      |
| ------------ | ----------------------------------------- |
| int *p;      | p 可以指向 int 类型的数据，也可以指向类似 int arr[n] 的数组。  |
| int **p;     | p 为二级指针，指向 int * 类型的数据。                   |
| int *p[n];   | p 为指针数组。[ ] 的优先级高于 *，所以应该理解为 int *(p[n]); |
| int (*p)[n]; | p 为二维数组指针。                                |
| int *p();    | p 是一个函数，它的返回值类型为 int *。                   |
| int (*p)();  | p 是一个函数指针，指向原型为 int func() 的函数。           |
1. 指针变量可以进行**加减运算**，例如`p++`、`p+i`、`p-=i`。指针变量的加减运算并不是简单的加上或减去一个整数，而是跟指针指向的数据类型有关。
2. 给指针变量赋值时，要将一份**数据的地址**赋给它，不能直接赋给一个整数，例如`int *p = 1000;`是没有意义的，使用过程中一般会导致程序崩溃。
3. 使用指针变量之前一定要**初始化**，否则就不能确定指针指向哪里，如果它指向的内存没有使用权限，程序就崩溃了。对于暂时没有指向的指针，建议赋值`NULL`。
4. 两个指针变量可以相减。如果两个指针变量指向同一个数组中的某个元素，那么相减的结果就是两个指针之间相差的**元素个数**。
5. 数组也是有类型的，数组名的本意是表示一组类型相同的数据。在定义数组时，或者和 sizeof、& 运算符一起使用时数组名才表示整个数组，表达式中的数组名会被转换为**一个指向数组的指针**。

## 2.结构体
### 2.1结构体的定义
在C语言中，可以使用**结构体**（Struct)来存放一组不同类型的数据。结构体的定义形式为：
```c
struct 结构体名{  
    结构体所包含的变量或数组  
};
```
```C
struct stu{
    char *name;  //姓名
    int num;  //学号
    int age;  //年龄
    char group;  //所在学习小组
    float score;  //成绩
};
```
## 2.2成员的获取和赋值
- 数组使用下标`[ ]`获取单个元素，结构体使用点号`.`获取单个成员。`结构体变量名.成员名;`
```c
#include <stdio.h>
int main(){
    struct{
        char *name;  //姓名
        int num;  //学号
        int age;  //年龄
        char group;  //所在小组
        float score;  //成绩
    } stu1;

    //给结构体成员赋值
    stu1.name = "Tom";
    stu1.num = 12;
    stu1.age = 18;
    stu1.group = 'A';
    stu1.score = 136.5;

    //读取结构体成员的值
    printf("%s的学号是%d，年龄是%d，在%c组，今年的成绩是%.1f！\n", stu1.name, stu1.num, stu1.age, stu1.group, stu1.score);
    //运行结果：  
	//Tom的学号是12，年龄是18，在A组，今年的成绩是136.5！
    return 0;
}
```
- **结构体是一种自定义的数据类型，是创建变量的模板，不占用内存空间；结构体变量才包含了实实在在的数据，需要内存空间来存储。**

### 2.3结构体数组
```c
struct stu{
    char *name;  //姓名
    int num;  //学号
    int age;  //年龄
    char group;  //所在小组 
    float score;  //成绩
}class[5] = {
    {"Li ping", 5, 18, 'C', 145.0},
    {"Zhang ping", 4, 19, 'A', 130.5},
    {"He fang", 1, 18, 'A', 148.5},
    {"Cheng ling", 2, 17, 'F', 139.0},
    {"Wang ming", 3, 17, 'B', 144.5}
};
```
或者
```c
struct stu{
    char *name;  //姓名
    int num;  //学号
    int age;  //年龄
    char group;  //所在小组 
    float score;  //成绩
}class[5];
```
或者
```c
struct stu{
    char *name;  //姓名
    int num;  //学号
    int age;  //年龄
    char group;  //所在小组 
    float score;  //成绩
}class[] = {                   //不给出数组的长度
    {"Li ping", 5, 18, 'C', 145.0},
    {"Zhang ping", 4, 19, 'A', 130.5},
    {"He fang", 1, 18, 'A', 148.5},
    {"Cheng ling", 2, 17, 'F', 139.0},
    {"Wang ming", 3, 17, 'B', 144.5}
};
```
### 2.4结构体指针
#### 2.4.1基本知识
- 一个指针变量指向结构体
```c
//结构体
struct stu{
    char *name;  //姓名
    int num;  //学号
    int age;  //年龄
    char group;  //所在小组
    float score;  //成绩
} stu1 = { "Tom", 12, 18, 'A', 136.5 };
//结构体指针
struct stu *pstu = &stu1;
```
- 结构体变量名和数组名**不同**，数组名在表达式中会被转换为数组指针，而结构体变量名不会，**无论在任何表达式中它表示的都是整个集合本身**，要想取得结构体变量的地址，**必须**在前面加`&`，所以给 pstu 赋值只能写作：`struct stu *pstu = &stu1;`
- 结构体和结构体**变量**是两个不同的概念：结构体是一种**数据类型**，是一种**创建变量的模板**，编译器不会为它分配内存空间，就像 int、float、char 这些关键字本身不占用内存一样；结构体变量才包含实实在在的数据，才需要内存来存储。下面的写法是错误的，不可能去取一个结构体名的地址，也不能将它赋值给其他变量：`struct stu *pstu = &stu; `or`struct stu *pstu = stu;`
#### 2.4.2获取结构体成员
- 通过结构体指针可以获取结构体成员，一般形式为：`(*pointer).memberName`或者：`pointer->memberName`
- 第一种写法中，`.`的优先级高于`*`，`(*pointer)`两边的括号不能少。如果去掉括号写作`*pointer.memberName`，那么就等效于`*(pointer.memberName)`，这样意义就完全不对了。  
- 第二种写法中，`->`是一个新的运算符，习惯称它为“箭头”，有了它，可以通过结构体指针直接取得结构体成员；这也是`->`在C语言中的唯一用途。
```c
#include <stdio.h>
int main(){
    struct{
        char *name;  //姓名
        int num;  //学号
        int age;  //年龄
        char group;  //所在小组
        float score;  //成绩
    } stu1 = { "Tom", 12, 18, 'A', 136.5 }, *pstu = &stu1;

    //读取结构体成员的值
    printf("%s的学号是%d，年龄是%d，在%c组，今年的成绩是%.1f！\n", (*pstu).name, (*pstu).num, (*pstu).age, (*pstu).group, (*pstu).score);
    printf("%s的学号是%d，年龄是%d，在%c组，今年的成绩是%.1f！\n", pstu->name, pstu->num, pstu->age, pstu->group, pstu->score);

    return 0;
}
```
#### 2.4.3结构体指针作为函数参数
- 结构体变量名代表的是**整个集合本身**，作为函数参数时传递的整个集合，也就是所有成员，而不是像数组一样被编译器转换成一个指针。如果结构体成员较多，尤其是成员为数组时，传送的时间和空间开销会很大，影响程序的运行效率。所以最好的办法就是使用结构体指针，这时**由实参传向形参的只是一个地址**，非常快速。
```c
#include <stdio.h>

struct stu{
    char *name;  //姓名
    int num;  //学号
    int age;  //年龄
    char group;  //所在小组
    float score;  //成绩
}stus[] = {
    {"Li ping", 5, 18, 'C', 145.0},
    {"Zhang ping", 4, 19, 'A', 130.5},
    {"He fang", 1, 18, 'A', 148.5},
    {"Cheng ling", 2, 17, 'F', 139.0},
    {"Wang ming", 3, 17, 'B', 144.5}
};

void average(struct stu *ps, int len);

int main(){
    int len = sizeof(stus) / sizeof(struct stu);
    average(stus, len);
    return 0;
}

void average(struct stu *ps, int len){
    int i, num_140 = 0;
    float average, sum = 0;
    for(i=0; i<len; i++){
        sum += (ps + i) -> score;
        if((ps + i)->score < 140) num_140++;
    }
    printf("sum=%.2f\naverage=%.2f\nnum_140=%d\n", sum, sum/5, num_140);
}
```
### 2.5枚举类型
- 定义形式`enum typeName{valueName1, valueName2, .....};`
例如，列出一个星期有几天：
	1. `enum week{ Mon, Tues, Wed, Thurs, Fri, Sat, Sun };`
	2. `enum week{ Mon = 1, Tues = 2, Wed = 3, Thurs = 4, Fri = 5, Sat = 6, Sun = 7 };`
	3. `enum week{ Mon = 1, Tues, Wed, Thurs, Fri, Sat, Sun };`
	- 第3种最为简单，枚举值从1开始递增
- 也可以在定义枚举类型的同时定义变量：
	`enum week{ Mon = 1, Tues, Wed, Thurs, Fri, Sat, Sun } a, b, c;`
- 有了枚举变量，就可以把列表中的值赋给它：
	1. `enum week{ Mon = 1, Tues, Wed, Thurs, Fri, Sat, Sun };
	2. `enum week a = Mon, b = Wed, c = Sat;
	或者：
	 `enum week{ Mon = 1, Tues, Wed, Thurs, Fri, Sat, Sun } a = Mon, b = Wed, c = Sat;
- 示例：
```c
#include <stdio.h>
int main(){
    enum week{ Mon = 1, Tues, Wed, Thurs, Fri, Sat, Sun } day;
    scanf("%d", &day);
    switch(day){
        case Mon: puts("Monday"); break;
        case Tues: puts("Tuesday"); break;
        case Wed: puts("Wednesday"); break;
        case Thurs: puts("Thursday"); break;
        case Fri: puts("Friday"); break;
        case Sat: puts("Saturday"); break;
        case Sun: puts("Sunday"); break;
        default: puts("Error!");
    }
    return 0;
}
```
- case 关键字后面必须是一个整数，或者是结果为整数的表达式，但不能包含任何变量，正是由于 `Mon、Tues、Wed `这些名字最终会被替换成一个整数，所以它们才能放在 `case` 后面。
- `Mon、Tues、Wed` 等都是**常量**，不能对它们赋值，只能将它们的值赋给其他的变量。  
- 枚举和宏其实非常类似：宏在**预处理阶段**将名字替换成对应的值，枚举在**编译阶段**将名字替换成对应的值。我们可以将枚举理解为编译阶段的宏。
## 3.文件
### 3.1 基本概念
- 通常把显示器称为标准输出文件，printf 就是向这个文件输出数据；
- 通常把键盘称为标准输入文件，scanf 就是从这个文件读取数据。

| 文件     | 硬件设备                                                 |
| ------ | ---------------------------------------------------- |
| stdin  | 标准输入文件，一般指键盘；scanf()、getchar() 等函数默认从 stdin 获取输入。    |
| stdout | 标准输出文件，一般指显示器；printf()、putchar() 等函数默认向 stdout 输出数据。 |
| stderr | 标准错误文件，一般指显示器；perror() 等函数默认向 stderr 输出数据（后续会讲到）。    |
| stdprn | 标准打印文件，一般指打印机。                                       |
## 3.2 文件流
- 所有的文件（保存在磁盘）都要载入内存才能处理，所有的数据必须写入文件（磁盘）才不会丢失。
- 数据在文件和内存之间传递的过程叫做**文件流**，类似水从一个地方流动到另一个地方。
- 数据从文件复制到内存的过程叫做**输入流**，从内存保存到文件的过程叫做**输出流**。
- 我们把数据在数据源和程序（内存）之间传递的过程叫做数据流(Data Stream)。相应的，数据从数据源到程序（内存）的过程叫做**输入流**(Input Stream)，从程序（内存）到数据源的过程叫做**输出流**(Output Stream)。
- 打开文件就是打开了一个流。
### 3.3 打开文件
#### 3.3.1 基本知识
- 使用 `<stdio.h>` 头文件中的` fopen() `函数即可打开文件，它的用法为：
	`FILE *fopen(char *filename, char *mode);`
	- `filename`为文件名（包括文件路径），`mode`为打开方式，它们都是字符串。
#### 3.3.2`fopen()`函数的返回值
- `fopen()`会获取文件信息，包括文件名、文件状态、当前读写位置等，并将这些信息保存到一个 FILE 类型的**结构体变量**中，然后将该变量的地址返回。  
- `FILE`是 `<stdio.h>`头文件中的一个结构体，它专门用来保存文件信息。我们不用关心 FILE 的具体结构，只需要知道它的用法就行。  
- 如果希望接收 `fopen()`的返回值，就需要定义一个 FILE 类型的指针。
	例如：  
	`FILE *fp = fopen("demo.txt", "r");`
	- 表示以“只读”方式打开当前目录下的 demo.txt 文件，并使` fp `指向该文件，这样就可以通过` fp `来操作 `demo.txt `了。`fp `通常被称为文件指针。
##### 判断文件是否打开成功
- 打开文件出错时，`fopen()` 将返回一个空指针，也就是 NULL，我们可以利用这一点来判断文件是否打开成功，请看下面的代码：
```c
FILE *fp;
if( (fp=fopen("D:\\demo.txt","rb")) == NULL ){
    printf("Fail to open file!\n");
    exit(0);  //退出程序（结束程序）
}
```
- 我们通过判断` fopen()`的返回值是否和 NULL 相等来判断是否打开失败：如果 `fopen()`的返回值为 NULL，那么 `fp`的值也为  NULL，此时 if 的判断条件成立，表示文件打开失败。
#### 3.3.3fopen() 函数的打开方式
- 不同的操作需要不同的**文件权限**。例如，只想**读取**文件中的数据的话，“只读”权限就够了；既想读取又想写入数据的话，“读写”权限就是必须的了。  
- 另外，文件也有不同的类型，按照数据的存储方式可以分为二进制文件和文本文件，它们的操作细节是不同的。   
- 在调用 `fopen()` 函数时，这些信息都必须提供，称为“**文件打开方式**”。最基本的文件打开方式有以下几种：


| 打开方式             | 说明                                                                                                         |
| ---------------- | ---------------------------------------------------------------------------------------------------------- |
| "r"              | 以“只读”方式打开文件。只允许读取，不允许写入。文件必须存在，否则打开失败。                                                                     |
| "w"              | 以“写入”方式打开文件。如果文件不存在，那么创建一个新文件；如果文件存在，那么清空文件内容（相当于删除原文件，再创建一个新文件）。                                          |
| "a"              | 以“追加”方式打开文件。如果文件不存在，那么创建一个新文件；如果文件存在，那么将写入的数据追加到文件的末尾（文件原有的内容保留）。                                          |
| "r+"             | 以“读写”方式打开文件。既可以读取也可以写入，也就是随意更新文件。文件必须存在，否则打开失败。                                                            |
| "w+"             | 以“写入/更新”方式打开文件，相当于`w`和`r+`叠加的效果。既可以读取也可以写入，也就是随意更新文件。如果文件不存在，那么创建一个新文件；如果文件存在，那么清空文件内容（相当于删除原文件，再创建一个新文件）。 |
| "a+"             | 以“追加/更新”方式打开文件，相当于a和r+叠加的效果。既可以读取也可以写入，也就是随意更新文件。如果文件不存在，那么创建一个新文件；如果文件存在，那么将写入的数据追加到文件的末尾（文件原有的内容保留）。     |


- 调用 `fopen()`函数时必须指明读写权限，但是可以不指明读写方式（此时默认为`"t"`）。  
- 读写权限和读写方式可以组合使用，但是必须将读写方式放在读写权限的中间或者尾部（换句话说，不能将读写方式放在读写权限的开头）。例如：
	- 将读写方式放在读写权限的末尾："rb"、"wt"、"ab"、"r+b"、"w+t"、"a+t"
	- 将读写方式放在读写权限的中间："rb+"、"wt+"、"ab+"

整体来说，文件打开方式由 `r、w、a、t、b、+`六个字符拼成，各字符的含义是：
- r(read)：读
- w(write)：写
- a(append)：追加
- t(text)：文本文件
- b(binary)：二进制文件
- +：读和写

### 3.4关闭文件
- 文件一旦使用完毕，应该用 `fclose()`函数把文件关闭，以释放相关资源，避免数据丢失。`fclose()`的用法为：
	`int fclose(FILE *fp);`
	- `fp` 为文件指针。
- `fclose(fp);
- 文件正常关闭时，fclose() 的返回值为0，如果返回非零值则表示有错误发生。  

### 3.5实例演示

最后，我们通过一段完整的代码来演示 fopen 函数的用法，这个例子会一行一行地读取文本文件的所有内容：
```c
#include <stdio.h>
#include <stdib.h>
#define N 100
int main(){
	FILE *fp;
	char str[N + 1];
	//判断文件是否打开失败
	if ((fp = fopen("d:\\demo.txt", "rt")) == NULL) {
		puts("Fail to open file!");
		exit(0);
	}
	//循环读取文件的每一行数据
    while( fgets(str, N, fp) != NULL ) {
        printf("%s", str);
    }
   
    //操作结束后关闭文件
    fclose(fp);
    return 0;
}
```
