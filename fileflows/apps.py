import re

from fileflows.api import Apps, LunaSea, ResponseData

class Sonarr(Apps, LunaSea):
    def __init__(
        self,
        item_path: str,
        root_url: str = "https://sonarr.joshl.xyz"
    ) -> None:
        self._headers: dict[str, str] = {"X-Api-Key": "ea493233b98848b2bd364aa53759ec29"}
        Apps.__init__(
            self,
            root_url=root_url,
            api_key="ea493233b98848b2bd364aa53759ec29",
            item_path=item_path
        )
        LunaSea.__init__(self)
        
        self.series_name = self.get_item_name_from_input_path()
        self.season_number = self.get_season_number_from_path()
        self.episode_number = self.get_episode_number_from_path()
        self.image_paths: list[dict[str, str]] = self.get_image_paths(
            input_item=self.series_name,
            root_url=self.root_url,
            path=f"/api/v3/series?includeSeasonImages=false",
            headers=self.headers
        )
        
    def get_all_items(self) -> dict[str, str]:
        response: ResponseData = self.get(
            root_url=self.root_url,
            path="/api/v3/series?includeSeasonImages=false",
            headers=self.headers
        )
        return response.json
    
    def get_season_number_from_path(self) -> int:
        """
        Input: /mnt/unionfs/TV Shows/My Hero Academia/S03E01 - The Power of One.mkv
        Output: 3
        
        Given an input string, this function will search for "S03E01" and return 03
        :return:
        """
        for part in self.item_path.split("/"):
            match = re.search(r"S\d{2}E\d{2}", part)
            if match:
                season_episode: str = match.group()
                return int(season_episode[1:3])
            
    def get_episode_number_from_path(self) -> int:
        """
        Input: /mnt/unionfs/TV Shows/My Hero Academia/S03E01 - The Power of One.mkv
        Output: 1
        
        Given an input string, this function will search for "S03E01" and return 1

        :return:
        """
        for part in self.item_path.split("/"):
            match = re.search(r"S\d{2}E\d{2}", part)
            if match:
                season_episode: str = match.group()
                return int(season_episode[4:6])
    
    @property
    def banner_image(self) -> str:
        for item in self.image_paths:
            if item["coverType"] == "banner":
                return item["remoteUrl"]
        
        return ""
    
    @property
    def poster_image(self):
        for item in self.image_paths:
            if item["coverType"] == "poster":
                return item["remoteUrl"]
        
        return ""
    
    @property
    def fanart_image(self):
        for item in self.image_paths:
            if item["coverType"] == "fanart":
                return item["remoteUrl"]
        
        return ""


class Radarr(Apps, LunaSea):
    def __init__(
        self,
        item_path: str,
        root_url: str = "https://radarr.joshl.xyz"
    ) -> None:
        Apps.__init__(
            self,
            root_url=root_url,
            api_key="13a31afac3af4ab8a2cc83f5ffe19e11",
            item_path=item_path
        )
        LunaSea.__init__(self)
        
        self._headers: dict[str, str] = {"X-Api-Key": "13a31afac3af4ab8a2cc83f5ffe19e11"}
        
        self.movie_name: str = self.get_item_name_from_input_path()
        self.movie_year: int = self.get_item_year_from_input_path()
        self.image_paths: list[dict[str, str]] = self.get_image_paths(
            input_item=self.movie_name,
            root_url=self.root_url,
            path="/api/v3/movie",
            headers=self.headers
        )
        
    @property
    def get_all_items(self):
        return self._get_all_items("/api/v3/movie")
    
    @property
    def banner_image(self) -> str:
        for item in self.image_paths:
            if item["coverType"] == "banner":
                return item["remoteUrl"]
        
        return ""
    
    @property
    def poster_image(self):
        for item in self.image_paths:
            if item["coverType"] == "poster":
                return item["remoteUrl"]
        
        return ""
    
    @property
    def fanart_image(self):
        for item in self.image_paths:
            if item["coverType"] == "fanart":
                return item["remoteUrl"]
        
        return ""
