from ultralytics import YOLO

    # Load a pretrained model (e.g., yolov8n.pt for a nano model)
model = YOLO('yolov8n.pt')

    # Train the model with your custom dataset
model.train(data='./data.yaml', epochs=200, imgsz=640, batch=6,patience=50,lr0=0.001,optimizer='AdamW',)