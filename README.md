# HandMotion

Este projeto implementa um sistema de controle por gestos utilizando uma webcam para detectar e rastrear as mãos em tempo real. O movimento da mão é convertido em movimentos do cursor do mouse, e um gesto específico com os dedos pode ser utilizado para executar cliques no mouse. Além disso, o projeto conta com um executável, permitindo que o sistema seja utilizado sem a necessidade de rodar o código manualmente em um ambiente de desenvolvimento.

## Tecnologias Utilizadas
Python: Linguagem de programação utilizada para o desenvolvimento do projeto.
OpenCV: Biblioteca utilizada para captura de vídeo e manipulação de imagens.
MediaPipe: Framework da Google utilizado para a detecção e rastreamento das mãos.
PyAutoGUI: Biblioteca utilizada para controle do mouse no sistema operacional.

## Funcionalidades
Detecção de Mãos em Tempo Real: O projeto usa a webcam para capturar vídeo em tempo real e rastrear a mão do usuário.

Controle do Cursor: O movimento da mão, detectado pela MediaPipe, é mapeado para a tela do computador. O dedo indicador (ponto 9 na MediaPipe) é utilizado para mover o cursor do mouse.

Execução de Cliques: Um gesto específico (todos os dedos fechados) aciona um clique no mouse.

Margem de Segurança: Um ajuste de "margem de segurança" evita que o cursor se mova para além das bordas da tela.

Geração de Executável: O projeto pode ser empacotado como um executável para facilitar a execução em diferentes máquinas sem a necessidade de configurar dependências Python.

## Estrutura do Código
Importação de Bibliotecas: Importação do OpenCV para captura de vídeo, MediaPipe para detecção de mãos, e PyAutoGUI para controle do mouse.

Inicialização da Webcam: O OpenCV (cv2.VideoCapture(0)) é utilizado para abrir a webcam.

Configuração do MediaPipe: MediaPipe Hands é configurado para detectar apenas uma mão por vez (max_num_hands=1).

Configuração da Resolução da Tela: As dimensões da tela são obtidas através da função pyautogui.size().

Rastreamento da Mão: A cada frame capturado pela webcam, o código converte a imagem para RGB, processa a imagem com MediaPipe para obter as landmarks (pontos-chave da mão), e mapeia a posição dos pontos da mão para a tela.

Movimentação do Cursor: O dedo indicador (landmark 9) é mapeado para controlar a posição do cursor.

Condicional para Clique: O sistema checa se os pontos dos dedos estão dobrados (a posição Y dos dedos é maior do que a base dos mesmos). Se todos os dedos indicados estiverem dobrados, um clique é acionado.

## Configuração e Instalação
### Requisitos
Python 3.8 ou superior
Bibliotecas Python:
opencv-python
mediapipe
pyautogui

## Executavel
[Clique aqui para realizar o download do executavel](https://github.com/Gustavo-michel/HandMotion/raw/refs/heads/main/handmotion/HandTracking.exe?download=) 
