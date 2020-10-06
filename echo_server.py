import socket
import sys
import traceback


def server(log_buffer=sys.stderr):
    # set an address for our server
    address = ('127.0.0.1', 5001)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)

    # log that we are building a server
    print("making a server on {0}:{1}".format(*address), file=log_buffer)
    sock.bind(('127.0.0.1', 5001))
    sock.listen(1)
    connection, client_address = sock.accept()

    try:
        # the outer loop controls the creation of new connection sockets. The
        # server will handle each incoming connection one at a time.
        while True:
            print('waiting for a connection', file=log_buffer)

            conn, addr = sock.accept()
            #conn, addr = ('foo', ('bar', 'baz'))
            try:
                print('connection - {0}:{1}'.format(*addr), file=log_buffer)
                # the inner loop will receive messages sent by the client in
                # buffers.  When a complete message has been received, the
                # loop will exit
                incoming_message = ''
                while True:
                    data = conn.recv(16)
                    incoming_message += data.decode('utf8')
                    if len(data.decode('utf8')) < 16 :
                        out_message = 'You sent the server this: ' + incoming_message
                        print('sent "{0}"'.format(out_message))
                        conn.sendall(out_message.encode('utf8'))
                        break
            except Exception as e:
                traceback.print_exc()
                sys.exit(1)
            finally:
                conn.close()
                print(
                    'echo complete, client connection closed', file=log_buffer
                )

    except KeyboardInterrupt:
        # TODO: Use the python KeyboardInterrupt exception as a signal to
        #       close the server socket and exit from the server function.
        #       Replace the call to `pass` below, which is only there to
        #       prevent syntax problems
        #pass
        sock.close()
        print('quitting echo server', file=log_buffer)
        sys.exit(0)

if __name__ == '__main__':
    server()
    sys.exit(0)
