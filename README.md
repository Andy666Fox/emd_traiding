# Emperical Mode Decomposition (EMD) for stock data analyze

## **About**
## <p>This method based on decomposing signal (natural analog signals or artificial stock pricing in that case) into **Intrinsic Mode Functions** (IMF)</p>

## **Quick Start**
1. Clone the repo
2. check and install requiered dependencies (*libs in pyproject.toml*)
3. last step - call the **get_data_slope** func with necessary stock symbol
`get_data_slope('BTCUSDT')`


## Features
1. Easy data loading
2. Ability to customize IMF level
3. A negative slope value indicates a downward price movement, and the opposite is also true.

### EMD on [wiki](https://ru.wikipedia.org/wiki/Empirical_Mode_Decomposition)
### EMD python [library](https://pyemd.readthedocs.io/en/latest/emd.html) 