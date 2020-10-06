import socket
import sys
import traceback


def client(msg, log_buffer=sys.stderr):
    server_address = ('localhost', 5001)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    print('connecting to {0} port {1}'.format(*server_address), file=log_buffer)
    # TODO: connect your socket to the server here.
    sock.connect(('127.0.0.1', 5001))

    # you can use this variable to accumulate the entire message received back
    # from the server
    received_message = ''

    # this try/finally block exists purely to allow us to close the socket
    # when we are finished with it
    try:
        print('sending "{0}"'.format(msg), file=log_buffer)
        sock.sendall(msg.encode('utf8'))
        #       Log each chunk you receive.  Use the print statement below to
        #       do it. This will help in debugging problems
        data = ''
        while True:
            recv_data = sock.recv(16)
            data += recv_data.decode('utf8')
            if len(recv_data.decode('utf8')) < 16:
                print('received "{0}"'.format(data), file=log_buffer)
                break

    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
    finally:
        print('closing socket...', file=log_buffer)
        sock.close()

        # TODO: when all is said and done, you should return the entire reply
        # you received from the server as the return value of this function.

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage = '\nusage: python echo_client.py "this is my message"\n'
        print(usage, file=sys.stderr)
        sys.exit(1)

    msg = sys.argv[1]
    client(msg)
