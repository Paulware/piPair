#ifndef DASH_CONFIG_H
#define DASH_CONFIG_H

#include <Arduino.h>

void initShift(void);
void shiftUpdate(void);

typedef struct outdata
{
  // shift 1
  unsigned segA:1;
  unsigned segB:1;
  unsigned segC:1;
  unsigned segD:1;
  unsigned segE:1;
  unsigned segF:1;
  unsigned segG:1;
  unsigned segDP:1;
  // shift 2
  unsigned b4:1;
  unsigned b3:1;
  unsigned b2:1;
  unsigned b1:1;
  unsigned r4:1;
  unsigned r3:1;
  unsigned r2:1;
  unsigned r1:1;
  // shift 3
  unsigned g4:1;
  unsigned g3:1;
  unsigned g2:1;
  unsigned g1:1;
  unsigned seg1:1;
  unsigned seg2:1;
  unsigned seg3:1;
  unsigned seg4:1;
  
} outdata;

union SROut {
  outdata data;
  uint8_t sr[3];
};
extern SROut srdata;
extern char str[5];

//Pin connected to ST_CP of 74HC595
const int latchPin = 7;
//Pin connected to SH_CP of 74HC595
const int clockPin = 6;
////Pin connected to DS of 74HC595
const int dataPin = 5;


const uint8_t SevenSegmentASCII[96] = {
  0x00, /* (space) */
  0x86, /* ! */
  0x22, /* " */
  0x7E, /* # */
  0x6D, /* $ */
  0xD2, /* % */
  0x46, /* & */
  0x20, /* ' */
  0x29, /* ( */
  0x0B, /* ) */
  0x21, /* * */
  0x70, /* + */
  0x10, /* , */
  0x40, /* - */
  0x80, /* . */
  0x52, /* / */
  0x3F, /* 0 */
  0x06, /* 1 */
  0x5B, /* 2 */
  0x4F, /* 3 */
  0x66, /* 4 */
  0x6D, /* 5 */
  0x7D, /* 6 */
  0x07, /* 7 */
  0x7F, /* 8 */
  0x6F, /* 9 */
  0x09, /* : */
  0x0D, /* ; */
  0x61, /* < */
  0x48, /* = */
  0x43, /* > */
  0xD3, /* ? */
  0x5F, /* @ */
  0x77, /* A */
  0x7C, /* B */
  0x39, /* C */
  0x5E, /* D */
  0x79, /* E */
  0x71, /* F */
  0x3D, /* G */
  0x76, /* H */
  0x30, /* I */
  0x1E, /* J */
  0x75, /* K */
  0x38, /* L */
  0x15, /* M */
  0x37, /* N */
  0x3F, /* O */
  0x73, /* P */
  0x6B, /* Q */
  0x33, /* R */
  0x6D, /* S */
  0x78, /* T */
  0x3E, /* U */
  0x3E, /* V */
  0x2A, /* W */
  0x76, /* X */
  0x6E, /* Y */
  0x5B, /* Z */
  0x39, /* [ */
  0x64, /* \ */
  0x0F, /* ] */
  0x23, /* ^ */
  0x08, /* _ */
  0x02, /* ` */
  0x5F, /* a */
  0x7C, /* b */
  0x58, /* c */
  0x5E, /* d */
  0x7B, /* e */
  0x71, /* f */
  0x6F, /* g */
  0x74, /* h */
  0x10, /* i */
  0x0C, /* j */
  0x75, /* k */
  0x30, /* l */
  0x14, /* m */
  0x54, /* n */
  0x5C, /* o */
  0x73, /* p */
  0x67, /* q */
  0x50, /* r */
  0x6D, /* s */
  0x78, /* t */
  0x1C, /* u */
  0x1C, /* v */
  0x14, /* w */
  0x76, /* x */
  0x6E, /* y */
  0x5B, /* z */
  0x46, /* { */
  0x30, /* | */
  0x70, /* } */
  0x01, /* ~ */
  0x00, /* (del) */
};


#endif
