from ultralytics import YOLO

if __name__ == "__main__":
    # Load a pretrained YOLOv8s model
    model = YOLO("yolov8s.pt")

    # Train the model
    model.train(
        data="data.yaml",   # dataset config file
        epochs=50,
        imgsz=640,
        batch=16,
        device=0,
        workers=0   # <--- important for Windows
    )
