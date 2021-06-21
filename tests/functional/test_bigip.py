from tempfile import NamedTemporaryFile
import os


mergefile = '''
ltm pool mergepool {
    members {
        192.168.103.20:http {
            address 192.168.103.20
            session monitor-enabled
            state down
        }
    }
    monitor http
}
'''


class TstFileContent:
    def __init__(self, content):

        self.file = NamedTemporaryFile(mode='w', delete=False, suffix='.cfg')

        with self.file as f:
            f.write(content)

    @property
    def filename(self):
        return self.file.name

    @property
    def basename(self):
        return os.path.basename(self.file.name)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        os.unlink(self.filename)


def test_create_object(bigrest_root):
    data = {'name': 'pytest_pool'}
    pool = bigrest_root.create('/mgmt/tm/ltm/pool', data)
    assert pool.properties.get('name') == 'pytest_pool'


def test_exists_object(bigrest_root):
    assert bigrest_root.exist('/mgmt/tm/ltm/pool/pytest_pool') is True


def test_load_object(bigrest_root):
    pool = bigrest_root.load('/mgmt/tm/ltm/pool/pytest_pool')
    assert pool.properties.get('name') == 'pytest_pool'


def test_modify_object(bigrest_root):
    pool = bigrest_root.load('/mgmt/tm/ltm/pool/pytest_pool')
    assert pool.properties.get('description') is None
    pool_update = bigrest_root.modify('/mgmt/tm/ltm/pool/pytest_pool', {'description': 'bigrest testing'})
    assert pool_update.properties.get('description') == 'bigrest testing'
    assert pool.properties.get('description') != pool_update.properties.get('description')


def test_show_object(bigrest_root):
    pool_show = bigrest_root.show('/mgmt/tm/ltm/pool/pytest_pool')
    assert pool_show.properties.get('status.enabledState').get('description') == 'enabled'


def test_delete_object(bigrest_root):
    assert bigrest_root.exist('/mgmt/tm/ltm/pool/pytest_pool') is True
    bigrest_root.delete('/mgmt/tm/ltm/pool/pytest_pool')
    assert bigrest_root.exist('/mgmt/tm/ltm/pool/pytest_pool') is False


def test_save_object(bigrest_root):
    dns = bigrest_root.load('/mgmt/tm/sys/dns')
    assert dns.properties.get('nameServers') is None
    dns.properties['nameServers'] = ['1.1.1.1', '8.8.8.8']
    dns = bigrest_root.save(dns)
    assert dns.properties.get('nameServers') == ['1.1.1.1', '8.8.8.8']
    dns_update = bigrest_root.load('/mgmt/tm/sys/dns')
    assert dns_update.properties.get('nameServers') == ['1.1.1.1', '8.8.8.8']
    dns_update.properties.pop('nameServers')
    dns_update = bigrest_root.save(dns_update)
    assert dns_update.properties.get('nameServers') is None


def test_example_object(bigrest_root):
    example = bigrest_root.example('/mgmt/tm/ltm/rule')
    assert 'The application service' in example.properties.get('items')[0].get('propertyDescriptions').get('appService')


def test_upload_command_download(bigrest_root):
    with TstFileContent(mergefile) as f:
        bigrest_root.upload('/mgmt/shared/file-transfer/uploads/', f.filename)
        ls = bigrest_root.command('/mgmt/tm/util/bash',
                                  {'command': 'run', 'utilCmdArgs': '-c "ls /var/config/rest/downloads"'})
        assert f.basename in ls

        result = bigrest_root.command('/mgmt/tm/util/bash',
                                      {'command': 'run', 'utilCmdArgs': f'-c "mv /var/config/rest/downloads/{f.basename} /shared/images/"'})
        assert result == ''

        bigrest_root.download('/mgmt/cm/autodeploy/software-image-downloads/', f.basename)
        assert os.path.isfile(f.basename) is True
        os.remove(f.basename)
        assert os.path.isfile(f.basename) is False

        result = bigrest_root.command('/mgmt/tm/util/bash',
                                         {'command': 'run',
                                          'utilCmdArgs': f'-c "rm -rf /shared/images/{f.basename}"'})
        assert result == ''


# def test_async_task_bigip(bigrest_root):
#     pass
#
#
# def test_transaction_bigip(bigrest_root):
#     pass
