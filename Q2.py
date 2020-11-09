import wave
import numpy as np
import matplotlib.pyplot as plt

def get_wave_params(wavfile):

    wf = wave.open(wavfile, "rb")    # open wav
    params = wf.getparams()     # get parameters
    nchannels, sampwidth, framerate, nframes = params[:4]
    return nchannels, sampwidth, framerate, nframes

def get_wavedata(wavfile):

    wf = wave.open(wavfile, "rb")    # open wav
    params = wf.getparams()     # get parameters
    nchannels, sampwidth, framerate, nframes = params[:4]
    str_data = wf.readframes(nframes)   # read whole frame data to str_data
    wf.close()  # close wave

    # transform wave data to array
    wave_data = np.frombuffer(str_data, dtype=np.short)
    wave_data.shape = -1, 2
    wave_data = wave_data.T
    return wave_data

def get_timedomain(wavfile):

    wave_data = get_wavedata(wavfile)  # Get processed wave data
    nchannels, sampwidth, framerate, nframes=get_wave_params(wavfile)

    # Construct abscissa
    time_length = np.arange(0, nframes) * (1.0 / framerate)
    return time_length, wave_data[0], wave_data[1]

def get_freqdomain(wavfile):

    waveData = get_wavedata(wavfile)  # get wave data
    nchannels, sampwidth, framerate, nframes = get_wave_params(wavfile)

    # FFT，get amplitude
    fft_y1 = np.fft.fft(waveData[0]) / nframes  # left vocal channel
    fft_y2 = np.fft.fft(waveData[1]) / nframes  # right vocal channel

    # calculate frequency domain x
    freqs = np.linspace(0, framerate, nframes)

    return freqs, np.abs(fft_y1), np.abs(fft_y2)

# Draw the time / frequency domain diagram of left and right channels
def plot_single(time_length, wave_data, freqs_length, fft_data, mode="left", title_size=15,
                label_size=10, color_type=["orange", "lavender"]):

    fig = plt.figure(figsize=(20, 10))
    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)

    ax1.set_title('Time Domain', fontsize=title_size)
    ax1.set_xlabel("time(seconds)")
    ax1.set_ylabel("amplitudes")

    ax2.set_title('Frequency Domain', fontsize=title_size)
    ax2.set_xlabel("frequence(Hz)")
    ax2.set_ylabel("amplitudes")

    ax1.plot(time_length, wave_data, c=color_type[0])
    ax2.plot(freqs_length, fft_data, c=color_type[1])

    plt.show()
    #plt.savefig(mode+"_audio_signal.png", dpi=300)

# draw all diagrams in one picture
def plot_all(time_length, wave_data_left, wave_data_right, freqs_length, fft_left, fft_right, title_size=15,
        label_size=10, color_type=["orange", "lavender"]):

    fig = plt.figure(figsize=(20, 20))
    ax1 = fig.add_subplot(221)
    ax2 = fig.add_subplot(222)
    ax3 = fig.add_subplot(223)
    ax4 = fig.add_subplot(224)

    ax1.set_title('Time Domain (left)', fontsize=title_size)
    ax1.set_xlabel("time(seconds)")
    ax1.set_ylabel("amplitudes")

    ax2.set_title('Time Domain (right)', fontsize=title_size)
    ax2.set_xlabel("time(seconds)")
    ax2.set_ylabel("amplitudes")

    ax3.set_title('Frequency Domain (left)', fontsize=title_size)
    ax3.set_xlabel("frequence(Hz)")
    ax3.set_ylabel("amplitudes")

    ax4.set_title('Frequency Domain (right)', fontsize=title_size)
    ax4.set_xlabel("frequence(Hz)")
    ax4.set_ylabel("amplitudes")

    ax1.plot(time_length, wave_data_left, c=color_type[0])
    ax2.plot(time_length, wave_data_right, c=color_type[0])

    ax3.plot(freqs_length, fft_left, c=color_type[1])
    ax4.plot(freqs_length, fft_right, c=color_type[1])

    plt.show()
    #plt.savefig("all_audio_signal.png", dpi=300)


def plot_audio_signal(wavfile):

    # get time length, left&right time data
    time_length, wave_data_left, wave_data_right = get_timedomain(wavfile)
    # get frequency length 44100 ，left&right part freq data
    freqs_length, fft_left, fft_right = get_freqdomain(wavfile)

    # draw left part time/frequency
    plot_single(
        time_length, wave_data_left,freqs_length, fft_left,
        mode="left", title_size=15, label_size=10, color_type=["orange","lavender"]
    )
    # draw right part time/frequency
    plot_single(
        time_length, wave_data_right, freqs_length, fft_right,
        mode="right", title_size=15, label_size=10, color_type=["orange","lavender"]
    )
    # draw left&right part time/frequency
    plot_all(
        time_length, wave_data_left,wave_data_right,
        freqs_length, fft_left,fft_right,
        title_size = 15, label_size = 10, color_type = ["orange", "lavender"]
    )

if __name__=="__main__":
    file = r"/Users/luyinan/Desktop/original.wav"
    plot_audio_signal(file)
