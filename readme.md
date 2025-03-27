# ScoreInsight

**ScoreInsight** é um projeto que utiliza o Selenium para coletar estatísticas de times de futebol em competições específicas. Ele automatiza a extração de dados de sites como o SofaScore e organiza as informações em um formato estruturado para fácil manipulação e análise.

## Funcionalidades

- Navegação automatizada para a página de um time específico.
- Extração de estatísticas de diferentes categorias, como:
  - Posição e pontuação.
  - Resumo.
  - Ataque.
  - Passe.
  - Defesa.
  - Outros.
- Organização das estatísticas em uma classe (`TeamStats`) para fácil manipulação.
- Exibição das estatísticas coletadas no console.

## Estrutura do Projeto
ScoreInsight/ ├── dto/ │ └── teamStats.py # Classe para armazenar e manipular estatísticas do time. ├── utils/ │ └── constants.py # Constantes e XPaths utilizados no projeto. ├── competition_team_stats.py # Script principal para extração de estatísticas. └── README.md # Documentação do projeto.

## Pré-requisitos

- Python 3.8 ou superior.
- Google Chrome instalado.
- [ChromeDriver](https://chromedriver.chromium.org/) compatível com a versão do Chrome instalada.
- Bibliotecas Python:
  - `selenium`

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/ScoreInsight.git
   cd ScoreInsight

2. Crie um ambiente virtual (opcional, mas recomendado):
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

3. Instale as dependências:
pip install selenium

4. Certifique-se de que o ChromeDriver está no PATH ou no mesmo diretório do projeto.
Uso
  1. Abra o arquivo competition_team_stats.py e configure o time desejado na variável teams (exemplo: Real Madrid).
  2. Execute o script: python competition_team_stats.py
  3. As estatísticas coletadas serão exibidas no console.

Personalização
  - Adicionar novos times: Atualize o dicionário teams no arquivo competition_team_stats.py com o nome do time e o XPath correspondente.
  - Alterar categorias ou XPaths: Edite o arquivo utils/constants.py para ajustar os XPaths ou adicionar novas categorias.

Contribuição
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

Licença
Este projeto está licenciado sob a MIT License.

Autor: Renan Silva
Contato: renan.asilva0@gmail.com