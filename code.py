import sys

try:
  buffer = []
  while True:
    data = sys.stdin.read(1)
    if data != None and data != '':
      buffer.append(ord(data))

    sys.stdout.write("chat %s\r\n" % buffer)

    # we start getting out of sync with our messages, so pop anything that isn't a 1
    while len(buffer) > 0 and buffer[0] != 1:
      sys.stdout.write("chat popping %s\r\n" % buffer.pop(0))

    if len(buffer) >= 4 and buffer[0] == 1 and buffer[1] == 83 and buffer[2] == 67 and len(buffer) >= buffer[3]+4:
      del buffer[0:4+buffer[3]]
except Exception as e:
  sys.stdout.write("chat %s" % str(e))
