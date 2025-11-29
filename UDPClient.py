# UDPClient.py
# 导入 socket 模块，这是进行网络编程的基础
from socket import *
# 导入 sys 模块，用于获取命令行参数（如服务器IP、端口等）
import sys
# 导入 time 模块，为了演示效果，可以稍微加一点延时（可选）
import time

# -------------------- 配置与初始化阶段 --------------------

# 检查命令行参数是否足够
# 格式要求：python UDPClient.py <服务器IP> <服务器端口> <要发送的文件名>
# 例如：python UDPClient.py 192.168.1.100 12000 test.txt
if len(sys.argv) != 4:
    print("使用方法错误！请按照如下格式运行：")
    print("python UDPClient.py <server_ip> <server_port> <filename>")
    sys.exit()

# 获取服务器 IP 地址（从命令行第一个参数获取）
serverName = sys.argv[1]

# 获取服务器端口号（从命令行第二个参数获取），注意要转换成整数类型
serverPort = int(sys.argv[2])

# 获取要发送的文件名（从命令行第三个参数获取）
filename = sys.argv[3]

# 创建客户端 Socket
# AF_INET 表示使用 IPv4 地址
# SOCK_DGRAM 表示使用 UDP 协议（无连接的数据报文）
clientSocket = socket(AF_INET, SOCK_DGRAM)

# 设置超时时间，防止握手失败时程序一直卡死（例如等待 2 秒）
clientSocket.settimeout(2.0)

try:
    # -------------------- 阶段一：模拟 TCP 建立连接 (握手) --------------------
    
    # 定义握手消息，这里按照题目建议，发送 'c-hello'
    handshake_msg = "c-hello"
    
    print(f"正在尝试连接服务器 {serverName}:{serverPort} ...")
    
    # 发送握手消息到服务器
    # 注意：网络传输需要 bytes 类型，所以要用 .encode() 编码
    clientSocket.sendto(handshake_msg.encode(), (serverName, serverPort))
    
    # 等待接收服务器的回复
    # 2048 是接收缓冲区的最大字节数
    response, serverAddress = clientSocket.recvfrom(2048)
    
    # 解码服务器的消息
    decoded_response = response.decode()
    
    # 检查服务器是否回复了约定的 's-hello'
    if decoded_response == "s-hello":
        print("连接建立成功！服务器回复:", decoded_response)
    else:
        print("连接异常，服务器回复了意外的消息:", decoded_response)
        sys.exit() # 握手失败直接退出

    # -------------------- 阶段二：数据传输 (发送文件) --------------------
    
    print(f"开始发送文件: {filename}")
    
    # 以只读模式 ('r') 打开本地文件，如果包含非文本内容建议用 'rb'
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            # 读取文件内容
            # 对于大文件，应该分块读取发送，但题目要求是"小文本文件"，一次读取即可
            file_data = f.read()
            
            # 将文件内容编码并通过 socket 发送
            clientSocket.sendto(file_data.encode(), (serverName, serverPort))
            print("文件内容已发送完毕。")
            
    except FileNotFoundError:
        print(f"错误：找不到文件 {filename}")
        clientSocket.close()
        sys.exit()

    # -------------------- 阶段三：模拟 TCP 释放连接 (挥手) --------------------
    
    # 稍微暂停一下，防止数据包粘连（虽然 UDP 边界清晰，但在逻辑上区分开）
    time.sleep(0.1)
    
    # 发送关闭连接的请求 'bye'
    print("请求断开连接，发送 'bye'...")
    clientSocket.sendto("bye".encode(), (serverName, serverPort))
    
    # 等待服务器确认关闭
    print("等待服务器确认...")
    response, serverAddress = clientSocket.recvfrom(2048)
    
    if response.decode() == "bye":
        print("服务器已确认断开 (收到 'bye')。")
        print("连接已正常释放。")
    else:
        print("断开连接过程出现异常。")

except Exception as e:
    # 捕获可能出现的网络错误（如超时、无法连接等）
    print("发生错误:", e)

finally:
    # -------------------- 结束：关闭资源 --------------------
    # 无论成功与否，都要关闭 socket，释放系统资源
    clientSocket.close()
    print("客户端已退出。")
    