TICKETS_SLIDER = """
<style>
.ticker-container {
    overflow: hidden;
    white-space: nowrap;
    background: linear-gradient(90deg, #1f77b4, #ff7f0e);
    color: white;
    padding: 10px;
    border-radius: 5px;
    margin: 20px 0;
}

.ticker-text {
    display: inline-block;
    animation: scroll-left 30s linear infinite;
    font-weight: bold;
}

.ticker-text::after {
    content: " • BTCUSDT • ETHUSDT • ADAUSDT • SOLUSDT • DOTUSDT • BNBUSDT • XRPUSDT • LINKUSDT • MATICUSDT • AVAXUSDT • LTCUSDT • UNIUSDT";
    margin-left: 50px;
}

@keyframes scroll-left {
    0% { transform: translateX(0%); }
    100% { transform: translateX(-100%); }
}
</style>
<div class="ticker-container">
    <div class="ticker-text">
        BTCUSDT • ETHUSDT • ADAUSDT • SOLUSDT • DOTUSDT • BNBUSDT • XRPUSDT • LINKUSDT • MATICUSDT • AVAXUSDT • LTCUSDT • UNIUSDT
    </div>
</div>
"""


CARD_STYLE = '''<div style="
            border: 2px solid #451818;
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
            background: linear-gradient(135deg, #6f86a8 0%, #1d7f8a 100%);
        ">
            <h3>{} {}</h3>
            <div style="display: flex; justify-content: space-between;">
                <div>
                    <strong>Slope:</strong> {:.6f}<br>
                    <strong>Derivation:</strong> {:.6f}
                </div>
                <div>
                    <strong>Trend:</strong> {}<br>
                    <strong>Strength:</strong> {}
                </div>
            </div>
        </div>'''
