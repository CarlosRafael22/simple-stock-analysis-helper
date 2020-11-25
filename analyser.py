import pandas as pd
from typing import Dict, List
from extractor import YubbExtractor, StockIndicatorsDict


class StringToFloatParser:
    ''' Responsible to parse string values to float '''

    @staticmethod
    def convert_dotted_value_to_float_string(value_string: str) -> str:
        ''' Used to convert number value strings to strings better to be converted to float. 1.207.03	-> 1207.03'''
        if type(value_string) == str:
            splits = value_string.split('.')
            try:
                new_value_string = '.'.join(splits) if len(splits) <= 2 else splits[0]+''+splits[1]+'.'+splits[2]
            except TypeError:
                import pdb
                pdb.set_trace()
        else:
            import pdb; pdb.set_trace()
        return new_value_string

    @staticmethod
    def is_currency_value(value: str) -> bool:
        return 'R$' in value

    @staticmethod
    def get_multiply_factor_to_millions_unit(value: str) -> float:
        ''' Receives a currency string and returns the multiply factor to millions according to the mil, milhões, bilhões, trilhões found on the string '''
        multiply_factor = {
            'milhões': 1,
            'bilhões': 1000,
            'trilhões': 1000000,
            'mil': 0.001
        }
        # Even if we cant find any of the strings on multiply_factor then we set the standard to 1
        factor = 1
        for key in multiply_factor.keys():
            if key in value:
                factor = multiply_factor[key]
                break
        return factor

    @staticmethod
    def parse_float_string_to_float_number(value_string: str):
        import re
        number = value_string
        if value_string and type(value_string) == str:
            try:
                numbers = re.findall(r"[-+]?\d*\.\d+|\d+", value_string)
                number = float(numbers[0])
            except:
                import pdb
                pdb.set_trace()

        if number and StringToFloatParser.is_currency_value(value_string):
            factor = StringToFloatParser.get_multiply_factor_to_millions_unit(value_string)
            number = number * factor
        
        return number


class DataFrameParser:
    ''' Responsible for parsing the cells contents of a DataFrame according to its needs '''

    @staticmethod
    def get_columns_to_convert_to_float(dataframe: pd.DataFrame) -> List[str]:
        ''' Get the columns with number values formatted as string. Initially we would only remove the first and last columns in the list of columns in this dataframe '''
        # ['Ação', 'Valor atual', 'Variação atual', 'Dividend Yield', 'P / L', 'P / VPA', 'P / Ativos', 'Margem Bruta', 'Margem EBIT', 'Margem Líquida', 'P / EBIT', 'EV / EBIT', 'Dívida Líquida / EBIT', 'Dívida Líq. / Patrimônio Líq.',
        # 'PSR', 'Preço / Capital de Giro', 'Preço / Ativo Circ. Líq.', 'ROE', 'ROIC', 'ROA', 'Liquidez Corrente', 'Patrimônio / Ativos', 'Passivos / Ativos', 'Giro do ativo', 'CAGR Receitas 5 anos', 'CAGR Lucros 5 anos',
        # 'Liquidez média diária', 'Patrimônio Líquido', 'Ativos', 'Ativo Circulante', 'Valor de Mercado', 'Dívida Bruta', 'Caixa Livre', 'Dívida Líquida', 'Valor de Firma (EV)', 'Total de Papéis', 'Free Float', 'Segmento de Listagem']
        return list(dataframe.columns)[1:-1]

    @staticmethod
    def replace_nan_with_0_string(dataframe: pd.DataFrame) -> pd.DataFrame:
        import numpy as np
        return dataframe.replace(np.nan, '0')

    @staticmethod
    def replace_comma_to_dot_on_columns(dataframe: pd.DataFrame) -> pd.DataFrame:
        ''' Replaces commas on number strings to dots. Later we handle these strings better to convert to float '''
        # '1.207,03' -> '1.207.03'
        columns_to_convert = DataFrameParser.get_columns_to_convert_to_float(dataframe)
        for column in columns_to_convert:
          dataframe[column] = dataframe[column].str.replace(',','.')
        return dataframe

    @staticmethod
    def convert_columns_dotted_values_to_float_strings(dataframe: pd.DataFrame) -> pd.DataFrame:
        ''' Convert all cell values to strings better to be converted to float for all columns that need to have float values '''
        # Now, to fix errors like -13.548.48% to -13,548.48% on specific columns we call convert_values_to_usa_str
        columns_to_convert = DataFrameParser.get_columns_to_convert_to_float(dataframe)
        for column in columns_to_convert:
            dataframe[column] = dataframe[column].apply(StringToFloatParser.convert_dotted_value_to_float_string)
        return dataframe

    @staticmethod
    def convert_columns_float_strings_to_floats(dataframe: pd.DataFrame) -> pd.DataFrame:
        ''' Converts all cell values which are float strings now to float for all columns that need to have float values '''
        columns_to_convert = DataFrameParser.get_columns_to_convert_to_float(dataframe)

        for column in columns_to_convert:
            dataframe[column] = dataframe[column].apply(StringToFloatParser.parse_float_string_to_float_number)
        return dataframe

    @staticmethod
    def parse_columns_to_float(dataframe: pd.DataFrame) -> pd.DataFrame:
        ''' Parses all cell values from columns that need to be converted to floats '''
        handled_nan_dataframe = DataFrameParser.replace_nan_with_0_string(dataframe)
        numbers_with_dots_dataframe = DataFrameParser.replace_comma_to_dot_on_columns(handled_nan_dataframe)
        float_strings_dataframe = DataFrameParser.convert_columns_dotted_values_to_float_strings(numbers_with_dots_dataframe)
        float_values_dataframe = DataFrameParser.convert_columns_float_strings_to_floats(float_strings_dataframe)
        return float_values_dataframe

    @staticmethod
    def change_columns_names_for_rows_to_be_numbers(dataframe: pd.DataFrame) -> pd.DataFrame:
        new_dataframe = dataframe.rename({
            'Margem Bruta': 'Margem Bruta (%)',
            'Margem EBIT': 'Margem EBIT (%)',
            'Margem Líquida': 'Margem Líquida (%)',
            'ROE': 'ROE (%)',
            'ROIC': 'ROIC (%)',
            'ROA': 'ROA (%)',
            'CAGR Receitas 5 anos': 'CAGR Receitas 5 anos (%)',
            'CAGR Lucros 5 anos': 'CAGR Lucros 5 anos (%)',
            'Liquidez média diária': 'Liquidez média diária (R$ milhões)',
            'Patrimônio Líquido': 'Patrimônio Líquido (R$ milhões)',
            'Ativos': 'Ativos (R$ milhões)',
            'Ativo Circulante': 'Ativo Circulante (R$ milhões)',
            'Valor de Mercado': 'Valor de Mercado (R$ milhões)',
            'Dívida Bruta': 'Dívida Bruta (R$ milhões)',
            'Caixa Livre': 'Caixa Livre (R$ milhões)',
            'Dívida Líquida': 'Dívida Líquida (R$ milhões)',
            'Valor de Firma (EV)': 'Valor de Firma (EV) (R$ milhões)',
            'Total de Papéis': 'Total de Papéis (R$ milhões)',
            'Free Float': 'Free Float (%)'
        }, axis='columns')
        return new_dataframe


class Analyser:
    dataframe: pd.DataFrame = None
    main_indicators = ['Ação', 'P / L', 'P / VPA', 'Margem Bruta (%)', 'Margem EBIT (%)', 'Margem Líquida (%)', 'ROE (%)', 'ROIC (%)',
        'ROA (%)', 'CAGR Receitas 5 anos (%)', 'CAGR Lucros 5 anos (%)', 'Patrimônio Líquido (R$ milhões)', 'Dívida Bruta (R$ milhões)', 'Valor de Firma (EV) (R$ milhões)']

    @classmethod
    def create_dataframe_dict_from_indicators_dict(cls, indicators_dict: StockIndicatorsDict) -> Dict[str, List[str]]:
        ''' Returns a dictionary with the column name and each value from the indicators_dict for it to be used to create a DataFrame '''
        data_frame_dict = {}

        for indicators in indicators_dict.values():
            print(indicators)
            # Only consider it if it has all the fields
            if len(indicators) > 1:
                for (indicator_name, indicator_value) in indicators:
                    if data_frame_dict.get(indicator_name, None) is not None:
                        data_frame_dict[indicator_name].append(indicator_value)
                    else:
                        data_frame_dict[indicator_name] = [indicator_value]

        return data_frame_dict

    @classmethod
    def get_dataframe_indicators_for_stocks(cls, stocks: List[str]) -> pd.DataFrame:
        indicators_dict = YubbExtractor.get_indicators_from_stocks(stocks)

        data_frame = cls.create_dataframe_dict_from_indicators_dict(indicators_dict)
        df = pd.DataFrame(data_frame)
        # df.to_csv('dataframe.csv', index=False)
        return df

    def set_dataframe(self, dataframe: pd.DataFrame) -> None:
        ''' Save this dataframe to this instance of the Analyser '''
        self.dataframe = dataframe

    @classmethod
    def parse_dataframe(cls, dataframe: pd.DataFrame) -> pd.DataFrame:
        ''' Parses the cells and columns titles of the dataframe for it to be better to handle and extract data '''
        dataframe_with_floats = DataFrameParser.parse_columns_to_float(dataframe)
        changed_columns_dataframe = DataFrameParser.change_columns_names_for_rows_to_be_numbers(dataframe_with_floats)
        return changed_columns_dataframe
