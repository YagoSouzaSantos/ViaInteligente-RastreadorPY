# Rastreador - Projeto Via inteligente RESTIC36
Este projeto realiza a detecção de objetos em colisão a partir de imagens de vídeo, utilizando o modelo YOLO. Ao identificar um objeto, envia os dados para uma API Django no formato JSON. Os dados enviados incluem uma descrição, uma imagem no formato base64 e informações de localização do evento capturado pela aplicação.

## Requisitos
Certifique-se de ter os seguintes itens instalados no seu ambiente antes de começar:

- Python 3.8 ou superior
- pip (gerenciador de pacotes do Python)
- OpenCV (cv2)
- Ultralytics YOLO
- Biblioteca requests

# Configuração do Ambiente
1. **Clone o Repositório**
``` bash
git clone https://github.com/seu_usuario/seu_repositorio.git
cd ViaInteligente-RastreadorPY
```

2. **Instale as Dependências**
```bash
pip install -r requirements.txt
```

Se o arquivo requirements.txt ainda não existir, crie-o com o seguinte conteúdo:

```plaintext
ultralytics
opencv-python
requests
numpy
```
Para gerar automaticamente um requirements.txt com os pacotes instalados no ambiente, execute:
```bash
pip freeze > requirements.txt
```

# Como Rodar o Projeto
1. Execute o Código de Detecção
Com o ambiente configurado, execute o script principal:
```bash
python collision_capture_test.py
```

O script:
- Lê o vídeo especificado.
- Usa o modelo YOLO para detectar objetos.
- Quando um objeto é detectado, converte o frame em base64 e envia um POST para a API Django configurada.
