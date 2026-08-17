# Fight Analysis System

Sistema de análise técnica para vídeos de lutas (MMA, Muay Thai e Jiu-Jitsu).

## 🥋 Funcionalidades

- ✅ Análise de performance dos lutadores
- ✅ Identificação de erros técnicos
- ✅ Processamento de frames de vídeo
- ✅ Detecção de movimentos e posições
- ✅ Estatísticas em tempo real
- ✅ Relatórios detalhados de análise
- ✅ **Sistema de planos mensal (Individual R$40/mês, Academia R$80/mês)**

## 📋 Requisitos

- Python 3.8+
- OpenCV
- MediaPipe
- NumPy
- Matplotlib

## 🚀 Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/Isac-Figueira/fight-analysis.git
cd fight-analysis
```

### 2. Crie um ambiente virtual
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

## 📁 Estrutura do Projeto

```
fight-analysis/
├── src/
│   ├── __init__.py
│   ├── video_processor.py      # Processa vídeos e orquestra análise
│   ├── pose_detector.py        # Detecta poses com MediaPipe
│   ├── movement_analyzer.py    # Analisa movimentos por tipo de luta
│   ├── performance_evaluator.py # Avalia performance geral
│   ├── error_detector.py       # Detecta erros técnicos
│   ├── subscription_manager.py # Gerencia planos e assinaturas
│   └── utils.py                # Funções auxiliares
├── data/
│   ├── videos/                 # Armazena vídeos para análise
│   ├── models/                 # Modelos treinados (futuro)
│   └── outputs/                # Resultados das análises
├── tests/                      # Testes unitários
├── main.py                     # Script principal
├── requirements.txt            # Dependências do projeto
├── README.md                   # Este arquivo
├── SUBSCRIPTION.md             # Documentação do sistema de planos
└── .gitignore                  # Arquivos ignorados pelo Git
```

## 💻 Como Usar

### Via linha de comando:
```bash
python main.py data/videos/meu_video.mp4 --fight-type mma --sample-rate 1
```

### Opções disponíveis:
- `video_path`: Caminho do vídeo (obrigatório)
- `--fight-type`: Tipo de luta (mma, muay_thai, jiu_jitsu) [padrão: mma]
- `--sample-rate`: Processar cada Nº frame [padrão: 1]
- `--output`: Arquivo de saída [padrão: data/outputs/analysis_results.json]

### Via Python:
```python
from src.video_processor import FightAnalyzer

analyzer = FightAnalyzer(
    video_path='data/videos/meu_video.mp4',
    fight_type='mma'
)

results = analyzer.analyze(sample_rate=1)
print(f"Performance: {results['performance_metrics']['overall_score']}/10")
```

## 💳 Sistema de Planos

O aplicativo possui um sistema de assinatura mensal:

### 🎓 Plano Individual - R$ 40/mês
- 10 análises de vídeos por mês
- 50GB de armazenamento
- Relatórios mensais
- Suporte via email

### 🏢 Plano Academia - R$ 80/mês
- 100 análises de vídeos por mês
- 500GB de armazenamento
- Múltiplos usuários
- Suporte prioritário

Veja [SUBSCRIPTION.md](SUBSCRIPTION.md) para mais detalhes.

## 📊 Saída da Análise

O programa gera:
- **Métricas de Performance**: Score geral (0-10), qualidade de postura, movimentação
- **Movimentos Detectados**: Lista de técnicas identificadas com confiança
- **Erros Técnicos**: Problemas encontrados com severidade
- **Relatórios Detalhados**: Frame-by-frame analysis

## 🛠️ Tecnologias

- **OpenCV** - Processamento de vídeo
- **MediaPipe** - Detecção de poses em tempo real
- **NumPy** - Cálculos matemáticos
- **Matplotlib** - Visualizações
- **tqdm** - Barra de progresso

## 🔧 Próximas Features

- [ ] Integração com Stripe/PayPal
- [ ] Interface gráfica com Tkinter/PyQt
- [ ] Exportar vídeo com anotações
- [ ] Banco de dados de técnicas
- [ ] API REST para integração
- [ ] Dashboard de administrador
- [ ] Modelos de IA (CNN) para detecção avançada

## 📝 Licença

MIT License - veja LICENSE para detalhes

## 👤 Autor

Isac Figueira - [@Isac-Figueira](https://github.com/Isac-Figueira)
