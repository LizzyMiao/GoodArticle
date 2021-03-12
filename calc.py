# Python code demonstrate creating
# pandas DataFrame with indexed by  

# DataFrame using arrays. 
import pandas as pd
import math


# # print the data
# print(df)
#
# print(df.loc[:, ['marks']])

def normalize_value(x):
        if x is None:
                return None

        target_value = 0.0
        remove_dollor = x
        if type(x) == str and "$" in x:
            remove_dollor = x[1:]

        if type(remove_dollor) == str:
            remove_dollor.replace(' ', '')
            remove_dollor.replace('"','')
            remove_dollor.replace('\'', '')
            if not remove_dollor:
                    return 0

            target_value = float(remove_dollor.replace(',', ''))

        return target_value



def normalize_dataframe(dataframe_input):
        for column_name in dataframe_input.columns:
                if column_name != 'time' and column_name != 'year':
                        dataframe_input[column_name] = dataframe_input[column_name].apply(lambda x: normalize_value(x))

def normalize_column_as_numerator(dataframe_input, column_name):
        dataframe_input[column_name] = dataframe_input[column_name].apply(
                lambda x: 0 if x == 0 or not x or x == ' ' or x == '$0' else x)


def multiple(x, y):
        if x is None or y is None:
                return None

        x_float = x
        y_float = y

        return x_float * y_float


def divid(x, y):
        if x is None or y is None:
                return None

        if y == 0:
                return 0

        x_float = x
        y_float = y

        if type(x) == str:
                x_float = float(x.replace(',',''))

        if type(y) == str:
                y_float = float(y.replace(',',''))

        return x_float/y_float


def add(x, y):
        if x is None or y is None:
                return None

        x_float = x
        y_float = y

        return x_float + y_float


def minus(x, y):
        if x is None or y is None:
                return None
        x_float = x
        y_float = y

        return x_float - y_float

def log_function(x):
        if x == 0:
                return 0
        return math.log(x)

def get_all_financial_data():
    df = pd.read_csv('sp100_2-left.csv', index_col=False, sep='\t', header=None)
    #df = pd.read_csv('bankrupted.csv', index_col=False, sep='\t', header=None)
    company = df.loc[:, [0, 1]]

    for row in company.values:
        company_code = row[0]
        print("Generating index content for " + company_code)
        basic_process(company_code)

def constructX21(origianl_dataframe, target_dataframe):
        revenue_df = origianl_dataframe[['revenue', 'year']]
        year_revenue = revenue_df.groupby(['year']).sum()
        year_revenue.columns = ['year_revenue']
        year_revenue['shifted_year_revenue'] = year_revenue['year_revenue'].shift(1)
        year_revenue['X21'] = year_revenue[['year_revenue', 'shifted_year_revenue']].apply(lambda x: divid(*x), axis=1)

        target_value = year_revenue[['X21']]
        merged_dataframe = origianl_dataframe.merge(target_value, on='year')
        target_dataframe['X21'] = merged_dataframe[['X21']]


def constructX24(original_dataframe, target_dataframe):
        inputs_df = original_dataframe[['gross-profit', 'total-assets', 'year']]
        year_total = inputs_df.groupby(['year']).sum()
        year_total['shifted-year-gross-profit-1'] = year_total['gross-profit'].shift(1)
        year_total['shifted-year-gross-profit-2'] = year_total['gross-profit'].shift(2)
        year_total['X24'] = year_total[['gross-profit', 'shifted-year-gross-profit-1', 'shifted-year-gross-profit-2', 'total-assets']].apply(
                lambda x: divid(add(add(x['gross-profit'], x['shifted-year-gross-profit-1']), x['shifted-year-gross-profit-2']), x['total-assets']), axis=1
        )

        target_value = year_total[['X24']]
        merged_dataframe = original_dataframe.merge(target_value, on='year')

        target_dataframe['X24'] = merged_dataframe[['X24']]



def basic_process(company_code):

        if company_code == '':
                print("lalala")

        basic_financial_df = pd.read_csv("./sp_100_company_financial_info/{0}_basic_financial_year.csv".format(company_code),
                                         index_col=False, sep=',', header=None)
        basic_financial_df = pd.DataFrame(basic_financial_df.values[1:], columns=basic_financial_df.iloc[0])
        normalize_dataframe(basic_financial_df)

        basic_financial_df_2 = pd.read_csv("./sp_100_company_financial_info/{0}_basic_financial.csv".format(company_code), index_col=False,
                                           sep=',', header=None)
        basic_financial_df_2 = pd.DataFrame(basic_financial_df_2.values[1:], columns=basic_financial_df_2.iloc[0])
        normalize_dataframe(basic_financial_df_2)


        basic_financial_df_2['year'] = basic_financial_df_2['time'].apply(lambda x: x[:4])

        merged_df_origianl = basic_financial_df_2.merge(basic_financial_df, on='year')
        merged_df = basic_financial_df_2.merge(basic_financial_df, on='year')
        merged_df['net-income-loss'] = merged_df[['net-income-loss']].apply(lambda x: x/4.0, axis=1)
        merged_df['total-depreciation-amortization-cash-flow'] = merged_df[['total-depreciation-amortization-cash-flow']].apply(lambda x: x/4.0, axis=1)

        result_df = basic_financial_df_2.loc[:, ['time']]

        normalize_column_as_numerator(merged_df, 'total-assets')
        normalize_column_as_numerator(merged_df, 'net-income-loss')
        normalize_column_as_numerator(merged_df, 'total-liabilities')

        result_df['X1'] = merged_df[['net-income-loss', 'total-assets']].apply(lambda x: divid(*x), axis=1)
        result_df['X2'] = merged_df[['total-liabilities', 'total-assets']].apply(lambda x: divid(*x), axis=1)

        normalize_column_as_numerator(merged_df, 'total-current-assets')
        normalize_column_as_numerator(merged_df, 'total-current-liabilities')
        result_df['X4'] = merged_df[['total-current-assets', 'total-current-liabilities']].apply(lambda x: minus(*x), axis=1)
        result_df['X3'] = merged_df['total-assets']
        result_df['X3'] = result_df[['X4', 'X3']].apply(lambda x: divid(*x), axis=1)

        normalize_column_as_numerator(merged_df, 'ebit')
        result_df['X7'] = merged_df[['ebit', 'total-assets']].apply(lambda x: divid(*x), axis=1)

        normalize_column_as_numerator(merged_df, 'total-liabilities')
        normalize_column_as_numerator(merged_df, 'book-value-per-share')
        result_df['X8'] = merged_df[['book-value-per-share', 'total-liabilities']].apply(lambda x: divid(*x), axis=1)

        normalize_column_as_numerator(merged_df, 'revenue')
        result_df['X9'] = merged_df[['revenue', 'total-assets']].apply(lambda x: divid(*x), axis=1)

        normalize_column_as_numerator(merged_df, 'total-share-holder-equity')
        result_df['X10'] = merged_df[['total-share-holder-equity', 'total-assets']].apply(lambda x: divid(*x), axis=1)

        normalize_column_as_numerator(merged_df, 'gross-profit')
        result_df['X12'] = merged_df[['gross-profit', 'total-current-liabilities']].apply(lambda x: divid(*x), axis=1)

        #x.col_1, x.col_2
        normalize_column_as_numerator(merged_df, 'total-depreciation-amortization-cash-flow')
        result_df['X13'] = merged_df[['gross-profit', 'total-depreciation-amortization-cash-flow', 'revenue']].apply(lambda x: divid(add(x['gross-profit'], x['total-depreciation-amortization-cash-flow']), x['revenue']), axis=1)

        result_df['X15'] = merged_df[['total-liabilities', 'gross-profit', 'total-depreciation-amortization-cash-flow']].\
                apply(lambda x: divid(x['total-liabilities'] * 90, add(x['gross-profit'], x['total-depreciation-amortization-cash-flow'])), axis=1)

        result_df['X16'] = merged_df[['gross-profit', 'total-depreciation-amortization-cash-flow', 'total-liabilities']].apply(lambda x: divid(add(x['gross-profit'], x['total-depreciation-amortization-cash-flow']), x['total-liabilities']), axis=1)

        result_df['X17'] = merged_df[['total-assets', 'total-liabilities']].apply(lambda x: divid(*x), axis=1)

        result_df['X18'] = merged_df[['gross-profit', 'total-assets']].apply(lambda x: divid(*x), axis=1)

        result_df['X19'] = merged_df[['gross-profit', 'revenue']].apply(lambda x: divid(*x), axis=1)

        normalize_column_as_numerator(merged_df, 'inventory')
        result_df['X20'] = merged_df[['inventory', 'revenue']].apply(lambda x: divid(x['inventory']*90, x['revenue']), axis=1)

        normalize_column_as_numerator(merged_df, 'operating-income')
        result_df['X22'] = merged_df[['operating-income', 'total-assets']].apply(lambda x: divid(*x), axis=1)

        result_df['X23'] = merged_df[['net-income-loss', 'revenue']].apply(lambda x: divid(*x), axis=1)

        result_df['X26'] = merged_df[['net-income-loss', 'total-depreciation-amortization-cash-flow', 'total-liabilities']].apply(lambda x: divid(add(x['net-income-loss'], x['total-depreciation-amortization-cash-flow']), x['total-liabilities']),  axis=1)

        normalize_column_as_numerator(merged_df, 'net-property-plant-equipment')
        result_df['X28'] = merged_df[['total-current-assets', 'total-current-liabilities', 'net-property-plant-equipment']].apply(lambda x: divid(minus(x['total-current-assets'], x['total-current-liabilities']), x['net-property-plant-equipment']), axis=1)

        result_df['X29'] = merged_df['total-assets'].apply(lambda x: log_function(x))

        normalize_column_as_numerator(merged_df, 'cash-on-hand')
        result_df['X30'] = merged_df[['total-liabilities', 'cash-on-hand', 'revenue']].apply(lambda x: divid(minus(x['total-liabilities'], x['cash-on-hand']), x['revenue']), axis=1)

        normalize_column_as_numerator(merged_df, 'cost-goods-sold')
        result_df['X32'] = merged_df[['total-current-liabilities', 'cost-goods-sold']].apply(lambda x: divid(x['total-current-liabilities'] * 90, x['cost-goods-sold']), axis=1)

        result_df['X33'] = merged_df[['operating-expenses', 'total-current-liabilities']].apply(lambda x: divid(*x), axis=1)

        result_df['X34'] = merged_df[['operating-expenses', 'total-liabilities']].apply(lambda x: divid(*x), axis=1)

        normalize_column_as_numerator(merged_df, 'total-long-term-liabilities')
        result_df['X37'] = merged_df[['total-current-assets', 'inventory', 'total-long-term-liabilities']].apply(lambda x: divid(minus(x['total-current-assets'], x['inventory']), x['total-long-term-liabilities']), axis=1)

        normalize_column_as_numerator(merged_df, 'receivables-total')
        result_df['X40'] = merged_df[['total-current-assets', 'inventory', 'receivables-total', 'total-current-liabilities']].\
                apply(lambda x: divid(minus(minus(x['total-current-assets'], x['inventory']), x['receivables-total']), x['total-current-liabilities']), axis=1)

        result_df['X41'] = merged_df[['total-liabilities', 'operating-income', 'total-depreciation-amortization-cash-flow']].apply(
                lambda x: divid(x['total-liabilities'], add(x['operating-income'], x['total-depreciation-amortization-cash-flow']) * (3/90)), axis=1
        )

        result_df['X42'] = merged_df[['operating-income', 'revenue']].apply(lambda x: divid(*x), axis=1)

        result_df['X44'] = merged_df[['receivables-total', 'revenue']].apply(lambda x: divid(*x)*90, axis=1)

        result_df['X45'] = merged_df[['net-income-loss', 'inventory']].apply(lambda x: divid(*x), axis=1)

        result_df['X46'] = merged_df[['total-current-assets', 'inventory', 'total-long-term-liabilities']].apply(lambda x: divid(minus(x['total-current-assets'], x['inventory']), x['total-long-term-liabilities']), axis=1)
        
        result_df['X47'] = merged_df[['inventory', 'cost-goods-sold']].apply(lambda x: divid(*x)*90, axis=1)

        normalize_column_as_numerator(merged_df, 'ebitda')
        result_df['X48'] = merged_df[['ebitda', 'total-assets']].apply(lambda x: divid(*x), axis=1)

        result_df['X49'] = merged_df[['ebitda', 'revenue']].apply(lambda x: divid(*x), axis=1)

        result_df['X50'] = merged_df[['total-current-assets', 'total-liabilities']].apply(lambda x: divid(*x), axis=1)

        result_df['X51'] = merged_df[['total-current-liabilities', 'total-assets']].apply(lambda x: divid(*x), axis=1)

        result_df['X53'] = merged_df[['total-share-holder-equity', 'net-property-plant-equipment']].apply(lambda x: divid(*x), axis=1)

        result_df['X55'] = merged_df[['total-current-assets', 'total-current-liabilities']].apply(lambda x: divid(*x), axis=1)

        result_df['X56'] = merged_df[['revenue', 'cost-goods-sold']].apply(lambda x: divid(minus(x['revenue'], x['cost-goods-sold']), x['revenue']), axis=1)

        result_df['X57'] = merged_df[['total-current-assets', 'inventory', 'total-current-liabilities', 'revenue', 'gross-profit', 'total-depreciation-amortization-cash-flow']].apply(
                lambda x: divid(minus(minus(x['total-current-assets'], x['inventory']), x['total-current-liabilities']),
                                minus(minus(x['revenue'], x['gross-profit']), x['total-depreciation-amortization-cash-flow'])),
                axis=1
        )

        result_df['X59'] = merged_df[['total-long-term-liabilities', 'total-share-holder-equity']].apply(lambda x: divid(*x), axis=1)

        result_df['X60'] = merged_df[['revenue', 'inventory']].apply(lambda x: divid(*x), axis=1)

        result_df['X61'] = merged_df[['revenue', 'receivables-total']].apply(lambda x: divid(*x), axis=1)

        result_df['X62'] = merged_df[['total-current-liabilities', 'revenue']].apply(lambda x: divid(*x) * 90, axis=1)

        result_df['X63'] = merged_df[['revenue', 'total-current-liabilities']].apply(lambda x: divid(*x), axis=1)

        result_df['X64'] = merged_df[['revenue', 'net-property-plant-equipment']].apply(lambda x: divid(*x), axis=1)

        constructX21(merged_df, result_df)

        constructX24(merged_df, result_df)

        result_df.to_csv(
                '.\\sp_100_financial_index_result\\{0}_result.csv'.format(company_code))

if __name__ == '__main__':
    get_all_financial_data()
