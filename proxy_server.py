import socket, time, sys

#define global adress and buffer size
HOST=""
PORT=8001
BUFFER_SIZE=1024

#get_ip
def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip=socket.gethostbyname( host )
    except socket.gaierror:
        print('Hostname could not be resolved. Exiting')
        sys.exit()

    print(f'IP adress of {host} is {remote_ip}')
    return remote_ip
def main():
    #Question 6
    host='www.google.com'
    port=80

    #create socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_start:
        print("starting proxy server")
        #allow reused address, bind and set to listening mode
        proxy_start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        proxy_start.bind((HOST,PORT))
        proxy_start.listen(1)

        while True:
            #connect proxy_start
            conn,addr=proxy_start.accept()
            print("Connected by", addr)

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM)as proxy_end:
                print("Connecting to google")
                remote_ip=get_remote_ip(host)

                #end connnection
                proxy_end.connect((remote_ip,port))

                #send data
                send_full_data=conn.recv(BUFFER_SIZE)
                print(f"Sending recieved data {send_full_data} to google")
                proxy_end.sendall(send_full_data)

                #shut down
                proxy_end.shutdown(socket.SHUT_WR)

                data=proxy_end.recv(BUFFER_SIZE)
                print(f"Sending recieved data {data} to client")
                #send data back
                conn.send(data)

            conn.close()

if __name__=="__main__":
    main()