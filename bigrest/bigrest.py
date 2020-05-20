# External Imports
# Import only with 'import package',
# it will make explicity in the code where it came from.

# Turns all annotations into string literals.
# This is one exception to the external import rule.
from __future__ import annotations
import requests
import time
import urllib3
import pathlib

# Internal Imports
# Import only with 'from x import y', to simplify the code.

from .common.restobject import RESTObject
from .common.exceptions import RESTAPIError
from .common.exceptions import InvalidOptionError
from .common.constants import TOKEN_EXTRA_TIME
from .common.constants import REST_API_MAXIMUM_CHUNK_SIZE

# Disable urllib3 SSL warnings
urllib3.disable_warnings()


class BIGREST:
    """Define all methods to call the iControl REST API."""

    def __init__(self, device: str, username: str,
                 password: str, *, login_provider: str = 'local',
                 request_token: bool = False, token: str = None,
                 refresh_token: str = None) -> BIGREST:

        # Input validations
        if request_token and token is not None:
            raise InvalidOptionError(
                'Use only one option,\
                request_token or token or refresh_token.')
        if request_token and refresh_token is not None:
            raise InvalidOptionError(
                'Use only one option,\
                request_token or token or refresh_token.')
        if token is not None and refresh_token is not None:
            raise InvalidOptionError(
                'Use only one option,\
                request_token or token or refresh_token.')

        # Variables
        self.device = device
        self.username = username
        self.password = password
        self.request_token = request_token
        self.login_provider = login_provider
        self._token = None
        self._token_timeout = None
        self._token_counter = None
        self.token = token
        self.refresh_token = refresh_token
        self._transaction = None
        self.session = requests.Session()

        # Session settings
        if self.request_token is False:
            self.session.auth = (username, password)
        if self.token is not None:
            self.session.headers.update({'X-F5-Auth-Token': f'{self.token}'})
        self.session.headers.update({'Content-Type': 'application/json'})
        self.session.verify = False

        # Connect to device
        self._connect()

    def load(self, path: str) -> list[RESTObject]:
        """
        Send a GET request to the iControl REST API.
        Return a list of objects that represents the objects on the device.
        """

        if self.request_token or self.refresh_token is not None:
            self._check_token()
        response = self.session.get(self._url(path))
        if response.status_code != 200:
            raise RESTAPIError(response)
        response_json = response.json()
        objects = []
        if 'items' in response_json:
            for obj in response_json['items']:
                objects.append(RESTObject(obj))
        else:
            objects.append(RESTObject(response_json))
        return objects

    def save(self, obj: RESTObject) -> RESTObject:
        """
        Send a PUT request to the iControl REST API.
        This will save on the device, the object modifications that were made.
        """

        if self.request_token or self.refresh_token is not None:
            self._check_token()
        path = self._get_path(obj)
        response = self.session.put(self._url(path), json=obj.asdict())
        if response.status_code != 200:
            raise RESTAPIError(response)
        return RESTObject(response.json())

    def delete(self, path: str) -> None:
        """
        Send a DELETE request to the iControl REST API.
        This will delete the object on the device.
        """

        if self.request_token or self.refresh_token is not None:
            self._check_token()
        response = self.session.delete(self._url(path))
        if response.status_code != 200:
            raise RESTAPIError(response)

    def create(self, path: str, data: dict) -> RESTObject:
        """
        Send a POST request to the iControl REST API.
        This will create the object on the device.
        """

        if self.request_token or self.refresh_token is not None:
            self._check_token()
        response = self.session.post(self._url(path), json=data)
        if response.status_code != 200:
            raise RESTAPIError(response)
        return RESTObject(response.json())

    def modify(self, path: str, data: dict) -> RESTObject:
        """
        Send a PATCH request to the iControl REST API.
        This will modifiy the object on the device.
        """

        if self.request_token or self.refresh_token is not None:
            self._check_token()
        response = self.session.patch(self._url(path), json=data)
        if response.status_code != 200:
            raise RESTAPIError(response)
        return RESTObject(response.json())

    def exist(self, path: str) -> bool:
        """
        Send a GET request to the iControl REST API.
        Return true or false indicating if the object exists or not.
        """

        if self.request_token or self.refresh_token is not None:
            self._check_token()
        response = self.session.get(f'{self._url(path)}?$select=""')
        if response.status_code == 200:
            return True
        if response.status_code == 404:
            return False
        raise RESTAPIError(response)

    def show(self, path: str) -> list[RESTObject]:
        """
        Send a GET request to the iControl REST API.
        Return a list of objects with statistics information.
        Similar to tmsh show command.
        """

        if self.request_token or self.refresh_token is not None:
            self._check_token()
        response = self.session.get(self._url(f'{path}/stats'))
        if response.status_code != 200:
            raise RESTAPIError(response)
        response_json = response.json()
        objects = []
        if 'entries' in response_json:
            for obj_entries in response_json['entries']:
                objects.append(
                    RESTObject(response_json['entries']
                               [f'{obj_entries}']['nestedStats']['entries']))
        else:
            objects.append(RESTObject(response_json))
        return objects

    def transaction_start(self) -> RESTObject:
        """
        Send a POST request to the iControl REST API.
        Create a transaction.
        """

        if self.request_token or self.refresh_token is not None:
            self._check_token()
        response = self.session.post(
            self._url('/mgmt/tm/transaction'), json={})
        if response.status_code != 200:
            raise RESTAPIError(response)
        self._transaction = response.json()['transId']
        self.session.headers.update(
            {'X-F5-REST-Coordination-Id': f'{self._transaction}'})
        return RESTObject(response.json())

    def __enter__(self) -> RESTObject:
        return self.transaction_start()

    def transaction_finish(self) -> RESTObject:
        """
        Send a PATCH request to the iControl REST API.
        Create commit the transaction.
        """

        if self.request_token or self.refresh_token is not None:
            self._check_token()
        self.session.headers.pop('X-F5-REST-Coordination-Id')
        data = {}
        data['state'] = 'VALIDATING'
        response = self.session.patch(
            self._url(f'/mgmt/tm/transaction/{self._transaction}'), json=data)
        if response.status_code != 200:
            raise RESTAPIError(response)
        return RESTObject(response.json())

    def __exit__(self, type, value, traceback) -> None:
        self.transaction_finish()

    def transaction_validate(self) -> RESTObject:
        """
        Send a PATCH request to the iControl REST API.
        Create validate a transaction.
        """

        if self.request_token or self.refresh_token is not None:
            self._check_token()
        self.session.headers.pop('X-F5-REST-Coordination-Id')
        data = {}
        data['validateOnly'] = True
        data['state'] = 'VALIDATING'
        response = self.session.patch(
            self._url(f'/mgmt/tm/transaction/{self._transaction}'), json=data)
        self.session.headers.update(
            {'X-F5-REST-Coordination-Id': f'{self._transaction}'})
        if response.status_code != 200:
            raise RESTAPIError(response)
        return RESTObject(response.json())

    def transaction_delete(self) -> None:
        """
        Send a DELETE request to the iControl REST API.
        Delete the transaction.
        """

        if self.request_token or self.refresh_token is not None:
            self._check_token()
        self.session.headers.pop('X-F5-REST-Coordination-Id')
        response = self.session.delete(
            self._url(f'/mgmt/tm/transaction/{self._transaction}'))
        if response.status_code != 200:
            raise RESTAPIError(response)

    def command(self, path: str, data: dict) -> RESTObject:
        """
        Send a POST request to the iControl REST API.
        This will create the object on the device.
        """

        return self.create(path, data)

    def task_start(self, path: str, data: dict) -> str:
        """
        Send a POST and PUT requests to the iControl REST API.
        This will create and start a task.
        """

        if self.request_token or self.refresh_token is not None:
            self._check_token()
        response = self.session.post(self._url(path), json=data)
        if response.status_code != 200:
            raise RESTAPIError(response)
        id = response.json()['_taskId']
        data = {}
        data['_taskState'] = 'VALIDATING'
        response_put = self.session.put(f'{self._url(path)}/{id}', json=data)
        if response_put.status_code != 202:
            raise RESTAPIError(response_put)
        return id

    def task_running(self, path: str, id: str) -> bool:
        """
        Send a GET request to the iControl REST API.
        Verify if the task is completed.
        """

        if self.request_token or self.refresh_token is not None:
            self._check_token()
        response = self.session.get(f'{self._url(path)}/{id}')
        if response.status_code != 200:
            raise RESTAPIError(response)
        if response.json()['_taskState'] == 'COMPLETED':
            return False
        else:
            return True

    def task_result(self, path: str, id: str) -> str:
        """
        Send a GET request to the iControl REST API.
        Return the result of the task.
        """

        if self.request_token or self.refresh_token is not None:
            self._check_token()
        response = self.session.get(f'{self._url(path)}/{id}/result')
        if response.status_code != 200:
            raise RESTAPIError(response)
        return response.json()['commandResult']

    def download(self, path: str, filename: str) -> None:
        """
        Send a GET request to the iControl REST API.
        Download a file from the device.
        """
        
        # Content-Range: <range-start>-<range-end>/<size>
        if self.request_token or self.refresh_token is not None:
            self._check_token()
        self.session.headers.update(
            {'Content-Type': 'application/octet-stream'})
        filename_without_path = pathlib.PurePath(filename).name
        response = self.session.get(
            self._url(f'{path}/{filename_without_path}'))
        if response.status_code != 200 and response.status_code != 206:
            raise RESTAPIError(response)
        if response.status_code == 206:
            content_range = response.headers.get('Content-Range')
            range_start = 0
            range_size = int(content_range.split('/')[0].split('-')[1])
            range_end = range_size
            size = int(content_range.split('/')[1])
            size = size - 1
            with open(filename, 'wb') as destination_file:
                destination_file.write(response.content)
                while size > range_end:
                    range_start = range_end + 1
                    range_end = range_start + range_size
                    if range_end > size:
                        range_end = size
                    self.session.headers.update(
                        {'Content-Range': f'{range_start}-{range_end}/'})
                    response = self.session.get(
                        self._url(f'{path}/{filename_without_path}'))
                    destination_file.write(response.content)
                    if (response.status_code != 200
                            and response.status_code != 206):
                        raise RESTAPIError(response)
        self.session.headers.pop('Content-Range')
        self.session.headers.update({'Content-Type': 'application/json'})

    def upload(self, path: str, filename: str) -> None:
        """
        Send a POST request to the iControl REST API.
        Upload a file to the device.
        """

        # Content-Range: <range-start>-<range-end>/<size>
        if self.request_token or self.refresh_token is not None:
            self._check_token()
        self.session.headers.update(
            {'Content-Type': 'application/octet-stream'})
        filename_without_path = pathlib.PurePath(filename).name
        range_start = 0
        range_size = REST_API_MAXIMUM_CHUNK_SIZE - 1
        range_end = REST_API_MAXIMUM_CHUNK_SIZE - 1
        size = pathlib.Path(filename).stat().st_size - 1
        with open(filename, 'rb') as file_:
            if size <= range_size:
                self.session.headers.update(
                    {'Content-Range': f'{range_start}-{size}/{size + 1}'})
                response = self.session.post(
                    self._url(f'{path}/{filename_without_path}'),
                    data=file_.read(size + 1))
                if response.status_code != 200:
                    raise RESTAPIError(response)
            else:
                while size >= range_start:
                    if range_end > size:
                        range_end = size
                    content_range = f'{range_start}-{range_end}/{size + 1}'
                    self.session.headers.update(
                        {'Content-Range': content_range})
                    bytes_to_read = (range_end - range_start) + 1
                    response = self.session.post(
                        self._url(f'{path}/{filename_without_path}'),
                        data=file_.read(bytes_to_read))
                    if response.status_code != 200:
                        raise RESTAPIError(response)
                    range_start = range_end + 1
                    range_end = range_end + range_size + 1
        self.session.headers.pop('Content-Range')
        self.session.headers.update({'Content-Type': 'application/json'})

    def _url(self, path: str) -> str:
        """Format the URL to be used to connect to the device."""

        return f'https://{self.device}{path}'

    def _check_token(self) -> None:
        if self._token is None:
            self._get_token()
        else:
            time_passed = time.time() - self._token_counter
            # Only use token if still valid for TOKEN_EXTRA_TIME seconds
            time_passed = time_passed + TOKEN_EXTRA_TIME
            if time_passed > self._token_timeout:
                self._get_token()

    def _get_token(self) -> None:
        if 'X-F5-Auth-Token' in self.session.headers:
            self.session.headers.pop('X-F5-Auth-Token')
        response = None
        if self.refresh_token is None:
            data = {}
            data['username'] = self.username
            data['password'] = self.password
            data['loginProviderName'] = self.login_provider
            response = self.session.post(
                f'https://{self.device}/mgmt/shared/authn/login', json=data)
        else:
            data_token = {}
            data_token['token'] = self.refresh_token
            data = {}
            data['refreshToken'] = data_token
            response = self.session.post(
                f'https://{self.device}/mgmt/shared/authn/exchange', json=data)
        if response.status_code != 200:
            raise RESTAPIError(response)
        self._token_counter = time.time()
        self._token = response.json()['token']['token']
        self.session.headers.update({'X-F5-Auth-Token': f'{self._token}'})
        self._token_timeout = response.json()['token']['timeout']

    def _get_path(self, obj: RESTObject) -> str:
        self_link = obj.properties['selfLink']
        # remove https://localhost
        self_link = self_link[17:]
        return self_link

    def _connect(self) -> None:
        """
        Send a GET request to the iControl REST API.
        Return true or false indicating if the object exists or not.
        """

        if self.request_token or self.refresh_token is not None:
            self._get_token()
        else:
            data = {}
            data['username'] = self.username
            data['password'] = self.password
            data['loginProviderName'] = self.login_provider
            response = self.session.post(
                f'https://{self.device}/mgmt/shared/authn/login', json=data)
            if response.status_code != 200:
                raise RESTAPIError(response)
