class Command:
    def __init__(self): 
        #+++++++++++++++++++++++++++++++++++++++++
        # for personal use, you can modify this section accroding your needs.
        #+++++++++++++++++++++++++++++++++++++++++    
        self.FUNC_ADD = bytes([0]) 
        self.ADD_DONE = bytes([1]) 
        
        self.map={}        
        
        #+++++++++++++++++++++++++++++++++++++++++
        # for communacation
        #+++++++++++++++++++++++++++++++++++++++++
        self.ACK = bytes([199]) 
        self.Hi = bytes([198])  # 
        self.Completed=bytes([200]) 

        self.ERROR_NO_ACK=bytes([232]) 
        self.ERROR_NOT_CONNECTED=bytes([233]) 
        self.TIME_OUT=bytes([234]) 
        self.ERROR_UNKNOW=bytes([235])
            
        self.initialize_map()
    
    def initialize_map(self):  
        if self.map=={}:            
            for attri_name,value in vars(self).items():
                if type(value)==type(bytes([0])):
                    self.map[value]=attri_name
                    
    def decode(self,s_byte):
        if s_byte in self.map:
            return self.map[s_byte]
        else:
            return "instruction decode error"