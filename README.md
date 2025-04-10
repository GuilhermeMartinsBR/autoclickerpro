# Auto Clicker Pro

Um autoclicker avançado com interface gráfica amigável, desenvolvido em Python usando Tkinter e pynput.

![Badge do Python](https://img.shields.io/badge/Python-3.10-blue.svg)
![Licença - GitHub](https://img.shields.io/github/license/GuilhermeMartinsBR/autoclickerpro)

![Auto Clicker Pro Screenshot](https://github.com/GuilhermeMartinsBR/autoclickerpro/blob/main/Janela%20AutoClickerPro%20-%20PrintScreen.png?raw=true)

## Características

- Interface gráfica moderna e intuitiva com abas organizadas
- Controle de intervalo entre cliques (em segundos)
- Múltiplos tipos de clique (único, duplo, triplo)
- Escolha do botão do mouse (esquerdo, direito, meio)
- Opção para clicar na posição atual do cursor ou em posição fixa
- Definição de coordenadas X e Y para cliques em posição específica
- Captura automática da posição atual do cursor
- Personalização da tecla de atalho para ativar/desativar
- Opção para enviar teclas do teclado em vez de cliques do mouse
- Salvamento e carregamento de configurações personalizadas

## Requisitos

- Python 3.6 ou superior
- Bibliotecas:
  - tkinter (normalmente incluído na instalação padrão do Python)
  - pynput
  - threading (biblioteca padrão)
  - json (biblioteca padrão)

## Instalação

1. Clone este repositório:
```bash
git clone https://github.com/seu-usuario/auto-clicker-pro.git
cd auto-clicker-pro
```

2. Instale as dependências necessárias:
```bash
pip install pynput
```

3. Execute o programa:
```bash
python main.py
```

## Como usar

### Configurações Básicas

Na aba "Configurações Principais":

1. **Intervalo entre cliques**: Defina o tempo (em segundos) entre cada clique
2. **Tipo de clique**: Escolha entre clique único, duplo ou triplo
3. **Botão do mouse**: Selecione qual botão do mouse será usado (esquerdo, direito ou meio)
4. **Posição do clique**:
   - **Cursor**: Os cliques seguirão a posição atual do cursor
   - **Posição fixa**: Os cliques ocorrerão sempre nas coordenadas X,Y especificadas
   - Use o botão "Capturar posição atual" para definir automaticamente as coordenadas

### Configurações Avançadas

Na aba "Configurações Avançadas":

1. **Tecla de atalho**:
   - Clique em "Definir nova tecla" e pressione a tecla desejada para ativar/desativar o autoclicker
   - A tecla padrão é F6

2. **Enviar tecla em vez de clicar**:
   - Ative esta opção para que o programa envie pressionamentos de tecla repetidos em vez de cliques do mouse
   - Especifique qual tecla deve ser enviada (ex: a, b, enter, space, etc.)

3. **Salvar configurações**:
   - Use o botão "Salvar configurações" para manter suas preferências para uso futuro
   - O botão "Restaurar padrões" retorna todas as configurações aos valores iniciais

### Controles Principais

- **Iniciar**: Começa a sequência de cliques automáticos com as configurações atuais
- **Parar**: Interrompe a sequência de cliques
- A tecla de atalho definida (F6 por padrão) alterna entre iniciar e parar

## Notas importantes

- O programa salva suas configurações em um arquivo chamado `autoclicker_config.json` no mesmo diretório
- Para usar a captura de posição fixa, a janela será minimizada por 1 segundo para permitir que você posicione o cursor
- Para aplicações que exigem direitos de administrador, execute o programa com privilégios elevados
- O programa usa threads para não bloquear a interface enquanto executa os cliques

## Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fazer um fork do projeto
2. Criar uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas alterações (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Criar um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## Aviso Legal

Este software é fornecido apenas para fins educacionais e de produtividade. O uso indevido para burlar sistemas de jogos, sites ou outros serviços pode violar os termos de serviço desses produtos. Use com responsabilidade.
