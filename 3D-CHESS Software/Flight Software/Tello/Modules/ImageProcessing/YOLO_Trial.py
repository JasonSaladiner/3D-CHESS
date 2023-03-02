import tellopy
import cv2

# Initialize Tello drone
drone = tellopy.Tello()
drone.connect()
drone.wait_for_connection()

# Initialize OpenCV video capture
cap = cv2.VideoCapture(0)

# Load YOLO Darknet model and configuration
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")

# Set classes to detect
classes = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

# Set confidence threshold for object detection
conf_threshold = 0.5

while True:
    # Capture frame from video stream
    ret, frame = cap.read()

    # Run object detection on captured frame
    blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    outputs = net.forward()

    # Process object detection results
    for output in outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > conf_threshold:
                x, y, w, h = detection[:4] * np.array([frame.shape[1], frame.shape[0], frame.shape[1], frame.shape[0]])
                x, y, w, h = int(x - w/2), int(y - h/2), int(w), int(h)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, classes[class_id], (x, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Show processed frame
    cv2.imshow("Object detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video capture and close OpenCV window
cap.release()
cv2.destroyAllWindows()

# Disconnect from Tello drone
drone.quit()
