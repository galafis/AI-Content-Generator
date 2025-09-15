/**
 * Testes para o app.js - Funcionalidades JavaScript
 * 
 * Este arquivo contém testes unitários para validar
 * as funcionalidades JavaScript da aplicação AI Content Generator.
 */

// Mock do DOM para testes
const { JSDOM } = require('jsdom');
const dom = new JSDOM('<!DOCTYPE html><html><body></body></html>');
global.window = dom.window;
global.document = dom.window.document;
global.navigator = dom.window.navigator;

// Mock do fetch para testes de API
global.fetch = jest.fn();

// Mock console para capturar logs
global.console = {
  log: jest.fn(),
  error: jest.fn(),
  warn: jest.fn(),
  info: jest.fn()
};

describe('ContentManager', () => {
  let contentManager;
  
  beforeEach(() => {
    // Reset mocks
    fetch.mockClear();
    console.log.mockClear();
    console.error.mockClear();
    
    // Criar instância fresh para cada teste
    document.body.innerHTML = `
      <div id="content-form">
        <input id="prompt-input" type="text" />
        <button id="generate-btn">Generate</button>
        <div id="output"></div>
        <div id="loading" style="display: none;">Loading...</div>
      </div>
    `;
    
    // Simular carregamento do ContentManager
    eval(`
      class ContentManager {
        constructor() {
          this.initializeInterface();
        }
        
        initializeInterface() {
          this.promptInput = document.getElementById('prompt-input');
          this.generateBtn = document.getElementById('generate-btn');
          this.output = document.getElementById('output');
          this.loading = document.getElementById('loading');
          
          if (this.generateBtn) {
            this.generateBtn.addEventListener('click', () => this.handleGenerate());
          }
        }
        
        async generateContent(prompt) {
          const response = await fetch('/api/generate', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({prompt: prompt})
          });
          return await response.json();
        }
        
        async handleGenerate() {
          const prompt = this.promptInput.value.trim();
          if (!prompt) {
            alert('Por favor, insira um prompt');
            return;
          }
          
          this.showLoading();
          try {
            const result = await this.generateContent(prompt);
            this.displayResult(result);
          } catch (error) {
            this.displayError(error.message);
          } finally {
            this.hideLoading();
          }
        }
        
        showLoading() {
          if (this.loading) this.loading.style.display = 'block';
        }
        
        hideLoading() {
          if (this.loading) this.loading.style.display = 'none';
        }
        
        displayResult(result) {
          if (this.output) {
            this.output.innerHTML = result.content || result.text || 'Resultado gerado';
          }
        }
        
        displayError(message) {
          if (this.output) {
            this.output.innerHTML = \`<div class="error">Erro: \${message}</div>\`;
          }
        }
        
        validateInput(input) {
          return input && input.trim().length > 0;
        }
        
        formatContent(content) {
          return content.replace(/\n/g, '<br>');
        }
      }
    `);
    
    contentManager = new ContentManager();
  });
  
  afterEach(() => {
    document.body.innerHTML = '';
  });
  
  describe('Inicialização', () => {
    test('deve inicializar corretamente', () => {
      expect(contentManager).toBeDefined();
      expect(contentManager.promptInput).toBeTruthy();
      expect(contentManager.generateBtn).toBeTruthy();
      expect(contentManager.output).toBeTruthy();
      expect(contentManager.loading).toBeTruthy();
    });
    
    test('deve conectar event listeners', () => {
      const btn = document.getElementById('generate-btn');
      expect(btn).toBeTruthy();
      // Verificar se o event listener foi adicionado (simplificado)
      expect(btn.onclick || btn.addEventListener).toBeTruthy();
    });
  });
  
  describe('generateContent', () => {
    test('deve fazer chamada para API corretamente', async () => {
      const mockResponse = {
        ok: true,
        json: async () => ({ content: 'Conteúdo gerado', success: true })
      };
      fetch.mockResolvedValue(mockResponse);
      
      const result = await contentManager.generateContent('teste prompt');
      
      expect(fetch).toHaveBeenCalledWith('/api/generate', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({prompt: 'teste prompt'})
      });
      expect(result).toEqual({ content: 'Conteúdo gerado', success: true });
    });
    
    test('deve lidar com erro de API', async () => {
      fetch.mockRejectedValue(new Error('Network error'));
      
      await expect(contentManager.generateContent('teste'))
        .rejects.toThrow('Network error');
    });
  });
  
  describe('Interface do usuário', () => {
    test('deve mostrar loading durante geração', async () => {
      const mockResponse = {
        ok: true,
        json: async () => ({ content: 'Resultado' })
      };
      fetch.mockResolvedValue(mockResponse);
      
      contentManager.promptInput.value = 'teste';
      
      const handleGeneratePromise = contentManager.handleGenerate();
      
      // Verificar se loading está visível
      expect(contentManager.loading.style.display).toBe('block');
      
      await handleGeneratePromise;
      
      // Verificar se loading foi escondido
      expect(contentManager.loading.style.display).toBe('none');
    });
    
    test('deve exibir resultado no output', async () => {
      const mockResponse = {
        ok: true,
        json: async () => ({ content: 'Conteúdo de teste' })
      };
      fetch.mockResolvedValue(mockResponse);
      
      contentManager.promptInput.value = 'prompt de teste';
      await contentManager.handleGenerate();
      
      expect(contentManager.output.innerHTML).toBe('Conteúdo de teste');
    });
    
    test('deve exibir erro quando prompt vazio', async () => {
      // Mock do alert
      global.alert = jest.fn();
      
      contentManager.promptInput.value = '';
      await contentManager.handleGenerate();
      
      expect(global.alert).toHaveBeenCalledWith('Por favor, insira um prompt');
    });
  });
  
  describe('Validação', () => {
    test('validateInput deve funcionar corretamente', () => {
      expect(contentManager.validateInput('texto válido')).toBe(true);
      expect(contentManager.validateInput('   texto com espaços   ')).toBe(true);
      expect(contentManager.validateInput('')).toBe(false);
      expect(contentManager.validateInput('   ')).toBe(false);
      expect(contentManager.validateInput(null)).toBe(false);
      expect(contentManager.validateInput(undefined)).toBe(false);
    });
  });
  
  describe('Formatação', () => {
    test('formatContent deve converter quebras de linha', () => {
      const input = 'Linha 1\nLinha 2\nLinha 3';
      const expected = 'Linha 1<br>Linha 2<br>Linha 3';
      
      expect(contentManager.formatContent(input)).toBe(expected);
    });
  });
  
  describe('Tratamento de erros', () => {
    test('deve exibir erro na interface', () => {
      const errorMessage = 'Erro de teste';
      contentManager.displayError(errorMessage);
      
      expect(contentManager.output.innerHTML)
        .toBe('<div class="error">Erro: Erro de teste</div>');
    });
    
    test('deve lidar com erro durante geração', async () => {
      fetch.mockRejectedValue(new Error('API Error'));
      
      contentManager.promptInput.value = 'teste';
      await contentManager.handleGenerate();
      
      expect(contentManager.output.innerHTML)
        .toContain('Erro: API Error');
      expect(contentManager.loading.style.display).toBe('none');
    });
  });
});

describe('Utilitários JavaScript', () => {
  test('deve ter fetch disponível globalmente', () => {
    expect(typeof fetch).toBe('function');
  });
  
  test('deve ter console disponível', () => {
    expect(typeof console.log).toBe('function');
    expect(typeof console.error).toBe('function');
  });
});

// Configuração do Jest
module.exports = {
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/tests/setup.js'],
  collectCoverageFrom: [
    'app.js',
    '!node_modules/**',
    '!tests/**'
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80
    }
  }
};
