# wsl2的nat,mirrored都是啥？
## 前置问题与解决  
之前每次打开WSL2时，顶部均会报错：  
`wsl: 检测到 localhost 代理配置，但未镜像到 WSL。NAT 模式下的 WSL 不支持 localhost 代理。`  

通过谷歌搜索，参考[知乎帖子](https://zhuanlan.zhihu.com/p/15762609815)的方法（推测为切换到Mirrored网络模式，或配置代理镜像），该代理报错问题立竿见影地解决。  
## 后续新问题  
解决代理问题后，在WSL2中运行Java后端程序时，出现如下错误：  
```  
Error: JMX connector server communication error: service:jmx:rmi://0.0.0.0:26203  
jdk.internal.agent.AgentConfigurationError: java.rmi.server.ExportException: Port already in use: 26203; nested exception is:  
    java.net.BindException: Address already in use  
```  

## 不同模式的区别  
- **NAT模式**：WSL2拥有独立的私有网络和端口空间，与Windows宿主机的端口互不干扰（例如Windows占用26203端口时，WSL2仍可绑定该端口），因此该Java程序可正常运行，无端口冲突。  
- **Mirrored模式**：WSL2与Windows宿主机共享网络接口和端口空间（相当于“同一设备”的不同进程），若Windows中已有进程占用26203端口，WSL2的Java程序再绑定该端口时会触发“地址已被使用”错误，即上述报错。  

| 对比维度        | NAT 模式            | Mirrored 模式        |
| ----------- | ----------------- | ------------------ |
| **默认状态**    | 默认启用              | 需手动启用（Win11 22H2+） |
| **IP 分配**   | 私有子网 IP（动态）       | 复用宿主机 IP           |
| **局域网可达性**  | 外部设备无法直接访问        | 外部设备可直接访问          |
| **端口转发**    | 需手动配置             | 无需配置（共享宿主机端口）      |
| **网络切换适应性** | 较差（切换网络后需重新获取 IP） | 优秀（同步宿主机网络）        |
| **性能**      | 中等                | 中等                 |
| **兼容性**     | 最佳（全平台支持）         | 有限（仅 Win11 22H2+）  |

### 一、默认模式：NAT（网络地址转换）
#### 1. 工作原理
NAT 是 WSL2 的**默认网络模式**，基于 Hyper-V 虚拟交换机实现。Windows 会创建一个内部虚拟网络（通常为 `WSL` 虚拟交换机），WSL2 实例被分配一个**私有子网IP**（如 `172.x.x.x` 网段），通过宿主机的网络接口进行 NAT 转换，从而访问外部网络（互联网、局域网）。

#### 2. 核心特性
- **网络可达性**：
  - WSL2 可访问宿主机（通过宿主机私有IP或 `host.docker.internal` 等特殊域名）和外部网络。
  - 宿主机可访问 WSL2（通过 WSL2 的私有IP）。
  - 局域网内其他设备**无法直接访问** WSL2（需手动配置端口转发或桥接）。
- **IP 动态性**：WSL2 重启后可能分配新的私有IP，稳定性较差。
- **端口转发**：外部设备访问 WSL2 服务（如 Web 服务）时，需手动在 Windows 防火墙和虚拟交换机中配置端口转发规则（或使用工具自动转发）。
- **性能**：基础网络性能满足日常开发需求，但 NAT 转换会带来轻微开销。

#### 3. 适用场景
- 本地开发（如运行数据库、后端服务，仅需宿主机访问）。
- 无需局域网内其他设备交互的场景。

### 二、镜像模式：Mirrored（网络镜像）
#### 1. 工作原理
Mirrored 是 Windows 11 22H2 及以上版本新增的模式，核心是**将 WSL2 的网络接口与宿主机网络接口镜像对齐**。WSL2 会共享宿主机的所有网络配置（包括 Wi-Fi、以太网、VPN），相当于 WSL2 和宿主机处于**同一网络层面**，拥有与宿主机相同的网络可达性。

#### 2. 核心特性
- **网络可达性**：
  - WSL2 与宿主机完全共享网络环境，可直接访问局域网内其他设备，外部设备也能通过宿主机的 IP 直接访问 WSL2 服务（无需端口转发）。
  - 支持动态网络切换（如宿主机从 Wi-Fi 切换到以太网），WSL2 网络会同步更新。
- **IP 分配**：WSL2 不单独分配私有 IP，而是复用宿主机的网络身份。
- **兼容性**：对 VPN、企业网络策略的兼容性更好（部分复杂 VPN 环境下，NAT 模式可能失效，Mirrored 模式可正常工作）。
- **限制**：仅支持 Windows 11 22H2 及以上版本，旧系统无法使用。

#### 3. 适用场景
- 需要局域网内其他设备访问 WSL2 服务（如测试环境共享、多设备联调）。
- 宿主机频繁切换网络（如笔记本电脑移动办公）。
- 需通过 VPN 访问企业内网的场景。
## 报错的原因  
切换到Mirrored模式后，WSL2与Windows共享端口空间，而Java程序试图绑定的26203端口已被Windows宿主机中的其他进程（如另一个Java程序、后台服务等）占用，导致端口冲突。  


## 解决方法  
1. **定位占用端口的进程**：  
   - 在Windows中（PowerShell/命令提示符）：  
     ```powershell  
     netstat -ano | findstr :26203  # 查找占用26203端口的进程PID  
     tasklist | findstr <PID>       # 查看该PID对应的进程名称  
     ```  
   - 在WSL2中（需安装`net-tools`）：  
     ```bash  
     sudo netstat -tulpn | grep 26203  # 检查WSL2内部是否有进程占用  
     ```  

2. **释放冲突端口**：  
   - 若占用进程为非必要程序，直接在Windows任务管理器（通过PID查找）或WSL2中结束进程（`kill -9 <PID>`）。  

3. **修改Java程序端口**：  
   若无法释放端口，修改Java程序的JMX端口为未被占用的值（例如26204），启动命令示例：  
   ```bash  
   java -Dcom.sun.management.jmxremote \  
        -Dcom.sun.management.jmxremote.port=26204 \  
        -Dcom.sun.management.jmxremote.rmi.port=26204 \  
        -Dcom.sun.management.jmxremote.ssl=false \  
        -Dcom.sun.management.jmxremote.authenticate=false \  
        -jar your-program.jar  
   ```  
