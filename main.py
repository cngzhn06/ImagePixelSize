import cv2
import numpy as np

# Görüntüyü yükleme
image_path = "image.jpeg"  # Görüntü yolu
image = cv2.imread(image_path)

# Görüntüyü HSV renk uzayına dönüştürme
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Yeşil renk için maske oluşturma (HSV aralığı ayarlanabilir)
green_lower = np.array([35, 100, 50])  # Yeşil alt sınır (HSV)
green_upper = np.array([85, 255, 255])  # Yeşil üst sınır (HSV)
mask = cv2.inRange(hsv, green_lower, green_upper)

# Konturları bulma
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# En büyük konturu seçme (alan olarak)
largest_contour = max(contours, key=cv2.contourArea)

# Konturdan dikdörtgen boyutlarını alma
x, y, width, height = cv2.boundingRect(largest_contour)

# Gerçek dünya boyutlarını tanımlama (örnek: 1 piksel = 0.1 metre)
pixel_to_meter = 0.1
real_width = width * pixel_to_meter
real_height = height * pixel_to_meter

# Sonuçları yazdırma
print(f"Objenin yandan görünüşteki genişliği: {width} piksel ({real_width:.2f} metre)")
print(f"Objenin yandan görünüşteki yüksekliği: {height} piksel ({real_height:.2f} metre)")

# Görselleştirme (isteğe bağlı)
result_image = image.copy()
cv2.rectangle(result_image, (x, y), (x + width, y + height), (0, 0, 255), 2)
cv2.imshow("Sonuç", result_image)
cv2.waitKey(0)
cv2.destroyAllWindows()