
#ifndef COMMAND_LIST_H //avoid duplicate include!
#define COMMAND_LIST_H

class Command{
  public:
  //+++++++++++++++++++++++++++++++++++++++++
  // for personal use, you can modify this section accroding your needs.
  //+++++++++++++++++++++++++++++++++++++++++
  const byte FUNC_ADD = 0; 
  const byte ADD_DONE = 1;

  
  //+++++++++++++++++++++++++++++++++++++++++
  // for communacation
  //+++++++++++++++++++++++++++++++++++++++++
  const byte ACK = 199;
  const byte Hi = 198; 
  const byte Completed=200;
  
  const byte ERROR_NO_ACK=232;
  const byte ERROR_NOT_CONNECTED=233;
  const byte TIME_OUT=234;
  const byte ERROR_UNKNOW=235;
};


#endif
