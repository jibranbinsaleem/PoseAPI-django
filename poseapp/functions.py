from ultralytics import YOLO
import cv2
import time
import numpy as np

model = YOLO('yolov8n-pose.pt')
# print(model)

def visualize_keypoints(image, keypoints, confidence_threshold=0.5):
    # Convert image to numpy array if necessary
    if not isinstance(image, np.ndarray):
        image = np.array(image)

    keypoint_pairs = [(0, 1), (0, 2), (0, 3), (0, 4), (1, 5), (1, 6), (6, 8), (10, 8), (7, 9), (6, 12),
                      (7, 5), (11, 12), (11, 5), (12, 14), (13, 11), (13, 15), (14, 16)]

    try:
        if keypoints.numel() != 0:
            for pair in keypoint_pairs:
                # print(keypoints)\
                for point in keypoints:
                    point1 = point[pair[0]]
                    point2 = point[pair[1]]

                    # Only draw the line if both keypoints are detected with confidence above the threshold
                    # if point1[2] > confidence_threshold and point2[2] > confidence_threshold:
                    x1, y1 = int(point1[0]), int(point1[1])
                    x2, y2 = int(point2[0]), int(point2[1])
                    if x1 != 0.0 and y1 != 0.0 and x2 != 0.0 and y2 != 0.0:
                        # Draw a line between the keypoints
                        cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), thickness=1)
                
            for keypoint in keypoints:
                for x, y in keypoint:
                    # Draw a circle on the image for each keypoint
                    cv2.circle(image, (int(x), int(y)), 5, (0, 255, 0), thickness=-1)   
    except Exception as e:
        cv2.imwrite('error.jpg', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        print(keypoints)
    
        print(e)
        exit()
    
    return image


  

# Load the image
def infer(image):
    
    # Get the keypoints from your YOLOv8 inference
    print("line 50 ingfeer")
    result = model(image)
    # Visualize the keypoints
    keypoints = result[0].keypoints.xy
    print(keypoints)
    image_with_keypoints = visualize_keypoints(image, keypoints)

    return image_with_keypoints

def inferpoints(image):
    
    # Get the keypoints from your YOLOv8 inference
    print("line 567 ingfeer")
    result = model(image)
    # Visualize the keypoints
    keypoints = result[0].keypoints.xy

    return keypoints.tolist()

if __name__ == "__main__":
    infer()
