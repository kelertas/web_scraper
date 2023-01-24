from typing import List
from .base import BaseScraper
from src.models.flat import Flat, FlatUrl


class Realu_Lt(BaseScraper):
    __items_per_page__: int = 16
    __domain__: str = "https://www.realu.lt/nekilnojamasis-turtas"

    def _retrieve_flat_links(self, pages_count: int, keyword: str) -> List[FlatUrl]:
        url_prefix: str = "https://www.realu.lt"
        links: List[FlatUrl] = []

        for page_num in range(1, pages_count + 1):
            query = f"?op=sale&estate_type={keyword}&page={page_num}"

            content = self._get_page_content(query=query)
            if content:
                divs = content.find_all("div", class_="col-md-6 col-xl-3")

                for div in divs:
                    flat_url = FlatUrl(url=url_prefix + div.find("a", class_="info")["href"])
                    links.append(flat_url)

            else:
                break
        return links

    def _retrieve_flat_info(self, link: FlatUrl) -> Flat:
        links_to_img_list: List[str] = []
        print(link)
        content = self._get_page_content(link)

        address = content.find("span", class_="address").text.split(",")
        city = address[-1].strip()
        street = address[0].strip()

        accordion_body_class = content.find_all("div", class_="accordion-body")
        extra_info_on_flat = accordion_body_class[0].find_all("span")
        length_of_extra_info = len(extra_info_on_flat)
        if length_of_extra_info == 7:
            ad_status = extra_info_on_flat[0].text
            object_ = extra_info_on_flat[1].text
            build_year = extra_info_on_flat[2].text
            furnishment = extra_info_on_flat[3].text
            heating = extra_info_on_flat[4].text
            building = extra_info_on_flat[5].text
            operation = extra_info_on_flat[6].text
        elif length_of_extra_info == 6:
            ad_status = extra_info_on_flat[0].text
            object_ = extra_info_on_flat[1].text
            build_year = extra_info_on_flat[2].text
            furnishment = extra_info_on_flat[3].text
            heating = extra_info_on_flat[4].text
            building = extra_info_on_flat[5].text
            operation = None
        elif length_of_extra_info == 5:
            ad_status = extra_info_on_flat[0].text
            object_ = extra_info_on_flat[1].text
            build_year = extra_info_on_flat[2].text
            furnishment = extra_info_on_flat[3].text
            heating = extra_info_on_flat[4].text
            building = None
            operation = None
        elif length_of_extra_info == 4:
            ad_status = extra_info_on_flat[0].text
            object_ = extra_info_on_flat[1].text
            build_year = extra_info_on_flat[2].text
            furnishment = extra_info_on_flat[3].text
            heating = None
            building = None
            operation = None
        elif length_of_extra_info == 3:
            ad_status = extra_info_on_flat[0].text
            object_ = extra_info_on_flat[1].text
            build_year = extra_info_on_flat[2].text
            furnishment = None
            heating = None
            building = None
            operation = None
        elif length_of_extra_info == 2:
            ad_status = extra_info_on_flat[0].text
            object_ = extra_info_on_flat[1].text
            build_year = None
            furnishment = None
            heating = None
            building = None
            operation = None
        elif length_of_extra_info == 1:
            ad_status = extra_info_on_flat[0].text
            object_ = None
            build_year = None
            furnishment = None
            heating = None
            building = None
            operation = None
        elif length_of_extra_info == 0:
            ad_status = None
            object_ = None
            build_year = None
            furnishment = None
            heating = None
            building = None
            operation = None

        description = ""
        if len(accordion_body_class) == 2:
            description_ps = accordion_body_class[1].find_all("p")
            for p in description_ps:
                description += p.text + " "

        imgs = content.find("div", class_="swiper-wrapper").find_all("img")
        for img in imgs:
            links_to_img_list.append(img["src"])
        links_to_img = ",".join(links_to_img_list)

        div_meta = content.find("div", class_="meta")
        data_grid = div_meta.find_all("div", class_="dl")

        if len(data_grid) == 3:
            area_field: str = data_grid[0].find("span", class_="dd").text.split(" ")
            area = area_field[0]
            floor_field: str = data_grid[1].find("span", class_="dd").text.split("/")
            if len(floor_field) == 2:
                floor = floor_field[0]
                floors = floor_field[1]
            elif len(floor_field) == 1:
                floor = floor_field[0]
                floors = "0"
            number_of_rooms: str = data_grid[2].find("span", class_="dd").text

        elif len(data_grid) == 2:
            area_field: str = data_grid[0].find("span", class_="dd").text.split(" ")
            area = area_field[0]
            floor = "0"
            floors = "0"
            number_of_rooms: str = data_grid[1].find("span", class_="dd").text

        elif len(data_grid) == 1:
            area_field: str = data_grid[0].find("span", class_="dd").text.split(" ")
            area = area_field[0]
            floor = "0"
            floors = "0"
            number_of_rooms = "0"
        else:
            area = "0"
            floor = "0"
            floors = "0"
            number_of_rooms = "0"

        price_per_square_m_field: str = content.find("span", class_="area").text.split()
        price_per_square_m = "".join(price_per_square_m_field[:-1])

        total_price_field: str = content.find("span", class_="price").text.split()
        total_price = "".join(total_price_field[:-1])

        flat: Flat = Flat(
            city=city,
            street=street,
            description=description,
            area=area,
            floors=floors,
            floor=floor,
            number_of_rooms=number_of_rooms,
            price_per_square_m=price_per_square_m,
            total_price=total_price,
            links_to_img=links_to_img,
            object_=object_,
            build_year=build_year,
            furnishment=furnishment,
            heating=heating,
            building=building,
            operation=operation,
        )

        return flat
