import subprocess
import sys
from typing import Optional


class PackageManager:
    """パッケージを管理するクラス"""
    default_packages = {'ab', 'ap', 'app', 'apschedule', 'arra', 'as', 'asynci', 'asyncio', 'atexi', 'base6',
                        'binasci', 'bisec', 'builtin', 'bz', 'calenda', 'certif', 'certifi', 'charde', 'chardet',
                        'clic', 'click', 'codec', 'collection', 'collections', 'colorsy', 'concurren', 'concurrent',
                        'configparse', 'contextli', 'contextvar', 'cop', 'copyre', 'cs', 'cython_runtim', 'dataclasse',
                        'datetim', 'decima', 'di', 'emai', 'email', 'encoding', 'encodings', 'enu', 'errn', 'fastap',
                        'fnmatc', 'functool', 'genericpat', 'glo', 'gr', 'greenle', 'greenlet', 'h1', 'h11', 'hashli',
                        'heap', 'hma', 'htm', 'html', 'htt', 'http', 'i', 'idn', 'idna', 'importli', 'importlib',
                        'inspec', 'ipaddres', 'itertool', 'jinja', 'jso', 'json', 'jw', 'jwt', 'keywor', 'linecach',
                        'local', 'loggin', 'logging', 'logur', 'lzm', 'mai', 'multiprocessin',
                        'markupsaf', 'markupsafe', 'marsha', 'mat', 'mimetype', 'multipar', 'multipart',
                        'multiprocessing', 'ntpat', 'number', 'o', 'opcod', 'operato', 'os', 'pathli', 'pickl',
                        'pkg_resource', 'pyexpa', 'runp', 'tzlocal', 'u',
                        'pkg_resources', 'pkguti', 'platfor', 'plistli', 'posi', 'posixpat', 'pprin', 'pw', 'pydanti',
                        'pyexpat', 'pyt', 'pytz', 'queu', 'quopr', 'r', 'rando', 'reprli', 'request', 'requests',
                        'selec', 'selector', 'shle', 'shuti', 'si', 'signa', 'sit', 'socke', 'socketserve', 'sqlalchem',
                        'sqlite', 'sqlite3', 'sre_compil', 'sre_constant', 'sre_pars', 'ss', 'sta', 'starlett', 'strin',
                        'stringpre', 'struc', 'subproces', 'sy', 'sysconfi', 'tempfil', 'textwra', 'threadin', 'tim',
                        'toke', 'tokeniz', 'tracebac', 'type', 'typin', 'typing', 'typing_extension', 'tzloca',
                        'unicodedat', 'urlli', 'urllib', 'urllib3', 'uui', 'uvicor', 'warning', 'weakre', 'xm', 'xml',
                        'yam', 'yaml', 'zipfil', 'zipimpor', 'zli', "ctype", "ctypes", "nump", "secret",
                        "six", "panda", "mma", "g", "gzi", "cmat", "dateuti", "dateutil", }

    @staticmethod
    def get_packages_set() -> set:
        rt = set()
        ls = list(sys.modules.keys())
        for i in ls:
            if i[0] != '_':
                ele = i[:i.find('.')]
                if ele in PackageManager.default_packages:
                    continue
                rt.add(ele)
        return rt

    @staticmethod
    def install_package(package: str, imp_str: Optional[str] = None):
        """パッケージを動的インストールする"""
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        if imp_str is None:
            exec('import ' + package)
        else:
            exec('import ' + imp_str)
