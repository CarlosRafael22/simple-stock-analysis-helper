import requests
from bs4 import BeautifulSoup
from typing import Tuple, List, Dict

# Defining Types to be easier to type hint methods
IndicatorTupleList = List[Tuple[str, str]]
StockIndicatorsDict = Dict[str, List[Tuple[str, str]]]

class YubbExtractor:
    @staticmethod
    def reorder_tuple_list_with_first_element_as(tuple_key: str, tuple_list: IndicatorTupleList) -> IndicatorTupleList:
        ''' Order the list with tuples setting the first element of this list as the tuple_key tuple and all the elements before it put in the last positions '''
        keys = [elem[0] for elem in tuple_list]
        try:
            tuple_key_position = keys.index(tuple_key)
        except ValueError:
            return tuple_list
        before_threshold_list = tuple_list[:tuple_key_position]
        first_list = tuple_list[tuple_key_position:]
        return first_list + before_threshold_list

    @classmethod
    def get_main_indicators_from_page(cls, soup: BeautifulSoup) -> IndicatorTupleList:
        indicators = soup.find_all('div', class_='card investmentDetails__card')
        indicator_tuples = [(indicator.find('dt', class_='investmentDetails__label').get_text(), indicator.find('dd', class_='investmentDetails__value').get_text()) for indicator in indicators]
        # Reorder elements for the most important items be first
        ordered_indicator_tuples = cls.reorder_tuple_list_with_first_element_as('Dividend Yield', indicator_tuples)
        return ordered_indicator_tuples

    @classmethod
    def get_stock_summaries_from_page(cls, soup: BeautifulSoup) -> IndicatorTupleList:
        summary_infos = soup.find_all('div', class_='investmentSummary__label')
        summary_infos = [info.get_text() for info in summary_infos]

        summary_values = soup.find_all('div', class_='investmentSummary__value')
        summary_values = [value.get_text() for value in summary_values]

        ziped_summary = zip(summary_infos, summary_values)
        # tuple(ziped_summary)
        stock_summaries = list(ziped_summary)
        return stock_summaries

    @classmethod
    def get_stock_name_tuple(cls, soup: BeautifulSoup) -> Tuple[str, str]:
        h1_name = soup.find('h1', class_='investmentPageHeader__title')
        stock_name = h1_name.get_text() if h1_name else None
        print('Nome - ', stock_name)
        name_tuple = ('Ação', stock_name)
        return name_tuple

    @classmethod
    def get_stock_section_info(cls, soup: BeautifulSoup) -> Tuple[str, str]:
        cards = soup.select('div.card.shadow-sm')
        # import pdb
        # pdb.set_trace()
        section_info = [(card.dt.text, card.dd.text) for card in cards]
        return section_info

    @classmethod
    def get_stock_indicators(cls, stock_name: str) -> IndicatorTupleList:
        print('Vai pegar da acao: ', stock_name)
        page = requests.get(f'https://yubb.com.br/investimentos/acoes/{stock_name}')
        soup = BeautifulSoup(page.content, 'html.parser')

        indicator_tuples = cls.get_main_indicators_from_page(soup)
        stock_summaries = cls.get_stock_summaries_from_page(soup)
        name_tuple = cls.get_stock_name_tuple(soup)
        # section_info = get_stock_section_info(soup)
        print('A tupla - ', name_tuple)

        stock_indicators = [name_tuple] + stock_summaries + indicator_tuples
        return stock_indicators

    @classmethod
    def get_indicators_from_stocks(cls, stocks: List[str]) -> StockIndicatorsDict:
        ''' Returns a dictionary with each key being the stock name and its value is a list containing all indicators tuple extracted from YUBB page '''
        indicators_dict = {}
        for stock in stocks:
            print('Indicadores para -> ', stock)
            indicators_dict[stock] = cls.get_stock_indicators(stock)
        
        return indicators_dict

    @classmethod
    def get_tickers_from_page(cls, page_number: int) -> List[str]:
        ''' Returns a list with stock tickers from Yubb collection's page with page_number index '''
        page = requests.get(f'https://yubb.com.br/investimentos/acoes?collection_page={page_number}&sort_by=ticker')
        soup = BeautifulSoup(page.content, 'html.parser')
        header_divs = soup.select('div.header__title.header__title--column.investmentCard__row')
        tickers = []
        for div in header_divs:
            stock_title = div.h3.text
            ticker = stock_title.split(' ')[0]
            tickers.append(ticker)
        return tickers

    @classmethod
    def get_all_tickers(cls) -> List[str]:
        ''' Returns a list with all tickers from Yubb collection's pages. It scrapes up until 30 collection's pages by now. '''
        all_tickers = []
        for i in range(1,30):
            tickers = cls.get_tickers_from_page(i)
            all_tickers = all_tickers + tickers
        return all_tickers

    @staticmethod
    def save_list_to_file(tickers_list: List[str], filename: str) -> None:
        with open(filename, "w") as output:
            for item in tickers_list:
                output.write(f'{item}\n')

    @staticmethod
    def get_list_from_file(filename: str) -> List[str]:
        import os.path
        file_exists = os.path.exists(filename)

        if file_exists:
            tickers_list = []
            try:
                with open(filename, "r") as file:
                    for line in file:
                        ticker = line.replace('\n', '')
                        tickers_list.append(ticker)
            except Exception as excp:
                raise excp
        else:
            raise Exception('File does not exist')
        return tickers_list
