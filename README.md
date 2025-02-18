# ESP32-Multiplayer Remote Game

<p align="middle">
  <img src="esp32-setup.gif" alt="Set Up" width="20%"/> 
  <img src="esp32-ingame.png" alt="In Game" width="49%"/>
  <img src="esp32-end.png" alt="End" width="17%"/> 
</p>

**Creators:** David Benkö, Christina Tüchler, Patrick Trollmann, Renate Zhang \
**Course:** Foundations of Ubiquitous Computing and IoT 2023WS, TU Vienna

## Project Description

The project explores the theme of **remote multiplayer gaming** using technology to foster interaction over a distance. It focuses on creating tangible interfaces to enable a seamless and engaging gaming experience for 2 or more players. The project utilized ESP32 microcontrollers and various hardware components to achieve its objectives, developed with MicroPython. The player have to memorize a sequence of LED lights, repeat it over the buttons below. After each round players gain points, the winner is the one who memorized more sequences, thus collected more points at the end. 

### Features
- Multiplayer functionality over a distance.
- Tangible artifacts to enhance gameplay and communication.
- Integration of IoT and ubiquitous computing principles.

## Technical Details

- **`G1_Project.py`**: Main Python script implementing the game's core functionalities.
- **`G1_WebServer.py`**: Python script managing the web server for remote interaction.
- **`ClosedBox.svg`**: A visual asset used in the project.

### Used Hardware
The project utilized the following hardware components:
- ESP32: Microcontrollers for managing input and communication.
- LEDs: For visual feedback.
- Push Buttons : For repeating the inputs.
- Wi-Fi Module: Integrated into the ESP32 for remote connectivity.
- Speakers: Auditory output, supporting the LED lights. 

## License

This project is licensed under the [MIT License](LICENSE).



