import cv2
import numpy as np
from pathlib import Path


class ShipAnalyzer:
    def __init__(self, cm_per_pixel=0.1):
        self.cm_per_pixel = cm_per_pixel
        # Ship types and their properties
        self.ship_types = {
            'Tanker': {'color': ([20, 100, 100], [30, 255, 255]), 'size': 250},
            'Cargo Ship': {'color': ([0, 100, 100], [10, 255, 255]), 'size': 180},
            'Warship': {'color': ([100, 100, 100], [140, 255, 255]), 'size': 120},
            'Sailboat': {'color': ([35, 50, 50], [85, 255, 255]), 'size': 12}
        }

    def analyze_image(self, image_path):
        """Process the image and detect ships"""
        img = cv2.imread(str(image_path))
        if img is None:
            print(f"Error: {image_path} not found!")
            return None, None

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        output_img = img.copy()
        detected_ships = []

        for ship_name, properties in self.ship_types.items():
            lower_color, upper_color = properties['color']
            mask = cv2.inRange(hsv, np.array(lower_color), np.array(upper_color))

            # Noise removal
            kernel = np.ones((3, 3), np.uint8)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for i, contour in enumerate(contours):
                if cv2.contourArea(contour) > 10:
                    rect = cv2.minAreaRect(contour)
                    box = cv2.boxPoints(rect)
                    box = np.intp(box)

                    # Draw ship rectangle
                    cv2.drawContours(output_img, [box], 0, (0, 0, 255), 2)

                    # Label the ship
                    center = (int(rect[0][0]), int(rect[0][1]))
                    cv2.putText(output_img, f"{ship_name}-{i + 1}",
                                (center[0] - 50, center[1] - 20),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

                    # Store measurements
                    length_px = max(rect[1])
                    width_px = min(rect[1])
                    detected_ships.append({
                        'type': ship_name,
                        'number': i + 1,
                        'length_cm': length_px * self.cm_per_pixel,
                        'width_cm': width_px * self.cm_per_pixel,
                        'position': rect[0],
                        'angle': rect[2]
                    })

        return detected_ships, output_img


if __name__ == "__main__":
    analyzer = ShipAnalyzer()

    # Analyze the image
    ships, output_img = analyzer.analyze_image("radar1.png")

    if ships:
        # Show results
        cv2.imshow('Detected Ships', output_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Save the image
        cv2.imwrite("ship_detections1.png", output_img)
        print("Image saved as 'ship_detections.png'")

        # Print report to console
        print("\nSHIP DETECTION REPORT")
        print("=" * 60)
        for ship in ships:
            print(f"\n{ship['type']}-{ship['number']}:")
            print(f"  Length: {ship['length_cm']:.2f} cm")
            print(f"  Width: {ship['width_cm']:.2f} cm")
            print(f"  Position (X,Y): ({ship['position'][0]:.1f}, {ship['position'][1]:.1f})")
            print("-" * 60)
    else:
        print("No ships detected!")
