from enum import Enum

SendMsgType = Enum('SendMsgType',('Init','ReceiveThoughtSuccess','SendThoughtGroup'))
ReceiveMsgType = Enum('ReceiveMsgType',('SendThought'))