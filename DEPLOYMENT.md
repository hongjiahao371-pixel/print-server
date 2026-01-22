# 部署指南

本文档提供了在不同NAS系统上部署Docker打印服务器的详细说明。

## 目录

- [通用部署步骤](#通用部署步骤)
- [Synology NAS部署](#synology-nas部署)
- [QNAP NAS部署](#qnap-nas部署)
- [TrueNAS部署](#truenas部署)
- [其他Linux系统部署](#其他linux系统部署)
- [故障排除](#故障排除)

## 通用部署步骤

### 前提条件

1. 确保你的NAS支持Docker
2. 确保你的NAS支持USB设备直通
3. 确保打印机已通过USB连接到NAS

### 部署步骤

1. **下载项目文件**
   ```bash
   # 将项目文件上传到NAS的某个目录
   # 例如: /volume1/docker/docker-print-server
   ```

2. **构建并启动容器**
   ```bash
   cd /path/to/docker-print-server
   docker-compose up -d
   ```

3. **验证容器运行**
   ```bash
   docker-compose ps
   ```

4. **访问服务**
   - 打印应用: http://nas-ip:5000
   - CUPS管理: http://nas-ip:8631

## Synology NAS部署

### 1. 安装Docker

1. 打开套件中心
2. 搜索并安装"Container Manager"或"Docker"
3. 等待安装完成

### 2. 启用USB设备直通

1. 进入控制面板 > 终端机和SNMP > 终端机
2. 勾选"启用SSH服务"
3. 通过SSH连接到NAS
4. 运行以下命令确认USB设备:
   ```bash
   lsusb
   ```
5. 如果看到打印机，说明USB设备已被识别

### 3. 部署容器

#### 方法一: 使用Docker Compose（推荐）

1. 通过File Station将项目文件上传到NAS
2. 通过SSH连接到NAS
3. 进入项目目录:
   ```bash
   cd /volume1/docker/docker-print-server
   ```
4. 启动容器:
   ```bash
   sudo docker-compose up -d
   ```

#### 方法二: 使用Docker GUI

1. 打开Container Manager
2. 创建新项目
3. 填写项目名称: `docker-print-server`
4. 选择项目路径
5. 复制`docker-compose.yml`内容到配置中
6. 点击"下一步"完成创建

### 4. 配置打印机

1. 访问 http://nas-ip:8631
2. 点击"Administration" > "Add Printer"
3. 选择检测到的USB打印机
4. 按照提示完成配置

### 5. 防火墙设置

如果无法访问Web界面:

1. 控制面板 > 安全性 > 防火墙
2. 编辑规则，允许端口8631和5000
3. 保存并应用

## QNAP NAS部署

### 1. 安装Container Station

1. 打开App Center
2. 搜索并安装"Container Station"
3. 等待安装完成

### 2. 启用USB设备直通

1. 通过SSH连接到NAS
2. 运行以下命令:
   ```bash
   lsusb
   ```
3. 确认打印机已被识别

### 3. 部署容器

#### 方法一: 使用Docker Compose

1. 通过File Station将项目文件上传到NAS
2. 通过SSH连接到NAS
3. 进入项目目录:
   ```bash
   cd /share/CACHEDEV1_DATA/docker-print-server
   ```
4. 启动容器:
   ```bash
   docker-compose up -d
   ```

#### 方法二: 使用Container Station GUI

1. 打开Container Station
2. 点击"创建"
3. 选择"创建应用程序"
4. 填写名称: `docker-print-server`
5. 复制`docker-compose.yml`内容
6. 点击"创建"

### 4. 配置防火墙

1. 控制台 > 安全性 > 防火墙
2. 添加规则允许端口8631和5000
3. 保存设置

## TrueNAS部署

### 1. 安装Docker插件

1. 打开TrueNAS Web界面
2. 插件 > 安装插件
3. 选择"Docker"官方插件
4. 等待安装完成

### 2. 创建数据集

1. 存储 > 数据集
2. 创建新数据集: `docker/print-server`
3. 设置权限

### 3. 部署容器

1. 将项目文件上传到数据集
2. 通过SSH连接到TrueNAS
3. 进入项目目录:
   ```bash
   cd /mnt/pool_name/docker/print-server
   ```
4. 启动容器:
   ```bash
   docker-compose up -d
   ```

### 4. 配置USB直通

1. TrueNAS > 系统 > 高级设置
2. 勾选"启用USB直通"
3. 重启系统

## 其他Linux系统部署

### 1. 安装Docker

```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# CentOS/RHEL
sudo yum install -y docker docker-compose
```

### 2. 启用USB设备访问

```bash
# 将当前用户添加到docker组
sudo usermod -aG docker $USER

# 重启docker服务
sudo systemctl restart docker

# 验证USB设备
lsusb
```

### 3. 部署容器

```bash
cd /path/to/docker-print-server
docker-compose up -d
```

## 故障排除

### 问题1: 容器无法启动

**症状**: `docker-compose up -d` 后容器立即退出

**解决方案**:
```bash
# 查看容器日志
docker-compose logs -f

# 检查Docker版本
docker --version
docker-compose --version
```

### 问题2: USB打印机未被检测到

**症状**: CUPS中看不到USB打印机

**解决方案**:
```bash
# 检查USB设备
lsusb

# 检查USB设备权限
ls -l /dev/bus/usb/

# 重启容器
docker-compose restart
```

### 问题3: 无法访问Web界面

**症状**: 浏览器无法打开 http://nas-ip:5000 或 http://nas-ip:8631

**解决方案**:
```bash
# 检查容器状态
docker-compose ps

# 检查端口映射
docker port docker-print-server

# 检查防火墙
sudo iptables -L -n

# 测试容器内部
docker exec -it docker-print-server curl http://localhost:5000
```

### 问题4: 文件转换失败

**症状**: 上传文件后转换失败

**解决方案**:
```bash
# 检查LibreOffice是否安装
docker exec -it docker-print-server libreoffice --version

# 检查ImageMagick是否安装
docker exec -it docker-print-server convert --version

# 查看转换日志
docker-compose logs -f
```

### 问题5: 打印任务卡住

**症状**: 打印任务一直处于队列中

**解决方案**:
```bash
# 访问CUPS管理界面
# http://nas-ip:8631

# 或通过命令行取消任务
docker exec -it docker-print-server cancel -a

# 重启CUPS服务
docker-compose restart
```

### 问题6: 权限错误

**症状**: 容器日志显示权限拒绝错误

**解决方案**:
```bash
# 修复上传目录权限
docker exec -it docker-print-server chmod 777 /app/uploads

# 修复CUPS配置权限
docker exec -it docker-print-server chown -R root:root /etc/cups
```

## 性能优化

### 1. 限制内存使用

编辑`docker-compose.yml`:

```yaml
services:
  print-server:
    mem_limit: 1g
    memswap_limit: 1g
```

### 2. 优化文件转换

对于大型文档，可以增加转换超时时间:

编辑`app/utils/file_converter.py`:

```python
result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
```

### 3. 日志管理

限制日志大小:

```yaml
services:
  print-server:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

## 安全加固

### 1. 使用非root用户

编辑`Dockerfile`:

```dockerfile
RUN useradd -m -u 1000 printuser
USER printuser
```

### 2. 限制容器权限

编辑`docker-compose.yml`:

```yaml
services:
  print-server:
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
```

### 3. 使用HTTPS

在Nginx反向代理后面部署:

```nginx
server {
    listen 443 ssl;
    server_name print.yourdomain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 备份和恢复

### 备份配置

```bash
# 备份CUPS配置
docker run --rm -v docker-print-server_cups-config:/data \
    -v $(pwd):/backup alpine tar czf /backup/cups-backup.tar.gz -C /data .

# 备份上传的文件
docker run --rm -v docker-print-server_uploads:/data \
    -v $(pwd):/backup alpine tar czf /backup/uploads-backup.tar.gz -C /data .
```

### 恢复配置

```bash
# 恢复CUPS配置
docker run --rm -v docker-print-server_cups-config:/data \
    -v $(pwd):/backup alpine tar xzf /backup/cups-backup.tar.gz -C /data

# 重启容器
docker-compose restart
```

## 监控和维护

### 查看资源使用

```bash
# 查看容器资源使用
docker stats docker-print-server

# 查看磁盘使用
docker system df
```

### 清理旧文件

```bash
# 清理未使用的Docker资源
docker system prune -a

# 清理上传的旧文件
docker exec -it docker-print-server find /app/uploads -type f -mtime +7 -delete
```

## 更新和维护

### 更新容器

```bash
# 停止并删除旧容器
docker-compose down

# 拉取最新镜像
docker-compose pull

# 启动新容器
docker-compose up -d
```

### 滚动更新

为了最小化停机时间:

```bash
# 启动新容器
docker-compose up -d --scale print-server=2 --no-recreate

# 等待新容器就绪
sleep 30

# 停止旧容器
docker-compose stop print-server_1
```

## 获取帮助

如果遇到问题:

1. 查看容器日志: `docker-compose logs -f`
2. 检查CUPS日志: `docker exec -it docker-print-server tail -f /var/log/cups/error_log`
3. 提交Issue到项目仓库
4. 参考CUPS官方文档: https://www.cups.org/documentation.html

---

**注意**: 不同NAS系统可能有特定的配置要求，请根据实际情况调整部署步骤。
