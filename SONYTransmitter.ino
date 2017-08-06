#define IRLEDpin  2              //the arduino pin connected to IR LED to ground. HIGH=LED ON
#define BITtime   600            //length of the carrier bit in microseconds
#define DoubleBITtime 1200

//12 bits code for IR transmission
unsigned long IRcode=0;  
unsigned long p;
char c;
int x;
int i;
int flag = 0;

void setup()
{
  Serial.begin(115200);
  pinMode(IRLEDpin, OUTPUT);
  digitalWrite(IRLEDpin, LOW);
  Serial.write("Begin communication\n");
}

// Ouput the 40KHz carrier frequency for the required time in microseconds
// This is timing critial and just do-able on an Arduino using the standard I/O functions.
// If you are using interrupts, ensure they disabled for the duration.
void IRcarrier(unsigned int IRtimemicroseconds)
{
  for(int i=0; i < (IRtimemicroseconds / 25); i++)
  {
    digitalWrite(IRLEDpin, HIGH);   //turn on the IR LED
    //NOTE: digitalWrite takes about 3.5us to execute, so we need to factor that into the timing.
    delayMicroseconds(8.5);          //delay for 12.5us (8.5us + digitalWrite), half the carrier frequnecy
    digitalWrite(IRLEDpin, LOW);    //turn off the IR LED
    delayMicroseconds(8.5);          //delay for 12.5us (8.5us + digitalWrite), half the carrier frequnecy
  }
}

//Sends the IR code in 12 bits Sony format
void IRsendCode(unsigned long code)
{
  //send the leading pulse
  IRcarrier(2400);            //2.4ms of carrier
 
  //send the user defined 12bit code
  for (int i = 0; i < 12; i++)      
  {
    delayMicroseconds(BITtime); // leading pulse
    if (code & 0b100000000000)  //get the current bit by masking all but the MSB
      IRcarrier(DoubleBITtime);
    else
      IRcarrier(BITtime);
    code <<= 1;                        //shift to the next bit for this byte
  }
}

void loop()
{
  // Get data from serial, when available
  if(Serial.available() > 0) {
          // Convert data to IRcode format
          p = pow(2, 11);
          for (i = 0; i < 12; i++) {
            c = Serial.read();
            x = c - '0';
            IRcode = IRcode + x * p;
            p /= 2;
          }

          // Send 9 samples of IRcode
          IRsendCode(IRcode);                 
          delayMicroseconds(45000);        
          IRsendCode(IRcode);                 
          delayMicroseconds(45000);
          IRsendCode(IRcode);                 
          delayMicroseconds(45000);
          IRsendCode(IRcode);                 
          delayMicroseconds(45000);        
          IRsendCode(IRcode);                 
          delayMicroseconds(45000);
          IRsendCode(IRcode);                 
          delayMicroseconds(45000);
          IRsendCode(IRcode);                 
          delayMicroseconds(45000);        
          IRsendCode(IRcode);                 
          delayMicroseconds(45000);
          IRsendCode(IRcode);                 
          delayMicroseconds(45000);
          IRsendCode(IRcode);                 
          delayMicroseconds(45000);        
          IRsendCode(IRcode);                 
          delayMicroseconds(45000);
          IRsendCode(IRcode);                 
          delayMicroseconds(45000);
          IRsendCode(IRcode);                 
          delayMicroseconds(45000);
          IRsendCode(IRcode);                 
          delayMicroseconds(45000);
          while(1);
    }
}
