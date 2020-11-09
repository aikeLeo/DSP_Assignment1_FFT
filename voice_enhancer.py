import wave
import numpy as np
import math
import matplotlib.pyplot as plt


def get_wave_params(wavfile):

    wf = wave.open(wavfile, "rb")        # open wav
    params = wf.getparams()     # get parameters
    nchannels, sampwidth, framerate, nframes = params[:4]
    return nchannels, sampwidth, framerate, nframes


def get_wavedata(wavfile):

    # read wave file
    wf = wave.open(wavfile, "rb")
    params = wf.getparams()
    nchannels, sampwidth, framerate, nframes = params[:4]
    str_data = wf.readframes(nframes)   # read whole frame data to str_data
    wf.close()  # close wave

    # Convert waveform data to array
    wave_data = np.frombuffer(str_data, dtype=np.short)
    wave_data.shape = -1, 2
    wave_data = wave_data.T
    return wave_data

# enhance tone amplitude
def amplitudes_increase(freq_data, real_value, imag_value):

    freq_data = freq_data.tolist()
    freq_data_real = [x.real for x in freq_data]
    freq_data_imag = [x.imag for x in freq_data]

    # enhance amplitude
    freq_data_real = [x*real_value for x in freq_data_real]
    freq_data_imag = [x*imag_value for x in freq_data_imag]
    freq_data_enhance = np.array([complex(x, freq_data_imag[step]) for step, x in enumerate(freq_data_real)])

    return freq_data_enhance


# 6k-10k area, filtering
def region_enhance(freq_data, framerate, nframes, enhance_region=[6000,10000]):

    half_framerate = math.ceil(framerate/2)
    symmetry_enhance_region = [(half_framerate-x)*2+x for x in enhance_region]
    enhance_region = [int(x/framerate * nframes) for x in enhance_region]
    symmetry_enhance_region = [int(x/framerate * nframes) for x in symmetry_enhance_region]

    for i in range(enhance_region[0], enhance_region[1]):
        freq_data[i] = complex(0, 0)
    for i in range(symmetry_enhance_region[1], symmetry_enhance_region[0]):
        freq_data[i] = complex(0, 0)

    return freq_data


def enhance_freq(waveData, framerate, nframes, real_value, imag_value):

    freq_data = np.fft.fft(waveData)/nframes
    # enhance amplitude
    freq_data_enhance = amplitudes_increase(freq_data, real_value, imag_value)
    # 6k-10k area, filter to remove noise
    freq_data_enhance = region_enhance(freq_data_enhance, framerate, nframes)
    # Inverse Fourier transform
    time_data = np.fft.ifft(freq_data_enhance*nframes).real.astype(np.short)

    return time_data


def save_wav(wav_data, wav_name, nchannels, sampwidth, framerate):

    f = wave.open(wav_name, "wb")

    # Configure the number of channels, quantization bits, sampling frequency
    f.setnchannels(nchannels)
    f.setsampwidth(sampwidth)
    f.setframerate(framerate)

    # convert Wav_ Data to binary data and write into a file
    f.writeframes(wav_data.tostring())
    f.close()


def voice_quality_improve(wavfile):
    waveData = get_wavedata(wavfile)
    nchannels, sampwidth, framerate, nframes = get_wave_params(wavfile)
    # data of L&R channels
    time_data_left = enhance_freq(waveData[0], framerate, nframes, 5, 5)
    time_data_right = enhance_freq(waveData[1], framerate, nframes, 2, 2)
    # merge data
    time_data = np.concatenate(
        [np.expand_dims(time_data_left, axis=1),
         np.expand_dims(time_data_right, axis=1)], axis=1).T
    # save as wav
    save_wav(time_data, wav_name=r"improved.wav", nchannels=1, sampwidth=sampwidth, framerate=framerate)


if __name__=="__main__":
    file = r"/Users/luyinan/Desktop/original.wav"
    voice_quality_improve(file)
