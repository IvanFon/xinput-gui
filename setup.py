from distutils.core import setup

setup(
    name='xinput-gui',
    version='0.1.1',
    description='A simple GUI for Xorg\'s Xinput tool.',
    author='Ivan Fonseca',
    author_email='ivanfon@riseup.net',
    url='https://github.com/IvanFon/xinput-gui',
    license='GPL3',
    packages=['src'],
    scripts=['xinput-gui'],
    data_files=[('share/xinput-gui', ['xinput.ui'])]
)
