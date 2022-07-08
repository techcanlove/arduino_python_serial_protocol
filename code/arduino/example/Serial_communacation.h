#include "instruction_list.h"
class Serial_com {
  public:
    Command C = Command();
    int TIMEOUT = 100;    
    byte Value_len = 3;
    byte Instruction_len = 1;
    byte Command_len = Value_len + Instruction_len;

    //byte *buffer_;
    bool connected_ = false;

    Serial_com(int baud_rate=9600, int timeout=60, byte val_len=3) {
      TIMEOUT = timeout;
      Value_len = val_len;
      
      
      Serial.setTimeout(10);
      //Serial.print("_init_");
      Command_len = Instruction_len + Value_len;
      //byte buffers[Command_len];
      //buffer_ = buffers;

      connect_();
    }
    bool connect_() {
      //Serial.print("try connecte\n");
      //Serial.write(C.Hi);      
      if (Serial.available()>=1 && Serial.read() == C.Hi) {
          //Serial.flush();
          connected_ = true;
          Serial.write(C.ACK);
          return true ;
      }
      return false;

    }
    byte send_(byte instruction, byte* values) {
      //Serial.print("try send\n");
      if (connected_) {
        Serial.write(instruction);
        Serial.write(values, Value_len);
        unsigned long startTime = millis();
        while ((Serial.available() < 1) && (millis() - startTime < TIMEOUT)) {}
        if (Serial.available() >= 1) {            
            if (Serial.read() == C.ACK)
              return C.Completed;
            else{
              connected_=false; //don't receive ack signal
              return C.ERROR_NO_ACK; //don't receive ack signal
              }
              
        }else{
          connected_=false;
          return C.TIME_OUT;// exceed timeout exception
          }

      }

      return C.ERROR_NOT_CONNECTED;
    }
    byte listen_(byte *cur_command) {
      //Serial.print("try listen\n");      
      if (connected_) {
        unsigned long startTime = millis();
        //Wait bytes coming or exceed the timeout
        while ((Serial.available() < Command_len) && (millis() - startTime < TIMEOUT)) {}

        if (Serial.available() >= Command_len) {          
          Serial.readBytes(cur_command, Command_len);
          //Serial.readBytes(buffer_, Command_len);
          Serial.write(C.ACK);
          return C.Completed;
        } else {
          return C.TIME_OUT;// exceed timeout exception

        }
      }
      return C.ERROR_NOT_CONNECTED;
    }



};
