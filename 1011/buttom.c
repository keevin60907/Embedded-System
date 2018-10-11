#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <stdlib.h>
#include <wiringPi.h>

#define BUTTON_PIN0 0
#define BUTTON_PIN1 4
#define LED_LIGHT   18

volatile int eventCounter = 0; 

void myirq1(void) {
    eventCounter++;
    printf( "counter++: %d\n", eventCounter ); 
}

void myirq2(void) {
    eventCounter++;
    printf( "counter++: %d\n", eventCounter );
}

int main (void) {
    // sets up the wiringPi library 
    if (wiringPiSetupGpio () < 0) {
        fprintf (stderr, "Unable to setup wiringPi: %s\n", strerror (errno));
        return 1; 
    }

    pinMode(BUTTON_PIN0, INPUT); 
    pinMode(BUTTON_PIN1, INPUT); 
    pullUpDnControl (BUTTON_PIN0, PUD_UP); 
    pullUpDnControl (BUTTON_PIN1, PUD_UP); 
    pinMode(LED_LIGHT, OUTPUT);

    if ( wiringPiISR (BUTTON_PIN0, INT_EDGE_FALLING, &myirq1) < 0 ) { 
        fprintf (stderr, "Unable to setup ISR: %s\n", strerror (errno)); 
        return 1;
    }

    if ( wiringPiISR (BUTTON_PIN1, INT_EDGE_FALLING, &myirq2) < 0 ) {
        fprintf (stderr, "Unable to setup ISR: %s\n", strerror (errno));
        return 1; 
    }

    while ( 1 ) {
        // printf( "%d\n", eventCounter );
        // eventCounter = 0;
        if (eventCounter % 2){
            digitalWrite(LED_LIGHT, LOW);
            delay( 500 ); // wait 1 second
            digitalWrite(LED_LIGHT, HIGH);
            delay( 500 ); // wait 1 second
        }
    }
    return 0; 
}
