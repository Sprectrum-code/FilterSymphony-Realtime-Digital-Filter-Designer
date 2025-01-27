import numpy as np
import matplotlib.pyplot as plt

def compute_response(zeros, poles, w_range=(0, np.pi), num_points=500):
    """
    Computes the magnitude and phase response of a system given its zeros and poles.

    Parameters:
    - zeros: List of tuples [(z1_real, z1_imag), (z2_real, z2_imag), ...]
    - poles: List of tuples [(p1_real, p1_imag), (p2_real, p2_imag), ...]
    - w_range: Tuple specifying the frequency range in radians (default: 0 to π).
    - num_points: Number of points in the frequency range (default: 500).

    Returns:
    - w: Array of frequency values.
    - magnitude: Magnitude response.
    - phase: Phase response.
    """
    # Frequency range
    w = np.linspace(w_range[0], w_range[1], num_points)

    # Convert zeros and poles to complex numbers
    zeros = [z[0] + 1j * z[1] for z in zeros]
    poles = [p[0] + 1j * p[1] for p in poles]

    # Initialize frequency response
    H = np.ones(len(w), dtype=complex)

    # Compute numerator and denominator for each frequency
    for z in zeros:
        H *= np.exp(-1j * w) - z
    for p in poles:
        H /= np.exp(-1j * w) - p

    # Compute magnitude and phase
    magnitude = np.abs(H)
    phase = np.angle(H)

    return w, magnitude, phase

# Example: Define zeros and poles
zeros = [(0.5, 0.5), (0.5, -0.5)]  # Two zeros
poles = [(0.9, 0.1), (0.9, -0.1)]  # Two poles

# Compute response
w, magnitude, phase = compute_response(zeros, poles)

# Plot magnitude response
plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plt.plot(w, magnitude, label="Magnitude Response")
plt.title("Magnitude and Phase Response")
plt.ylabel("Magnitude")
plt.xlabel("Frequency (radians/sample)")
plt.grid(True)
plt.legend()

# Plot phase response
plt.subplot(2, 1, 2)
plt.plot(w, phase, label="Phase Response", color="orange")
plt.ylabel("Phase (radians)")
plt.xlabel("Frequency (radians/sample)")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()
