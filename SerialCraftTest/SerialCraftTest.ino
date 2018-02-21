uint8_t buffer[100];
int len = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available() > 0) {
    buffer[len++] = Serial.read();
    Serial.print("chat ");
    for(int i = 0; i < len; i++) {
      Serial.print(buffer[i]);
      if(i != len-1) {
        Serial.print(", ");
      }
    }
    Serial.println();
  }

  if(len >= 4 && buffer[0] == 1 && buffer[1] == 83 && buffer[2] == 67 && len >= buffer[3]+4) {
    len = 0;
  }

}
