import uuid
import httpx
from leomaine.base_states import BaseState


class QueryState(BaseState):
    req_methods: list[str] = ["GET", "POST", "PUT", "DELETE"]
    req_url: str = "https://jsonplaceholder.typicode.com/posts"
    current_req_method: str = "GET"
    get_params_body: list[str] = ["JSON", "Form", "Raw", "None"]
    post_params_body: list[str] = [
        "x-www-form-urlencoded",
        "Form Data",
        "JSON",
        "Form",
        "Raw",
        "None",
    ]

    url_params: dict[str, str]
    headers: list[dict[str, str]]
    body: list[dict[str, str]]
    cookies: list[dict[str, str]]

    get_data: list[dict[str, str]]

    def get_request(self, method: str):
        self.current_req_method = method

    def add_header(self):
        self.headers.append({"key": "", "value": ""})

    def add_body(self):
        self.body.append({"key": "", "value": ""})

    def add_cookie(self):
        self.cookies.append({"key": "", "value": ""})

    def add_url_param(self):
        self.url_params.append({"key": "", "value": ""})

    async def update_attribute(self, data: dict[str, str], attribute: str, value: str):
        data[attribute] = value

        if data["identifier"] == "headers":
            self.headers = [
                data if item["id"] == data["id"] else item for item in self.headers
            ]

        if data["identifier"] == "body":
            self.body = [
                data if item["id"] == data["id"] else item for item in self.body
            ]

        if data["identifier"] == "cookies":
            self.cookies = [
                data if item["id"] == data["id"] else item for item in self.cookies
            ]

    async def update_keys(self, key: str, data: dict[str, str]):
        await self.update_attribute(data, "key", key)

    async def update_values(self, value: str, data: dict[str, str]):
        await self.update_attribute(data, "value", value)

    async def remove_entry(self, data: dict[str, str]):
        if data["identifier"] == "headers":
            self.headers = [item for item in self.headers if item["id"] != data["id"]]

        if data["identifier"] == "body":
            self.body = [item for item in self.body if item["id"] != data["id"]]

        if data["identifier"] == "cookies":
            self.cookies = [item for item in self.cookies if item["id"] != data["id"]]


class QueryAPI(QueryState):
    async def process_headers(self):
       for item in self.headers:
            if item["key"]:
                self.formatted_headers[item["key"]] = item["value"]
    async def run_get_request(self):
        await self.process_headers()
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self.req_url, headers=self.formatted_headers
            )
            self.get_data = response.json()
            self.number_of_rows = len(self.get_data)
            self.get_table_headers = list(self.get_data[0].keys())