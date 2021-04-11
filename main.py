import requests, sys
from datetime import datetime

def getExchangeStatistics( symbol , exchange = 'blockchain' ):

    URL = f'https://api.blockchain.com/v3/exchange/l2/{symbol}'

    response = requests.get( URL, verify = True)
    l2_data = response.json()

    spread    = ( l2_data['asks'][0]['px'] - l2_data['bids'][0]['px'] ) * 10000. / l2_data['bids'][0]['px']
    askdepth  = l2_data['asks'][0]['qty']
    biddepth  = l2_data['bids'][0]['qty']

    summary_data = [ datetime.now().strftime('%Y-%m-%d %H:%M:%S') , symbol , spread , biddepth , askdepth ]

    return summary_data

def saveJob():

    symbols = ['BTC-USD','BTC-TRY']

    for symbol in symbols:
        data = getExchangeStatistics(symbol)
        fileName = ''.join(symbol.split('-'))
        writeToCSV(data , f'{fileName}.csv')
        print(fileName + ' saved!')
    
def writeToCSV( data , file ):

    import csv   

    with open(file, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(data)

if __name__ == "__main__":

    import schedule, time

    schedule.every(1).minutes.do(saveJob)

    print('Starting script to save exchange statistics...')
    
    while True:
        schedule.run_pending()
        time.sleep(1)

