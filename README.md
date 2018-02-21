# Circuit Python Serial Glitchiness

I was playing playing around with Circuit Python and SerialCraft and ran into some unexpected behavior.

Check out [this video](https://www.youtube.com/watch?v=PU3UaNmLeHA) to see what was happening.

See [this instructable](https://www.instructables.com/id/Creeper-Detector/) for an example how to get a real 
project up and running with SerialCraft.

# Problem

The SerialCraft mod reports the distance to the nearest creeper whenever the distance changes by a whole block. 
A message consists of a 1 followed by 83, then 67 ('SC'), followed by the number of bytes the rest of the message 
contains (in this case 2), followed by a type (creeper distance message is 4), followed by the number of blocks 
to the nearest creeper. In this demo, the numbers should always be (1, 83, 67, 2, 4, creeper distance). In the demo, 
I have 2 devices connected: an Arduino Uno and a Circuit Playground Express. 

The Uno is running [this code](https://www.youtube.com/redirect?redir_token=g7IaR6mTG_GsVjQPnXCGvwX5Pzp8MTUxOTM0MjU5N0AxNTE5MjU2MTk3&event=video_description&v=PU3UaNmLeHA&q=https%3A%2F%2Fgithub.com%2FAllwineDesigns%2FCircuitPythonSerialGlitchiness%2Fblob%2Fmaster%2FSerialCraftTest%2FSerialCraftTest.ino).

The Circuit Playground Express is running [this Circuit Python script](https://www.youtube.com/redirect?redir_token=g7IaR6mTG_GsVjQPnXCGvwX5Pzp8MTUxOTM0MjU5N0AxNTE5MjU2MTk3&event=video_description&v=PU3UaNmLeHA&q=https%3A%2F%2Fgithub.com%2FAllwineDesigns%2FCircuitPythonSerialGlitchiness%2Fblob%2Fmaster%2Fcode.py).

I've tested the Circuit Playground Express (CPX) with the same native code as the Uno and see the correct behavior. The python code on the CPX has incorrect behavior.

The python code outputs the numbers in square brackets, the Uno just outputs the numbers. You'll see that at 13 blocks away, the Uno outputs the correct 13 blocks, but the CPX outputs 10 blocks. Also, when under 4 blocks, the CPX seems to crash or reboot or something as it is stops reporting messages until you go back out to 4 blocks or further away.

# Causes

## Under 4 blocks

Turns out CircuitPython checks the serial stream for control characters (Ctrl+C and Ctrl+D). 
Ctrl+C stops the python script and Ctrl+D reloads the script. Ctrl+C has a byte representation of 3 and 
Ctrl+D has a byte representation of 4, so at 3 blocks away SerialCraft is killing the CircuitPython script 
on the Circuit Playground express. Go back to 4 blocks and the script is restarted. 

## At 13 blocks

13 is a carriage return (\r) which CircuitPython is changing to a newline (\n or 10). See this [GitHub issue](https://www.youtube.com/redirect?redir_token=g7IaR6mTG_GsVjQPnXCGvwX5Pzp8MTUxOTM0MjU5N0AxNTE5MjU2MTk3&event=video_description&v=PU3UaNmLeHA&q=https%3A%2F%2Fgithub.com%2Fadafruit%2Fcircuitpython%2Fissues%2F554) for more about that.

## Blocking

Another issue that isn't shown in this demo is that reading from stdin is the only way to access serial data over the
CPX's USB cable. The problem with that is there is no way to access that data without blocking the whole program, which
means other animations/interactions can't be happening while polling for data on the serial port.

# Solution

Current workaround is to use a separate USB to serial cable to connect to the RX and TX pins of the Circuit 
Playground Express, exposing a second serial port that we can connect to using busio.UART. This allows any 
data to be sent (rather than any data besides certain control characters), while also providing a means to 
timeout during serial reads rather than blocking when reading from stdin (see [busio.UART](http://circuitpython.readthedocs.io/en/2.x/shared-bindings/busio/UART.html)). 
When doing it this way the Circuit Playground Express's regular serial USB connection can be dedicated to debugging which is handy. It is an extra ~$10 
for the extra USB to serial cable and you'll need to install drivers for it to make it work, so it's not quite ideal, but it works.
