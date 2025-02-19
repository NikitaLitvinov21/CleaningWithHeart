from typing import List

from requests import get


class AddressesService:

    def find_addresses(
        self,
        search: str,
        city: str = "Toronto",
        country: str = "Canada",
        limit: int = 10,
    ) -> List[str]:
        url = "https://photon.komoot.io/api/"
        params = {
            "q": f"{search.lower()}, {city}, {country}",
            "limit": limit,
            "lang": "en",
            "osm_tag": "highway",
        }

        response = get(url, params=params)
        response.raise_for_status()

        data = response.json()
        addresses: List[str] = []

        for feature in data.get("features", []):
            properties = feature.get("properties", {})
            street_name = properties.get("name")
            city_name = properties.get("city")
            postcode = properties.get("postcode", "")

            if street_name:
                full_address = f"{street_name}"
                if city_name:
                    full_address += f", {city_name}"
                if postcode:
                    full_address += f" {postcode}"

                if full_address not in addresses:
                    addresses.append(full_address)

        return addresses
