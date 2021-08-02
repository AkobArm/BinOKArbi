import requests
import pandas

url = "https://api.binance.com/api/v1/ticker/24hr"
response = requests.get(url).json()

binance_dict = {}
for currency in response:
        name = currency['symbol']
        price = currency['lastPrice']
        volume = currency['volume']
        binance_dict[name] = [price, volume]

url = "https://okex.com/api/spot/v3/instruments/ticker/"
response = requests.get(url).json()
okex_dict = {}
for currency in response:
    name = currency['instrument_id'].replace('-', '')
    price = currency['ask']
    volume = currency['base_volume_24h']
    okex_dict[name] = [price, volume]

bin_list = list(binance_dict.keys())
okex_list = list(okex_dict.keys())
all_list = set(bin_list + okex_list)

unify_names = pandas.Series([name for name in all_list])
binance_names = pandas.Series([f'{price}$/{volume}' for name in all_list for price, volume in [binance_dict.get(name, ['-', '-'])]])
okex_names = pandas.Series([f'{price}$/{volume}' for name in all_list for price, volume in [okex_dict.get(name, ['-', '-'])]])

Data = pandas.DataFrame([unify_names, binance_names, okex_names]).T
Data.columns = ['Unify_name', 'Binance_name', 'Okex_name']
Data.sort_values(by='Unify_name')

print(Data)
