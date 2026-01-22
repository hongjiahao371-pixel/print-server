#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文件格式转换工具
将各种文件格式转换为PDF或TXT格式，以便CUPS能够识别和打印
"""

import os
import logging
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)


class FileConverter:
    """文件格式转换器"""
    
    def __init__(self):
        self.supported_formats = {
            'doc': self._convert_doc_to_pdf,
            'docx': self._convert_docx_to_pdf,
            'xls': self._convert_xls_to_pdf,
            'xlsx': self._convert_xlsx_to_pdf,
            'ppt': self._convert_ppt_to_pdf,
            'pptx': self._convert_pptx_to_pdf,
            'jpg': self._convert_image_to_pdf,
            'jpeg': self._convert_image_to_pdf,
            'png': self._convert_image_to_pdf,
            'gif': self._convert_image_to_pdf,
        }
    
    def convert_to_pdf(self, filepath):
        """
        将文件转换为PDF格式
        
        Args:
            filepath: 输入文件路径
            
        Returns:
            转换后的PDF文件路径，如果转换失败则返回None
        """
        try:
            if not os.path.exists(filepath):
                logger.error(f"文件不存在: {filepath}")
                return None
            
            file_ext = Path(filepath).suffix.lower().lstrip('.')
            
            # 如果已经是PDF，直接返回
            if file_ext == 'pdf':
                return filepath
            
            # 如果是TXT文件，直接返回（CUPS支持TXT）
            if file_ext == 'txt':
                return filepath
            
            # 检查是否支持该格式
            if file_ext not in self.supported_formats:
                logger.warning(f"不支持的文件格式: {file_ext}")
                return None
            
            # 调用对应的转换函数
            converter = self.supported_formats[file_ext]
            return converter(filepath)
            
        except Exception as e:
            logger.error(f"文件转换失败: {str(e)}")
            return None
    
    def _convert_doc_to_pdf(self, filepath):
        """将DOC文件转换为PDF"""
        try:
            output_pdf = filepath.rsplit('.', 1)[0] + '.pdf'
            
            # 使用LibreOffice进行转换
            cmd = [
                'libreoffice',
                '--headless',
                '--convert-to', 'pdf',
                '--outdir', os.path.dirname(output_pdf),
                filepath
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0 and os.path.exists(output_pdf):
                logger.info(f"DOC转PDF成功: {output_pdf}")
                return output_pdf
            else:
                logger.error(f"DOC转PDF失败: {result.stderr}")
                return None
                
        except Exception as e:
            logger.error(f"DOC转换出错: {str(e)}")
            return None
    
    def _convert_docx_to_pdf(self, filepath):
        """将DOCX文件转换为PDF"""
        return self._convert_doc_to_pdf(filepath)
    
    def _convert_xls_to_pdf(self, filepath):
        """将XLS文件转换为PDF"""
        return self._convert_doc_to_pdf(filepath)
    
    def _convert_xlsx_to_pdf(self, filepath):
        """将XLSX文件转换为PDF"""
        return self._convert_doc_to_pdf(filepath)
    
    def _convert_ppt_to_pdf(self, filepath):
        """将PPT文件转换为PDF"""
        return self._convert_doc_to_pdf(filepath)
    
    def _convert_pptx_to_pdf(self, filepath):
        """将PPTX文件转换为PDF"""
        return self._convert_doc_to_pdf(filepath)
    
    def _convert_image_to_pdf(self, filepath):
        """将图片文件转换为PDF"""
        try:
            output_pdf = filepath.rsplit('.', 1)[0] + '.pdf'
            
            # 使用ImageMagick的convert命令
            cmd = [
                'convert',
                filepath,
                output_pdf
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0 and os.path.exists(output_pdf):
                logger.info(f"图片转PDF成功: {output_pdf}")
                return output_pdf
            else:
                logger.error(f"图片转PDF失败: {result.stderr}")
                return None
                
        except Exception as e:
            logger.error(f"图片转换出错: {str(e)}")
            return None
    
    def get_supported_formats(self):
        """获取支持的文件格式列表"""
        return list(self.supported_formats.keys()) + ['pdf', 'txt']
