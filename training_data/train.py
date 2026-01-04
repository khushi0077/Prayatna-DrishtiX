from ultralytics import YOLO

def train_model():
    # 1. Load the "Nano" model (v8n)
    # This is the smallest, fastest model available, perfect for low latency.
    model = YOLO('yolov8n.pt') 

    # 2. Train the model
    # data: Path to your data.yaml file
    # epochs: 50 is a good balance for speed vs accuracy
    # imgsz: 640 is standard, but 320 is faster (less accurate)
    results = model.train(
        data='dataset/data.yaml', 
        epochs=50, 
        imgsz=640, 
        batch=16,
        name='agrishield_model' 
    )

    # 3. Export for optimization
    # Exporting to TFLite or ONNX creates a lighter file for edge devices
    model.export(format='tflite') 

if __name__ == '__main__':
    train_model()
