# Decrypt Chrome Passwords using usb ducky (raspberry pi pico)
This is a simple modification of [this repo](https://github.com/ohyicong/decrypt-chrome-passwords) and addition of a script. <br>
Used by a raspberry pi pico as a usb ducky to extract the passwords stored localy by chrome. <br>
Then use a pc to decode the passwords that were extracted. <br>

## local python script
A simple program to decrypt chrome password saved on your machine. <br>
This code has only been tested on windows, so it may not work on other OS.<br>

## Raspberry pi scirpt
A scirpt for a USB-Ducky that extracts the password database from a machine. <br>
for instructions on how to modify a raspi pico to be a usb ducky [see this video](https://youtu.be/e_f9p-_JWZw?t=288)

## OS support
1. Windows

## Dependencies for python script
1. pycryptodomex
2. pywin32

## Usage
* put the `payload.dd` scirpt in the usb ducky.<br>
* plug it to a pc that you want to extract the passwords from and wait for it to finih. <br>
* plug it to you machine (on off mode). <br>
* run `python decrypt_chrome_password.py`<br>

## Output
Saved as decrypted_password.csv and shown in console. <br>

## Demo
![rpiDemo](https://github.com/matanton666/rpi-pico-chrome-passwords-extractor/assets/54497551/d7add63c-3d62-4fe4-a8ef-ea99d281e4a7)

### for more info check out [this repo](https://github.com/ohyicong/decrypt-chrome-passwords)


