# -*- coding: utf-8 -*-
"""
Configuração da aplicação AI Content Generator.

Este arquivo contém as configurações principais da aplicação,
incluindo configurações do Flask, limites de conteúdo e
parâmetros de funcionalidade.
"""

import os
from typing import Dict, Any, List

# Configurações principais da aplicação Flask
APP_CONFIG: Dict[str, Any] = {
    'debug': os.getenv('FLASK_ENV') != 'production',
    'host': os.getenv('FLASK_HOST', '0.0.0.0'),
    'port': int(os.getenv('FLASK_PORT', 5000)),
    'max_content_length': 16 * 1024 * 1024,  # 16MB
    'secret_key': os.getenv('SECRET_KEY', 'dev-key-change-in-production'),
    'testing': False
}

# Configurações específicas do gerador de conteúdo
CONTENT_CONFIG: Dict[str, Any] = {
    'default_language': 'pt-br',
    'max_article_length': 2000,
    'supported_formats': ['html', 'markdown', 'pdf'],
    'content_types': [
        'article',
        'blog_post',
        'social_media',
        'report',
        'description'
    ],
    'styles': [
        'technical',
        'casual',
        'formal',
        'marketing',
        'academic'
    ]
}

# Configurações de análise de dados
ANALYTICS_CONFIG: Dict[str, Any] = {
    'default_chart_width': 800,
    'default_chart_height': 600,
    'supported_file_types': ['csv', 'xlsx', 'json'],
    'max_file_size': 10 * 1024 * 1024,  # 10MB
    'cache_duration': 300,  # 5 minutos
    'visualization_types': [
        'bar',
        'line',
        'scatter',
        'histogram',
        'pie',
        'heatmap'
    ]
}

# Configurações de API
API_CONFIG: Dict[str, Any] = {
    'rate_limit': '100/hour',
    'request_timeout': 30,
    'response_format': 'json',
    'cors_origins': ['http://localhost:3000', 'http://127.0.0.1:3000'],
    'api_version': 'v1'
}

# Configurações de templates
TEMPLATE_CONFIG: Dict[str, Any] = {
    'template_dir': 'templates',
    'custom_template_dir': 'custom_templates',
    'allowed_template_extensions': ['.html', '.jinja2'],
    'template_variables': {
        'author': 'AI Content Generator',
        'generator': 'AI Content Generator v1.0',
        'charset': 'UTF-8'
    }
}

# Configurações de logging
LOGGING_CONFIG: Dict[str, Any] = {
    'level': os.getenv('LOG_LEVEL', 'INFO'),
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': 'app.log',
    'max_file_size': 10 * 1024 * 1024,  # 10MB
    'backup_count': 5
}

# Configurações de banco de dados (se necessário)
DATABASE_CONFIG: Dict[str, str] = {
    'url': os.getenv('DATABASE_URL', 'sqlite:///ai_content_generator.db'),
    'echo': os.getenv('DATABASE_ECHO', 'False').lower() == 'true'
}

def get_config() -> Dict[str, Any]:
    """Retorna todas as configurações consolidadas."""
    return {
        'app': APP_CONFIG,
        'content': CONTENT_CONFIG,
        'analytics': ANALYTICS_CONFIG,
        'api': API_CONFIG,
        'template': TEMPLATE_CONFIG,
        'logging': LOGGING_CONFIG,
        'database': DATABASE_CONFIG
    }

def validate_config() -> bool:
    """Valida se todas as configurações necessárias estão presentes."""
    required_env_vars = ['SECRET_KEY'] if APP_CONFIG['debug'] is False else []
    
    for var in required_env_vars:
        if not os.getenv(var):
            print(f"Erro: Variável de ambiente {var} não encontrada")
            return False
    
    return True

if __name__ == '__main__':
    # Teste das configurações
    config = get_config()
    print("Configurações carregadas com sucesso:")
    for section, settings in config.items():
        print(f"  {section}: {len(settings)} configurações")
    
    print(f"\nValidação: {'✓ Passou' if validate_config() else '✗ Falhou'}")
