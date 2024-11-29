

## Simulação Sistema Massa Mola

### Objetivo e Tipo de Projeto:
Este projeto é uma **simulação** criada para **visualizar** o comportamento de um sistema massa-mola com amortecimento. O objetivo principal é simular o movimento de uma massa presa a uma mola, permitindo que o usuário interaja com a simulação ajustando parâmetros como massa, constante da mola e coeficiente de amortecimento. A simulação ajuda a compreender como esses fatores influenciam o movimento da massa ao longo do tempo.

A simulação é **interativa** e permite ao usuário visualizar o impacto das mudanças nos parâmetros físicos diretamente no comportamento da mola e da massa.

![Imagem do sistema massa-mola](images/spring_system.gif) *(Coloque aqui uma imagem ou GIF da simulação)*

### Conceitos de Física e Modelo Matemático:

- **Conceito Principal:** A simulação explora o **movimento oscilatório** de um sistema massa-mola com amortecimento. A massa é puxada para a direita e, em seguida, é retardada pela força da mola e pela força de amortecimento.

- **Modelo Matemático:** O modelo matemático utilizado é baseado na **segunda lei de Newton** para sistemas dinâmicos, que pode ser expresso pela equação diferencial:

  \[
  m \cdot \ddot{x} = -k \cdot x - b \cdot \dot{x}
  \]

  Onde:
  - \(m\) é a massa da partícula,
  - \(k\) é a constante elástica da mola,
  - \(b\) é o coeficiente de amortecimento,
  - \(x\) é o deslocamento da massa em função do tempo.

- **Aplicabilidade:** Esta simulação permite observar o comportamento do sistema com diferentes valores para a massa, a constante da mola e o amortecimento. É útil para estudar o efeito do amortecimento no movimento oscilatório, o que é relevante para muitas aplicações, como em sistemas mecânicos e engenharia.

## Implementação

### Linguagens e Pacotes:
O projeto foi implementado em **Python**, utilizando o pacote **PyGame** para a interface gráfica e a simulação interativa. PyGame fornece funcionalidades para desenhar a mola e a massa, e também para capturar a interação do usuário.

### Como Usar

#### Instalação e Dependências:

Certifique-se de que o **Python 3.6+** está instalado no seu sistema.

Dependências do projeto:

- **PyGame**: para renderizar a interface gráfica e simular o movimento da massa e da mola.

Para instalar as dependências necessárias, execute o seguinte comando:

```bash
pip install -r requirements.txt
```

#### Exemplos de Uso:

Para rodar a simulação básica, basta executar o código com o comando:

```bash
python spring.py
```

### Configuração Inicial:
A simulação começa com valores padrão para os parâmetros de massa (1.0 kg), constante da mola (10.0 N/m) e coeficiente de amortecimento (0.5 kg/s). No entanto, o usuário pode ajustar esses valores dinamicamente durante a execução da simulação utilizando caixas de entrada interativas.

Os parâmetros podem ser ajustados para diferentes experimentos, o que permite ao usuário explorar como esses parâmetros influenciam o movimento da massa.

## Informações sobre o Projeto:

Este projeto foi desenvolvido por:

- **Rafael Corona**: rafael@usp.br
- **Gustavo Brunelli**: gustavo@usp.br
- **Alexandre Brito Gomes**: alexandre.brito@usp.br

Como parte do processo avaliativo da disciplina **7600105 - Física Básica I (2024)** da **USP-São Carlos**, ministrada pela(o) **Prof. Krissia de Zawadzki/Esmerindo de Sousa Bernardes**.

---

Esse README segue o formato e as diretrizes que você pediu, oferecendo uma explicação clara do projeto, sua implementação e instruções de uso. Se precisar de mais detalhes ou ajustes, posso ajudar!