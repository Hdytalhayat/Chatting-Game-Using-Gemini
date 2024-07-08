import socket
import threading
import google.generativeai as genai

genai.configure(api_key="AIzaSyBRqw3Ozd7fNRmKAvzglsrtEPKrs2tAxOU")
model = genai.GenerativeModel('gemini-1.5-flash')

conversation_history = []

file_path = 'F:\PythonGAme\American Sign (2)\American Sign\CharInfo.txt'

try:
    with open(file_path, 'r') as file:
        char_info_string = file.read()
        print("String loaded successfully from CharInfo.txt:")
except FileNotFoundError:
    print(f"Error: File '{file_path}' not found.")
except IOError:
    print(f"Error: Could not read file '{file_path}'.")

def sentToAI(inputan):
    global conversation_history
    conversation_history.append(char_info_string+". " + inputan)
    
    # Gabungkan seluruh sejarah percakapan
    full_conversation = "\n".join(conversation_history)
    
    response = model.generate_content(full_conversation)
    response_text = response.text
    conversation_history.append("AI: " + response_text)
    
    return response_text

def handle_client(data, address, udpServerSocket):
    # Decode the byte message to a string
    decoded_message = data.decode('utf-8')

    clientMsg = "Message from Client:{}".format(decoded_message)
    clientIP = "Client IP Address:{}".format(address)
    print(clientMsg)
    print(clientIP)

    ai_response = sentToAI(decoded_message)
    print("AI Response: {}".format(ai_response))

    # Processing AI response based on specific keywords
    if "stops accepting your prompts" in ai_response.lower() or "stops making proactive suggestions" in ai_response.lower():
        ai_response = "bye."
    else:
        # Normal response handling
        pass


    # Sending a reply to client
    udpServerSocket.sendto(ai_response.encode('utf-8'), address)

def start_server():
    serverAddressPort = ("127.0.0.1", 1209)
    bufferSize = 1024

    # Create a UDP socket
    udpServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    udpServerSocket.bind(serverAddressPort)

    print("UDP server up and listening")

    while True:
        # Listen for incoming datagrams
        data, address = udpServerSocket.recvfrom(bufferSize)
        client_thread = threading.Thread(target=handle_client, args=(data, address, udpServerSocket))
        client_thread.start()

if __name__ == "__main__":
    start_server()
