#include <wiringPi.h>
#include <string.h>
#define PIN 20

void tone(int freq, float time){
    int i;
    int loop = (int)(time*(float)freq);
    float fwait=((1.0/(float)freq)/2.0);
    int wait=(int)(fwait*1000000.0);
    for(i=0; i<loop; i++){
        digitalWrite(PIN, HIGH);
        delayMicroseconds(wait);
        digitalWrite(PIN, LOW);
        delayMicroseconds(wait);
    }
}

void mac(void){
    int i;
    for(i=0; i<3; i++){
        tone(880,0.3);
        tone(783,0.3);
        tone(880,0.3);
        delay(200);
    }
    delay(1000);
}
void tel(void){
    int i;
    for(i=0; i<3; i++){
        tone(1975, 0.05);
        tone(1046, 0.05);
        delay(10);
        tone(1975, 0.05);
        tone(1046, 0.05);
        delay(500);
    }
    delay(1000);
}

int main(int argc, char *argv[]){
    if(argc <= 1) return 1;
    if(wiringPiSetupGpio() == -1) return 1;
    pinMode(PIN, OUTPUT);
    if(strcmp(argv[1], "mac")==0) mac();
    else if(strcmp(argv[1], "tel")==0) tel();

    return 0;
}
