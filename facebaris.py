import cv2
import os

# Kamera numarası (0, 1, 2, ...) - Birden fazla kamera varsa değiştirilebilir
camera_number = 0

# Haar Cascade yüz sınıflandırıcısı
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Kamera açma
cap = cv2.VideoCapture(camera_number)

# Klasörü oluştur
output_folder = 'faces'
os.makedirs(output_folder, exist_ok=True)

# Tanınan yüz sayısı
recognized_faces = set()

while True:
    # Kameradan bir kare al
    ret, frame = cap.read()

    # Gri tona dönüştür
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Yüzleri tespit et
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    # Her yüzü işle
    for (x, y, w, h) in faces:
        # Yüzü kırp
        face_img = frame[y:y+h, x:x+w]

        # Yüzü tanıma kontrolü
        face_hash = hash(face_img.tobytes())
        if face_hash not in recognized_faces:
            # Tanınan yüzü kaydet
            img_name = os.path.join(output_folder, f'{len(recognized_faces) + 1}.jpg')

            # Yüzü işaretle
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, 'Face', (x, y-10), font, 0.9, (0, 0, 255), 2)

            # Görüntüyü tam ekran kaydet
            cv2.imwrite(img_name, frame, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

            recognized_faces.add(face_hash)

    # Kameradan alınan görüntüyü tam ekran göster
    cv2.imshow('Camera', frame)

    # Çıkış için 'q' tuşuna basın
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Kamera ve pencereyi kapat
cap.release()
cv2.destroyAllWindows()
