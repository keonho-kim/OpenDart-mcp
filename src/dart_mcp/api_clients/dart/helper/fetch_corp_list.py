from io import BytesIO
from zipfile import ZipFile

import httpx
import xmltodict

from .const import urls


def get_corp_list():
    """
    DART에 등록된 기업 목록을 가져옵니다.
    """

    URL = urls.FETCH_COMPANY_LIST.value

    with httpx.Client() as client:
        response = client.get(URL)

        if response.status_code != 200:
            raise Exception(f"API 요청 실패: 상태 코드 {response.status_code}")

        with ZipFile(BytesIO(response.content)) as zip_file:
            if "CORPCODE.xml" not in zip_file.namelist():
                    raise FileNotFoundError("Could not find company list file.")

            with zip_file.open("CORPCODE.xml") as f:
                parsed = xmltodict.parse(f.read())

            return parsed["result"]["list"]