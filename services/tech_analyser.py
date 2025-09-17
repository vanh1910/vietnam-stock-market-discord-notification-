from pathlib import Path
import numpy as np
import pandas as pd
import datetime as dt
import json

root = Path(__file__).resolve().parent.parent

class TechAnalyser:
    df = pd.DataFrame()

    def load_json(self, relative_path: str) -> dict:
        """Đọc file JSON và trả về dict"""
        json_path = root / relative_path
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
        
    
    def data_processor(self, path):
        json_path = root / path 
        #take data from json file

        data = self.load_json(json_path)
        
        #process data to dataframe
        ticker = data["params"]["symbol"]
        self.df["timestamp"] = pd.to_datetime(data["t"], unit='s')
        self.df["open"] =  data["o"]
        self.df["high"] =  data["h"]
        self.df["low"] =  data["l"]
        self.df["close"] =  data["c"]
        self.df["volumn"] =  data["v"]    
        self.df["ticker"] = ticker

    def sma(self, period: int):
        self.df[f'sma_{period}'] = self.df['close'].rolling(window=period).mean()
    
    def ema(self, period: int):
        self.df[f'ema_{period}'] = self.df['close'].ewm(span=period, adjust=False).mean()
    
    def rsi(self, period: int):
        delta = self.df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        self.df[f'rsi_{period}'] = 100 - (100 / (1 + rs))
    
    
    def test(self):
        path = "data/json/cache.json"
        self.data_processor(path)
        self.ema(9)
        self.ema(26)
        self.rsi(14)
        print(self.df)
    

    


if __name__ == "__main__":
    analyser = TechAnalyser()
    analyser.test()
        





