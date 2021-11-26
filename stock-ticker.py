from RPLCD.i2c import CharLCD
import os
from dotenv import load_dotenv
import json
import time
import http.client
import urllib.parse


load_dotenv()


def write_to_lcd(lcd, framebuffer, num_cols):
    lcd.home()
    for row in framebuffer:
        lcd.write_string(row.ljust(num_cols)[:num_cols])
        lcd.write_string('\r\n')


def loop_string(string, lcd, framebuffer, row, num_cols, delay=0.15):
    padding = ' ' * num_cols
    s = padding + string + padding
    for i in range(len(s) - num_cols + 1):
        framebuffer[row] = s[i:i+num_cols]
        write_to_lcd(lcd, framebuffer, num_cols)
        time.sleep(delay)


def format_num(num):
    return "{:.2f}".format(num)


conn = http.client.HTTPSConnection("seeking-alpha.p.rapidapi.com")

# Get you own API key from Rapid API
# No more freebies
headers = {
    'x-rapidapi-host': "seeking-alpha.p.rapidapi.com",
    'x-rapidapi-key': os.getenv("RAPID_API")
}

stocks = ["AAPL","ADBE","ADI","ADP","ADSK","AEP","ALGN","AMAT","AMD","AMGN","AMZN","ANSS","ASML","ATVI","AVGO","BIDU","BIIB","BKNG","CDNS","CDW","CERN","CHKP",
"CHTR","CMCSA","COST","CPRT","CRWD","CSCO","CSX","CTAS","CTSH","DLTR","DOCU","DXCM","EA","EBAY","EXC","FAST","FB","FISV","FOX",
"FOXA","GILD","GOOG","GOOGL","HON","IDXX","ILMN","INCY","INTC","INTU","ISRG","JD","KDP","KHC","KLAC","LRCX","LULU","MAR","MCHP",
"MDLZ","MELI","MNST","MRNA","MRVL","MSFT","MTCH","MU","NFLX","NTES","NVDA","NXPI","OKTA","ORLY","PAYX","PCAR","PDD","PEP","PTON","PYPL","QCOM","REGN","ROST","SBUX",
"SGEN","SIRI","SNPS","SPLK","SWKS","TCOM","TEAM","TMUS","TSLA","TXN","VRSK","VRSN","VRTX","WBA","WDAY","XEL","XLNX","ZM"]

conn.request("GET", "/market/get-realtime-prices?symbols=" + "%2C".join(stocks),
             headers=headers)

res = conn.getresponse()
data = res.read()

ticker_data = json.loads(data.decode("utf-8"))["data"]

stock_data = ""
for ticker_obj in ticker_data:
    stock_attributes = ticker_obj["attributes"]
    stock_data = stock_data + stock_attributes["identifier"] + ": " + format_num(stock_attributes["last"]) + "(" + format_num(stock_attributes["change"]) + ") "

framebuffer = [
    'Stock Ticker',
    '',
]

lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=16, rows=2,
              dotsize=8, charmap='A02', auto_linebreaks=True, backlight_enabled=True)

while True:
    loop_string(stock_data, lcd, framebuffer, 1, 16)
