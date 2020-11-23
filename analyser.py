import pandas as pd
from typing import Dict, List
from extractor import YubbExtractor, StockIndicatorsDict


class Analyser:

    @classmethod
    def create_dataframe_dict_from_indicators_dict(cls, indicators_dict: StockIndicatorsDict) -> Dict[str, List[str]]:
        ''' Returns a dictionary with the column name and each value from the indicators_dict for it to be used to create a DataFrame '''
        data_frame = {}

        for indicators in indicators_dict.values():
            print(indicators)
            # Only consider it if it has all the fields
            if len(indicators) > 1:
                for (indicator_name, indicator_value) in indicators:
                    if data_frame.get(indicator_name, None) is not None:
                        data_frame[indicator_name].append(indicator_value)
                    else:
                        data_frame[indicator_name] = [indicator_value]

        return data_frame

    @classmethod
    def get_dataframe_indicators_for_stocks(cls, stocks: List[str]) -> pd.DataFrame:
        Extractor = YubbExtractor()
        indicators_dict = Extractor.get_indicators_from_stocks(stocks)

        data_frame = cls.create_dataframe_dict_from_indicators_dict(indicators_dict)

        df = pd.DataFrame(data_frame)
        # df.to_csv('dataframe.csv', index=False)
        return df
