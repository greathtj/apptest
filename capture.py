import streamlit as st
import cv2
import numpy as np
import mss
import mss.tools

def main():
    st.title("Webcam Capture")

    # Define the screen size and capture region
    monitor = {"top": 0, "left": 0, "width": 640, "height": 480}
    
    # Create a placeholder to display the captured image
    image_placeholder = st.empty()

    # Add a button to capture an image
    if st.button("Capture"):
        # Create a screenshot of the capture region
        with mss.mss() as sct:
            sct_img = sct.grab(monitor)
            # Convert the screenshot to a numpy array
            img = np.array(sct_img)
            # Convert the image to RGB format
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
            # Display the captured image
            image_placeholder.image(img, caption="Captured Image")

    # Release the camera and close the window
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
