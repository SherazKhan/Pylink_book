# Filename: retrieve_events_2.py
# Author: Zhiguo Wang
# Date: 11/7/2020
#
# Description:
# A short script illustrating online retrieval of eye events

import pylink

# Connect to the tracker and open an EDF
tk = pylink.EyeLink('100.1.1.1')
tk.openDataFile('ev_test.edf')

tk.sendCommand('sample_rate 1000')  # set sample rate to 1000 Hz

# Make all types of event data are available over the link
event_flgs = 'LEFT,RIGHT,FIXATION,FIXUPDATE,SACCADE,BLINK,BUTTON,INPUT'
tk.sendCommand('link_event_filter = %s' % event_flgs)

# Open an SDL window to calibrate the tracker
pylink.openGraphics()
tk.doTrackerSetup()
pylink.closeGraphics()

# Start recording
error = tk.startRecording(1, 1, 1, 1)
pylink.msecDelay(100)  # cache some samples for event parsing

t_start = tk.trackerTime()  # current tracker time
while True:
    # Break after 5 seconds have elapsed
    if tk.trackerTime() - t_start > 5000:
        break

    # Retrieve the oldest event in the buffer
    dt = tk.getNextData()
    if dt > 0:
        ev = tk.getFloatData()
        if dt == pylink.ENDSACC:
            print('ENDSACC Event: \n',
                  'Amplitude', ev.getAmplitude(), '\n',
                  'Angle', ev.getAngle(), '\n',
                  'AverageVelocity', ev.getAverageVelocity(), '\n',
                  'PeakVelocity', ev.getPeakVelocity(), '\n',
                  'StartTime', ev.getStartTime(), '\n',
                  'StartGaze', ev.getStartGaze(), '\n',
                  'StartHREF', ev.getStartHREF(), '\n',
                  'StartPPD', ev.getStartPPD(), '\n',
                  'StartVelocity', ev.getStartVelocity(), '\n',
                  'EndTime', ev.getEndTime(), '\n',
                  'EndGaze', ev.getEndGaze(), '\n',
                  'EndHREF', ev.getEndHREF(), '\n',
                  'StartPPD', ev.getStartPPD(), '\n',
                  'EndVelocity', ev.getEndVelocity(), '\n',
                  'Eye', ev.getEye(), '\n',
                  'Time', ev.getTime(), '\n',
                  'Type', ev.getType(), '\n')

tk.stopRecording()  # stop recording
tk.closeDataFile()  # close the EDF data file on the Host
# Download the EDF data file from Host
tk.receiveDataFile('ev_test.edf', 'ev_test.edf')
tk.close()  # close the link to the tracker
