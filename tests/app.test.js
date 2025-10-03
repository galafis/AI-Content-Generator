/**
 * Testes para o app.js - Funcionalidades JavaScript
 * 
 * Este arquivo contém testes unitários para validar
 * as funcionalidades JavaScript da aplicação AI Content Generator.
 */

// Mock do DOM para testes
const { JSDOM } = require("jsdom");
const dom = new JSDOM("<!DOCTYPE html><html><body></body></html>");
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

// Importar a classe ApplicationManager diretamente
const ApplicationManager = require("../src/app.js");

describe("ApplicationManager - Content Generation", () => {
  let appManager;
  
  beforeEach(() => {
    // Reset mocks
    fetch.mockClear();
    console.log.mockClear();
    console.error.mockClear();
    
    // Criar uma estrutura DOM mínima para o teste
    document.body.innerHTML = `
      <form id="content-form">
        <input id="topic" type="text" value="Test Topic" />
        <input id="length" type="number" value="100" />
        <select id="style">
          <option value="technical" selected>Technical</option>
          <option value="marketing">Marketing</option>
        </select>
        <button type="submit">Generate</button>
      </form>
      <pre id="output-content"></pre>
    `;
    
    // Instanciar ApplicationManager
    appManager = new ApplicationManager();
    // Chamar setupContentGeneratorForm explicitamente, pois o DOMContentLoaded já pode ter disparado
    appManager.setupContentGeneratorForm();
  });
  
  afterEach(() => {
    document.body.innerHTML = "";
  });
  
  test("deve gerar conteúdo com sucesso", async () => {
    const mockContent = "Generated content for Test Topic.";
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ content: mockContent }),
    });

    const form = document.getElementById("content-form");
    form.dispatchEvent(new dom.window.Event("submit"));

    // Aguardar a conclusão da Promise dentro do event listener
    await new Promise(resolve => setTimeout(resolve, 0));

    expect(fetch).toHaveBeenCalledWith("/api/generate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ topic: "Test Topic", length: 100, style: "technical" }),
    });
    expect(document.getElementById("output-content").textContent).toBe(mockContent);
  });

  test("deve exibir mensagem de erro em caso de falha na API", async () => {
    fetch.mockResolvedValueOnce({
      ok: false,
      status: 500,
    });

    const form = document.getElementById("content-form");
    form.dispatchEvent(new dom.window.Event("submit"));

    await new Promise(resolve => setTimeout(resolve, 0));

    expect(document.getElementById("output-content").textContent).toContain("Failed to generate content");
    expect(console.error).toHaveBeenCalled();
  });

  test("deve mostrar mensagem de 'Generating content...' durante a geração", async () => {
    fetch.mockReturnValueOnce(new Promise(() => {})); // Never resolve to keep it in pending state

    const form = document.getElementById("content-form");
    form.dispatchEvent(new dom.window.Event("submit"));

    expect(document.getElementById("output-content").textContent).toBe("Generating content...");
  });
});

// Configuração do Jest
module.exports = {
  testEnvironment: "jsdom",
  // setupFilesAfterEnv: ["<rootDir>/tests/setup.js"], // Removido ou ajustado conforme necessário
  collectCoverageFrom: [
    "src/app.js",
    "!node_modules/**",
    "!tests/**"
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
