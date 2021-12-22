import numpy as np

# Definition of pulses follow Chen et al. PRL, 116, 020501 (2016)


def drag_gaussian_pulse_waveforms(
    amplitude, length, sigma, alpha, detune, delta, substracted
):
    """
    Function that returns DRAG pulses that compensate for leakage and also for the AC stark shift
    that the leakage creates to the qubit frequency.

    Envelope: gaussian

    :param amplitude: amplitude of voltage
    :param length: pulse length
    :param sigma: gaussian standard deviation
    :param alpha: DRAG coefficient
    :param detune: frequency shift to correct for AC start shift
    :param delta: f_21 - f_10 - detune
    :param substracted: if you would like to use a substracted gaussian
    """
    t = np.arange(length, dtype=int)  # array of size pulse length in ns
    gauss_wave = amplitude * np.exp(
        -((t - length / 2) ** 2) / (2 * sigma ** 2)
    )  # gaussian function
    gauss_der_wave = (
        amplitude
        * (-2 * 1e9 * (t - length / 2) / (2 * sigma ** 2))
        * np.exp(-((t - length / 2) ** 2) / (2 * sigma ** 2))
    )  # derivative of gaussian
    if substracted:  # if statement to determine usage of subtracted gaussian
        gauss_wave = gauss_wave - gauss_wave[-1]  # subtracted gaussian
    z = gauss_wave + 1j * gauss_der_wave * (alpha / delta)  # complex DRAG envelope
    z *= np.exp(1j * 2 * np.pi * detune * t * 1e-9)  # complex DRAG detuned envelope
    I_wf = z.real.tolist()  # get the real part of the I component of waveform
    Q_wf = z.imag.tolist()  # get the imaginary part for the Q component of waveform
    return I_wf, Q_wf


def drag_cosine_pulse_waveforms(amplitude, length, alpha, detune, delta):
    """
    Function that returns DRAG pulses that compensate for leakage and also for the AC stark shift
    that the leakage creates to the qubit frequency.

    Envelope: cosine

    :param amplitude: amplitude of voltage
    :param length: pulse length
    :param alpha: DRAG coefficient
    :param detune: frequency shift to correct for AC start shift
    :param delta: f_21 - f_10 - detune
    """
    t = np.arange(length, dtype=int)  # array of size pulse length in ns
    cos_wave = 0.5 * amplitude * (1 - np.cos(t * 2 * np.pi / length))  # cosine function
    sin_wave = (
        0.5 * amplitude * (2 * np.pi / length * 1e9) * np.sin(t * 2 * np.pi / length)
    )  # derivative of cos_wave
    z = cos_wave + 1j * sin_wave * (alpha / delta)  # complex DRAG envelope
    z *= np.exp(1j * 2 * np.pi * detune * t * 1e-9)  # complex DRAG detuned envelope
    I_wf = z.real.tolist()  # get the real part for the I component of waveform
    Q_wf = z.imag.tolist()  # get the imaginary part for the Q component of waveform
    return I_wf, Q_wf
