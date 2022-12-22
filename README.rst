pdf417as_str
============

Create pdf417 barcode by special font without using images.

.. image:: https://img.shields.io/pypi/dm/pdf417as_str.svg?style=social

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

    pdf417_encoded_text = pdf417as_str.encode417('https://github.com', columns=5)

3. Paste encoded text into any text editor.

::

    +*xfs*prA*kuk*iDo*ixA*sxn*xdw*-
    +*yog*slv*Arv*Fyg*tgE*fwg*zew*-
    +*uny*BCj*iaw*jcE*AxD*ykx*pDw*-
    +*ftw*sgf*AoC*dAc*ajb*ofA*yrx*-

4. Choose "Code PDF417" font for text and adjust line spacing. You will receive pdf417 barcode.

  .. image:: https://github.com/ikvk/pdf417as_str/blob/master/test/barcode.png

NOTE: Small empty space between rows not affects to reading barcode. Anyway you can find suited size.

Also you can make .png barcode using pdf417as_str.convert.to_png, but this function for tests and not efficient.

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
