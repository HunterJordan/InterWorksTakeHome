import pandas as pd
import numpy as np


def wrangle():
    df = pd.read_csv(
        'app/data/flights.txt',
        sep='|',
        header=None,
        low_memory=False,
        on_bad_lines='skip',
    )

    def wrap(df):
        df.columns = [
            'TRANSACTIONID', 'FLIGHTDATE', 'AIRLINECODE', 'AIRLINENAME',
            'TAILNUM', 'FLIGHTNUM', 'ORIGINAIRPORTCODE', 'ORIGAIRPORTNAME',
            'ORIGINCITYNAME', 'ORIGINSTATE', 'ORIGINSTATENAME', 'DESTAIRPORTCODE',
            'DESTAIRPORTNAME', 'DESTCITYNAME', 'DESTSTATE', 'DESTSTATENAME',
            'CRSDEPTIME', 'DEPTIME', 'DEPDELAY', 'TAXIOUT', 'WHEELSOFF',
            'WHEELSON', 'TAXIIN', 'CRSARRTIME', 'ARRTIME', 'ARRDELAY',
            'CRSELAPSEDTIME', 'ACTUALELAPSEDTIME', 'CANCELLED', 'DIVERTED',
            'DISTANCE'
        ]

        # SETTING TRANSACTION ID AS INDEX AND DROPPING COLUMN
        df.set_index(
            'TRANSACTIONID'
        )

        df['FLIGHTDATE'] = pd.to_datetime(
            df['FLIGHTDATE'],
            errors='coerce',
            format='%Y-%m-%d'
        ).dt.date

        # STRIPPING ' miles' OFF DISTANCE COLUMN TO BIN VALUES
        df['DISTANCEGROUP'] = df['DISTANCE'].str.strip(' miles')

        df['DISTANCEGROUP'] = df['DISTANCEGROUP'].str.replace(
            '([0-9]+)',
            r'\1',
            regex=True
        )

        # REPLACING BOOLEAN VALUES
        df['DIVERTED'] = df['DIVERTED'].replace(
            {'False': 0,
             'F': 0,
             '0': 0}
        )
        df['CANCELLED'] = df['CANCELLED'].replace(
            {'False': 0,
             'F': 0,
             '0': 0}
        )

        # DROPPED NULL VALUES
        df.dropna(inplace=True)
        # REMOVING '@' FROM TAILNUM
        df = df[~df.TAILNUM.str.contains('@')]
        # REMOVING AIRLINECODE
        pd.options.mode.chained_assignment = None
        df['AIRLINENAME'] = df['AIRLINENAME'].str[:-4]
        df['AIRLINENAME'] = df['AIRLINENAME'].apply(
                                            lambda x: x.replace(
                                                ': HP (Merged with US Airways 9/05.Stopped reporting 10/',
                                                '')
                                            )

        df['AIRLINENAME'] = df['AIRLINENAME'].apply(lambda x: x.replace('/', ''))
        # REMOVING CONCATENATED CITY AND STATE
        df['ORIGAIRPORTNAME'] = df['ORIGAIRPORTNAME'].str.split(':', n=1).str.get(-1)
        df['DESTAIRPORTNAME'] = df['DESTAIRPORTNAME'].str.split(':', n=1).str.get(-1)
        return df

    df = wrap(df)

    # CREATING LIST FOR DISTANCEGROUP VALUES
    grouplst = list(df['DISTANCEGROUP'])
    lst = []
    label = []
    bins = [0] + [n for n in range(101, 5101, 100)]
    for i in grouplst:
        lst.append(int(i))

    # CREATING GROUP INCREMENTS AND ADDING ' miles'
    for i in bins[:-1]:
        if i == 0:
            nlst = str(i) + '-' + str(100) + ' miles'
        else:
            nlst = str(i) + '-' + (str(i + 99)) + ' miles'
        label.append(str(nlst))

    df['DISTANCEGROUP'] = pd.cut(
        x=lst,
        bins=bins,
        labels=label
    )
    # CREATING DEPDELAYGT15 COLUMN
    dvalueslst = list(df['DEPDELAY'])
    dlst = []
    delaylst = []
    for i in dvalueslst:
        dlst.append(int(i))

    # REPLACING NA VALUES WITH WITH 0's
    for i in dlst:
        if i > 15:
            delaylst.append(1)
        else:
            delaylst.append(0)
    df['DEPDELAYGT15'] = delaylst

    # CLEANING MISSING DATA WITH TIME COLUMNS
    def new_time(df, column):
        rdf = df[column].replace(2400, 0000)
        lst = list(rdf)
        vals = []
        fvals = []
        for i in lst:
            vals.append(int(i))
        for i in vals:
            nt = str(i)
            if nt == '2400':
                nt = '0000'
            chars = (4 - len(nt)) * '0'
            nt1 = chars + nt
            nt2 = nt1[:2] + ":" + nt1[2:]
            fvals.append(nt2)
        df[column] = fvals

    cols = 'CRSDEPTIME', 'DEPTIME', 'WHEELSOFF', 'WHEELSON', 'CRSARRTIME', 'ARRTIME'
    for i in cols:
        new_time(df, i)

    # CONVERTING DATATYPES FOR INT COLUMNS
    intcols = ['DEPDELAY', 'ARRDELAY', 'CRSELAPSEDTIME',
               'ACTUALELAPSEDTIME', 'TAXIIN', 'TAXIOUT']
    for col in intcols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # CREATING NEXTDAYARR
    df['NEXTDAYARR'] = np.where(df['ARRTIME'] < df['DEPTIME'], 1, 0)

    return df


"""
NOTES ON DF:
    - TAILNUM has @ symbols in this columns
    - 1073206 NA values
    - Columns CANCELLED and DIVERTED are all False
    - Time columns cause some issues with Timezone stamp
"""
