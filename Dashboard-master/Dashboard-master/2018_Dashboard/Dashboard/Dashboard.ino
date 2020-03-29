#include <SPI.h>
#include <mcp_can.h>
#include "shift.h"
#include "ecu.h"



long unsigned int rxId;
unsigned char len = 0;
unsigned char rxBuf[8];

#define CAN0_INT 2
MCP_CAN CAN0(10);

// pin for overheat light
int overheatPin = A0;
int rpm, coolant;

void setup() {
  pinMode(overheatPin, OUTPUT);
  initShift();
  rpm = coolant = 0;
  update_outputs();

  if(CAN0.begin(MCP_ANY, CAN_500KBPS, MCP_16MHZ) == CAN_OK) {
    strcpy(str, "CONN"); // success
  } else {
    strcpy(str, "EEEE"); // failed to connect to CAN chips
  }
  
  CAN0.setMode(MCP_NORMAL);
  pinMode(CAN0_INT, INPUT);

}
#define STEP 1084
void update_outputs()
{
  snprintf(str, 5, "%4d", rpm / 10);
  if (coolant > 200) {
    digitalWrite(overheatPin, LOW);
  } else {
    digitalWrite(overheatPin, HIGH);
  }
  srdata.data.g1 = (rpm > STEP*1);
  srdata.data.g2 = (rpm > STEP*2);
  srdata.data.g3 = (rpm > STEP*3);
  srdata.data.g4 = (rpm > STEP*4);
  srdata.data.r1 = (rpm > STEP*5);
  srdata.data.r2 = (rpm > STEP*6);
  srdata.data.r3 = (rpm > STEP*7);
  srdata.data.r4 = (rpm > STEP*8);
  srdata.data.b1 = (rpm > STEP*9);
  srdata.data.b2 = (rpm > STEP*10);
  srdata.data.b3 = (rpm > STEP*11);
  srdata.data.b4 = (rpm > STEP*12);
}

void loop() {
  if (!digitalRead(CAN0_INT)) {
    CAN0.readMsgBuf(&rxId, &len, rxBuf);
    if ((rxId & 0x1fffffff) == ID_AEMEngine0) {
      rpm = (int) CALC_AEMEngine0_EngineSpeed(GET_AEMEngine0_EngineSpeed(rxBuf), 1.f);
      coolant = (int) CALC_AEMEngine0_CoolantTemp(GET_AEMEngine0_CoolantTemp(rxBuf), 1.f);
      update_outputs();
    }
  }
  shiftUpdate();
}
