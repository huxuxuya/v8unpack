from ..version import __version__
from .. import helper
from ..MetaObject import MetaObject
from ..ext_exception import ExtException


class ExternalDataProcessor(MetaObject):

    def __init__(self):
        super(ExternalDataProcessor, self).__init__()
        self.data = None

    @classmethod
    def decode(cls, src_dir, dest_dir, *, version=None, parent_type=None):
        self = cls()
        self.header = {}
        self.data = {}
        root = helper.brace_file_read(src_dir, 'root')
        self.header["file_uuid"] = root[0][1]
        _header_data = helper.brace_file_read(src_dir, f'{self.header["file_uuid"]}')
        self.set_header_data(_header_data)

        root = helper.brace_file_read(src_dir, 'root')
        self.header['v8unpack'] = __version__
        self.header['file_uuid'] = root[0][1]
        self.data['version'] = helper.brace_file_read(src_dir, 'version')
        self.header['versions'] = helper.brace_file_read(src_dir, 'versions')
        self.data['copyinfo'] = helper.brace_file_read(src_dir, 'copyinfo')

        try:
            form1 = helper.brace_file_read(src_dir, f'{self.header["uuid"]}.1')
        except FileNotFoundError:
            form1 = None

        self.data['form1'] = form1

        self.decode_code(src_dir)
        pass
        _file_name = self.get_class_name_without_version()
        helper.json_write(self.header, dest_dir, f'{_file_name}.json')
        helper.json_write(self.data, dest_dir, f'{_file_name}.data{self.version}.json')
        self.write_decode_code(dest_dir, 'ExternalDataProcessor')

        tasks = self.decode_includes(src_dir, dest_dir, '', self.header['data'])
        return self, tasks
        # helper.run_in_pool(self.decode_include, tasks, pool)
        pass

    @classmethod
    def get_decode_includes(cls, header_data):
        return [header_data[0][3][1]]

    @classmethod
    def get_decode_header(cls, header_data):
        return header_data[0][3][1][1][3][1]

    @classmethod
    def encode(cls, src_dir, dest_dir, *, version=None, file_name=None, **kwargs):
        try:
            self = cls()
            helper.clear_dir(dest_dir)
            _file_name = self.get_class_name_without_version()
            self.header = helper.json_read(src_dir, f'{_file_name}.json')
            helper.check_version(__version__, self.header.get('v8unpack', ''))
            try:
                self.data = helper.json_read(src_dir, f'{_file_name}.data{self.version}.json')
            except FileNotFoundError:
                self.data = self.encode_empty_data()

            self.set_product_info(src_dir, file_name)

            helper.brace_file_write(self.encode_root(), dest_dir, 'root')
            helper.brace_file_write(self.encode_version(), dest_dir, 'version')
            helper.brace_file_write(self.header['versions'], dest_dir, 'versions')
            helper.brace_file_write(self.data['copyinfo'], dest_dir, 'copyinfo')
            helper.brace_file_write(self.header['data'], dest_dir, self.header["file_uuid"])
            if self.data.get('form1'):
                helper.brace_file_write(self.data['form1'], dest_dir, f'{self.header["uuid"]}.1')
            self.encode_code(src_dir, 'ExternalDataProcessor')
            self.write_encode_code(dest_dir)
            tasks = self.encode_includes(src_dir, file_name, dest_dir, version)
            return tasks
        except Exception as err:
            raise ExtException(parent=err)

    def encode_root(self):
        return [[
            "2",
            self.header["file_uuid"],
            ""
        ]]

    def encode_empty_data(self):
        return {
            "copyinfo": [
                [
                    "4",
                    [
                        "0"
                    ],
                    [
                        "0"
                    ],
                    [
                        "0"
                    ],
                    [
                        "0",
                        "0"
                    ],
                    [
                        "0"
                    ]
                ]
            ]
        }
