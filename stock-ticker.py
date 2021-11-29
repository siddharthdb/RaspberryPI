import I2C_LCD_driver
import os
from dotenv import load_dotenv
import json
import time
import http.client

load_dotenv()

def format_num(num):
    return "{:.2f}".format(num)


conn = http.client.HTTPSConnection("seeking-alpha.p.rapidapi.com")

# Get you own API key from Rapid API
# No more freebies
headers = {
    'x-rapidapi-host': "seeking-alpha.p.rapidapi.com",
    'x-rapidapi-key': os.getenv("RAPID_API")
}

stocks = ["AAPL", "ADBE", "ADI", "ADP", "ADSK", "AEP", "ALGN", "AMAT", "AMD", "AMGN", "AMZN", "ANSS", "ASML", "ATVI", "AVGO", "BIDU", "BIIB", "BKNG", "CDNS", "CDW",
          "CERN", "CHKP", "CHTR", "CMCSA", "COST", "CPRT", "CRWD", "CSCO", "CSX", "CTAS", "CTSH", "DLTR", "DOCU", "DXCM", "EA", "EBAY", "EXC", "FAST", "FB", "FISV", 
          "FOX", "FOXA", "GILD", "GOOG", "GOOGL", "HON", "IDXX", "ILMN", "INCY", "INTC", "INTU", "ISRG", "JD", "KDP", "KHC", "KLAC", "LRCX", "LULU", "MAR", "MCHP",
          "MDLZ", "MELI", "MNST", "MRNA", "MRVL", "MSFT", "MTCH", "MU", "NFLX", "NTES", "NVDA", "NXPI", "OKTA", "ORLY", "PAYX", "PCAR", "PDD", "PEP", "PTON", "PYPL",
          "QCOM", "REGN", "ROST", "SBUX", "SGEN", "SIRI", "SNPS", "SPLK", "SWKS", "TCOM", "TEAM", "TMUS", "TSLA", "TXN", "VRSK", "VRSN", "VRTX", "WBA", "WDAY", "XEL", "XLNX", "ZM"]

conn.request("GET", "/market/get-realtime-prices?symbols=" + "%2C".join(stocks),
             headers=headers)

res = conn.getresponse()
data = res.read()

ticker_data = json.loads(data.decode("utf-8"))["data"]

stock_data = ""
for ticker_obj in ticker_data:
    stock_attributes = ticker_obj["attributes"]
    stock_data = stock_data + stock_attributes["identifier"] + ": " + format_num(
        stock_attributes["last"]) + "(" + format_num(stock_attributes["change"]) + ") "

lcd = I2C_LCD_driver.lcd()
str_pad = " " * 16
stock_data = str_pad + stock_data

while True:
    for i in range(0, len(stock_data)):
        lcd_text = stock_data[i:(i+16)]
        lcd.lcd_display_string("Stock Ticker!", 1)
        lcd.lcd_display_string(lcd_text, 2)
        time.sleep(0.08)
        lcd.lcd_display_string(str_pad, 2)
