# 连接 AWS EC2 失败问题记录（DNS 污染导致解析异常）

## 一、问题背景

| 环境   | 详情                                               |
| ---- | ------------------------------------------------ |
| 客户端  | WSL 2（Ubuntu 子系统），用户名 `frank`                    |
| 目标服务 | AWS EC2 实例（东京区域 `ap-northeast-1`）                |
| 预期配置 | 实例公网 IP：`54.95.61.230`（AWS 控制台确认），连接方式：SSH（密钥认证） |
| 网络环境 | 校园网，客户端运行 FClash 代理工具                            |

## 二、核心现象

### 1. SSH 连接错误

```bash
frank@LAPTOP-D1IUBHQH:~$ ssh -i /home/frank/learning/cloud.pem ubuntu@ec2-54-95-61-230.ap-northeast-1.compute.amazonaws.com
kex_exchange_identification: Connection closed by remote host
Connection closed by 28.0.0.22 port 22
```

- 关键信息：连接被错误 IP `28.0.0.22` 拒绝，而非预期的 `54.95.61.230`。

### 2. 后续连接域名解析失败

```bash
frank@LAPTOP-D1IUBHQH:~$ ssh -i /home/frank/learning/cloud.pem ubuntu@ec2-54-95-61-230.ap-northeast-1.compute.amazonaws.com
ssh: Could not resolve hostname ec2-54-95-61-230.ap-northeast-1.compute.amazonaws.com: Temporary failure in name resolution
```

- 关键信息：域名解析超时，无法获取 IP 地址。

## 三、逐步排查过程

### 1. 核心排查：验证域名解析有效性

通过 `nslookup` 命令定位解析异常，结果显示 DNS 返回错误 IP：

```bash
frank@LAPTOP-D1IUBHQH:~$ nslookup ec2-54-95-61-230.ap-northeast-1.compute.amazonaws.com
Server:         10.255.255.254  # 本地私有 DNS 服务器（代理分配）
Address:        10.255.255.254#53

Name:   ec2-54-95-61-230.ap-northeast-1.compute.amazonaws.com
Address: 28.0.0.22  # 错误解析结果，与 EC2 真实 IP 不符
```

- 结论：域名解析被篡改，未指向 AWS EC2 实例的真实公网 IP `54.95.61.230`。

### 2. 补充验证：排除其他层面问题

| 排查方向         | 操作步骤                                 | 结果反馈                                                                 |
|------------------|------------------------------------------|--------------------------------------------------------------------------|
| 校园网直接解析   | Windows 主机执行 `nslookup` 相同域名     | 同样解析到 `28.0.0.22`，排除 WSL 独立问题                                |
| 公共 DNS 测试    | 指定 Google DNS（8.8.8.8）解析           | 仍返回 `28.0.0.22`，说明解析请求被拦截篡改                               |
| 代理工具影响     | 关闭 FClash 后重新解析                   | 解析结果恢复为 `54.95.61.230`，确认代理工具是污染源头                     |

## 四、根本原因

**FClash 代理工具导致 DNS 污染**，具体机制：

1. FClash 未正确配置 DNS 转发规则，将 AWS 域名（`*.amazonaws.com`）的解析请求劫持，返回虚假 IP（`28.0.0.22`）；
2. 代理的 DNS 缓存未及时清理，即使后续调整配置，旧的错误解析结果仍被复用；
3. WSL 2 共享 Windows 系统的 DNS 配置，FClash 对 Windows DNS 的修改直接同步到 WSL 环境，导致子系统解析异常。

## 五、解决方案

### 1. 临时解决：快速恢复连接

- 关闭 FClash 代理工具；
- 清理系统与 WSL 的 DNS 缓存：

```bash
# WSL 终端执行（清理 WSL 缓存）
sudo systemd-resolve --flush-caches
# Windows 管理员终端执行（清理系统缓存）
ipconfig /flushdns
```

### 2. 长期解决：正确配置 FClash 避免污染

#### （1）DNS 配置优化

1. 打开 FClash → 「设置」→「DNS 设置」；
2. 启用「自定义 DNS 服务器」，添加加密 DNS（防止劫持）：
   - Cloudflare DNS：`1.1.1.1`（DoH 地址：`https://cloudflare-dns.com/dns-query`）
   - Google DNS：`8.8.8.8`（DoH 地址：`https://dns.google/dns-query`）
3. 关闭「虚假 DNS」「DNS 劫持」功能，开启「DNS 缓存自动清理」。

#### （2）分流规则配置

添加 AWS 域名专属规则，确保解析走代理且不被污染：

1. 「规则」→「添加规则」，选择「域名后缀匹配」；
2. 匹配值：`amazonaws.com`（覆盖所有 AWS 服务域名）；
3. 动作：「代理」（若校园网封锁 AWS，需选择有效代理节点）；
4. 调整规则优先级至顶部（优先匹配）。

### 3. 验证修复效果

```bash
# 解析验证（正确返回 EC2 真实 IP）
frank@LAPTOP-D1IUBHQH:~$ nslookup ec2-54-95-61-230.ap-northeast-1.compute.amazonaws.com
Server:         1.1.1.1
Address:        1.1.1.1#53

Name:   ec2-54-95-61-230.ap-northeast-1.compute.amazonaws.com
Address: 54.95.61.230

# SSH 连接验证（成功建立会话）
frank@LAPTOP-D1IUBHQH:~$ ssh -i /home/frank/learning/cloud.pem ubuntu@ec2-54-95-61-230.ap-northeast-1.compute.amazonaws.com
Welcome to Ubuntu 22.04.3 LTS (GNU/Linux 5.15.0-1019-aws x86_64)
...
ubuntu@ip-xxx-xxx-xxx-xxx:~$  # 连接成功
```