# EC2实例连接与EC2-S3通信操作指南
## 一、EC2实例SSH连接步骤
### 1. 核心连接命令
使用以下命令通过SSH连接EC2实例（Ubuntu系统），需确保本地已保存`cloud.pem`私钥文件：
```bash
ssh -i /home/frank/learning/cloud.pem ubuntu@ec2-54-95-61-230.ap-northeast-1.compute.amazonaws.com
```
- 说明：`-i` 后接本地私钥文件路径（此处为Windows路径`D:\download\cloud.pem`），`ubuntu`是EC2 Ubuntu系统的默认登录用户，后续为EC2实例的公网地址。


### 2. 私钥权限修改（关键前提）
SSH连接需确保私钥权限符合安全规范，Linux与Windows操作差异如下：
- **Linux/WSL系统（简单，1行命令）**：  
  在终端执行以下命令，将私钥权限设置为仅所有者可读写（避免权限过开放被SSH拒绝）：
  ```bash
  chmod 600 /path/to/cloud.pem  # 替换为Linux/WSL中cloud.pem的实际路径，如/home/frank/learning/cloud.pem
  ```
- **Windows系统（需手动配置）**：  
  1. 右键`cloud.pem`文件 → 选择「属性」→ 切换到「安全」选项卡；  
  2. 点击「高级」→ 禁用「继承」→ 选择「从此对象中删除所有已继承的权限」；  
  3. 点击「添加」→ 输入当前Windows用户名（如`DESKTOP-XXX\Frank`）→ 赋予「读取」权限，删除其他所有用户的权限（确保仅当前用户可访问）。


### 3. 连接成功验证
执行连接命令后，若出现以下界面，说明连接成功（对应参考图片）：
![image.png](https://raw.githubusercontent.com/Frank-whw/img/main/blog/202510141539976.png)
- 成功标志：终端提示符变为`ubuntu@ip-xxx-xx-xx-xxx:~$`（`ip-xxx`为EC2实例的内网IP）。


### 4. 切换至root用户
连接成功后，若需获取root权限（如配置`.aws`目录），执行以下命令（无需输入root密码，直接切换）：
```bash
sudo -i
```
- 切换成功标志：终端提示符变为`root@ip-xxx-xx-xx-xxx:~#`。  
- 注意：学长的`.aws`配置（AWS CLI凭证）保存在root用户目录下，切换后可直接使用AWS CLI操作S3，无需重复配置。


## 二、EC2与S3的通信方式（AWS CLI实操）
EC2与S3之间传输数据（上传/下载/同步）最常用的工具是**AWS CLI（命令行工具）**，适合手动操作或脚本自动化，以下为具体用法（需先切换至root用户，利用已配置的`.aws`凭证）。

### 1. 核心前提
- 已通过`sudo -i`切换至root用户（使用学长配置好的`.aws`凭证，无需额外执行`aws configure`）；  
- 目标S3桶名为`ecnu-cloudsys`（所有操作需指定此桶名）。


### 2. 常用通信命令示例
#### （1）EC2向S3上传文件
将EC2本地的文件上传到S3的`ecnu-cloudsys`桶中，命令格式：
```bash
aws s3 cp 本地文件路径 s3://ecnu-cloudsys/目标文件路径
```
- 实际示例：将EC2当前目录下的`file.txt`上传到S3桶根目录（保持文件名不变）：
  ```bash
  aws s3 cp file.txt s3://ecnu-cloudsys/file.txt
  ```
- 成功提示：`upload: ./file.txt to s3://ecnu-cloudsys/file.txt`。


#### （2）EC2从S3下载文件
将S3`ecnu-cloudsys`桶中的文件下载到EC2本地，命令格式：
```bash
aws s3 cp s3://ecnu-cloudsys/源文件路径 本地目标路径
```
- 实际示例：将S3桶根目录的`file.txt`下载到EC2的`/root/test`目录下：
  ```bash
  aws s3 cp s3://ecnu-cloudsys/file.txt /root/test/file.txt
  ```
- 成功提示：`download: s3://ecnu-cloudsys/file.txt to /root/test/file.txt`。


#### （3）EC2与S3文件夹同步
同步EC2本地文件夹与S3桶中的文件夹（自动对比差异，仅传输新增/修改的文件，效率高），命令格式：
```bash
# EC2本地文件夹 → S3文件夹（上传同步）
aws s3 sync 本地文件夹路径 s3://ecnu-cloudsys/目标文件夹路径

# S3文件夹 → EC2本地文件夹（下载同步）
aws s3 sync s3://ecnu-cloudsys/源文件夹路径 本地文件夹路径
```
- 实际示例：将EC2的`/root/easyCloudDisk`文件夹同步到S3的`ecnu-cloudsys/easyCloudDisk`目录：
  ```bash
  aws s3 sync /root/easyCloudDisk s3://ecnu-cloudsys/easyCloudDisk
  ```
- 成功提示：会列出同步的文件列表（如`upload: /root/easyCloudDisk/data.csv to s3://ecnu-cloudsys/easyCloudDisk/data.csv`）。

## 
```bash
# 设置必需的环境变量（根据实际配置修改值）
export DB_PASSWORD=
export JWT_SECRET=
export AWS_S3_BUCKET=
export AWS_REGION=us-west-1
export AWS_ACCESS_KEY=
export AWS_SECRET_KEY=

```


```bash
# 创建 AMI（替换 your-ami-name 为你想要的镜像名称）
aws ec2 create-image \
    --instance-id i-00bb935f7c6f15fd5 \
    --name "clouddisk-base-$(date +%Y%m%d)" \
    --description "CloudDisk server base image with Java, Maven, PostgreSQL and environment variables configured" \
    --no-reboot \
    --region ap-northeast-1

```

```bash
创建数据库与用户

- 切换到 Postgres 管理员并进到控制台：
  - sudo -u postgres psql
- 在 psql 里执行：
CREATE ROLE clouddisk WITH LOGIN PASSWORD '123456';
CREATE DATABASE clouddisk OWNER clouddisk;
GRANT ALL PRIVILEGES ON DATABASE clouddisk TO clouddisk;

```



  - `curl -i http://localhost:8080/health`
- 注册：
  - 
```bash
curl -sS -X POST http://localhost:8080/auth/register -H 'Content-Type: application/json' -d '{"email":"test@example.com","password":"P@ssw0rd!"}'


curl -sS -X POST http://ec2-54-95-61-230.ap-northeast-1.compute.amazonaws.com:8080/auth/register -H 'Content-Type: application/json' -d '{"email":"teqst@example.com","password":"P@ssw0rd!"}'

```
- 登录并获取 JWT：
  - `curl -sS -X POST http://localhost:8080/auth/login -H 'Content-Type: application/json' -d '{"email":"test@example.com","password":"P@ssw0rd!"}'`
  - 如果装了 `jq`，可提取令牌：
    - `TOKEN=$(curl -sS -X POST http://ec2-54-95-61-230.ap-northeast-1.compute.amazonaws.com:8080/auth/login -H 'Content-Type: application/json' -d '{"email":"test@example.com","password":"P@ssw0rd!"}' | jq -r '.data.token')`
    - `echo "$TOKEN"`
- 带授权头测试受保护接口（文件列表为示例，若未实现请先测认证接口）：
  - `curl -sS -H "Authorization: Bearer $TOKEN" http://ec2-54-95-61-230.ap-northeast-1.compute.amazonaws.com:8080/files`

**验证自动建表**
- 启动后端后进入数据库查看：
  - `psql -h ec2-54-95-61-230.ap-northeast-1.compute.amazonaws.com -U clouddisk -d clouddisk -W`
  - `\dt` 看表是否生成（如 `users`、`files`）
- 若未生成，检查 `application.yml` 配置：
  - `spring.jpa.hibernate.ddl-auto: update` 应启用自动建表
  - `spring.datasource.username: clouddisk`
  - `spring.datasource.password: ${DB_PASSWORD}`
  - `spring.datasource.url: jdbc:postgresql://localhost:5432/clouddisk`

**常见问题与排查**
- 401 未授权：
  - 是否加了 `Authorization: Bearer <token>` 头；token 是否来自登录响应。
- 数据库认证失败：
  - `DB_PASSWORD` 是否已设置；用户名是否为 `clouddisk`；能否用 psql 登录。
- 应用未启动或端口未监听：
  - 查看控制台日志或文件日志：`server/logs/server.log`
  - 确认端口：`ss -tln | grep 8080`
- 代码层注意：
  - `UserRepository` 的主键类型应与实体一致（当前实体是 `String`，建议改为 `JpaRepository<User, String>`）。
