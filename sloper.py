from data_scrapper import get_last_period
import numpy as np 
from PyEMD import CEEMDAN

def decompose(data_sample: np.array, delay: int=0) -> np.array:
    ''' function for decompose signal by the
      Complete Ensemble Empirical Mode Decomposition with Adaptive Noise (CEEMDAN)

      Params:
      data_sample: np.array
          sample of data, or raw signal

      delay: int
          option for separate data 

      Returns:
        imf: np.array
          complete CEEMDAN components (3 by default)

        t: np.array
          time of signal
    '''
    
    t = np.array([x+1+delay for x in range(len(data_sample))])
    S = np.array(data_sample)

    ceemdan = CEEMDAN()
    imf = ceemdan.ceemdan(S, t)

    return imf ,t

def get_slope(dc: np.array, derdc: np.array) -> float:
  '''function for calculate slope between emd signal and his derivative

     Params:
      dc: last two points of emd signal
      derdc: last two points of emd signal derivative

    Returns:
      slope: normalized slope (between -1 and 1) of lines
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
   '''
   '''

   data = get_last_period(symbol=symbol, period=period, tf=tf)
   dc, _ = decompose(data[col])
   dc_derivative = np.gradient(dc[imf_level])

   scale_coef = (dc[imf_level][-1] / dc_derivative[-1]) / 10
   slope = get_slope(dc[imf_level][-2:], dc_derivative[-2:]) * scale_coef
   # normalize slope value between [-1 , 1]

   return slope


s = get_data_slope('euraud', 200, 1)
print(f'Slope: {s:.5f}')