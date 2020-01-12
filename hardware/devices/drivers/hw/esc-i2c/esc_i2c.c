/*
    Copyright (C) 2019-2020  Andreas Kuster

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

#include <Servo.h>
#include<Wire.h>

/*
    Arduino ESC I2C Controller

    This device listens at address 77 on the i2c bus and sends PPM signals to the ESC controller for temperature control.
*/

// instantiate the servo object modules
Servo ESC0;
Servo ESC1;
Servo ESC2;

// i2c data receive event handler
void receiveEvent (int bytes) {

    // check if received data has correct length
    if(bytes == 2) {

        // read values of the tuple (device id, control value)
        byte device = Wire.read();

        // map value from [0, 200] to [1500, 2000]
        int value = map(Wire.read(), 0, 200, 150, 200);
        value *= 10;

        // choose the device according to the id
        switch(device){
            case 0:
                // send PPM value to ESC1
                ESC0.writeMicroseconds(value);
                break;
            case 1:
                // send PPM value to ESC2
                ESC1.writeMicroseconds(value);
                break;
            case 2:
                // send PPM value to ESC3
                ESC2.writeMicroseconds(value);
                break;
        }

         // print received control command
         Serial.print("device:");
         Serial.print(device);
         Serial.print(" value:");
         Serial.print(value);
         Serial.println();
    } else {

        // false length: read all and void
        for(int i = 0; i < bytes; i++){
            Wire.read();
        }
        Serial.println("wrong length, discard data");
    }
}

void setup() {

    // start serial debug output
    Serial.begin(9600);
    Serial.println("start device");

    // init esc controller
    Serial.println("init esc");
    ESC0.attach(9);
    ESC1.attach(10);
    ESC2.attach(11);
    ESC0.writeMicroseconds(1750);
    ESC1.writeMicroseconds(1750);
    ESC2.writeMicroseconds(1750);

    // start i2c slave at address 7
    Serial.println("init i2c");
    Wire.begin(7);
    Wire.onReceive(receiveEvent);

    // give the escs some time to set up
    Serial.println("wait for esc");
    delay(2000);

    // ready
    Serial.println("ready");
}

void loop() {
    // do nothing
}