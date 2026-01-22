#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Docker打印服务器 - Flask应用
支持文件上传、格式转换和打印功能
"""

import os
import subprocess
import logging
from flask import Flask, render_template, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
import mimetypes

# 导入格式转换工具
from utils.file_converter import FileConverter
from utils.printer_manager import PrinterManager

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 创建Flask应用
app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'

# 配置
UPLOAD_FOLDER = '/app/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'jpg', 'jpeg', 'png', 'gif'}
MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# 确保上传目录存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 初始化工具
file_converter = FileConverter()
printer_manager = PrinterManager()


def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """主页 - 显示上传界面"""
    return render_template('index.html')


@app.route('/api/printers', methods=['GET'])
def get_printers():
    """获取可用打印机列表"""
    try:
        printers = printer_manager.list_printers()
        return jsonify({
            'success': True,
            'printers': printers
        })
    except Exception as e:
        logger.error(f"获取打印机列表失败: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/upload', methods=['POST'])
def upload_file():
    """上传文件并打印"""
    try:
        # 检查是否有文件
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': '没有上传文件'
            }), 400

        file = request.files['file']
        printer_name = request.form.get('printer', '')
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': '未选择文件'
            }), 400

        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': f'不支持的文件类型。支持的格式: {", ".join(ALLOWED_EXTENSIONS)}'
            }), 400

        # 保存上传的文件
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        logger.info(f"文件已保存: {filepath}")

        # 获取文件扩展名
        file_ext = filename.rsplit('.', 1)[1].lower()

        # 如果不是PDF或TXT，需要转换
        converted_filepath = filepath
        if file_ext not in ['pdf', 'txt']:
            logger.info(f"文件格式转换: {file_ext} -> PDF")
            converted_filepath = file_converter.convert_to_pdf(filepath)
            
            if not converted_filepath:
                return jsonify({
                    'success': False,
                    'error': f'无法将 {file_ext} 格式转换为PDF'
                }), 400
            
            logger.info(f"转换完成: {converted_filepath}")

        # 发送到打印机
        if printer_name:
            result = printer_manager.print_file(converted_filepath, printer_name)
        else:
            # 使用默认打印机
            result = printer_manager.print_file(converted_filepath)

        if result['success']:
            return jsonify({
                'success': True,
                'message': f'文件 "{filename}" 已成功发送到打印机',
                'printer': result.get('printer', '默认打印机')
            })
        else:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 500

    except Exception as e:
        logger.error(f"上传文件时出错: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'服务器错误: {str(e)}'
        }), 500


@app.route('/api/status', methods=['GET'])
def get_status():
    """获取系统状态"""
    try:
        printers = printer_manager.list_printers()
        return jsonify({
            'success': True,
            'status': {
                'cups_running': printer_manager.check_cups_status(),
                'printers_count': len(printers),
                'printers': printers
            }
        })
    except Exception as e:
        logger.error(f"获取状态失败: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.errorhandler(413)
def request_entity_too_large(error):
    """处理文件过大错误"""
    return jsonify({
        'success': False,
        'error': f'文件过大，最大允许 {MAX_CONTENT_LENGTH // (1024*1024)}MB'
    }), 413


@app.errorhandler(500)
def internal_server_error(error):
    """处理服务器错误"""
    logger.error(f"服务器错误: {str(error)}")
    return jsonify({
        'success': False,
        'error': '服务器内部错误'
    }), 500


if __name__ == '__main__':
    logger.info("启动Flask应用...")
    app.run(host='0.0.0.0', port=5000, debug=False)
