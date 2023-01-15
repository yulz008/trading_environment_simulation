from flask import Flask, render_template, request, flash, redirect,jsonify
import csv
from binance.client import Client
from binance.enums import *
import time, random
import os
from dotenv import load_dotenv


# object creation for flask
app = Flask(__name__)
app.secret_key = b'asfdadagsdf.srewtsdfh3rt5rty3eg4543'










#functions

def get_symbol_info_change (**input):

    
    if input == {}:
         print("no input")
    else:
         
         print(input)
         present_day = input['end_str']
         prev_day = input['start_str']
         print(present_day,prev_day)

    info = client.get_account()
    balances = info['balances']
    exchange_info = client.get_exchange_info()
    #symbols = exchange_info['symbols']


    futures_exchange_info = client.futures_exchange_info()  # request info on all futures symbols
    futures_trading_pairs = [info['symbol'] for info in futures_exchange_info['symbols']]
    futures_trading_pairs_usdt = []
    for x in futures_trading_pairs:
        if 'USDT' in x:
            futures_trading_pairs_usdt.append(x)

    symbols =  futures_trading_pairs_usdt
    list_symbol = []


    #interval based from inputs that was passed in this function

 

    for x in symbols:

        try:
            # print(x)
            st = time.time()

            if input == {}:
                #candlesticks = client.get_historical_klines(x, Client.KLINE_INTERVAL_1DAY,'2 days ago')
                candlesticks = [[random.uniform(0, 100) for _ in range(7)],[random.uniform(0, 100) for _ in range(7)]]

            else:
                candlesticks = client.get_historical_klines(x, Client.KLINE_INTERVAL_1DAY,prev_day,present_day)
                #candlesticks = [[random.uniform(0, 100) for _ in range(7)],[random.uniform(0, 100) for _ in range(7)]]

            et = time.time()
            elapsed_time = et - st
            #print('Execution time:', elapsed_time, 'seconds')
            #print(candlesticks[1][0])
            candle_timestamp = candlesticks[1][0]
            candle_close = candlesticks[1][4]
            candle_volume = candlesticks[1][5]
            candle_change_percent =   round((((float(candlesticks[1][4]))-(float(candlesticks[0][4])))/(float(candlesticks[1][4])))*100,2)
            initial_list = [x,candle_timestamp,candle_close,candle_volume,candle_change_percent]   
              
            list_symbol.append(initial_list)
        except:
            print('invalid symbol', x)
    return list_symbol
        
        
    
    print(list_symbol)
    # here i will modify the list that will be pass towards HTML index.. for now, only the symbol extracted from the futures_exchange_info is available
    # using this one i will create a list that will contain information about the OHLC on the given day includng the previos close to compute the %


def numbers_to_months(argument):
    switcher = {
    
        '1': "Jan",
        '2': "Feb",
        '3': "Mar",
        '4': "Apr",
        '5': "May",
        '6': "Jun",
        '7': "Jul",
        '8': "Aug",
        '9': "Sep",
        '10': "Oct",
        '11': "Nov",
        '12': "Dec"

    }
 
    # get() method of dictionary data type returns
    # value of passed argument if it is present
    # in dictionary otherwise second argument will
    # be assigned as default value of passed argument
    return switcher.get(argument)



def format_date_binance_api_req (date_format):

       
    date_format = date_format.split("-")
   

    print(date_format[1][0])
    
    if  date_format[2][0] == '0':
        date_format[2] = date_format[2].replace('0','')

    if  date_format[1][0] == '0':
        date_format[1] = date_format[1].replace('0','')

    
    Day = date_format[2] + " "
    Year = date_format[0]
    Month = numbers_to_months(date_format[1]) + ", "
    string_date = Day + Month + Year

    
    return string_date






@app.route("/")
def index():
    title = 'Trading Environment Simulation'


    app_host = os.getenv("APP_HOST")
    app_port = os.getenv("APP_PORT")
    
    list_symbol = get_symbol_info_change()

        
    return render_template('index.html',title = title,  symbols = list_symbol, app_host = app_host, app_port=app_port)


@app.route("/buy", methods = ['POST'] ) # this allow post request
def buy():

    # print(request.form)
    
    try:
        order = client.create_order(
        symbol=request.form["symbol"],
        side=SIDE_BUY,
        type=ORDER_TYPE_MARKET,
        quantity=request.form["quantity"])
    except Exception as e:
        flash(e.message, "error")
    return redirect ('/')




@app.route("/sell")
def sell():
    return 'sell'




@app.route("/update_prices", methods = ['POST'])
def update_prices():

    


    present_day = request.headers['present_day']
    prev_day = request.headers['prev_day']
    
    

    #format for API binance date request
    present_day = format_date_binance_api_req(present_day)
    prev_day =  format_date_binance_api_req(prev_day)

    #print(present_day)
    #print(prev_day)
    
    list_symbol = get_symbol_info_change(start_str = prev_day, end_str = present_day )



    return list_symbol
   



@app.route('/history')


def history():

  

    candlesticks = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1DAY)
 
    processed_candlesticks = []

    for data in candlesticks:
         
        candlestick = { 
            "time": data[0]/1000, 
            "open": data[1], 
            "high": data[2], 
            "low": data[3], 
            "close": data[4] 
         }
    
        processed_candlesticks.append(candlestick)


    return jsonify(processed_candlesticks)



@app.route('/history_test', methods = ['POST'])
def history_test():
    
    #print("hello")
    #print(request.headers['Symbol'])

      # get the start time
    st = time.time()
    #print(request.headers['date_input'])

    date = request.headers['date_input']
    #print(date)
    date = format_date_binance_api_req(date)
    #print(date)
    candlesticks = client.get_historical_klines(request.headers['Symbol'], Client.KLINE_INTERVAL_1DAY,'12 Dec, 2000', date)


        # get the end time
    et = time.time()
    elapsed_time = et - st
    # print('Execution time:', elapsed_time, 'seconds')
 
    processed_candlesticks = []

    for data in candlesticks:
         
        candlestick = { 
            "time": data[0]/1000, 
            "open": data[1], 
            "high": data[2], 
            "low": data[3], 
            "close": data[4] 
         }
    
        processed_candlesticks.append(candlestick)



    
    
    return jsonify(processed_candlesticks)







def create_dotenv():
    if not os.path.exists('.env'):
        host = input("Enter the IP address or domain name of your GCP instance or localhost: ")
        port = input("Enter the port of your application: ")
        api_key = input("Enter your API key: ")
        api_secret = input("Enter your API secret: ")
        with open('.env', 'w') as f:
            f.write(f'APP_HOST={host}\nAPP_PORT={port}\nAPI_KEY={api_key}\nAPI_SECRET={api_secret}')


if __name__ == '__main__':
    create_dotenv()
    load_dotenv()
    client = Client(os.getenv("API_KEY"), os.getenv("API_SECRET"))
    app.run(host='0.0.0.0',port=os.getenv("APP_PORT"))
    


