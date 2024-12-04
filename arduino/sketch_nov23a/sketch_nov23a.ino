#include <MD_Parola.h>
#include <MD_MAX72XX.h>
#include <SPI.h>

#define HARDWARE_TYPE MD_MAX72XX::FC16_HW
#define MAX_DEVICES 4 // Jumlah modul LED Matrix
#define CS_PIN 10     // Pin CS

MD_Parola matrix = MD_Parola(HARDWARE_TYPE, CS_PIN, MAX_DEVICES);


const char *lyrics[] = {
  "Bet your feet feel numb", 
  "Crosswalks in my mind are shaky, so please hold on tight",
  "All my demons run wild",
  "All my demons have your smile",
  "In the city of angels",
  "In the city of angels",
  "Hope New York holds you",
  "Hope it holds you like I do",
  "While my demons stay faithful",
  "In the city of angels"
};

int lyricsDuration[] = {500, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000};

int scrollSpeed[] = {15, 13, 27, 27, 27, 27, 27, 27, 27, 27};

void setup() {
  matrix.begin();                      
  matrix.setIntensity(5);              
  matrix.displayClear();               
}

void loop() {
  
  for (int i = 0; i < sizeof(lyrics) / sizeof(lyrics[0]); i++) {
        matrix.displayText(lyrics[i], PA_CENTER, scrollSpeed[i], lyricsDuration[i], PA_SCROLL_LEFT, PA_SCROLL_LEFT);
    while (!matrix.displayAnimate()) {
    }

    matrix.displayReset();            
  }

  
  delay(3000);
}
