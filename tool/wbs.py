from websocket import create_connection
ws = create_connection("wss://zxst.foda.ai/ws?ref=10.21.6.72&port=10136")
print("Sending 'Hello, World'...")
ws.send("Hello, World")
print("Sent")
print("Receiving...")
result = ws.recv()
print("Received '%s'" % result)
ws.close()