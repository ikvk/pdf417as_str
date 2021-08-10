pdf417as_str
============

Create pdf417 barcode without using images.

===================  ===========================================
Python version       3.3+
License              LGPLv3
PyPI                 https://pypi.python.org/pypi/pdf417as_str/
===================  ===========================================

How it works
------------

1. Install font `pdf417.ttf <https://github.com/ikvk/pdf417as_str/raw/master/font/pdf417.ttf>`_ into your OS.

2. Encode your data string into special encoded strings.

.. code-block:: python

    pdf417_encoded_text = pdf417as_str.encode('https://github.com')

3. Paste encoded text into any text editor and choose "Code PDF417" font. You will receive pdf417 barcode.

  .. image:: https://github.com/ikvk/pdf417as_str/blob/master/test/barcode.png

NOTE: With some font sizes there will be empty space between rows.
It will not affect to reading barcode, but you can find suited size anyway.

Actually you can make png barcode, using pdf417as_str.convert.to_png, but this function not efficient.

Installation
------------
::

    $ pip install pdf417as-str

Authors
-------

* `Original code <http://grandzebu.net/informatique/codbar-en/pdf417.htm>`_ on VisualBasic and "Code PDF417" font:
  `Bazin Jean-Marie <http://grandzebu.net/>`_

* Porting to python, writing tests: `I'm <https://github.com/ikvk>`_

Thanks to
---------

`pennersr <https://github.com/pennersr>`_
