import time
import serial

from instruction_list import Command

class communication:
    Connected=False
    buffer=None
    
    def __init__(self,BAUD_RATES=9600,timeout=100,VAL_LEN=3,COM_PORT="COM1"):    
        self.TIMEOUT = timeout/1000
        self.Value_len = VAL_LEN
        self.Instruction_len = 1
        self.Command_len = self.Value_len + self.Instruction_len
        
        try:
            self.con = serial.Serial(COM_PORT, BAUD_RATES, timeout=10)   # initialize port
        except:
            print("Serial initialize fail!")
            return
            
        self.C=Command()
        #self.connect()
        
        
    def connect(self):  
        try:
            self.con.write(self.C.Hi) 
            time.sleep(self.TIMEOUT) 
             
            if self.con.in_waiting>=1:            
                res = self.con.read(size=1)  # read one char
                #self.con.flushInput()
                if res == self.C.ACK:
                    self.Connected=True                      
                    return True
            return False
        except:
            print("connect unknow fail")
            return False
        
    '''
    input:
        instruction: 0<=int<=255,values: list[int]
    output:
        instruction code
    '''    
    def send(self,instruction ,values):         
        try:
            ins_bytes = bytes([instruction])
            val_bytes = bytes(values)
        
            if self.Connected:
                self.con.write(ins_bytes)                              
                self.con.write(val_bytes)
                    
                time.sleep(self.TIMEOUT)
                if self.con.in_waiting>=1:    
                    res = self.con.read(size=1)
                    #self.con.flushInput()
                    if res== self.C.ACK:
                        return self.C.Completed
                    else:
                        self.Connected=False
                        return self.C.ERROR_NO_ACK
                else:
                    self.Connected=False
                    return self.C.TIME_OUT
                
            else:
                return self.C.ERROR_NOT_CONNECTED
        except:
            self.Connected=False
            return self.C.ERROR_UNKNOW
    
    '''
    input:
        none
    output:
        instruction code, buffer: bytes
    '''    
    def listen(self):
        try:
            if self.Connected: 
                
                time.sleep(self.TIMEOUT)
                
                if self.con.in_waiting>=self.Command_len:                    
                    buffer = self.con.read(size=self.Command_len)                     
                    self.con.write(self.C.ACK)
                    return self.C.Completed,buffer
                else:                
                    #self.con.flushInput()
                    return self.C.TIME_OUT,None
            else:
                return self.C.ERROR_NOT_CONNECTED,None
        except:
            self.Connected=False
            return self.C.ERROR_UNKNOW,"error! QQ"
            
    '''
    input:
        none
    output:
        string, bytes cnt
    '''            
    def read_all(self):
        try:
            wait_cnt = self.con.in_waiting
            print("read_all len:",wait_cnt)
            if wait_cnt==0:
                return "none",0
            
            s = self.con.read_all()
            #self.con.write(self.C.ACK)            
            
            return s,wait_cnt
        except:
            self.Connected=False
            return "error!",-1
    
    def close(self):
        self.con.close()



