import os
import shutil

from app.res import Const

datas = {}


def add_data(src, dest):
    if os.path.exists(src):
        datas[src] = dest


# reset dist directory.
shutil.rmtree('./build', ignore_errors=True)
shutil.rmtree('./dist', ignore_errors=True)

add_data('./app/res/libs/adb', './app/res/libs')

data_str = ''
for k, v in datas.items():
    data_str += ' \\\n\t'
    data_str += '--add-data "%s:%s"' % (k, v)

pyi_cmd = 'pyinstaller -F -w -n "%s" %s \\\n__main__.py' % (Const.app_name, data_str)
print(pyi_cmd)
os.system(pyi_cmd)
os.unlink('./%s.spec' % Const.app_name)
shutil.rmtree('./build', ignore_errors=True)
