#!/bin/bash

echo "Starting CUPS Print Server..."

# 启动CUPS服务
/etc/init.d/cups start

# 等待CUPS启动
sleep 5

# 配置CUPS允许远程访问
cupsctl --remote-any

# 检查USB打印机
echo "Checking for USB printers..."
lsusb

echo "CUPS Print Server is ready!"
echo "CUPS Web Interface: http://localhost:8631"
echo "Print Application: http://localhost:5000"

# 启动Flask应用
python3 /app/app.py
