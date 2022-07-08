import time
import random
from connect_arduino import communication
from instruction_list import Command
 

VAL_LEN=3
COMMAND_LEN = 1 + VAL_LEN   
BAUD_RATES=115200
COM='COM13'
timeout=20 #ms

arduino_con=communication(BAUD_RATES,timeout,VAL_LEN,COM) #BAUD_RATES=9600,timeout=100,VAL_LEN=3,COM_PORT="COM1"  
C=Command()        


while 1:
    if not arduino_con.Connected:
        re=arduino_con.connect()
        time.sleep(0.1)
        if re:
            print("\nconnected")

    else:  
    
        #**********get command 
        instruction=int.from_bytes(C.FUNC_ADD, "big")  
        a=random.randint(0,100)
        b=random.randint(0,100)
        #means add(a,b)
        time.sleep(1)
        #**********get command 
        
        
        '''
         send(instruction: int, values: List[int])
         res = response_code (define in instruction_list.py)
        '''
        res = arduino_con.send(instruction,[0,a,b])
        print("python send data:",instruction,[0,a,b])
        print("python send response:",C.decode(res))

        '''        
         re = response_code (define in instruction_list.py)
         type(buffer) = bytes         
        '''
        re,buffer=arduino_con.listen()
        #print(re,buffer)
        if re==C.Completed:                
            print("\npython get new data:",buffer)            
            print("data meaning:",C.decode(bytes([buffer[0]])),", values:",buffer[-1],"\n")
                
                
#arduino_con.close()    # CLEAR Connection
#print('bye bye')


      