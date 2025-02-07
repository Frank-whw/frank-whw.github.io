# Docker从入门到实践：以DataLab环境配置为例

>“明明在我的电脑上是可以运行的” 。
在部署[OpenChain](https://frank-whw.github.io/Note/Project/OpenChain/)时，我曾深陷环境配置的泥潭。虽然VM可以解决环境隔离问题，但其高资源占用、冗余操作和缓慢启动等痛点促使我们寻找更优解——这正是Docker容器技术的用武之地。

>另外摸索用 Docker 配置 Ubuntu 系统运行 DataLab 时，我发现网上教程少之又少。仅有的内容也满是晦涩术语与复杂步骤，对新手极不友好。所以这篇文章，以最细致、最易懂的方式，手把手带你上手 DataLab。
## 1. Docker介绍

### 1.1 容器化革命
Docker是一个开源的容器化平台，其通过操作系统级虚拟化技术，将应用程序及其依赖环境（包括代码、运行时、系统工具、系统库等）打包成标准化的、轻量级的**容器**（Container）。相较于传统虚拟机：

| 特性    | Docker容器 | 虚拟机    |
| ----- | -------- | ------ |
| 虚拟化层级 | OS级      | 硬件级    |
| 启动速度  | 秒级       | 分钟级    |
| 资源占用  | MB级      | GB级    |
| 性能损耗  | <5%      | 15-20% |
| 镜像大小  | 通常<100MB | 通常>1GB |

（数据来源：Docker官方基准测试报告）

### 1.2 核心概念解析
- **镜像（Image）**：不可变的模板文件，包含构建容器的完整指令集
- **容器（Container）**：镜像的可运行实例，具有独立文件系统和资源隔离
- **仓库（Registry）**：用于存储和分发镜像的中央服务（如Docker Hub）
- **Volume**：持久化数据存储方案，突破容器生命周期的限制

## 2. Docker安装

### 2.1 Windows 11专业版安装指南
1. 访问[Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/)下载安装包
2. 启用系统级支持：
   - 控制面板 → 程序 → 启用或关闭Windows功能
   - 勾选「Hyper-V」和「Windows Subsystem for Linux」
3. 安装时选择WSL2后端：
   ```powershell
   # 验证WSL版本
   wsl --list --verbose
   # 设置默认版本
   wsl --set-default-version 2
   ```
   - **架构选择建议**：
     - WSL2：推荐开发使用，提供完整Linux内核，I/O性能提升4-5倍
     - Hyper-V：适合企业级应用，支持高级虚拟化功能（动态内存分配、故障转移集群等）

### 2.2 镜像加速配置
针对国内网络环境优化，建议配置USTC镜像源：
- 作用是增加稳定性，提高下载镜像的速度，优化构建功能
![image.png](https://raw.githubusercontent.com/Frank-whw/img/main/blog/202502071010971.png)
4. 打开Docker Desktop → Settings → Docker Engine
5. 替换daemon.json配置：
```json
{
  "registry-mirrors": ["https://docker.mirrors.ustc.edu.cn"],
  "features": {
    "buildkit": true  // 启用新一代构建工具
  },
  "experimental": false  // 生产环境禁用实验特性
}
```
6. 应用配置并重启服务：
```bash
systemctl restart docker  # Linux
Get-Service docker | Restart-Service  # PowerShell
```

## 3. 配置Docker镜像
7. 拉取Ubuntu镜像
	- 可以直接在图形化界面搜索Ubuntu然后pull最新的版本
	![](https://raw.githubusercontent.com/Frank-whw/img/main/blog/202502071028767.png)
	- 也可以使用终端命令行的形式
	``` bash
	docker pull ubuntu:lastest  # 推荐使用LTS版本
	```
8. 创建容器
	- **图形化界面**
	![image.png](https://raw.githubusercontent.com/Frank-whw/img/main/blog/202502071042275.png)
	
	- Container name自拟
	- Port 端口设置
	- Volume卷挂载，作用是设置主机和容器之间的卷挂载，好处是主机和容器可以共享该目录下的文件，方便在主机上编辑代码并在容器内运行测试等操作
	- Environment variables环境变量设置，暂时不操作
	- **终端命令**
	`docker run -it -v <Host path>:<Container path> --name <Container name> ubuntu:latest`
## 4. 配置DataLab环境
9. 先更新软件包列表`apt-get update`
10. 安装wget`apt-get install -y wget`
11. 切换到共享文件夹`cd CSapp`
12. 从官网下载源码安装包`wget http://csapp.cs.cmu.edu/3e/datalab-handout.tar`
13. 将从官网下载的tar包解压，指令：`tar xvf FileName.tar`
14. 进入datalab-handout文件夹
15. 安装必备工具`apt install -y build-essential`
	- 这个软件包组包含了 GCC 编译器、G++ 编译器（用于 C++ 代码）、`make` 工具以及其他编译所需的基础库和头文件。

## 5. Finish！
- 接下来就可以在本机编译器中编写bit.c，然后在docker中的ubuntu系统中编译和运行代码了


> 容器化不是银弹，但确实是现代软件工程的必备技能。当再次面对"Works on my machine"的困境时，我们终于可以自信地说："It works on Docker!"


## References
- [Docker官方文档](https://docs.docker.com/)
- [CSAPP官网](http://csapp.cs.cmu.edu/)
- [中国科学技术大学镜像站](https://mirrors.ustc.edu.cn/)
