import re
import json
from enum import Enum
from http.client import HTTPResponse
from urllib.request import Request, urlopen

class Methods(Enum):
    GET = "GET"
    POST = "POST"


class ResponseData:
    def __init__(self, response: HTTPResponse) -> None:
        self._response: HTTPResponse = response
        self._json: dict[str, str] = json.loads(self._response.read())
        self._str: str = self._response.read().decode("utf-8")
        self._length: int = response.length
        self._status: int = response.status
    
    def __len__(self):
        return self._length
    
    @property
    def json(self) -> dict:
        return self._json
    
    @property
    def to_str(self) -> str:
        return self._str
    
    @property
    def length(self) -> int:
        return self.__len__()
    
    @property
    def status_code(self) -> int:
        return self._status

class _API:
    def __init__(self):
        pass
    
    def _make_request(
        self,
        root_url: str,
        path: str,
        data: bytes | None,
        method: Methods,
        headers: dict[str, str] = None
    ) -> ResponseData:
        if root_url[-1] != "/" and path[0] != "/":
            path = "/" + path
        full_url: str = root_url + path
        
        if method == Methods.GET:
            request: Request = Request(
                url=full_url,
                headers=headers,
                method=Methods.GET.value,
            )
        elif method == Methods.POST:
            request: Request = Request(
                url=full_url,
                headers=headers,
                data=data,
                method=Methods.POST.value,
            )
        response = urlopen(request)
        return ResponseData(response)
    
    def get(
        self,
        root_url: str,
        path: str,
        headers: dict[str, str]
    ) -> ResponseData:
        return self._make_request(
            root_url=root_url,
            path=path,
            data=None,
            method=Methods.GET,
            headers=headers
        )
    
    def post(
        self,
        root_url: str,
        path: str,
        data: bytes,
        headers: dict[str, str]
    ) -> ResponseData:
        return self._make_request(
            root_url=root_url,
            path=path,
            data=data,
            method=Methods.POST,
            headers=headers
        )
    
    def get_image_paths(
        self,
        input_item: str,
        root_url: str,
        path: str,
        headers: dict[str, str]
    ) -> list[dict[str, str]]:
        """
        This function will return the path to the image for the episode.
        :return:
        """
        all_items: ResponseData = self.get(
            root_url=root_url,
            path=path,
            headers=headers
        )
        
        for item in all_items.json:
            if input_item == item["title"]:
                return item["images"]
    
    
class LunaSea(_API):
    def __init__(self) -> None:
        super().__init__()
        self._root_url: str = "https://notify.lunasea.app"
        self._path: str = "v1/custom/user"
        self._api_key: str = "KklxIKhslMgnB6AY46Rj4CQwDJD3"
        
    def notify(
        self,
        title: str,
        body: str,
        image: str | None,
        extra_headers: dict[str, str] = None,
    ):
        headers: dict[str, str] = {"Content-Type": "application/json"}
        if extra_headers is not None:
            headers.update(extra_headers)
            
        # Test if image is a URL
        match = re.search(r"^https?://", image)
        if image is not None and not match:
            raise ValueError("`image` parameter must be a URL")
        
        data = {
            "title": str(title),
            "body": str(body)
        }
        if image is not None:
            data.update({"image": str(image)})
            
        response = self.post(
            root_url=self._root_url,
            path=f"{self._path}/{self._api_key}",
            data=json.dumps(data).encode("utf-8"),
            headers=headers
        )
    

class Apps(_API):
    def __init__(
        self,
        root_url: str,
        api_key: str,
        item_path: str
    ) -> None:
        super().__init__()
        self.root_url: str = root_url
        self.item_path: str = item_path
        self.api_key: str = api_key
        
        """
         --header "Content-Type: application/json"
         --request POST
         --data '{"title":"title","body":"body","image":"img.jpg"}'
         https://notify.lunasea.app/v1/custom/user/KklxIKhslMgnB6AY46Rj4CQwDJD3
        """
        
        self.api_key: str = api_key
        self.headers: dict[str, str] = {
            "accept": "application/json",
            "X-Api-Key": self.api_key
        }
        
        self._json: dict[str, str] = {}
        self._str: str = ""
        self._length: int = -1
    
    def _get_all_items(self, path: str):
        response = self.get(
            root_url=self.root_url,
            path=path,
            headers={}
        )
        
        name_id: dict[str, int] = {}
        for item in response.json:
            name_id[item["title"]] = int(item["id"])
        return name_id
    
    def get_item_name_from_input_path(self) -> str:
        for part in self.item_path.split("/"):
            match = re.search(r"\(\d{4}\)", part)
            if match:
                # Remove year from name
                return part.split(" (")[0]
            
    def get_item_year_from_input_path(self) -> int:
        for part in self.item_path.split("/"):
            match = re.search(r"\(\d{4}\)", part)
            if match:
                year = match.group()
                year = year.replace("(", "").replace(")", "")
                return int(year)
