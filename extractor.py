import requests
from bs4 import BeautifulSoup
from typing import Tuple, List, Dict

# Defining Types to be easier to type hint methods
IndicatorTupleList = List[Tuple[str, str]]
StockIndicatorsDict = Dict[str, List[Tuple[str, str]]]

class YubbExtractor:

    def reorder_tuple_list_with_first_element_as(self, tuple_key: str, tuple_list: IndicatorTupleList) -> IndicatorTupleList:
        ''' Order the list with tuples setting the first element of this list as the tuple_key tuple and all the elements before it put in the last positions '''
        keys = [elem[0] for elem in tuple_list]
        try:
            tuple_key_position = keys.index(tuple_key)
        except ValueError:
            return tuple_list
        before_threshold_list = tuple_list[:tuple_key_position]
        first_list = tuple_list[tuple_key_position:]
        return first_list + before_threshold_list


    def get_main_indicators_from_page(self, soup: BeautifulSoup) -> IndicatorTupleList:
        indicators = soup.find_all('div', class_='card investmentDetails__card')
        indicator_tuples = [(indicator.find('dt', class_='investmentDetails__label').get_text(), indicator.find('dd', class_='investmentDetails__value').get_text()) for indicator in indicators]
        # Reorder elements for the most important items be first
        ordered_indicator_tuples = self.reorder_tuple_list_with_first_element_as('Dividend Yield', indicator_tuples)
        return ordered_indicator_tuples


    def get_stock_summaries_from_page(self, soup: BeautifulSoup) -> IndicatorTupleList:
        summary_infos = soup.find_all('div', class_='investmentSummary__label')
        summary_infos = [info.get_text() for info in summary_infos]

        summary_values = soup.find_all('div', class_='investmentSummary__value')
        summary_values = [value.get_text() for value in summary_values]

        ziped_summary = zip(summary_infos, summary_values)
        # tuple(ziped_summary)
        stock_summaries = list(ziped_summary)
        return stock_summaries


    def get_stock_name_tuple(self, soup: BeautifulSoup) -> Tuple[str, str]:
        h1_name = soup.find('h1', class_='investmentPageHeader__title')
        stock_name = h1_name.get_text() if h1_name else None
        print('Nome - ', stock_name)
        name_tuple = ('Ação', stock_name)
        return name_tuple


    def get_stock_section_info(self, soup: BeautifulSoup) -> Tuple[str, str]:
        cards = soup.select('div.card.shadow-sm')
        # import pdb
        # pdb.set_trace()
        section_info = [(card.dt.text, card.dd.text) for card in cards]
        return section_info


    def get_stock_indicators(self, stock_name: str) -> IndicatorTupleList:
        print('Vai pegar da acao: ', stock_name)
        page = requests.get(f'https://yubb.com.br/investimentos/acoes/{stock_name}')
        soup = BeautifulSoup(page.content, 'html.parser')

        indicator_tuples = self.get_main_indicators_from_page(soup)
        stock_summaries = self.get_stock_summaries_from_page(soup)
        name_tuple = self.get_stock_name_tuple(soup)
        # section_info = get_stock_section_info(soup)
        print('A tupla - ', name_tuple)

        stock_indicators = [name_tuple] + stock_summaries + indicator_tuples
        return stock_indicators


    def get_indicators_from_stocks(self, stocks: List[str]) -> StockIndicatorsDict:
        ''' Returns a dictionary with each key being the stock name and its value is a list containing all indicators tuple extracted from YUBB page '''
        indicators_dict = {}
        for stock in stocks:
            print('Indicadores para -> ', stock)
            indicators_dict[stock] = self.get_stock_indicators(stock)
        
        return indicators_dict