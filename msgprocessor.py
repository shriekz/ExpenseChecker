from datetime import datetime
import referencedata as refd
import pandas as pd
import numpy as np


# load xml to dataframe
def getAcctNumIfAny(smstext):
    acct_num = [acct for acct in refd.acct_dict if acct in smstext]

    return acct_num[0] if len(acct_num) else ''


# this converts the XML to a data frame
def loadXMLtoDF():
    cols_to_use = ['address', 'body', 'readable_date', 'contact_name']
    df = pd.read_xml(refd.filename, xpath=".//sms")
    df1 = df[cols_to_use].copy()
    df1['category'] = 'uncategorized'
    df1['account_num'] = 'X'
    df1['month'] = 0
    df1['year'] = 0
    df1['Merchant'] = 'M'
    df1['IsDebit'] = True
    df1['Amount'] = 0.0

    for idx, sms in df1.iterrows():
        date_time_obj = datetime.strptime(sms['readable_date'], '%b %d, %Y %I:%M:%S %p')
        acct_num = getAcctNumIfAny(sms['body'])
        df1.at[idx, 'account_num'] = acct_num
        df1.at[idx, 'month'] = date_time_obj.month
        df1.at[idx, 'year'] = date_time_obj.year
        if df1.at[idx, 'account_num']:
            # get a function pointer for each account number that holds the
            # function that is used to process the string for the account.
            fp = getattr(refd, refd.acct_dict[acct_num])

            # Interesting way of calling a function using the function pointer
            # it returns multiple values.
            isProcess, isDebit, Amt, Category = fp(sms['body'], sms['address'])
            if isProcess:
                df1.at[idx, 'IsDebit'], df1.at[idx, 'Amount'] = isDebit, Amt
                df1.at[idx, 'category'] = Category

    return df1


# process all sms data
def aggregateStatistics(df):
    # group by all values by account num, year, month and get sum
    gp = df.groupby(['account_num', 'IsDebit', 'year', 'month', 'category']).agg(np.sum)
    gp.to_csv('temp.csv')


def processAccount():
    #   Load the XML to DF
    df = loadXMLtoDF()

    #   Filter DF for acct_number add acct_number to DF col
    aggregateStatistics(df)

    # Dump df to file
    df.to_csv('temp1.csv')
    #   Get date and amount and load them into DF


if __name__ == '__main__':
    processAccount()
