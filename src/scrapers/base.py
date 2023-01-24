import math
import requests
import lxml
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
from typing import List, Optional
from tqdm import tqdm
from src.models.flat import Flat, FlatUrl


class BaseScraper(ABC):
    __items_per_page__: int = 0
    __domain__: str = ""

    @abstractmethod
    def _retrieve_flat_links(self, pages_count: int, keyword: str) -> List[FlatUrl]:
        pass

    def _get_page_content(self, query: str) -> Optional[BeautifulSoup]:
        resp = requests.get(f"{self.__domain__}/{query}")
        if resp.status_code == 200:
            return BeautifulSoup(resp.content, "lxml")
        raise Exception("Cannot reach the content")

    @abstractmethod
    def _retrieve_flat_info(self, link: FlatUrl) -> Optional[Flat]:
        pass

    def scrape(self, flats_count: int, keyword: str) -> List[Optional[Flat]]:
        try:
            pages_count = math.ceil(flats_count / self.__items_per_page__)
        except ZeroDivisionError:
            raise AttributeError("Flats per page is set to zero")

        flat_links = self._retrieve_flat_links(pages_count, keyword)
        scraped_flats: List[Optional[Flat]] = []
        for flat_link in tqdm(flat_links):
            scraped_flat = self._retrieve_flat_info(flat_link)
            if scraped_flat:
                scraped_flats.append(scraped_flat)
        
        return scraped_flats
