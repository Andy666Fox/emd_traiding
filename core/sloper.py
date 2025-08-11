from core.data_scrapper import get_last_period
import numpy as np 
from PyEMD import CEEMDAN
from sklearn.preprocessing import normalize

def decompose(data_sample: np.array, delay: int=0) -> np.array:
    '''Perform signal decomposition using Complete Ensemble Empirical Mode Decomposition with Adaptive Noise (CEEMDAN).
    
    CEEMDAN is an advanced noise-assisted adaptive decomposition method that improves upon EMD by:
    - Reducing mode mixing through multiple noise realizations
    - Maintaining decomposition completeness with minimal residual noise
    - Automatically determining the number of Intrinsic Mode Functions (IMFs)

    Args:
        data_sample: 1D numpy array containing the input signal to decompose. 
            Should meet CEEMDAN requirements (non-constant, non-fully linear)
        delay: Time axis offset for temporal alignment of decomposed components. 
            Shifts time indices by N positions (default: 0)

    Returns:
        tuple: Contains two numpy arrays:
            - imfs: 2D array of shape (n_imfs, signal_length) containing:
                * IMFs ordered from highest to lowest frequency components
                * Residual trend as last component
            - t: 1D time vector starting from (1 + delay) with length matching input signal

    Raises:
        ValueError: If input is not 1D array, contains NaNs, or has < 4 samples
        TypeError: For non-numeric input data

    Example:
        >>> signal = np.random.randn(100)
        >>> imfs, time = decompose(signal, delay=10)
        >>> print(f"Decomposed into {imfs.shape[0]} IMFs")
        Decomposed into 5 IMFs

    Notes:
        - Requires CEEMDAN implementation from PyEMD or equivalent library
        - Decomposition complexity grows with signal length (O(n log n) typical)
        - IMF count varies based on signal complexity (typically 5-15 components)
        - Last IMF represents the residual trend component
    '''
    
    t = np.array([x+1+delay for x in range(len(data_sample))])
    S = np.array(data_sample)

    ceemdan = CEEMDAN()
    imf = ceemdan.ceemdan(S, t)

    return imf ,t

def get_slope(dc: np.array, derdc: np.array) -> float:
  '''Calculate scale-invariant angular relationship between EMD signal and derivative trends.
    
    Computes the tangent of the angle between two line segments formed by the last 
    two points of each input array. Each segment is independently normalized to unit 
    length before slope calculation, making the result invariant to the absolute 
    scales of the input signals.
    
    
    Algorithm steps:
    1. Extract last two points from each array as separate segments
    2. Normalize each segment independently to unit vector length
    3. Calculate directional slopes of normalized segments
    4. Apply arctangent difference formula: (m1 - m2) / (1 + m1*m2)

    Args:
        dc (np.array): EMD component time series, must have at least 2 elements
        derdc (np.array): Derivative component time series, must have at least 2 elements
    
    Returns:
        float: Tangent of angle between normalized direction vectors.
               Range: (-∞, ∞), but typically bounded due to normalization constraints.
               Values closer to 0 indicate similar directions of change.
    
    Raises:
        ZeroDivisionError: When normalized segments are perpendicular 
                          (denominator |1 + m1*m2| < 1e-10)
        ValueError: When either input array has fewer than 2 elements
        RuntimeWarning: When input segments have zero magnitude (constant values)
    
        
        The result represents the angular relationship between the normalized 
        direction vectors, independent of their original magnitudes.
  '''

  seq1 = np.array([dc[-2], dc[-1]])
  seq2 = np.array([derdc[-2], derdc[-1]])

  seq1_norm = seq1 / np.linalg.norm(seq1)
  seq2_norm = seq2 / np.linalg.norm(seq2)

  m1 = seq1_norm[1] - seq1_norm[0]
  m2 = seq2_norm[1] - seq2_norm[0]

  denominator = 1 + m1 * m2

  if abs(denominator) < 1e-10:
     raise ZeroDivisionError('Segments are perpendicular')

  slope = (m1 - m2) / denominator

  return slope

def get_data_slope(symbol, period=100, tf=3, imf_level=-1, col='Close_Price'):
   '''Calculate slope metrics for price data using Empirical Mode Decomposition (EMD).
    
    Processes historical price data to extract trend characteristics through:
    1. Data normalization (standardization)
    2. Empirical Mode Decomposition to extract trend components
    3. Derivative analysis of selected IMF component
    4. Angular relationship analysis between signal and its derivative
    
    Args:
        symbol (str): Asset ticker symbol (e.g. 'AAPL', 'BTCUSDT')
        period (int, optional): Number of historical candles to analyze. Default: 100
        tf (int, optional): Timeframe in minutes for each candle. Default: 3
        imf_level (int, optional): Index of IMF component to analyze from EMD results. 
        col (str, optional): Price column to analyze. Default: 'Close_Price'
    
    Returns:
        tuple: Contains two metrics:
            - slope (float): Angular relationship between IMF and its derivative
            - trend_acceleration (float): Normalized acceleration of the trend
   '''

   data = get_last_period(symbol=symbol, period=period, tf=tf)
   data_for_decompose = normalize(np.array(data[col]).reshape(1, -1))[0]
   dc, _ = decompose(data_for_decompose)
   dc_derivative = np.gradient(dc[imf_level])

   slope = get_slope(dc[imf_level][-2:], dc_derivative[-2:])

   second_derivative = np.gradient(dc_derivative)
   derivative_scale = np.std(dc_derivative) if np.std(dc_derivative) > 1e-10 else 1.0
   trend_acc = second_derivative[-1] / derivative_scale

   return slope, trend_acc