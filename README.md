# HandMotion
This project implements a gesture control system using a webcam to detect and track hands in real time. The hand movement is converted into mouse cursor movements, and a specific finger gesture can be used to perform mouse clicks. Additionally, the project includes an executable, allowing the system to be used without the need to manually run the code in a development environment.

## Executable
[View Releases](https://github.com/Gustavo-michel/HandMotion/releases)

## Technologies Used
Python: Programming language used for project development.

OpenCV: Library used for video capture and image processing.

MediaPipe: Google's framework used for hand detection and tracking.

PyAutoGUI: Library used for mouse control on the operating system.

## Features
Real-Time Hand Detection: The project uses the webcam to capture real-time video and track the user's hand.

Cursor Control: The hand movement detected by MediaPipe is mapped to the computer screen. The index finger (point 9 in MediaPipe) is used to move the mouse cursor.

Click Execution: A specific gesture (all fingers closed) triggers a mouse click.

Safety Margin: A "safety margin" adjustment prevents the cursor from moving beyond the edges of the screen.

Executable Generation: The project can be packaged as an executable to facilitate execution on different machines without the need to configure Python dependencies.

## Setup and Installation
### Requirements
Python 3.8 or higher (Python 3.12 recommended)
