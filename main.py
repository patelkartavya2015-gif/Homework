import cv2

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_smile.xml")

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera")
    raise SystemExit(1)

while True:
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to capture image.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        face_gray = gray[y:y + h, x:x + w]
        smiles = smile_cascade.detectMultiScale(
            face_gray,
            scaleFactor=1.7,
            minNeighbors=20,
            minSize=(15, 15),
        )
        expression = "Smiling" if len(smiles) > 0 else "No smile detected"

        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        label_size, baseline = cv2.getTextSize(
            expression,
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            2,
        )
        label_y = max(y - 8, label_size[1] + baseline + 2)
        label_top = label_y - label_size[1] - baseline
        cv2.rectangle(
            frame,
            (x, label_top),
            (x + label_size[0], label_y),
            (255, 0, 0),
            cv2.FILLED,
        )
        cv2.putText(
            frame,
            expression,
            (x, label_y - baseline),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )

    cv2.imshow("Face and expression detection - Press q to Quit", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()