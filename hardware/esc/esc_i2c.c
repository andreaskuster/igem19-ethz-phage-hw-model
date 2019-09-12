#include <Servo.h>
#include<Wire.h>

// instantiate the servo object modules
Servo ESC1;
Servo ESC2;
Servo ESC3;

// i2c data receive event handler
void receiveEvent (int bytes)
{
    if(bytes == 2){

        byte device = Wire.read();
        int value = map(Wire.read(),150,200,0,200);
        value *= 10;
        switch(device){
            case 1:
                ESC1.writeMicroseconds(value);
                break;
            case 2:
                ESC2.writeMicroseconds(value);
                break;
            case 3:
                ESC3.writeMicroseconds(value);
                break;
        }

          // print received control command
          Serial.print("device:");
          Serial.print(device);
          Serial.print(" value:");
          Serial.print(value);
          Serial.println();
    } else {
        //
        for(int i = 0; i < bytes; i++){
         Wire.read();
        }
    }
}


void setup() {

  // start serial debug output
  Serial.begin(9600);
  Serial.println("start device");

  // init esc controller
  Serial.println("init esc");
  ESC1.attach(9);
  ESC2.attach(10);
  ESC3.attach(11);
  ESC1.writeMicroseconds(1750);
  ESC2.writeMicroseconds(1750);
  ESC3.writeMicroseconds(1750);

  // start i2c slave at address 77
  Serial.println("init i2c");
  Wire.begin(77);
  Wire.onReceive(receiveEvent);

  Serial.println("wait for esc");
  delay(2000);
}

void loop() {
    // do nothing
}