# HandMotion
![Banner Handmotion](https://github.com/user-attachments/assets/43d3c10d-1c01-44f8-a090-4ee8d814eb70)
This project implements a gesture control system using a webcam to detect and track hands in real time. The hand movement is converted into mouse cursor movements, and a specific finger gesture can be used to perform mouse clicks. Additionally, the project includes an executable, allowing the system to be used without the need to manually run the code in a development environment.

## Executable
[View Releases](https://github.com/Gustavo-michel/HandMotion/releases)

## Technologies Used
- Python: Programming language used for project development.

- OpenCV: Library used for video capture and image processing.

- Tensorflow: Library to load the model and predict gestures.

- Numpy: Library to deal with arrays and mathematical things.

- MediaPipe: Google's framework used for hand detection and tracking.

- PyAutoGUI: Library used for mouse control on the operating system.

## Features
- Real-Time Hand Detection: The project uses the webcam to capture real-time video and track the user's hand.

- Cursor Control: The hand movement detected by MediaPipe is mapped to the computer screen. the center point of hand (point 9 in MediaPipe) is used to move the mouse cursor with  aspecific gesture (e.g., leave your hand open).

- Left-Click Gesture: A specific gesture (e.g., closing all fingers) triggers a left mouse click.

- Right-Click Gesture: A distinct gesture (e.g., lifting the thumb and thumb while keeping the other fingers closed) triggers a right mouse click.

- Next Tab Gesture: A gesture (e.g., make a right arrow) allows you to navigate to the next tab in your browser or application.

- Previous Tab Gesture: A gesture (e.g., make a left arrow) allows you to navigate to the previous tab in your browser or application.

- Page Up Gesture: A gesture (e.g., moving the hand upward) scrolls the page up.

- Page Down Gesture: A gesture (e.g., moving the hand downward) scrolls the page down.

Note: Detailed instructions on how to perform all gestures are provided in the  [User Guide](Shortly!). Make sure to refer to it for a seamless experience!

## Setup and Installation 
### Requirements (for developers)
Python 3.8 or higher (Python 3.12 recommended).
requirements.txt libraries.
