//Telefonklingel mit Tiny25 ansteuern
//(C) A. Lang 2007
// Code unter GPL v2

#include <inttypes.h>
#include <avr/io.h>
#include <avr/interrupt.h>
#include <avr/signal.h>
#include <stdio.h>
#include <avr/delay.h>
#include <avr/delay.h>

//global vars
const int16_t soll=744;    // entspricht etwa 24V
const uint8_t maxpwm=0xd0; // maximales Tastverhältis der PWM

SIGNAL(SIG_INTERRUPT0) {

}

SIGNAL(SIG_ADC) {
  static int16_t tmp=0;
  tmp=soll-ADC;
  tmp*=2;
  if (tmp<0) tmp=0;
  if (tmp>maxpwm) tmp=maxpwm;
  OCR1B=tmp;
}

int main(void)
  {
  TCCR1=1;
  GTCCR=(1<<COM1B1)|(1<<PWM1B);
  OCR1C=0xff;
  DDRB|=0x13;
  PORTB|=4;
  sei();
start:
  ADCSRA=(1<<ADEN)|(1<<ADIE)|(1<<ADATE)|5;
  ADMUX=(1<<REFS1)|3;
  ADCSRA|=(1<<ADSC);
ring:
    PORTB|=1;
    for(uint8_t k=0;k<50;k++) {
      PORTB^=3;
      for (uint8_t i=0;i<20;i++) {
        if (PINB&4) goto brk;
        _delay_ms(1);
      }
    }
    PORTB&=~0x03;
    for (uint16_t i=0;i<4000;i++) {
      if (PINB&4) goto brk;
      _delay_ms(1);
    }
    goto ring;
brk:
  ADCSRA=0;
  ADMUX=0;
  GIMSK|=(1<<INT0);
  OCR1B=0;
  TCCR1=0;
  GTCCR=0;
  PORTB=4;
  MCUCR=(MCUCR&0x43)|(1<<SM1)|(1<<SE);
  asm("sleep");
  GIMSK&=~(1<<INT0);
  TCCR1=1;
  GTCCR=(1<<COM1B1)|(1<<PWM1B);
  OCR1B=0x80;
  PORTB|=4;
  goto start;
}
