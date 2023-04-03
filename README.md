# Side Channel Analysis on RPi

Table of contents
=================

[[TOC]]

## Project Description
Collect traces,plaintext and ciphertext for Side Channel Attack on AES128 encryption algorithm

The computer collects the traces while the RPi collects the plaintext and ciphertext.
- The computer code can be altered to collect traces,plaintext and ciphertext for convenience, which is implemented in [Pico_C_program](https://github.com/TIrfana?tab=repositories) for reference. The RPi code has to be altered accordingly as well which is also in the link. However sending longer texts over serial communication will increase time taken to run project.  

## Directions
Download [For_Com](https://github.com/TIrfana/Raspberry-Pi/tree/main/For_Com) into your laptop and PyCharm.

Download [For_RPi](https://github.com/TIrfana/Raspberry-Pi/tree/main/For_RPi) into your RPi

### Set up UART serial communication between RPi and Computor.
1. RPi : follow [Configuring UART on RPi](https://www.engineersgarage.com/articles-raspberry-pi-serial-communication-uart-protocol-ttl-port-usb-serial-boards/#:~:text=The%20Raspberry%20Pi%20and%20a,TTL%20port%20for%20UART%20communication) steps 1-7
2. Laptop(Mac) : After connecting to RPi, type 

