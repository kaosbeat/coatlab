// USB MIDI receive example, Note on/off -> LED on/off
// contributed by Alessandro Fasan

int ledPin = 13;
int potPin = 14; 
int count = 0;
int t1div = 1;
int sensorValue = 0;

int hh[8] = {1, 1, 1, 1, 1, 1, 1, 1 };
int kick[8] = {1, 0, 0, 0, 0, 1, 0, 0 };
int snare[8] = {0, 0, 1, 0, 0, 0, 1, 0};

int step8 = 0;

int pulselength = 500;
int clkpls = 0;
int clkPin = 11;
int kickpls = 0;
int kickPin = 8;
int hhpls = 0;
int hhPin = 10;
int snarepls = 0;
int snarePin = 9;
int snarerepeat=5;
int snarewait= 1000;

void myClock(){
  count+=1;
  if (count%12 == 0){
    Serial.println(step8);
    snarerepeat = sensorValue;
    Serial.println(snarerepeat);
    Serial.println(snarewait);
    clkpls=0;
    digitalWrite(ledPin, HIGH);
    digitalWrite(clkPin, HIGH);
    step8+=1;
    if (step8 == 8) {
      step8 = 0;
    }
    setStepTrigger(step8);
  }

  if (count%3 == 0) {
    extraSteps();
  }

  if (count%24 == 0){
    digitalWrite(ledPin, LOW);
  }
}

void OnNoteOn(byte channel, byte note, byte velocity) {
  digitalWrite(ledPin, HIGH); // Any Note-On turns on LED
}

void OnNoteOff(byte channel, byte note, byte velocity) {
  digitalWrite(ledPin, LOW);  // Any Note-Off turns off LED
}

void setStepTrigger(int step){
  if (hh[step] == 1) {
    hhpls = 0;
    digitalWrite(hhPin, HIGH);
  }
  if (kick[step] == 1) {
    kickpls = 0;
    digitalWrite(kickPin, HIGH);
  }
  if (snare[step] == 1) {
    snarepls = 0;
    digitalWrite(snarePin, HIGH);
  }
}

void extraSteps(){
  if (sensorValue > 129){
    snarepls = 0;
    digitalWrite(snarePin, HIGH);
  }

}

void updatePulses(){
  if (clkpls < pulselength) {
    clkpls+=1;
    // if (clkpls > pulselength-2) {
    //   Serial.println(clkpls);
    // }
  } else {
    digitalWrite(clkPin, LOW);
  } 
  if (kickpls < pulselength) {
    kickpls+=1;
  } else {
    digitalWrite(kickPin, LOW);
  } 
  if (hhpls < pulselength) {
    hhpls+=1;
  }else {
    digitalWrite(hhPin, LOW);
  }   


  if (snarepls < pulselength) {
    snarepls+=1;
    snarewait = 1000;
  } else {
    digitalWrite(snarePin, LOW);
    snarewait-=1;
  } 

  if (snarewait < 1){
    if (snarerepeat > 0) {
      snarepls = 0;
      digitalWrite(snarePin, HIGH);
      snarerepeat-=1;
    } 
  } 
}



void setup() {
  pinMode(ledPin, OUTPUT);
  pinMode(clkPin, OUTPUT);
  pinMode(kickPin, OUTPUT);
  pinMode(snarePin, OUTPUT);
  pinMode(hhPin, OUTPUT);
  Serial.begin(9600);
  usbMIDI.setHandleNoteOff(OnNoteOff);
  usbMIDI.setHandleNoteOn(OnNoteOn) ;
  usbMIDI.setHandleClock(myClock);
  digitalWrite(ledPin, HIGH);
  delay(400);                 // Blink LED once at startup
  digitalWrite(ledPin, LOW);
}

void loop() {
  usbMIDI.read();
  updatePulses();
  sensorValue = analogRead(potPin)/64;
}

