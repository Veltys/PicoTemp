# PicoTemp
[![GitHub commits](https://badgen.net/github/commits/Veltys/PicoTemp)](https://GitHub.com/Veltys/PicoTemp/commit/)
[![GitHub latest commit](https://badgen.net/github/last-commit/Veltys/PicoTemp)](https://GitHub.com/Veltys/PicoTemp/commit/)
[![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://github.com/Veltys/Ansible/blob/master/LICENSE.md)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/29172a22cc744d2d8aaed3295e75d322)](https://app.codacy.com/gh/Veltys/PicoTemp/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)

PicoTemp software for Raspberry Pi Pico


## Description
PicoTemp measures the temperature thanks to a DHT11 sensor and returns it in the form of a web service that can be consulted by other applications or systems


## Changelog
### To-do (*TODO*)
- [x] Buttons support to switch off ~~LEDs~~ screen and system
- [x] Screen support... which reminds me...
    - [x] ... buy an screen, [like this one](https://amzn.eu/d/5Pab0Ox)
- [ ] Way to restore screen manager thread if crashs
- [ ] Better GMT correction handling
- [ ] DST handling
- [ ] Way to restore WiFi connection

### Cancelled
- [ ] ~~Asynchronous web server~~

### [2.4.0] - 2023-12-27
#### Added
- DHT22 sensor support
  New smaller icons 
  New layout

### [2.3.1] - 2023-12-05
#### Fixed
- 'LED' pin is bugged

### [2.3.0] - 2023-12-05
#### Added
- 'I am alive' LED support

### [2.2.0] - 2023-11-25
#### Fixed
- Functions refactoring

### [2.1.0] - 2023-11-25
#### Added
- Support for multiple DHT11 sensors

#### Fixed
- Some optimizations

### [2.0.3] - 2023-11-13
#### Fixed
- Better lib organization

### [2.0.2] - 2023-11-13
#### Fixed
- Initial GMT time correction

### [2.0.1] - 2023-11-12
#### Fixed
- Code quality

### [2.0.0] - 2023-11-12
#### Addedd
- Screen support
- Buttons support

### [1.0.3] - 2023-11-04
#### Fixed
- Micropython does not have ExitStatus library
- Documentation

### [1.0.2] - 2023-10-30
#### Added
- Codacy badge

#### Fixed
- Code quality

### [1.0.1] - 2023-10-29
#### Fixed
- Various optimizations

### [1.0.0] - 2023-10-29
#### Added
- Pre-existent work
- To-do list

### [0.0.2] - 2023-10-29
#### Added
- **.gitignore** file

### [0.0.1] - 2023-10-29
#### Added
- **README.md** file


## Acknowledgments, sources consulted and other credits
* To the [official MicroPython documentation](https://docs.micropython.org/en/latest/), for obvious reasons
* To the [Waveshare Wiki](https://www.waveshare.com/wiki/Pico-OLED-1.3), for the documentation available
* [Error icon](https://www.iconexperience.com/g_collection/icons/?icon=sign_warning)
* [Server icon](https://www.iconexperience.com/g_collection/icons/?icon=server)
* [Thermometer icon](https://www.iconexperience.com/g_collection/icons/?icon=thermometer)
* [WiFi icon](https://www.iconexperience.com/g_collection/icons/?icon=wifi)
