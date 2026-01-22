# 使用官方的CUPS镜像作为基础
FROM ubuntu:22.04

# 设置非交互式安装
ENV DEBIAN_FRONTEND=noninteractive

# 安装必要的依赖
RUN apt-get update && apt-get install -y \
    cups \
    cups-pdf \
    printer-driver-all \
    avahi-daemon \
    libavahi-client3 \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    libssl-dev \
    libffi-dev \
    wget \
    curl \
    vim \
    net-tools \
    usbutils \
    libreoffice \
    imagemagick \
    ghostscript \
    && rm -rf /var/lib/apt/lists/*

# 安装Python依赖
RUN pip3 install --no-cache-dir \
    flask \
    requests

# 创建应用目录
WORKDIR /app

# 复制应用文件
COPY app/ /app/
COPY cups/ /etc/cups/

# 设置CUPS权限
RUN usermod -aG lpadmin root && \
    usermod -aG lp root && \
    chmod -R 755 /etc/cups && \
    chown -R root:root /etc/cups

# 创建上传目录
RUN mkdir -p /app/uploads && chmod 777 /app/uploads

# 暴露端口
# 631 - CUPS Web界面
# 5000 - Flask应用
EXPOSE 631 5000

# 启动脚本
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# 启动服务
ENTRYPOINT ["/entrypoint.sh"]
