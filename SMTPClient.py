# SMTPClient.py
from socket import *

#方便展示，可删除
import os
import time

mailServer = "smtp.163.com"#选择163邮件服务
fromAddress = "fxmpsxs@163.com"#发送方地址
toAddress = "2831153594@qq.com"#接收方地址

#发送方验证信息，此处由于邮箱输入信息使用base64编码，因此需要对用户名和授权码进行编码
username = "ZnhtcHN4cw=="  #输入发送方的用户名（fxmpsxs）对应的base64编码
password = "Q0JQTlBTUkxZRVBDUFlLWA=="  #发送方开启163邮箱SMTP服务时显示的授权码base64编码（CBPNPSRLYEPCPYKX）

# 创建客户端套接字并建立连接
serverPort = 25  # SMTP使用25号端口
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailServer, serverPort))  
# 从客户套接字中接收信息
recv = clientSocket.recv(1024).decode()
print(recv)
if '220' != recv[:3]:
    print('未收到服务器状态码220，服务器未准备就绪')

#发送HELO命令并且显示服务端回复
#开始与服务器的交互
heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand.encode())  #对信息编码和解码
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if '250' != recv1[:3]:
    print('未收到服务器状态码250，未开启与服务器的交互')

#发送"AUTH LOGIN"命令，验证身份
clientSocket.sendall('AUTH LOGIN\r\n'.encode())
recv2 = clientSocket.recv(1024).decode()
print(recv2)
if '334' != recv2[:3]:
    print('未收到服务器状态码334，无法输入验证信息')

#发送验证信息
clientSocket.sendall((username + '\r\n').encode())
recvName = clientSocket.recv(1024).decode()
print(recvName)
if '334' != recvName[:3]:
    print('未收到服务器状态码334，无法输入验证信息')

clientSocket.sendall((password + '\r\n').encode())
recvPass = clientSocket.recv(1024).decode()
print(recvPass)
if '235' != recvPass[:3]:
    print('未收到服务器状态码235，发送方身份验证未通过')
    print('请检查：1.是否开启发送方邮箱的SMTP服务')
    print('        2.是否正确输入发送方邮箱的用户名与授权码')
    print('        3.是否将发送方邮箱的用户名与授权码转为base64编码')

#TCP连接建立成功，成功通过用户验证
#发送 MAIL FROM 命令
clientSocket.sendall(('MAIL FROM: <' + fromAddress + '>\r\n').encode())
recvFrom = clientSocket.recv(1024).decode()
print(recvFrom)
if '250' != recvFrom[:3]:
    print('未收到服务器状态码250，发件人邮箱地址未编辑成功')

#接着SMTP客户端发送一个或多个RCPT命令，格式为RCPT TO: <收件人地址>。
#发送 RCPT TO 命令
clientSocket.sendall(('RCPT TO: <' + toAddress + '>\r\n').encode())
recvTo = clientSocket.recv(1024).decode() 
print(recvTo)
if '250' != recvTo[:3]:
    print('未收到服务器状态码250，收件人邮箱地址未编辑成功')

#发送 DATA 命令
clientSocket.send('DATA\r\n'.encode())
recvData = clientSocket.recv(1024).decode()
print(recvData)
if '354' != recvData[:3]:
    print('未收到服务器状态码354，编辑发送内容失败')

#编辑邮件信息，发送数据
subject = "计算机网络06期末大作业"#邮件主题
msg = "\r\n 徐玮艺2020141490371!"#发送内容
endMsg = "\r\n.\r\n"
contentType = "text/plain"

message = 'from:' + fromAddress + '\r\n'
message += 'to:' + toAddress + '\r\n'
message += 'subject:' + subject + '\r\n'
message += 'Content-Type:' + contentType + '\t\n'
message += '\r\n' + msg
clientSocket.sendall(message.encode())

#发送内容以"."结束
clientSocket.sendall(endMsg.encode())
recvEnd = clientSocket.recv(1024).decode()
print(recvEnd)
if '250' != recvEnd[:3]:
    print('未收到服务器状态码250，发送邮件失败')
    
#发送"QUIT"命令，断开和邮件服务器的连接
clientSocket.sendall('QUIT\r\n'.encode())

clientSocket.close()

time.sleep(100) 
