import random

class ContentGenerator:
    def __init__(self):
        self.templates = {
            "technical": [
                "Avanços recentes em {topic} demonstram um potencial significativo para {application}.",
                "A implementação de {topic} requer uma compreensão aprofundada de {concept} e {methodology}.",
                "A análise de {topic} revela a importância de {factor} na otimização de {processo}."
            ],
            "marketing": [
                "Descubra como {topic} pode transformar seu negócio e impulsionar {resultado}.",
                "Maximize seu alcance com estratégias inovadoras de {topic} para {publico_alvo}.",
                "O futuro de {topic} está aqui: soluções personalizadas para {desafio}."
            ]
        }

    def generate_article(self, topic, length, style="technical"):
        if style not in self.templates:
            style = "technical"

        template = random.choice(self.templates[style])
        
        # Simple placeholder replacement for demonstration
        content = template.format(
            topic=topic,
            application="aplicações práticas",
            concept="algoritmos complexos",
            methodology="abordagens iterativas",
            factor="eficiência de dados",
            processo="sistemas distribuídos",
            resultado="o engajamento do cliente",
            publico_alvo="mercados emergentes",
            desafio="a competitividade do mercado"
        )
        
        # Simulate length by repeating content
        num_repetitions = length // len(content) + 1
        full_content = (content + " ") * num_repetitions
        
        return full_content[:length] + "..."

if __name__ == "__main__":
    generator = ContentGenerator()
    
    # Exemplo de geração de conteúdo técnico
    tech_content = generator.generate_article(
        topic="Inteligência Artificial",
        length=500,
        style="technical"
    )
    print("\n--- Conteúdo Técnico ---")
    print(tech_content)

    # Exemplo de geração de conteúdo de marketing
    marketing_content = generator.generate_article(
        topic="Marketing Digital",
        length=300,
        style="marketing"
    )
    print("\n--- Conteúdo de Marketing ---")
    print(marketing_content)

