## Simulação Sistema Massa Mola

### Objetivo e Tipo de Projeto:
Este projeto é uma **simulação** criada para **visualizar** o comportamento de um sistema massa-mola com amortecimento. O objetivo principal é simular o movimento de uma massa presa a uma mola, permitindo que o usuário interaja com a simulação ajustando parâmetros como massa, constante da mola e coeficiente de amortecimento. A simulação ajuda a compreender como esses fatores influenciam o movimento da massa ao longo do tempo.

A simulação é **interativa** e permite ao usuário visualizar o impacto das mudanças nos parâmetros físicos diretamente no comportamento da mola e da massa.

![Imagem do sistema massa-mola](images/spring_system.gif)

### Conceitos de Física e Modelo Matemático:

- **Conceito Principal:** A simulação explora o **movimento oscilatório** de um sistema massa-mola com amortecimento. A massa é puxada para a direita e, em seguida, é retardada pela força da mola e pela força de amortecimento.

- **Modelo Matemático:** O modelo matemático utilizado é baseado na **segunda lei de Newton** para sistemas dinâmicos, que pode ser expresso pela equação diferencial:

$$ m \cdot \ddot{x} = -k \cdot x - b \cdot \dot{x} $$

  Onde:
  - \(m\) é a massa da partícula,
  - \(k\) é a constante elástica da mola,
  - \(b\) é o coeficiente de amortecimento,
  - \(x\) é o deslocamento da massa em função do tempo.

- **Aplicabilidade:** Esta simulação permite observar o comportamento do sistema com diferentes valores para a massa, a constante da mola e o amortecimento. É útil para estudar o efeito do amortecimento no movimento oscilatório, o que é relevante para muitas aplicações, como em sistemas mecânicos e engenharia.

## Implementação

### Linguagens e Pacotes:
O projeto foi implementado em **Python**, utilizando o pacote **PyGame** para a interface gráfica e a simulação interativa. PyGame fornece funcionalidades para desenhar a mola e a massa, e também para capturar a interação do usuário.


### Como Rodar o Projeto

Há duas formas de executar o projeto: utilizando **Conda** (recomendado) ou diretamente com **Python** e o `pip`.

#### 1. Usando Conda (Recomendado)

**Passo 1: Instalar o Conda**  
Se você ainda não tem o Conda instalado, siga o guia oficial para instalação:
[Conda Installation Guide](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html).

**Passo 2: Criar o Ambiente Conda**  
Após instalar o Conda, crie o ambiente usando o arquivo `environment.yml`:

```bash
conda env create -f environment.yml
```

**Passo 3: Ativar o Ambiente**  
Ative o ambiente criado:

```bash
conda activate spring
```

**Passo 4: Rodar a Simulação**  
Execute o script da simulação:

```bash
python spring.py
```

---

#### 2. Usando Python e `pip`

Caso não utilize o Conda, você pode rodar o projeto diretamente com o Python. Siga os passos abaixo:

**Passo 1: Instalar o Python 3.6+**  
Certifique-se de que uma versão compatível do Python está instalada no seu sistema. Você pode baixar o Python [aqui](https://www.python.org/downloads/).

**Passo 2: Instalar Dependências**  
Instale os pacotes necessários utilizando o `pip`. No terminal, execute:

```bash
pip install -r requirements.txt
```

**Passo 3: Rodar a Simulação**  
Agora, execute o script para iniciar a simulação:

```bash
python spring.py
```

---

### Importações Necessárias:

O script principal (`spring.py`) depende dos seguintes módulos:

```python
import pygame
import sys
import math
```

Certifique-se de que estes pacotes estão instalados para evitar problemas ao executar o código.

---

### Configuração Inicial:
A simulação começa com valores padrão para os parâmetros de massa (1.0 kg), constante da mola (10.0 N/m) e coeficiente de amortecimento (0.5 kg/s). No entanto, o usuário pode ajustar esses valores dinamicamente durante a execução da simulação utilizando caixas de entrada interativas.

Os parâmetros podem ser ajustados para diferentes experimentos, o que permite ao usuário explorar como esses parâmetros influenciam o movimento da massa.
