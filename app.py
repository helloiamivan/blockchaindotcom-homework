import streamlit as st
import pandas as pd
import numpy as np
from tabulate import tabulate

def load_data( sym ):
    data = pd.read_csv( f'{sym}.csv' ,
                        index_col = 0, 
                        parse_dates = True,
                        header = None, 
                        names = ['Datetime','Symbol','Spread(bps)','Best Bid Size', 'Best Ask Size'])

    data.index = pd.to_datetime(data.index)

    return data

st.title('Blockchain Exchange Statistics')
symbols = ['BTCUSD','BTCTRY']

alldata = []
for sym in symbols:
    data = load_data(sym)

    st.subheader(f'Spread (bps) by time - {sym[:3]}/{sym[-3:]}')
    st.line_chart(data['Spread(bps)'])

    st.subheader(f'Best Bid Size by time - {sym[:3]}/{sym[-3:]}')
    st.bar_chart(data['Best Bid Size'])

    st.subheader(f'Best Ask Size by time - {sym[:3]}/{sym[-3:]}')
    st.bar_chart(data['Best Ask Size'])

    st.subheader(f'Most Recent Observations - {sym[:3]}/{sym[-3:]}')
    st.text(tabulate(data.tail(5) , headers = 'keys'))
    alldata.append(data)

alldata = pd.concat(alldata,axis=0)

## Get the historical summary stats
histdata = alldata.groupby('Symbol').mean()
startDate = histdata.index.min()
endDate   = histdata.index.max()

st.subheader(f'Historical Summary Statistics (Average)')

st.dataframe(histdata)

st.subheader(f'Historical Summary Statistics (Maximum)')

st.dataframe(alldata.groupby('Symbol').max())

st.subheader(f'Historical Summary Statistics (Minimum)')

st.dataframe(alldata.groupby('Symbol').min())
