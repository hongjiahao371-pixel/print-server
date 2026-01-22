# Docker打印服务器

一个基于Docker的打印服务器解决方案，可以在NAS上部署，通过USB连接打印机，并提供Web界面上传和打印文件。

## 功能特性

- ✅ 通过CUPS连接USB打印机
- ✅ Web界面上传文件进行打印
- ✅ 支持多种文件格式：PDF、TXT、DOC、DOCX、XLS、XLSX、PPT、PPTX、JPG、PNG、GIF
- ✅ 自动将非PDF/TXT文件转换为PDF格式
- ✅ CUPS Web管理界面（端口8631）
- ✅ 打印应用界面（端口5000）
- ✅ 实时打印机状态监控
- ✅ 适合NAS部署

## 系统要求

- Docker 20.10+
- Docker Compose 1.29+
- 支持USB设备直通的NAS系统
- 至少512MB可用内存
- 至少1GB可用磁盘空间

## 支持的文件格式

### CUPS原生支持（无需转换）
- PDF (.pdf)
- 纯文本 (.txt)

### 自动转换为PDF
- Microsoft Word (.doc, .docx)
- Microsoft Excel (.xls, .xlsx)
- Microsoft PowerPoint (.ppt, .pptx)
- 图片文件 (.jpg, .jpeg, .png, .gif)

## 快速开始

### 1. 克隆或下载项目

```bash
cd docker-print-server
```

### 2. 构建并启动容器

```bash
docker-compose up -d
```

### 3. 访问服务

- **打印应用**: http://your-nas-ip:5000
- **CUPS管理界面**: http://your-nas-ip:8631

## 详细配置

### USB打印机连接

确保打印机已通过USB连接到NAS。容器会自动检测USB设备。

如果打印机未被自动检测到，请检查：

1. USB设备是否正确连接
2. NAS是否支持USB设备直通
3. Docker容器是否有权限访问USB设备

### 在CUPS中添加打印机

1. 访问 CUPS 管理界面: http://your-nas-ip:8631
2. 点击 "Administration" -> "Add Printer"
3. 选择检测到的USB打印机
4. 选择合适的驱动程序
5. 设置打印机名称和描述
6. 完成添加

### 使用打印应用

1. 访问 http://your-nas-ip:5000
2. 选择要打印的文件
3. 选择目标打印机（可选，默认使用第一个可用打印机）
4. 点击"上传并打印"
5. 等待文件上传和打印完成

## 配置选项

### 修改端口

编辑 `docker-compose.yml` 文件：

```yaml
ports:
  - "8631:631"   # CUPS Web界面
  - "5000:5000" # Flask应用
```

### 修改时区

编辑 `docker-compose.yml` 文件：

```yaml
environment:
  - TZ=Asia/Shanghai  # 修改为你需要的时区
```

### 修改文件大小限制

编辑 `app/app.py` 文件：

```python
MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB，修改为你需要的大小
```

### 修改CUPS管理员密码

编辑 `docker-compose.yml` 文件：

```yaml
environment:
  - CUPS_USER=admin      # 用户名
  - CUPS_PASSWORD=admin  # 密码
```

## 常见问题

### 1. 打印机未被检测到

**解决方案**:
- 确认打印机已通过USB连接到NAS
- 检查Docker容器是否有USB设备访问权限
- 尝试重启容器: `docker-compose restart`
- 在NAS上运行 `lsusb` 确认打印机被系统识别

### 2. 文件转换失败

**解决方案**:
- 确认文件格式在支持列表中
- 检查文件是否损坏
- 查看容器日志: `docker-compose logs -f`

### 3. 无法访问Web界面

**解决方案**:
- 检查防火墙设置，确保端口8631和5000未被阻止
- 确认容器正在运行: `docker-compose ps`
- 查看容器日志: `docker-compose logs -f`

### 4. 打印任务卡住

**解决方案**:
- 访问CUPS管理界面查看打印队列
- 取消卡住的打印任务
- 重启CUPS服务: `docker-compose restart`

### 5. 文件上传失败

**解决方案**:
- 检查文件大小是否超过限制（默认50MB）
- 确认文件格式是否支持
- 查看浏览器控制台和容器日志获取详细错误信息

## 维护和监控

### 查看容器日志

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
docker-compose pull
docker-compose up -d
```

### 备份配置

CUPS配置和上传的文件存储在Docker卷中：

```bash
# 查看卷
docker volume ls

# 备份卷
docker run --rm -v docker-print-server_cups-config:/data -v $(pwd):/backup alpine tar czf /backup/cups-config-backup.tar.gz -C /data .
```

## 安全建议

1. **修改默认密码**: 在生产环境中，请修改CUPS管理员密码
2. **限制访问**: 使用防火墙限制对端口8631和5000的访问
3. **使用HTTPS**: 在反向代理（如Nginx）后面使用HTTPS
4. **定期更新**: 定期更新Docker镜像以获取安全补丁

## 技术架构

- **CUPS**: 打印管理系统
- **Flask**: Web应用框架
- **LibreOffice**: 文档格式转换
- **ImageMagick**: 图片格式转换
- **Docker**: 容器化平台

## 项目结构

```
docker-print-server/
├── Dockerfile              # Docker镜像构建文件
├── docker-compose.yml      # Docker Compose配置
├── entrypoint.sh          # 容器启动脚本
├── app/
│   ├── app.py             # Flask应用主程序
│   ├── requirements.txt   # Python依赖
│   ├── templates/         # HTML模板
│   │   └── index.html     # 主页面
│   ├── static/            # 静态资源
│   │   └── css/
│   │       └── style.css  # 样式文件
│   └── utils/             # 工具模块
│       ├── __init__.py
│       ├── file_converter.py    # 文件格式转换
│       └── printer_manager.py   # 打印机管理
├── cups/
│   └── cupsd.conf         # CUPS配置文件
└── README.md              # 项目文档
```

## 许可证

MIT License

## 贡献

欢迎提交问题和拉取请求！

## 支持

如有问题或建议，请提交Issue。

---

**注意**: 本项目适用于个人和小型办公环境。对于大规模打印需求，建议使用专业的打印服务器解决方案。
