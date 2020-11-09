import numpy as np
import matplotlib.pyplot as plt
#import peakutils

samplef = 500


# We know that DTMF frequencies are 697, 770, 852, 941, 1209, 1336, 1477

def analogf_detector(soundf):
    samplef = 1000  # due to the assighment request
    threshold = 2
    resolution = 0.001
    goal = np.array([0, 0, 0, 0, 0, 0, 0, 0])
    for i in range(int(threshold / resolution)):
        if (threshold < soundf[int(303 / samplef * len(soundf))] and goal[1] == 0):
            print('has analog frequency 697 Hz')
            goal[0] = goal[0] + 1
            goal[1] = goal[1] + 1
        if (threshold < soundf[int(230 / samplef * len(soundf))] and goal[2] == 0):
            print('has analog frequency 770 Hz')
            goal[0] = goal[0] + 1
            goal[2] = goal[2] + 1
        if (threshold < soundf[int(148 / samplef * len(soundf))] and goal[3] == 0):
            print('has analog frequency 852 Hz')
            goal[0] = goal[0] + 1
            goal[3] = goal[3] + 1
        if (threshold < soundf[int(59 / samplef * len(soundf))] and goal[4] == 0):
            print('has analog frequency 941 Hz')
            goal[0] = goal[0] + 1
            goal[4] = goal[4] + 1
        if (threshold < soundf[int(209 / samplef * len(soundf))] and goal[5] == 0):
            print('has analog frequency 1209 Hz')
            goal[0] = goal[0] + 1
            goal[5] = goal[5] + 1
        if (threshold < soundf[int(336 / samplef * len(soundf))] and goal[6] == 0):
            print('has analog frequency 1336 Hz')
            goal[0] = goal[0] + 1
            goal[6] = goal[6] + 1
        if (threshold < soundf[int(477 / samplef * len(soundf))] and goal[7] == 0):
            print('has analog frequency 1477 Hz')
            goal[0] = goal[0] + 1
            goal[7] = goal[7] + 1
        if (goal[0] != 2):
            threshold = threshold - resolution
        elif (goal[0] == 2):
            break


# importing the data
sound_track_0 = np.loadtxt('/Users/luyinan/Desktop/msc_matric_1.dat')
time = sound_track_0[:, 0]
sound = sound_track_0[:, 1]
plt.plot(sound, linewidth=0.5,)
plt.show()
# do FFT to all the imported data
# manually cutting the data
soundf_0 = np.fft.fft(sound[1900:2200])
soundf_1 = np.fft.fft(sound[2300:2500])
soundf_2 = np.fft.fft(sound[2700:2900])
soundf_3 = np.fft.fft(sound[4100:4300])
soundf_4 = np.fft.fft(sound[4500:4700])
soundf_5 = np.fft.fft(sound[4800:5100])
soundf_6 = np.fft.fft(sound[6200:6400])
soundf_7 = np.fft.fft(sound[6600:6800])
soundf_8 = np.fft.fft(sound[7000:7250])
soundf_9 = np.fft.fft(sound[8200:8400])
soundf_10 = np.fft.fft(sound[8500:8700])

print('0 part has')
analogf_detector(abs(soundf_0))
print('1 part has')
analogf_detector(abs(soundf_1))
print('2 part has')
analogf_detector(abs(soundf_2))
print('3 part has')
analogf_detector(abs(soundf_3))
print('4 part has')
analogf_detector(abs(soundf_4))
print('5 part has')
analogf_detector(abs(soundf_5))
print('6 part has')
analogf_detector(abs(soundf_6))
print('7 part has')
analogf_detector(abs(soundf_7))
print('8 part has')
analogf_detector(abs(soundf_8))
print('9 part has')
analogf_detector(abs(soundf_9))
print('10 part has')
analogf_detector(abs(soundf_10))

