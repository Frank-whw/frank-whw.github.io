# Gitlet之我见
## what is Gitlet
A **version-control system** is essentially a backup system for related collections of files. Gitlet is a simple version-control system that mimics some core functionalities of Git.


# the commands
##  init
1. 自动生产一个commit文件 没有别的文件并且有提交信息
2. 有个单一的分支 master ，points to the initial commit
3. timestamp?
	要判断是不是已经init过了
	
---

## add
1. **把文件添加到暂存区**：
   - 当你调用 `add` 命令时，它会把文件当前的内容复制到暂存区（通常在 `.gitlet` 目录中存放）。
   - **暂存区**就是一个临时存放你想提交的文件修改的地方。

2. **重复添加的处理**：
   - 如果一个文件已经被添加（暂存）过，再次调用 `add` 会用**新版本的文件内容覆盖**暂存区中已有的版本。

3. **文件没有变化时不需要添加**：
   - 如果工作目录中的文件和上一次提交的版本**完全一样**，就不需要再次暂存这个文件。因此你需要比较：
     - 当前工作目录中的文件（未提交的版本）和
     - 当前提交中的文件（最近一次提交的版本）
   
   - 如果两者相同，直接跳过这个文件，不需要把它加入暂存区。

4. **处理已经暂存的文件**：
   - 如果文件已经被暂存了，但后来被修改回了和提交中一样的状态，你需要把它**从暂存区移除**，因为不再需要提交这个文件。

5. **取消删除的暂存**：
   - 如果这个文件之前被标记为“删除”（用 `gitlet rm` 暂存删除），但现在你用 `add` 重新添加了文件，那么它将不再被标记为删除，你需要**取消这个删除的暂存**。

---

## commit
- **默认情况下**，每次提交的文件快照跟上一次提交的快照是一样的，也就是说文件版本不会自动更新。
- 只有那些已经被**暂存（staged**的文件会在新的提交中更新为暂存的版本。
- **新文件**（还没有被追踪的文件）如果暂存了，新的提交会开始追踪它们。
- 如果有文件被**rm命令**标记为删除，它们就不会再被新的提交追踪。

当你把文件**暂存**（staging）好后，提交时只会保存这些暂存的内容，**任何在暂存之后对文件的更改都不会被提交命令包含**。也就是说，提交（commit）操作只记录暂存区中的文件状态，不会管你在暂存后做了什么修改。

举个例子，如果你用Unix系统的`rm`命令删除了一个文件（而不是使用Gitlet的删除命令），Gitlet不会意识到这个删除操作，因为这个变化没有被暂存（staged）。因此，下一次提交时，这个被删除的文件的旧版本仍然会出现在提交记录中，**文件不会被真正删除**。

简化来说就是：

- 提交时只看**暂存区**的内容。
- 在暂存之后对文件做的任何修改，不会影响本次提交。
- 如果你没有用Gitlet的命令删除文件，而是用系统命令直接删除，Gitlet不会知道，提交时还是会保存旧的文件版本。

each commit should contain the date and time it was made
### 核心功能
- 保存文件的状态
- 记录提交的信息
- 更新版本历史
- 处理暂存区

---

## rm
- **跟add反一下就好，难度不大**
---
## log
- 要想清楚Commit的存储形式，以便通过getparent()返回的String类型找到上一个Commit，难度不大
- 我的解决方案是：commitId是由commit类型的时间戳sha1后的String，以此为文件名，文件内容是用writeObject把commit类型加密后写入。所以可以调用readObject（以commitId为名的文件，Commit.Class)返回commit类型
---
## global-log
- 和log逻辑类似
- 主要是利用plainFilenamesIn()返回dir下的文件，以List<String的形式
---
## find
- 给定message去找Commit，不难
---
## Status
- 需要理一下
1. Branches part 当前的branch前要加*
2. 所有的输出都需要按照lexicographic order
- 服了，写到这里发现自己对head和master的理解有误。
- 应该是：head指向一个分支，比如head指向master，然后master指向当前分支的最新提交。这样子在出现多分支的时候，一个head以及多个分支名就可以实现多线程推进
---
## checkout
- 3种应用方式
	1. checkout -- [filename]
		把head commit中的filename文件写入CWD
	2. checkout [commit id] -- [filename]
		把指定commit中的filename文件写入CWD
		- 这样看来，我完全可以先写第2钟情况，第一种无非就是传入一个headcommitID参数即可
	3. checkout [branch name]
		1. 把指定分支的commit中的文件全部写入到CWD
		2. 把HEAD更新为指定的branch
		3. 被当前branch跟踪的文件如果不在指定的branch中则删除
		4. staging area要被清空
- failure cases:
	1. file不存在
	2. no commit with the given id
	3. no branch with that name; 指定的branch是current branch
---
***problem***
写到这里 又发现我一处逻辑错误，我一开始的分配是commit类型的属性blobs是HashMap类型的，会有一个key->value的映射关系，而我出于序列和反序列之间的相互转换，认为我可以把key设置成文件名，value设置成序列化后文件内容，此时我发现blobs文件夹无用。错误之处在于，我试图通过readObject去恢复用sha1序列化的原始文件内容。

---
## branch
- 在BRANCHES_DIR下创建一个新的branch，文件内容是当前的commit
- 不难
---
## rm-branch
- 只要删除branches文件下的相应文件即可
- 注意2个报错情况
---
## reset
- 把给定commit追踪的文件添加到CWD
- 当前commit追踪的文件如果不在给定commit里，则删除
- 通过HEAD找到当前branch，然后更新branch指向为给定的commit
---
## merge

(More to come here. It's one of the more complex features, so it’s still a work in progress.)

---
于2024.11.11继续启动，被数学竞赛耽搁了2周，运气好的话有个省一？可惜进不了决赛

- split point：当前branch和given branch heads最近的共同“祖先”
- 所有的file都需要figure out
- 如何找到split point?
- 找到之后判断：

	1.  If the split point _is_ **the same commit as the given branch**, then we do nothing; the merge is complete, and the operation ends with the message `Given branch is an ancestor of the current branch.` 
		- 如果给定分支的commit就是split commit，那么不需要merge，返回message结束
	2. If the split point is **the current branch**, then the effect is to check out the given branch, and the operation ends after printing the message `Current branch fast-forwarded.` 
		- 如果split commit是在当前分支上，意味着当前分支落后于given branch（你要切换到的分支），并且可以直接通过快进的方式将其更新为目标分支的最新状态。这种情况无需产生新的合并提交，只需简单地将当前分支指针移动到目标分支的最新提交位置。
	3. 否则 下面7种情况执行merge
	 ![图片](https://raw.githubusercontent.com/Frank-whw/img/main/blog/202411121225.png)
	 
	![image.png](https://raw.githubusercontent.com/Frank-whw/img/main/blog/202411121225.png)
			1. 任何**在given branch中被修改，在current branch中没有被修改**的文件 ->given branch。然后这些文件应该被自动staged
			2. 任何**在current branch中被修改，在given branch中没有被修改**的文件 ->保持原样，既current branch
			3. 如果一个文件在current branch和given branch中**被修改的方式相同**（都被删除或或者具有相同的内容），那么保持不变。如果已经被删除且在CWD中存在同名文件，依旧是保持不变
			4. 任何**不在split commit和given branch中，而只在current branch中**的文件 -> current branch
			5. 任何**不在split commit和current branch中，而只在given branch中**的文件 -> given branch
			6. 任何**在spilit commit中且不在given branch中，在current branch 中没有被修改**的文件 -> 删除
			7. 任何**在spilit commit中且不在current branch中，在given branch 中没有被修改**的文件 -> 删除
			8. 如果一个文件在current branch和given branch中**被修改的方式不同** -> CONFLICT
	- failure massage：
		1. 暂存区有东西的话，报错并退出
		2. given branch不存在，报错并退出
		3. given branch == current branch，报错并退出
		4. 如果在执行合并（merge）操作时，系统会因为合并的提交（commit）没有实际更改而报错，那么就让系统按照正常的提交错误信息来处理。具体来说，在一些版本控制系统（如Git）中，当你尝试合并两个分支时，如果这次合并不会引入任何新的更改（即没有实际代码差异），系统可能会认为这是一个无意义的合并，并抛出错误。此句的意思是，**不需要专门为这种情况设计额外的错误处理逻辑，而是让系统默认的提交错误信息显示即可。**
		5. 如果一个没有被current commit追踪的文件即将被覆写或删除，报错并退出。**优先检查这一check**


---
## Some tools in Utils
### 1. **SHA-1 HASH 函数**

- **`static String sha1(Object... vals)`**:
    
    - **作用**: 计算传入的任意字节数组或字符串的 SHA-1 哈希值，并返回其 40 字符长度的十六进制表示。
    - **用途**: 用于唯一标识文件或数据，常用于版本控制系统中标识文件、提交等。
    - **原理**: 对每个输入（字符串或字节数组）进行更新，最终通过 `MessageDigest` 生成哈希值，并将其转换为 16 进制字符串。
- **`static String sha1(List<Object> vals)`**:
    
    - **作用**: 这个函数的功能和上一个相同，只是接收 `List<Object>` 作为输入，内部调用第一个 `sha1` 函数。

### 2. **文件删除函数**

- **`static boolean restrictedDelete(File file)`**:
    
    - **作用**: 删除指定的文件，前提是文件所在目录中包含 `.gitlet` 目录，并且目标文件是普通文件而不是目录。
    - **用途**: 防止在非版本控制目录中删除文件，确保用户只能在 `.gitlet` 目录下进行操作，增加安全性。
- **`static boolean restrictedDelete(String file)`**:
    
    - **作用**: 和上一个函数作用相同，只是接受 `String` 类型的文件路径作为参数，并通过创建 `File` 对象调用上一个函数。

### 3. **文件内容读取与写入**

- **`static byte[] readContents(File file)`**:
    - **作用**: 读取一个普通文件的所有内容，并返回为字节数组。
    - **用途**: 获取文件的二进制内容，常用于读取文件数据（如 blobs）。
    - **异常处理**: 如果文件不是普通文件或读取失败，会抛出 `IllegalArgumentException`。

- **`static String readContentsAsString(File file)`**:
    - **作用**: 读取文件的内容并将其转换为 UTF-8 编码的字符串。
    - **用途**: 读取文本文件的内容，常用于处理文本文件（如 commit 信息）。

- **`static void writeContents(File file, Object... contents)`**:
    - **作用**: 将传入的内容（可以是字符串或字节数组）写入文件，支持创建或覆盖文件。
    - **用途**: 写入文件内容，确保不会覆盖目录文件。
    - **异常处理**: 如果操作失败或者试图覆盖目录文件，会抛出 `IllegalArgumentException`。

### 4. **序列化与反序列化**

- **`static <T extends Serializable> T readObject(File file, Class<T> expectedClass)`**:
    - **作用**: 反序列化文件内容为 Java 对象，并将其强制转换为指定的类型。
    - **用途**: 从文件中恢复之前保存的 Java 对象（如保存的项目状态或版本信息）。
    - **异常处理**: 如果读取或类型转换失败，会抛出 `IllegalArgumentException`。


- **`static void writeObject(File file, Serializable obj)`**:
    - **作用**: 将一个可序列化的对象写入文件。
    - **用途**: 保存对象状态到文件（如提交信息、文件快照等）。
    - **调用内部函数**: 使用 `writeContents` 函数将序列化后的字节数据写入文件。

- **`static byte[] serialize(Serializable obj)`**:
    - **作用**: 将对象序列化为字节数组。
    - **用途**: 用于将对象转换为可存储或传输的字节格式（如保存到文件中）。

### 5. **目录与文件操作**

- **`static List<String> plainFilenamesIn(File dir)`**:
    
    - **作用**: 获取指定目录中的所有普通文件（非目录）的文件名，并按字典顺序排序。
    - **用途**: 用于获取目录中的文件列表，排除子目录，常用于版本控制操作中列出文件。
    - **异常处理**: 如果传入的不是目录，返回 `null`。
- **`static List<String> plainFilenamesIn(String dir)`**:
    
    - **作用**: 和上一个函数作用相同，只是接受字符串路径，内部通过创建 `File` 对象调用上一个函数。
- **`static File join(String first, String... others)`**:
    
    - **作用**: 将多个路径字符串拼接成一个 `File` 对象。
    - **用途**: 方便构建文件路径，类似 `Paths.get()` 方法。
- **`static File join(File first, String... others)`**:
    
    - **作用**: 和上一个函数相同，只是第一个参数是 `File` 对象。

### 6. **消息与错误处理**

- **`static GitletException error(String msg, Object... args)`**:
    
    - **作用**: 根据指定的消息和参数创建一个 `GitletException` 异常。
    - **用途**: 用于报告自定义错误，抛出项目中常见的异常。
- **`static void message(String msg, Object... args)`**:
    
    - **作用**: 打印格式化的消息，并在末尾添加换行符。
    - **用途**: 用于在控制台输出信息或提示，类似于 `System.out.printf()`。
---
## some note
为了便于调试，自己写了一个简易的键盘输入的程序
```python
import pyautogui
import time

time.sleep(1)

pyautogui.typewrite('javac gitlet/*.java', interval=0.001)
pyautogui.press('enter')  
time.sleep(0.5)

pyautogui.typewrite('java gitlet.Main init', interval=0.001)
pyautogui.press('enter')  
time.sleep(0.5)

pyautogui.typewrite('java gitlet.Main add "123.txt"', interval=0.001)
pyautogui.press('enter')  
time.sleep(0.5)

pyautogui.typewrite('java gitlet.Main commit "123.txt"', interval=0.001)
pyautogui.press('enter')
time.sleep(0.5)  

pyautogui.typewrite('java gitlet.Main log', interval=0.001)
pyautogui.press('enter')
time.sleep(0.5)  

pyautogui.typewrite('java gitlet.Main status', interval=0.001)
pyautogui.press('enter')  
time.sleep(0.5)

```
