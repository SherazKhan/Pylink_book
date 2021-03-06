# Filename: video_playback.py
# Author: Zhiguo Wang
# Date: 11/7/2020
#
# Description:
# Play video and record eye movements in Psychopy

import pylink
import os
import random
from psychopy import visual, core, event, monitors
from EyeLinkCoreGraphicsPsychoPy import EyeLinkCoreGraphicsPsychoPy
from psychopy.constants import STOPPED, PLAYING

# Screen resolution
SCN_WIDTH, SCN_HEIGHT = (1280, 800)

# SETP 1: Connect to the tracker
tk = pylink.EyeLink('100.1.1.1')

# Step 2: Open an EDF data file on the Host
tk.openDataFile('video.edf')
# Add preamble text (file header)
tk.sendCommand("add_file_preamble_text 'Movie playback demo'")

# Step 3: Setup Host parameters
# put the tracker in idle mode before we change its parameters
tk.setOfflineMode()
pylink.msecDelay(50)

# Sample rate, 250, 500, 1000, or 2000;
# this command does not support EyeLInk II/I
tk.sendCommand('sample_rate 500')

# Send the resolution of the monitor to the tracker
tk.sendCommand("screen_pixel_coords = 0 0 %d %d" % (SCN_WIDTH-1, SCN_HEIGHT-1))

# Save monitor resolution in EDF data file
# so Data Viewer can correctly load background graphics
tk.sendMessage("DISPLAY_COORDS = 0 0 %d %d" % (SCN_WIDTH-1, SCN_HEIGHT-1))

# Calibration type, H3, HV3, HV5, HV13 (HV = horiztonal/vertical)
tk.sendCommand("calibration_type = HV9")

# Step 4: Open a window for graphics and calibration
# always create a monitor object before you run the script
customMon = monitors.Monitor('demoMon', width=35, distance=65)
customMon.setSizePix((SCN_WIDTH, SCN_HEIGHT))
# Open a window
win = visual.Window((SCN_WIDTH, SCN_HEIGHT), fullscr=False,
                    monitor=customMon, units='pix', allowStencil=True)
# Require Pylink to use the window we just opened for calibration
graphics = EyeLinkCoreGraphicsPsychoPy(tk, win)
pylink.openGraphicsEx(graphics)

# Step 5: Calibrate the tracker, and run through all the trials
calib_prompt = "Press ENTER twice to calibrate the tracker"
calib_msg = visual.TextStim(win, text=calib_prompt, color='white', )
calib_msg.draw()
win.flip()
event.waitKeys()

# Calibrate the tracker
tk.doTrackerSetup()

# Step 6: Run through a couple of trials
# put the videos we would like to play in a list
trials = [
    ['t1', 'Seoul.mp4'],
    ['t2', 'Seoul.mp4']
    ]


# Here we define a helper function to group the code executed on each trial
def run_trial(pars):
    """ pars corresponds to a row in the trial list"""

    # Retrieve parameters from the trial list
    trial_num, movie_file = pars

    # Load the video to display
    mov = visual.MovieStim3(win, filename=movie_file, size=(960, 540))

    # Take the tracker offline
    tk.setOfflineMode()
    pylink.msecDelay(50)

    # Send the standard "TRIALID" message to mark the start of a trial
    tk.sendMessage("TRIALID %s %s" % (trial_num, movie_file))

    # Record_status_message : show some info on the Host PC
    msg = "record_status_message 'Movie File: %s'" % movie_file
    tk.sendCommand(msg)

    # Drift check/correction, params, x, y, draw_target, allow_setup
    try:
        tk.doDriftCorrect(int(SCN_WIDTH/2), int(SCN_HEIGHT/2), 1, 1)
    except:
        tk.doTrackerSetup()

    # Start recording;
    # params: sample_in_file, event_in_file,
    # sampe_over_link, event_over_link (1-yes, 0-no)
    tk.startRecording(1, 1, 1, 1)
    # Wait for 50 ms to cache some samples
    pylink.msecDelay(50)

    # The size of the video
    mo_width, mo_height = mov.size
    # position the movie at the center of the screen
    mov_x = int(SCN_WIDTH/2 - mo_width/2)
    mov_y = int(SCN_HEIGHT/2 - mo_height/2)

    # play the video till the end
    frame_n = 0
    prev_frame_timestamp = mov.getCurrentFrameTime()
    while mov.status is not STOPPED:
        # draw a movie frame and flip the video buffer
        mov.draw()
        win.flip()

        # if a new frame is drawn, check frame timestamp and
        # send a VFRAME message
        current_frame_timestamp = mov.getCurrentFrameTime()
        if current_frame_timestamp != prev_frame_timestamp:
            frame_n += 1
            # send a message to mark the onset of each video frame
            tk.sendMessage('Video_Frame: %d' % frame_n)
            # VFRAME message: "!V VFRAME frame_num movie_pos_x,
            # movie_pos_y, path_to_movie_file"
            m_path = '../' + movie_file
            msg = "!V VFRAME %d %d %d %s" % (frame_n, mov_x, mov_y, m_path)
            tk.sendMessage(msg)
            prev_frame_timestamp = current_frame_timestamp

    # Send a message to mark video playback end
    tk.sendMessage("Video_terminates")

    # Clear the subject display
    win.color = (0, 0, 0)
    win.flip()

    # Stop recording
    tk.stopRecording()

    # Send a'TRIAL_RESULT' message to mark the end of trial
    tk.sendMessage('TRIAL_RESULT')

# Run a block of 2 trials, in random order
test_list = trials[:]
random.shuffle(test_list)
for trial in test_list:
    run_trial(trial)

# Step 7: Close the EDF data file and put the tracker in idle mode
tk.closeDataFile()
tk.setOfflineMode()
pylink.pumpDelay(100)

# Step 8: Download EDF file to a local folder ('edfData')
msg = 'Downloading EDF file from the EyeLink Host PC ...'
edfTransfer = visual.TextStim(win, text=msg, color='white')
edfTransfer.draw()
win.flip()

if not os.path.exists('edfData'):
    os.mkdir('edfData')
tk.receiveDataFile('video.edf', 'edfData/video_demo.edf')

# Step 9: Close the connection to tracker, close graphics
tk.close()
core.quit()
