from ultralytics import YOLO

# para marcar as imagens
# https://www.makesense.ai/

def main():
    model = YOLO("yolov8n.pt")

    model.train(data="r_acidente.yaml", epochs=30, device=0)
    metrics = model.val()

if __name__ == '__main__':
    main()
