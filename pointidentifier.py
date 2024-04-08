import cv2

def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Coordinates: ({x}, {y})")

# Load an image
img = cv2.imread('Resources/check.jpg')  # Replace with the path to your image

# Create a window and set the callback function
cv2.namedWindow('Image')
cv2.setMouseCallback('Image', click_event)

while True:
    # Display the image
    cv2.imshow('Image', img)

    # Check for the 'ESC' key to exit the loop
    key = cv2.waitKey(1) & 0xFF
    if key == 27:
        break

# Close all OpenCV windows
cv2.destroyAllWindows()