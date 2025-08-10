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
  '''Calculate normalized angular relationship between EMD signal and its derivative.
    
    Computes the tangent of angle between two normalized line segments representing:
    1. Last two points of Empirical Mode Decomposition (EMD) component
    2. Corresponding points from its derivative component

    The calculation involves:
    1. Coordinate system normalization using Frobenius norm
    2. Slope calculation for both normalized line segments
    3. Angular relationship using arctangent formula

    Args:
        dc: 1D array with at least 2 elements from EMD component time series
        derdc: 1D array with at least 2 elements from derivative component time series

    Returns:
        float: Tangent of angle between normalized segments. Theoretical range (-∞, ∞),
        but typically constrained by normalization to (-2.0, 2.0) in practice

    Raises:
        ZeroDivisionError: If line segments are perfectly perpendicular
        ValueError: If input arrays contain less than 2 elements

    Example:
        >>> get_slope(np.array([2.1, 2.4]), np.array([0.1, 0.3]))
        -0.287
  '''

  fx1 = len(dc) - 1
  fy1 = dc[-2]

  fx2 = len(dc)
  fy2 = dc[-1]

  sx1 = len(derdc) - 1
  sy1 = derdc[-2]

  sx2 = len(derdc)
  sy2 = derdc[-1]

  arr = np.array([[fx1, fy1, fx2, fy2],
                  [sx1, sy1, sx2, sy2]])
  norm = np.linalg.norm(arr)
  arr = arr / norm

  fx1 = arr[0][0]
  fy1 = arr[0][1]
  fx2 = arr[0][2]
  fy2 = arr[0][3]

  sx1 = arr[1][0]
  sy1 = arr[1][1]
  sx2 = arr[1][2]
  sy2 = arr[1][3] 

  m1 = (fy2 - fy1) / (fx2 - fx1)
  m2 = (sy2 - sy1) / (sx2 - sx1)

  slope = (m1 - m2) / (1 + m1*m2)


  return slope

def get_data_slope(symbol, period=100, tf=3, imf_level=-1, col='Close_Price'):
   '''Calculate slope metrics for price data using Empirical Mode Decomposition (EMD).
    
    Processes historical price data to extract trend characteristics through:
    1. Signal normalization
    2. Empirical Mode Decomposition
    3. Derivative analysis of selected IMF component
    4. Slope scaling and rate-of-change calculation

    Args:
        symbol (str): Asset ticker symbol (e.g. 'AAPL', 'BTCUSDT')
        period (int, optional): Number of historical candles to analyze. Default: 100
        tf (int, optional): Timeframe in minutes for each candle. Default: 3
        imf_level (int, optional): Index of IMF component to analyze from EMD results. 
            Uses Python-style negative indexing. Default: -1 (last component)
        col (str, optional): Price column to analyze. Default: 'Close_Price'

    Returns:
        tuple: Contains two metrics:
            - slope (float): Scaled slope of selected IMF component (dimensionless)
            - der_slope (float): Rate of change of derivative (1e7 scaled value)

    Raises:
        ValueError: If input data is empty or IMF level is out of bounds
        TypeError: If required columns are missing in the data

    Notes:
        - Requires normalize(), decompose(), and get_slope() helper functions
        - IMF components are ordered from highest to lowest frequency
        - Final slope value represents recent trend characteristics in [-1, 1] range
        - der_slope indicates acceleration/deceleration of the trend
   '''

   data = get_last_period(symbol=symbol, period=period, tf=tf)
   data[col] = normalize(np.array(data[col]).reshape(1, -1)).reshape(-1, 1)
   dc, _ = decompose(data[col])
   dc_derivative = np.gradient(dc[imf_level])

   scale_coef = (dc[imf_level][-1] / dc_derivative[-1])
   slope = get_slope(dc[imf_level][-2:], dc_derivative[-2:]) * scale_coef
   der_slope = (dc_derivative[-1] - dc_derivative[-2]) * 1e7

   return slope, der_slope


print(get_data_slope('BTCUSDT'))