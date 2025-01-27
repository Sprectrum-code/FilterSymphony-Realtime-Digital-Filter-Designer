import numpy as np
from scipy import signal

class DigitalFilters:
    def __init__(self):
        pass
    
    def butterworth_lowpass(self, order=4, cutoff=0.5):
        """
        Butterworth lowpass filter
        Args:
            order: Filter order
            cutoff: Normalized cutoff frequency (0 to 1, where 1 is Nyquist frequency)
        Returns:
            tuple: (zeros, poles)
        """
        z, p, _ = signal.butter(order, cutoff, output='zpk')
        return [(z.real, z.imag) for z in z], [(p.real, p.imag) for p in p]
    
    def chebyshev1_lowpass(self, order=4, cutoff=0.5, ripple=1):
        """
        Chebyshev Type I lowpass filter
        Args:
            order: Filter order
            cutoff: Normalized cutoff frequency
            ripple: Maximum ripple allowed in passband (dB)
        """
        z, p, _ = signal.cheby1(order, ripple, cutoff, output='zpk')
        return [(z.real, z.imag) for z in z], [(p.real, p.imag) for p in p]
    
    def chebyshev2_lowpass(self, order=4, cutoff=0.5, attenuation=40):
        """
        Chebyshev Type II lowpass filter
        Args:
            order: Filter order
            cutoff: Normalized cutoff frequency
            attenuation: Minimum attenuation in stopband (dB)
        """
        z, p, _ = signal.cheby2(order, attenuation, cutoff, output='zpk')
        return [(z.real, z.imag) for z in z], [(p.real, p.imag) for p in p]
    
    # def inverse_chebyshev_lowpass(self, order=4, cutoff=0.5, attenuation=40):
    #     """
    #     Inverse Chebyshev lowpass filter
    #     Args:
    #         order: Filter order
    #         cutoff: Normalized cutoff frequency
    #         attenuation: Minimum attenuation in stopband (dB)
    #     Returns:
    #         tuple: (zeros, poles)
    #     Note:
    #         The inverse Chebyshev is similar to Chebyshev Type II but with
    #         maximally flat response in the passband and equiripple in the stopband
    #     """
    #     # The inverse Chebyshev is implemented using Chebyshev Type II
    #     # but with inversed specifications
    #     z, p, _ = signal.cheby2(order, attenuation, 1.0/cutoff, output='zpk')
        
    #     # Normalize the frequencies
    #     z = z / np.max(np.abs(z))
    #     p = p / np.max(np.abs(p))
        
    #     return [(z.real, z.imag) for z in z], [(p.real, p.imag) for p in p]
    
    def elliptic_lowpass(self, order=4, cutoff=0.5, ripple=1, attenuation=40):
        """
        Elliptic (Cauer) lowpass filter
        Args:
            order: Filter order
            cutoff: Normalized cutoff frequency
            ripple: Maximum ripple in passband (dB)
            attenuation: Minimum attenuation in stopband (dB)
        """
        z, p, _ = signal.ellip(order, ripple, attenuation, cutoff, output='zpk')
        return [(z.real, z.imag) for z in z], [(p.real, p.imag) for p in p]
    
    def bessel_lowpass(self, order=4, cutoff=0.5):
        """
        Bessel lowpass filter
        Args:
            order: Filter order
            cutoff: Normalized cutoff frequency
        """
        z, p, _ = signal.bessel(order, cutoff, output='zpk')
        return [(z.real, z.imag) for z in z], [(p.real, p.imag) for p in p]
    
    def notch_filter(self, Q=30.0, freq=0.5):
        """
        Notch filter to remove a specific frequency
        Args:
            Q: Quality factor
            freq: Normalized frequency to remove (0 < freq < 1)
        Returns:
            tuple: (zeros, poles)
        """
            
        b, a = signal.iirnotch(freq, Q)
        
        z, p, _ = signal.tf2zpk(b, a)
        
        return [(float(z.real), float(z.imag)) for z in z], [(float(p.real), float(p.imag)) for p in p]
    
    def bandpass_filter(self, order=4, lowcut=0.1, highcut=0.4):
        """
        Butterworth bandpass filter
        Args:
            order: Filter order
            lowcut: Lower cutoff frequency
            highcut: Higher cutoff frequency
        """
        z, p, _ = signal.butter(order, [lowcut, highcut], btype='band', output='zpk')
        return [(z.real, z.imag) for z in z], [(p.real, p.imag) for p in p]
    
    def highpass_filter(self, order=4, cutoff=0.5):
        """
        Butterworth highpass filter
        Args:
            order: Filter order
            cutoff: Normalized cutoff frequency
        """
        z, p, _ = signal.butter(order, cutoff, btype='high', output='zpk')
        return [(z.real, z.imag) for z in z], [(p.real, p.imag) for p in p]
    
    def bandstop_filter(self, order=4, lowcut=0.1, highcut=0.4):
        """
        Butterworth bandstop filter
        Args:
            order: Filter order
            lowcut: Lower cutoff frequency
            highcut: Higher cutoff frequency
        """
        z, p, _ = signal.butter(order, [lowcut, highcut], btype='stop', output='zpk')
        return [(z.real, z.imag) for z in z], [(p.real, p.imag) for p in p]
    
    def gaussian_filter(self, order=4, cutoff=0.5):
        """
        Gaussian filter approximation using Bessel filter
        Args:
            order: Filter order
            cutoff: Normalized cutoff frequency
        """
        z, p, _ = signal.bessel(order, cutoff, 'low', output='zpk', norm='phase')
        return [(z.real, z.imag) for z in z], [(p.real, p.imag) for p in p]