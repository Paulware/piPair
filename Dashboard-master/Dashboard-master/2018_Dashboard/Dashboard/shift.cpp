#include "shift.h"

SROut srdata;
char str[5];

int putChar(char);
void digitEnable(int);
void draw();
void draw();
void shiftOut(int, int, byte);
void startupAnimation(void);

static int putChar(char c)
{
  uint8_t value, bits, i;
  if (c < 32)
    c = ' ';
  value = SevenSegmentASCII[c-32];
  srdata.sr[0] = value;
  bits = 0;
  for (i = 0; i < 8; i++)
    bits += (value >> i) & 0x01;
  return bits;
}

static void digitEnable(int index)
{
  srdata.sr[2] |= 0xf0;
  srdata.sr[2] &= ~(16 << index);
}

void initShift()
{
  pinMode(latchPin, OUTPUT);
  srdata.sr[0] = srdata.sr[1] = srdata.sr[2] = 0;
  srdata.data.seg1 = srdata.data.seg2 = srdata.data.seg3 = srdata.data.seg4 = 1;
  //strcpy(str, "0000");
  strcpy(str, "----");
  startupAnimation();
  startupAnimation();
  startupAnimation();
}

static void startupAnimation()
{
  srdata.data.g1 = 1;
  shiftUpdate();
  delay(2);
  srdata.data.g1 = 0;
  srdata.data.g2 = 1;
  shiftUpdate();
  delay(2);
  srdata.data.g2 = 0;
  srdata.data.g3 = 1;
  shiftUpdate();
  delay(2);
  srdata.data.g3 = 0;
  srdata.data.g4 = 1;
  shiftUpdate();
  delay(2);
  srdata.data.g4 = 0;
  srdata.data.r1 = 1;
  shiftUpdate();
  delay(2);
  srdata.data.r1 = 0;
  srdata.data.r2 = 1;
  shiftUpdate();
  delay(2);
  srdata.data.r2 = 0;
  srdata.data.r3 = 1;
  shiftUpdate();
  delay(2);
  srdata.data.r3 = 0;
  srdata.data.r4 = 1;
  shiftUpdate();
  srdata.data.r4 = 0;
  srdata.data.b1 = 1;
  shiftUpdate();
  delay(2);
  srdata.data.b1 = 0;
  srdata.data.b2 = 1;
  shiftUpdate();
  delay(2);
  srdata.data.b2 = 0;
  srdata.data.b3 = 1;
  shiftUpdate();
  delay(2);
  srdata.data.b3 = 0;
  srdata.data.b4 = 1;
  shiftUpdate();
  delay(2);
  srdata.data.b4 = 0;
  srdata.data.b3 = 1;
  shiftUpdate();
  delay(2);
  srdata.data.b3 = 0;
  srdata.data.b2 = 1;
  shiftUpdate();
  delay(2);
  srdata.data.b2 = 0;
  srdata.data.b1 = 1;
  shiftUpdate();
  delay(2);
  srdata.data.b1 = 0;
  srdata.data.r4 = 1;
  shiftUpdate();
  delay(2);
  srdata.data.r4 = 0;
  srdata.data.r3 = 1;
  shiftUpdate();
  delay(2);
  srdata.data.r3 = 0;
  srdata.data.r2 = 1;
  shiftUpdate();
  delay(2);
  srdata.data.r2 = 0;
  srdata.data.r1 = 1;
  shiftUpdate();
  delay(2);
  srdata.data.r1 = 0;
  srdata.data.g4 = 1;
  shiftUpdate();
  delay(2);
  srdata.data.g4 = 0;
  srdata.data.g3 = 1;
  shiftUpdate();
  delay(2);
  srdata.data.g3 = 0;
  srdata.data.g2 = 1;
  shiftUpdate();
  delay(2);
  srdata.data.g2 = 0;
  srdata.data.g1 = 1;
  shiftUpdate();
  delay(2);
  srdata.data.g1 = 0;
  shiftUpdate();
  delay(2);
}

static void draw()
{
  //shift 3
  //shift 2
  //shift 1
  digitalWrite(latchPin, 0);
  shiftOut(dataPin, clockPin, srdata.sr[2]);
  shiftOut(dataPin, clockPin, srdata.sr[1]);
  shiftOut(dataPin, clockPin, srdata.sr[0]);
  digitalWrite(latchPin, 1);
}

void shiftUpdate()
{
  int i, bits;
  for (i = 0; i < 4; i++) {
    digitEnable(i);
    bits = putChar(str[i]);
    draw();
    delayMicroseconds(500 * bits);
  }
}



// the heart of the program
static void shiftOut(int myDataPin, int myClockPin, byte myDataOut) {
  // This shifts 8 bits out MSB first, 
  //on the rising edge of the clock,
  //clock idles low

  //internal function setup
  int i=0;
  int pinState;
  pinMode(myClockPin, OUTPUT);
  pinMode(myDataPin, OUTPUT);

  //clear everything out just in case to
  //prepare shift register for bit shifting
  digitalWrite(myDataPin, 0);
  digitalWrite(myClockPin, 0);

  //for each bit in the byte myDataOut�
  //NOTICE THAT WE ARE COUNTING DOWN in our for loop
  //This means that %00000001 or "1" will go through such
  //that it will be pin Q0 that lights. 
  for (i=7; i>=0; i--)  {
    digitalWrite(myClockPin, 0);

    //if the value passed to myDataOut and a bitmask result 
    // true then... so if we are at i=6 and our value is
    // %11010100 it would the code compares it to %01000000 
    // and proceeds to set pinState to 1.
    if ( myDataOut & (1<<i) ) {
      pinState= 1;
    }
    else {  
      pinState= 0;
    }

    //Sets the pin to HIGH or LOW depending on pinState
    digitalWrite(myDataPin, pinState);
    //register shifts bits on upstroke of clock pin  
    digitalWrite(myClockPin, 1);
    //zero the data pin after shift to prevent bleed through
    digitalWrite(myDataPin, 0);
  }

  //stop shifting
  digitalWrite(myClockPin, 0);
}


