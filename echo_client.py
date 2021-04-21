import socket
import sys
import traceback


def client(msg, log_buffer=sys.stderr):
    server_address = ('127.0.0.1', 10000)
    # TODO: Replace the following line with your code which will instantiate
    #       a TCP socket with IPv4 Addressing, call the socket you make 'sock'
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP)
    sock.connect(server_address)
    print('connecting to {0} port {1}'.format(*server_address), file=log_buffer)
    # TODO: connect your socket to the server here.

    # you can use this variable to accumulate the entire message received back
    # from the server
    buffer_size = 16
    received_message = ''

    # this try/finally block exists purely to allow us to close the socket
    # when we are finished with it
    try:
        print('sending "{0}"'.format(msg), file=log_buffer)
        # TODO: send your message to the server here.
        my_message = input("> ")
        if my_message.lower() == "port range":
            port_range_setup()
            print(my_message.lower())
        sock.sendall(my_message.encode('utf-8'))
        # TODO: the server should be sending you back your message as a series
        #       of 16-byte chunks. Accumulate the chunks you get to build the
        #       entire reply from the server. Make sure that you have received
        #       the entire message and then you can break the loop.
        #
        #       Log each chunk you receive.  Use the print statement below to
        #       do it. This will help in debugging problems
        while True:    
            chunk = sock.recv(buffer_size)

            print('received "{0}"'.format(chunk.decode('utf8')), file=log_buffer)
            received_message += chunk.decode('utf8')
            if len(chunk) < buffer_size:
                break
    except Exception:
        traceback.print_exc()
        sys.exit(1)
    finally:
        # TODO: after you break out of the loop receiving echoed chunks from
        #       the server you will want to close your client socket.
        print('closing socket', file=log_buffer)
        sock.close()
        # TODO: when all is said and done, you should return the entire reply
        # you received from the server as the return value of this function.
        print(received_message)
        return received_message

def port_range(upper, lower):
    '''
    lists the services provided by a given range of ports
    '''

    # Ports numbered 0 - 1023 are reserved
    # Ports numbered 1024 - 65535 are open
    # Ports numbered 1024 - 49151 may be registered
    # Ports numbered 49152 - 65535 are called ephemera

    if upper < 0 or lower < 0:
        print("Inputs can not be negative")
        return

    if upper > 65535 or lower > 65535:
        print("Inputs must be less than 65535")
        return

    if lower > upper:
        place_holder = upper
        upper = lower
        lower = place_holder
        print("Upper = {0}, Lower= {1}".format(upper, lower))

    #Determine Bucket "A"
    if upper < 1023:
        print("These ports are reserved, Do Not Use")
    #Determine Bucket "B"
    if upper < 49151:
        print(upper)
    #Determine Bucket "C"
    pass

def port_range_setup():
    '''setup inputs for port range'''
    upper = input('Select an upper limit for port list: ')
    lower = input('Select a lower limit for port list: ')
    port_range(int(upper), int(lower))
    return

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage = '\nusage: python echo_client.py "this is my message"\n'
        print(usage, file=sys.stderr)
        sys.exit(1)

    msg = sys.argv[1]
    client(msg)
