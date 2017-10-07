pdf417as_str
============

PDF417 barcode font and encoder for it.

===================  ===========================================
Python version       3.3+
License              GPLv3
PyPI                 https://pypi.python.org/pypi/pdf417as_str/
===================  ===========================================

How it works
------------

1. Install font pdf417.ttf into your OS.

  ::

    https://github.com/ikvk/pdf417as_str/blob/master/font/pdf417.ttf

2. Encode your data string into special encoded strings.

  ::

    .. code-block:: python

    pdf417text = pdf417as_str.encode('https://github.com')

3. Paste encoded text into any text editor and choose pdf417.ttf font for it.

  ::

    +*pBk*uiz*Aoc*yyf*ypy*-
    +*xcE*tlu*boy*ziv*xcc*-
    +*ejA*akw*jsx*rso*eBw*-

NOTE: With some font sizes there will be empty space between rows.
It will not affect to reading barcode, but you can find suited size anyway.

Installation
------------
::

    $ pip install pdf417as_str


Authors
-------

* Original code on VisualBasic and Code PDF417 font:
  Bazin Jean-Marie, http://grandzebu.net/informatique/codbar-en/pdf417.htm

* Porting to python, writing tests:
  I'm, https://github.com/ikvk
