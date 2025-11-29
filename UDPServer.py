# GitHub Repository: # GitHub Repository: https://github.com/The4leepy/Network-Lab-UDP
# UDPServer.py
# 导入 socket 模块
from socket import *

# -------------------- 服务器配置 --------------------

# 设置服务器监听端口，与客户端保持一致
serverPort = 12000

# 创建服务器 Socket
# AF_INET: IPv4
# SOCK_DGRAM: UDP
serverSocket = socket(AF_INET, SOCK_DGRAM)

# 将 Socket 绑定到本机所有 IP 的指定端口
# '' 表示绑定到所有可用的网络接口
serverSocket.bind(('', serverPort))

print(f"服务器已启动，正在端口 {serverPort} 等待数据...")

# -------------------- 主循环 --------------------

while True:
    try:
        # 1. 接收握手请求
        # recvfrom 会阻塞程序，直到收到数据
        # message 是收到的字节数据，clientAddress 是发送方的 (IP, Port)
        message, clientAddress = serverSocket.recvfrom(2048)
        
        # 解码消息
        msg_str = message.decode()
        
        # 判断是否是握手信号 'c-hello'
        if msg_str == "c-hello":
            print(f"收到来自 {clientAddress} 的握手请求: {msg_str}")
            
            # 回复 's-hello' 建立连接
            response = "s-hello"
            serverSocket.sendto(response.encode(), clientAddress)
            print("已回复 's-hello'，模拟连接建立。准备接收文件...")
            
            # 准备一个变量来存储接收到的文件内容
            file_content = ""
            
            # 进入接收文件数据的内部循环
            while True:
                # 接收下一条数据（可能是文件内容，也可能是 'bye'）
                data, addr = serverSocket.recvfrom(2048)
                
                # 验证发送方是否是同一个人
                if addr != clientAddress:
                    continue 
                
                decoded_data = data.decode()
                
                # 判断是否是断开连接的信号 'bye'
                if decoded_data == "bye":
                    print("收到断开连接请求: 'bye'")
                    
                    # 回复 'bye' 确认断开
                    serverSocket.sendto("bye".encode(), clientAddress)
                    print("已回复 'bye'，连接释放。")
                    
                    # 将接收到的内容写入本地文件
                    # 文件名自动命名为 received_file.txt
                    with open("received_file.txt", "w", encoding='utf-8') as f:
                        f.write(file_content)
                    print("文件已保存为 'received_file.txt'")
                    print("-" * 30)
                    
                    # 跳出内部循环，回到最外层继续等待新的客户端
                    break
                else:
                    # 如果不是 'bye'，说明收到的是文件内容
                    print(f"接收到数据片段 (长度 {len(decoded_data)} 字符)")
                    file_content += decoded_data
                    # 注意：如果是大文件，这里应该直接写入文件而不是存于内存变量
                    
        else:
            # 如果收到的不是 c-hello，可能是乱序包或干扰，暂时忽略
            print(f"收到非握手数据: {msg_str}，忽略。")

    except Exception as e:
        print("服务器运行出错:", e)
        # 出错后不退出，继续等待下一次连接