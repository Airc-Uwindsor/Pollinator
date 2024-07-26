from ultralytics import YOLO

# load pre-trained yolov5n model
model = YOLO('yolov5nu.pt')

# train yolov5n model on custom dataset
model.train(data='data.yaml', epochs=2, imgsz=640) # ep

# evaluate yolov5n model on test set
results = model.evaluate(data='data.yaml')
print(results)

# save yolov5n model
model.save('tomato_yolov5nu.pt')