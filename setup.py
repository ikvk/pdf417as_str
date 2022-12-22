from distutils.core import setup

with open("README.rst", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='pdf417as-str',
    version='1.0.0',
    packages=['pdf417as_str'],
    url='https://github.com/ikvk/pdf417as_str',
    license='LGPLv3',
    long_description=long_description,
    long_description_content_type="text/x-rst",
    author='Vladimir Kaukin',
    author_email='KaukinVK@ya.ru',
    keywords=['pdf417', 'font', 'barcode', 'generate', 'noimage', 'python'],
    description='Create pdf417 barcode by special font without using images',
)
