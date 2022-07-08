#include "Serial_communacation.h"
#include "instruction_list.h"


#define INS_LEN 1
#define VAL_LEN 3
#define COMMAND_LEN 4
//const byte bufferLength = INS_LEN + VAL_LEN; //20;
//char serialBuffer[bufferLength];

char cur_command[4]={88,66,66,66};
bool DEBUG = false;
/*how to debug: 
  1.set timeout at Serial_communacation send function = 5000 or larger, 
    so you can type response manually
  2. set instruction_list communacation as visible ascii code
  3. communacate with arduino by manually input in serial monitor!
*/

Serial_com connection(115200, 100, VAL_LEN);
Command C = Command();

void setup() {  
  Serial.begin(115200); 
}
String run_command() {
  String re_msg = "";
  byte ins=cur_command[0];
  if (ins == C.FUNC_ADD) {
    //Current_vals[0] = Current_vals[1]+Current_vals[2];
    re_msg = "FUNC_ADD:";
    
    
    //++++++++++++++++++
    //send part   
    byte re_val[VAL_LEN]={0,0,cur_command[2]+cur_command[3]} ;
    byte res = connection.send_(&C.ADD_DONE, re_val);
    if (DEBUG) {
      Serial.print("add done:");
      Serial.print(res)  ;      
    }   
    //send part 
    //++++++++++++++++++
    
    
  } else if (ins == C.Hi) {
    re_msg = "hi receive";
  } else
    re_msg = "invalid instruction";

  return re_msg;
}

void loop() {
  //++++++++++++++++++++
  //connect and listen part
  if (!connection.connected_) {
    connection.connect_();
    if (DEBUG){
      Serial.print("connecting");
      delay(1000);
      }
      
  } else {
    if (connection.listen_(cur_command) == C.Completed) { //serialBuffer
      //fill_command();
      String re_msg = run_command();

      if (DEBUG) {
        Serial.print("c:");
        Serial.write(cur_command,COMMAND_LEN);        
        Serial.print("msg:");
        if (re_msg == "") {
          Serial.print("invalid command! ");          
        } else
          Serial.print(re_msg);
      }

    }
  }


}
