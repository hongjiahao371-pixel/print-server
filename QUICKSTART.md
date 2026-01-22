# 快速启动指南

本指南将帮助你在5分钟内启动Docker打印服务器。

## 前提条件

- Docker已安装并运行
- 打印机已通过USB连接到NAS/服务器
- 至少1GB可用磁盘空间

## 快速启动

### 1. 进入项目目录

```bash
cd docker-print-server
```

### 2. 构建并启动容器

```bash
docker-compose up -d
```

### 3. 等待容器启动

容器首次启动需要几分钟时间来安装依赖包。你可以通过以下命令查看日志：

```bash
docker-compose logs -f
```

当你看到以下信息时，说明容器已成功启动：
```
CUPS Print Server is ready!
CUPS Web Interface: http://localhost:8631
Print Application: http://localhost:5000
```

### 4. 访问服务

- **打印应用**: http://your-nas-ip:5000
- **CUPS管理**: http://your-nas-ip:8631

### 5. 在CUPS中添加打印机

1. 访问 http://your-nas-ip:8631
2. 点击 "Administration" → "Add Printer"
3. 输入用户名和密码（默认: admin/admin）
4. 选择检测到的USB打印机
5. 选择合适的驱动程序
6. 设置打印机名称和描述
7. 点击 "Add Printer" 完成添加

### 6. 开始打印

1. 访问 http://your-nas-ip:5000
2. 选择要打印的文件
3. 选择目标打印机
4. 点击"上传并打印"

## 支持的文件格式

| 格式 | 是否需要转换 |
|------|-------------|
| PDF | ❌ 否 |
| TXT | ❌ 否 |
| DOC/DOCX | ✅ 是 |
| XLS/XLSX | ✅ 是 |
| PPT/PPTX | ✅ 是 |
| JPG/PNG/GIF | ✅ 是 |

## 常用命令

### 查看容器状态

```bash
docker-compose ps
```

### 查看日志

```bash
docker-compose logs -f
```

### 重启容器

```bash
docker-compose restart
```

### 停止容器

```bash
docker-compose down
```

### 更新容器

```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## 故障排除

### 问题：容器无法启动

**解决方案**：
```bash
# 查看详细日志
docker-compose logs

# 检查Docker是否运行
docker ps

# 重新构建
docker-compose down
docker-compose build
docker-compose up -d
```

### 问题：无法访问Web界面

**解决方案**：
```bash
# 检查容器是否运行
docker-compose ps

# 检查端口是否被占用
netstat -an | grep 5000
netstat -an | grep 8631

# 检查防火墙
sudo iptables -L -n
```

### 问题：打印机未被检测到

**解决方案**：
```bash
# 检查USB设备
lsusb

# 重启容器
docker-compose restart

# 在容器内检查USB设备
docker exec -it docker-print-server lsusb
```

### 问题：文件转换失败

**解决方案**：
```bash
# 检查LibreOffice
docker exec -it docker-print-server libreoffice --version

# 检查ImageMagick
docker exec -it docker-print-server convert --version

# 查看转换日志
docker-compose logs | grep -i error
```

## 配置修改

### 修改端口

编辑 `docker-compose.yml`：

```yaml
ports:
  - "8631:631"   # CUPS Web界面
  - "5000:5000" # Flask应用
```

### 修改文件大小限制

编辑 `app/app.py`：

```python
MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB
```

### 修改时区

编辑 `docker-compose.yml`：

```yaml
environment:
  - TZ=Asia/Shanghai
```

## 安全建议

1. **修改默认密码**：在CUPS管理界面修改管理员密码
2. **限制访问**：使用防火墙限制对端口8631和5000的访问
3. **使用HTTPS**：在反向代理后面部署
4. **定期更新**：定期更新Docker镜像

## 下一步

- 阅读完整的 [README.md](README.md) 了解更多功能
- 查看 [DEPLOYMENT.md](DEPLOYMENT.md) 了解详细部署指南
- 访问 CUPS 官方文档: https://www.cups.org/documentation.html

## 获取帮助

如果遇到问题：

1. 查看容器日志：`docker-compose logs -f`
2. 检查CUPS日志：`docker exec -it docker-print-server tail -f /var/log/cups/error_log`
3. 提交Issue到项目仓库

---

**提示**：首次构建可能需要10-15分钟，请耐心等待。
