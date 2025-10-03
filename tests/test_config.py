# -*- coding: utf-8 -*-
"""
Testes para o módulo de configuração.

Este arquivo contém testes unitários para validar
as configurações da aplicação AI Content Generator.
"""

import unittest
import os
import sys
from unittest.mock import patch

# Adiciona o diretório raiz ao path para importar config
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from config.config import (
    APP_CONFIG,
    CONTENT_CONFIG,
    ANALYTICS_CONFIG,
    API_CONFIG,
    TEMPLATE_CONFIG,
    LOGGING_CONFIG,
    DATABASE_CONFIG,
    get_config,
    validate_config
)


class TestConfig(unittest.TestCase):
    """Testes para configurações da aplicação."""
    
    def test_app_config_structure(self):
        """Testa se APP_CONFIG tem todas as chaves necessárias."""
        required_keys = ['debug', 'host', 'port', 'max_content_length', 'secret_key']
        
        for key in required_keys:
            self.assertIn(key, APP_CONFIG, f"Chave '{key}' não encontrada em APP_CONFIG")
    
    def test_content_config_structure(self):
        """Testa se CONTENT_CONFIG tem estrutura correta."""
        required_keys = ['default_language', 'max_article_length', 'supported_formats']
        
        for key in required_keys:
            self.assertIn(key, CONTENT_CONFIG, f"Chave '{key}' não encontrada em CONTENT_CONFIG")
        
        # Verifica se supported_formats é uma lista
        self.assertIsInstance(CONTENT_CONFIG['supported_formats'], list)
        self.assertGreater(len(CONTENT_CONFIG['supported_formats']), 0)
    
    def test_analytics_config_structure(self):
        """Testa configurações de analytics."""
        required_keys = ['default_chart_width', 'default_chart_height', 'supported_file_types']
        
        for key in required_keys:
            self.assertIn(key, ANALYTICS_CONFIG)
        
        # Verifica tipos de dados
        self.assertIsInstance(ANALYTICS_CONFIG['default_chart_width'], int)
        self.assertIsInstance(ANALYTICS_CONFIG['default_chart_height'], int)
        self.assertIsInstance(ANALYTICS_CONFIG['supported_file_types'], list)
    
    def test_api_config_structure(self):
        """Testa configurações da API."""
        required_keys = ['rate_limit', 'request_timeout', 'response_format']
        
        for key in required_keys:
            self.assertIn(key, API_CONFIG)
    
    def test_get_config_returns_all_sections(self):
        """Testa se get_config retorna todas as seções."""
        config = get_config()
        
        expected_sections = ['app', 'content', 'analytics', 'api', 'template', 'logging', 'database']
        
        for section in expected_sections:
            self.assertIn(section, config, f"Seção '{section}' não encontrada")
    
    def test_validate_config_success(self):
        """Testa validação de configuração com sucesso."""
        # Em modo debug, validação deve passar sem SECRET_KEY
        with patch.dict(os.environ, {}, clear=True):
            result = validate_config()
            self.assertTrue(result)
    
    @patch.dict(os.environ, {'SECRET_KEY': 'test-key'})
    def test_validate_config_with_secret_key(self):
        """Testa validação com SECRET_KEY definida."""
        result = validate_config()
        self.assertTrue(result)
    
    def test_port_is_integer(self):
        """Testa se a porta é um inteiro."""
        self.assertIsInstance(APP_CONFIG['port'], int)
        self.assertGreater(APP_CONFIG['port'], 0)
        self.assertLess(APP_CONFIG['port'], 65536)
    
    def test_max_content_length_is_reasonable(self):
        """Testa se o tamanho máximo de conteúdo é razoável."""
        max_length = APP_CONFIG['max_content_length']
        self.assertIsInstance(max_length, int)
        self.assertGreater(max_length, 1024)  # Pelo menos 1KB
        self.assertLess(max_length, 100 * 1024 * 1024)  # Menos que 100MB
    
    def test_supported_formats_valid(self):
        """Testa se os formatos suportados são válidos."""
        formats = CONTENT_CONFIG['supported_formats']
        valid_formats = ['html', 'markdown', 'pdf', 'txt', 'json']
        
        for format_type in formats:
            self.assertIn(format_type, valid_formats, f"Formato '{format_type}' não é válido")
    
    def test_language_code_format(self):
        """Testa se o código de idioma tem formato correto."""
        language = CONTENT_CONFIG['default_language']
        self.assertIsInstance(language, str)
        self.assertRegex(language, r'^[a-z]{2}(-[a-z]{2})?$', "Formato de idioma inválido")
    
    def test_logging_config_structure(self):
        """Testa estrutura da configuração de logging."""
        required_keys = ['level', 'format', 'file']
        
        for key in required_keys:
            self.assertIn(key, LOGGING_CONFIG)
        
        # Verifica se o nível de log é válido
        valid_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        self.assertIn(LOGGING_CONFIG['level'], valid_levels)
    
    def test_database_config_has_url(self):
        """Testa se a configuração do banco tem URL."""
        self.assertIn('url', DATABASE_CONFIG)
        self.assertIsInstance(DATABASE_CONFIG['url'], str)
        self.assertTrue(len(DATABASE_CONFIG['url']) > 0)


class TestConfigIntegration(unittest.TestCase):
    """Testes de integração para configurações."""
    
    def test_config_can_be_imported(self):
        """Testa se o módulo config pode ser importado sem erros."""
        try:
            import config
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Falha ao importar config: {e}")
    
    def test_all_configs_are_dicts(self):
        """Testa se todas as configurações são dicionários."""
        configs = [
            APP_CONFIG,
            CONTENT_CONFIG,
            ANALYTICS_CONFIG,
            API_CONFIG,
            TEMPLATE_CONFIG,
            LOGGING_CONFIG,
            DATABASE_CONFIG
        ]
        
        for config in configs:
            self.assertIsInstance(config, dict, "Configuração deve ser um dicionário")
    
    def test_no_empty_required_values(self):
        """Testa se valores obrigatórios não estão vazios."""
        # Valores que não devem estar vazios
        self.assertTrue(APP_CONFIG['host'])
        self.assertTrue(CONTENT_CONFIG['default_language'])
        self.assertTrue(API_CONFIG['response_format'])
        self.assertTrue(LOGGING_CONFIG['format'])


if __name__ == '__main__':
    # Configura o unittest para rodar com mais verbosidade
    unittest.main(verbosity=2)
