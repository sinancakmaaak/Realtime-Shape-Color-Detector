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
        if area < 500:  # Ignore small contours
            continue

        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)

        x, y, w, h = cv2.boundingRect(contour)
        roi = frame[y:y + h, x:x + w]
        mask = np.zeros_like(gray)
        cv2.drawContours(mask, [contour], -1, 255, -1)
        mean_color = cv2.mean(frame, mask=mask)

        # Determine shape
        shape = "Unknown"
        if len(approx) == 3:
            shape = "Triangle"
        elif len(approx) == 4:
            aspect_ratio = w / float(h)
            shape = "Square" if 0.95 <= aspect_ratio <= 1.05 else "Rectangle"
        elif len(approx) > 5:
            shape = "Circle"

        # Determine color
        color = "Unknown"
        b, g, r = int(mean_color[0]), int(mean_color[1]), int(mean_color[2])
        if r > g and r > b:
            color = "Red"
        elif g > r and g > b:
            color = "Green"
        elif b > r and b > g:
            color = "Blue"
        elif r > 200 and g > 200 and b < 100:
            color = "Yellow"
        elif r > 200 and g < 100 and b > 200:
            color = "Magenta"
        elif r < 100 and g > 200 and b > 200:
            color = "Cyan"

        # Draw the contour and details
        cv2.drawContours(output, [contour], -1, (255, 255, 255), 2)
        text = f"{shape}, {color}, Area: {int(area)}, Perim: {int(perimeter)}"
        cv2.putText(output, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

    return output

# Video capture
cap = cv2.VideoCapture(0)  # Replace 0 with video file path if needed

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
