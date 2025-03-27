import os
import websocket
import json
import time
from alpaca_trade_api.rest import REST

# Load Alpaca API credentials (replace with your actual keys)
ALPACA_API_KEY = os.getenv("ALPACA_API_KEY", "PKPQNB6A121H7BWQP31I")
ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY", "MgLLrGHBCL9R5swfllLFWTHOnQ1uuRh9MZMpTRO3")
BASE_URL = "https://paper-api.alpaca.markets"
DATA_STREAM_URL = "wss://stream.data.alpaca.markets/v2/iex"  # For historical data

# Initialize REST API client
alpaca_rest = REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, BASE_URL)

def on_message(ws, message):
    """Handles incoming WebSocket messages."""
    data = json.loads(message)
    print(type(data))

    if isinstance(data, list):
        for item in data:
            if item.get("T") == "b":  # "b" stands for bar (candlestick)
                symbol = item.get("S")  # Stock symbol (AAPL, etc.)
                time = item.get("t")  # Timestamp
                open_price = item.get("o")  # Open price
                high = item.get("h")  # High price
                low = item.get("l")  # Low price
                close = item.get("c")  # Close price
                volume = item.get("v")  # Trading volume
                
                print(f"[{symbol}] {time} | Open: {open_price} | High: {high} | Low: {low} | Close: {close} | Volume: {volume}")

def on_error(ws, error):
    print("WebSocket Error:", error)

def on_close(ws, close_status_code, close_msg):
    print("WebSocket Closed")

def on_open(ws):
    """Subscribe to real-time stock quotes."""
    auth_message = {
        "action": "auth",
        "key": ALPACA_API_KEY,
        "secret": ALPACA_SECRET_KEY
    }
    ws.send(json.dumps(auth_message))
    
    subscribe_message = {
        "action": "subscribe",
        "bars": ["AAPL"]  # Symbols to track
    }
    ws.send(json.dumps(subscribe_message))
    print("Subscribed to live data.")

def run_websocket():
    while True:
        ws = websocket.WebSocketApp(DATA_STREAM_URL, 
                                    on_open=on_open, 
                                    on_message=on_message, 
                                    on_error=on_error, 
                                    on_close=on_close)
        ws.run_forever()
        print("Reconnecting in 5 seconds...")
        time.sleep(5)  # Wait before retrying


if __name__ == "__main__":
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp(DATA_STREAM_URL, 
                                on_open=on_open, 
                                on_message=on_message, 
                                on_error=on_error, 
                                on_close=on_close)
    ws.run_forever()