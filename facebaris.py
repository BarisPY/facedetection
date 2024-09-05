import cv2
import os

# Camera number (0, 1, 2, ...) - can be changed if there is more than one camera
camera_number = 0

# Haar Cascade face classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Camera opening
cap = cv2.VideoCapture(camera_number)

# Create folder
output_folder = 'faces'
os.makedirs(output_folder, exist_ok=True)

# Number of recognised faces
recognized_faces = set()

while True:
    # Take a frame from the camera
    ret, frame = cap.read()

    # Convert to grey tone
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    # Process each face
    for (x, y, w, h) in faces:
        # Crop the face
        face_img = frame[y:y+h, x:x+w]

        # Face recognition check
        face_hash = hash(face_img.tobytes())
        if face_hash not in recognized_faces:
            # Save the recognisable face
            img_name = os.path.join(output_folder, f'{len(recognized_faces) + 1}.jpg')

            # Mark the face
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, 'Face', (x, y-10), font, 0.9, (0, 0, 255), 2)

            # Save image full screen
            cv2.imwrite(img_name, frame, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

            recognized_faces.add(face_hash)

    # Show the image from the camera full screen
    cv2.imshow('Camera', frame)

    # Press ‘q’ to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Close camera and window
cap.release()
cv2.destroyAllWindows()
