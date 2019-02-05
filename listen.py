#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Real-Time Input Device Listener
'''

import pyaudio
import time
import sys

p = pyaudio.PyAudio()


def audio_callback(in_data, frame_count, time_info, status):
    return (in_data, pyaudio.paContinue)
        
def StartStream(inputIdx=None,
                outputIdx=None,
                inName='DEFAULT',
                outName='DEFAULT',
                default=False):
    print("\nInput: " + inName)
    print("Output: " + outName)
    
    if not default:
        chans   = p.get_device_info_by_index(outputIdx)["maxOutputChannels"]
        defRate = p.get_device_info_by_index(outputIdx)["defaultSampleRate"]
    else:
        chans   = p.get_default_output_device_info()["maxOutputChannels"]
        defRate = p.get_default_output_device_info()["defaultSampleRate"]
        
    stream = p.open(format=pyaudio.paInt16,
                    channels=chans,
                    rate=int(defRate),
                    output=True,
                    input=True,
                    stream_callback=audio_callback,
                    input_device_index=inputIdx,
                    output_device_index=outputIdx)
    
    stream.start_stream()
    print("Streaming... Press Ctrl+C to Stop.")

    # Allow Program Stopping with Ctrl+C
    try:
        while stream.is_active():
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Stopping..")
        stream.stop_stream()
        stream.close()
        p.terminate()
        time.sleep(0.1) # To read print message


# Int() that acccepts blank strings safely 
def mk_int(s):
    s = s.strip()
    return int(s) if s else 0

# Get Input as Integer With option for default return value on invalid input
def getInputInt(text, default=None):
  result = input(text)
  if default != None:
    if (result == "") or (mk_int(result) == 0 and result != "0"):
      return default
  return mk_int(result)

def main():
    print("\nReal-Time Input Device Listener")
    print("\nIndex - Device:")
    deviceCount = p.get_device_count()
    for x in range(0, deviceCount):
        print("  " + str(x) + " - " + p.get_device_info_by_index(x)["name"] + "..")

    i = getInputInt("\nInput Device Index: ", -1)
    o = getInputInt("Output Device Index: ", -1)
    default = True if (i < 0 or o < 0) else False
    
    if i >= deviceCount:
        print("Bad Input Device Index.")
    elif o >= deviceCount:
        print("Bad Output Device Index.")
    else:
        if not default:
            inInfo = p.get_device_info_by_index(i)
            outInfo = p.get_device_info_by_index(o)

            if inInfo["maxInputChannels"] == 0:
                print("Selected Input Device does not support audio input.")
            elif outInfo["maxOutputChannels"] == 0:
                print("Selected Output Device does not support audio output.")
            else:
                StartStream(inputIdx=i,
                            outputIdx=o,
                            inName=inInfo["name"],
                            outName=outInfo["name"])
        else:
            StartStream(default=True)

if __name__ == "__main__":
    main()
 
