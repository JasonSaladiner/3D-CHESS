# Access Tello log data

import socket
import sys
import signal
import time

BUFFER_SIZE = 1024

STATE = ('x', 'y', 'z',
         'pitch', 'roll', 'yaw',
         'vgx', 'vgy', 'vgz', 'time',
         'agx', 'agy', 'agz')


def collect_state(state):
    dic = {k: v for k, v in zip(STATE, ['' for _ in STATE])}
    items = state.split(';')
    pairs = tuple(item.split(':') for item in items)
    values = tuple((pair[0].strip(), pair[-1].strip()) for pair in pairs)
    for i in range(len(values)):
        k, v = values[i][0], values[i][1]
        try:
            dic[k] = int(v)
        except:
            try:
                dic[k] = float(v)
            except:
                pass
    return dic


if __name__ == '__main__':

    local = ('', 8890)
    remote = ('192.168.10.1', 8889)

    signal.signal(signal.SIGINT, signal.SIG_DFL)

    socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket.bind(local)
    socket.setblocking(1)

    out = None

    attempts = 3
    for i in range(attempts):

        socket.sendto('command'.encode('latin-1'), remote)
        buffer = socket.recv(BUFFER_SIZE)
        out = buffer.decode('latin-1')

        if out == 'ok':
            print('accepted')
            break
        else:
            print('rejected')
            time.sleep(0.5)
            out = None

    while out:
        buffer = socket.recv(BUFFER_SIZE)
        out = buffer.decode('latin-1')
        out = out.replace('\n', '')
        dic = collect_state(out)
        t = time.time()
        print(''.join(str(dic).split(' ')), file=sys.stdout, flush=True)
        print('time:{:4d}\tnick:{:>4}\troll:{:>4}\tyaw:{:>4}'.format(
            int((t - int(t)) * 1000), dic['pitch'], dic['roll'], dic['yaw']),
            file=sys.stdout, flush=True)

    print('exit')
