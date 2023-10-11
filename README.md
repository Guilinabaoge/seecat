# Cat Drinking Frequency Monitor
I've developed this app to monitor my cat's drinking frequency. It's crucial to keep an eye on how much water your cat consumes since drinking too much or too little can be indicative of kidney problems that require immediate attention.

## How to use it? 
To set up and run this system, you will need a Raspberry Pi with an attached NoIR camera (for night monitoring). Follow these steps:
 
1. Position the camera so that it captures the water bowl.
2. Clone the code to your Raspberry Pi and execute the following command:
    ```bash
    sudo docker compose up
    ```

## Technologies Used
This system leverages the following technologies:
- Flask Web Framework: It enables remote streaming of camera input.
- Gunicorn (WSGI): This handles concurrency, ensuring that many people can simultaneously monitor my cat's kidney health.
- Yolo model for object detection
- Raspberry Pi + RPi NoIR camera



