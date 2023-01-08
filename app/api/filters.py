from os import path
import sys
import collections
import pandas as pd

base_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
sys.path.append(base_dir)
from app.database.crud import get_df
from app.common.consts import Quarters
from app.database.models import Accounts, Stocks, Amounts, Ratios

_quarters = Quarters().quarters
class Filter:
    def __init__(self):
        self.init_tbl()
        self.init_filter()
        
    def init_filter(self):
        self.init_quarters()
        self.init_amounts()
        self.init_ratios()
        self.init_codes()
        
    def init_tbl(self):
        amounts_col = ["stock_code", "account_nm_eng"] + list(_quarters.values())
        self.dart_amounts = get_df(model=Amounts, columns=amounts_col)
        
        ratios_col = ["stock_code", "ratio"] + list(_quarters.values())
        self.dart_ratios = get_df(model=Ratios, columns=ratios_col)
        
    def init_quarters(self):
        # ["Q202211012", "Q202211013", "Q202111011", ...]
        self.quarters = []
        
    def init_amounts(self):
        # {account(str): [min_amount(int or None), max_maount(int or None)]}
        self.amounts = {}
    
    def init_ratios(self):
        # {ratio(str): [min_ratio(float or None), max_ratio(float or None)]}
        self.ratios = {}
        
    def init_codes(self):
        self.codes_amount = None
        self.codes_ratio = None
        self.codes_filtered = []

    def filter_amounts(self):
        
        columns = ['stock_code'] + self.quarters
        stock_codes = []
        dart_amounts_filtered = self.dart_amounts.copy()
        for account in self.amounts.keys():

            _amount = self.amounts[account]
            min_amount = _amount[0]
            max_amount = _amount[1]
            
            df_amounts_acc = dart_amounts_filtered.loc[dart_amounts_filtered.account_nm_eng==account, columns].reset_index(drop=True)

            for quarter in self.quarters:
                if min_amount is None:
                    stock_codes = df_amounts_acc.loc[df_amounts_acc[quarter]<=max_amount, 'stock_code'].tolist()
                elif max_amount is None:
                    stock_codes = df_amounts_acc.loc[df_amounts_acc[quarter]>=min_amount, 'stock_code'].tolist()
                else:    
                    stock_codes = df_amounts_acc.loc[(df_amounts_acc[quarter]>=min_amount) & (df_amounts_acc[quarter]<=max_amount), 'stock_code'].tolist()    
                
                df_amounts_acc = df_amounts_acc[df_amounts_acc.stock_code.isin(stock_codes)].reset_index(drop=True)
            
            print(f'{account}: {len(stock_codes)}')
            dart_amounts_filtered = dart_amounts_filtered[dart_amounts_filtered.stock_code.isin(stock_codes)].reset_index(drop=True)
            
        self.codes_amount = dart_amounts_filtered.stock_code.unique().tolist()
        print(f'Filtered stock codes (amounts): {len(self.codes_amount)}')
    
    def filter_ratios(self):
        
        columns = ['stock_code'] + self.quarters
        stock_codes = []
        dart_ratios_filtered = self.dart_ratios.copy()
        for ratio in self.ratios.keys():
            
            _ratio = self.ratios[ratio]
            min_ratio = _ratio[0]
            max_ratio = _ratio[1]
            
            df_ratios_acc = dart_ratios_filtered.loc[dart_ratios_filtered['ratio']==ratio, columns].reset_index(drop=True)
            for quarter in self.quarters:
                if min_ratio is None:
                    stock_codes = df_ratios_acc.loc[df_ratios_acc[quarter]<=max_ratio, 'stock_code'].tolist()
                elif max_ratio is None:
                    stock_codes = df_ratios_acc.loc[df_ratios_acc[quarter]>=min_ratio, 'stock_code'].tolist()
                else:    
                    stock_codes = df_ratios_acc.loc[(df_ratios_acc[quarter]>=min_ratio) & (df_ratios_acc[quarter]<=max_ratio), 'stock_code'].tolist()    
                
                df_ratios_acc = df_ratios_acc[df_ratios_acc.stock_code.isin(stock_codes)].reset_index(drop=True)

            print(f'{ratio}: {len(stock_codes)}')
            dart_ratios_filtered = dart_ratios_filtered[dart_ratios_filtered.stock_code.isin(stock_codes)].reset_index(drop=True)
            
        self.codes_ratio = dart_ratios_filtered.stock_code.unique().tolist()
        print(f'Filtered stock codes (ratios): {len(self.codes_ratio)}')
        
    def intersect(self):
        ''' get intersect group '''
        
        if self.codes_amount is None and self.codes_ratio is None:
            # require msg box
            self.codes_filtered = []
        elif self.codes_amount is None:
            self.codes_filtered = self.codes_ratio
        elif self.codes_ratio is None:
            self.codes_filtered = self.codes_amount
        elif len(self.codes_amount) == 0 or len(self.codes_ratio) == 0:
            self.codes_filtered = []
        else:
            stock_codes = self.codes_amount + self.codes_ratio
            # get intersection 
            self.codes_filtered = [item for item, count in collections.Counter(stock_codes).items() if count == 2]
        print(f'Quarters: {self.quarters}\nFiltered stock codes (intersect): {len(self.codes_filtered)}')
    
    def conv_str(self, string, kind):
        status = True
        flt = None
        try:
            if kind == "amount":
                flt = float(string) * 1e8
            elif kind == "ratio":
                flt = float(string)
            else:
               raise ValueError("Wrong kind (amount or ratio)")
        except ValueError:
            status = False
        return flt, status
    
    def preprocessor(self, min_amount, max_amount, kind):
        ''' min max amount preprocess '''
        
        min_amount, max_amount = min_amount.strip(), max_amount.strip()
        if min_amount == '' and max_amount == '':
            min_amount, max_amount = None, None
            status = False
        elif min_amount == '':
            min_amount = None
            max_amount, status = self.conv_str(max_amount, kind)
        elif max_amount == '':
            max_amount = None
            min_amount, status = self.conv_str(min_amount, kind)
        else:
            min_amount, status = self.conv_str(min_amount, kind)
            max_amount, status = self.conv_str(max_amount, kind)
            try:
                if max_amount > min_amount:
                    status = True
                else:
                    pass
            except TypeError:
                status = False
        
        return min_amount, max_amount, status