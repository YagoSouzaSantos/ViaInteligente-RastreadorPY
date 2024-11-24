import cv2
import base64
import requests
from ultralytics import YOLO
from collections import defaultdict
import numpy as np

video_path = "traffic_images/night_collision_on_a_rainy_day.mp4"
cap = cv2.VideoCapture(video_path)

model = YOLO("runs/detect/train9/weights/best.pt")

track_history = defaultdict(lambda: [])
seguir = True
deixar_rastro = True

def img_to_base64(img):
    _, img_encoded = cv2.imencode('.jpg', img)
    img_base64 = base64.b64encode(img_encoded).decode('utf-8')
    return img_base64

api_url = "http://127.0.0.1:8000/api/acidentes/"

# Dados de autenticação (usuário e senha)
username = "yago"
password = "12345678"

while True:
    ret, img = cap.read()
    if not ret:
        print("Fim do vídeo ou erro na leitura!")
        break

    if seguir:
        results = model.track(img, persist=True)
    else:
        results = model(img)

    
    detected = False
    for result in results:        
        img = result.plot()

        if result.boxes is not None and len(result.boxes) > 0:
            detected = True

        if seguir and deixar_rastro:
            try:
                boxes = result.boxes.xywh.cpu()
                track_ids = result.boxes.id.int().cpu().tolist()

                for box, track_id in zip(boxes, track_ids):
                    x, y, w, h = box
                    track = track_history[track_id]
                    track.append((float(x), float(y)))
                    if len(track) > 30:  # Mantém até 30 pontos no histórico
                        track.pop(0)

                    points = np.hstack(track).astype(np.int32).reshape((-1, 1, 2))
                    cv2.polylines(img, [points], isClosed=False, color=(230, 0, 0), thickness=5)
            except:
                pass

    # Se algo foi detectado o envio deve ser realizado
    if detected:
        print("Objeto identificado, enviando dados para a API.")

        imagem_base64 = img_to_base64(img)
        data = {
            "descricao": "Identificação da imagem: CAM 14",
            "imagem_base64": imagem_base64,
            "localizacao": "Av. dos Navegantes, area32, Centro, Sobradinho"
        }

        try:
            response = requests.post(api_url, json=data, auth=(username, password))
            if response.status_code == 200:
                print("Dados enviados com sucesso!")
            else:
                print(f"Erro ao enviar dados: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição: {e}")
        
        break

    cv2.imshow("Tela", img)

    # Pressione 'q' para sair
    k = cv2.waitKey(1)
    if k == ord('q'):
        break

cap.release()  # Libera o vídeo após o processamento
cv2.destroyAllWindows()
print("Desligando")
