import cv2
import numpy as np

def detect_shapes_and_colors(frame):
    output = frame.copy()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)
        if area < 500:  
            continue

        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)

        x, y, w, h = cv2.boundingRect(contour)
        mask = np.zeros_like(gray)
        cv2.drawContours(mask, [contour], -1, 255, -1)
        mean_color = cv2.mean(frame, mask=mask)

      
        shape = "Unknown"
        if len(approx) == 3:
            shape = "Triangle"
        elif len(approx) == 4:
            aspect_ratio = w / float(h)
            shape = "Square" if 0.95 <= aspect_ratio <= 1.05 else "Rectangle"
        elif len(approx) == 5:
            shape = "Pentagon"
        elif len(approx) == 6:
            shape = "Hexagon"
        elif len(approx) > 6:
            shape = "Circle"

      
        color = "Unknown"
        b, g, r = int(mean_color[0]), int(mean_color[1]), int(mean_color[2])
        if r > 200 and g > 200 and b > 200:
            color = "White"
        elif r < 50 and g < 50 and b < 50:
            color = "Black"
        elif r > g and r > b:
            color = "Red"
        elif g > r and g > b:
            color = "Green"
        elif b > r and b > g:
            color = "Blue"
        elif r > 200 and g > 200 and b < 150:
            color = "Yellow"
        elif r > 200 and g < 150 and b > 200:
            color = "Magenta"
        elif r < 150 and g > 200 and b > 200:
            color = "Cyan"

        
        cv2.drawContours(output, [contour], -1, (255, 255, 255), 2)
        text = f"{shape}, {color}, Sinan Çakmak 22YOBİ 1035"
        cv2.putText(output, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

    return output


video_path = "video.mp4"  
cap = cv2.VideoCapture(video_path)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    processed_frame = detect_shapes_and_colors(frame)

    cv2.imshow("Shape and Color Detection", processed_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
