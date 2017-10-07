import html
import os
from random import randint
import requests
from pdf417as_str import convert
from pdf417as_str import main

# supported symbols
symbols = ' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~'

test_data = [
    (symbols, -1),
    ('ab12', 2),
    ('Transformation of each CW into a 3 characters string and addition of separators, start row character', -1),
    ('Transformation of each CW into a 3 characters string and addition of separators, start row character.', -1),
    ('.,', -1),
    ('https://wat.com/', -1),
    ('M1BYKOV/SERGEYAMR EZSTIVF SVXDMEU6 0262 304E000 0000 043>218 0000I 252625814571230', 6),
    ('M1EDEMSKIY/ANDREY EY5PRXC SVXDMEU6 0266 212Y021F0062 31C>2080 B0E 0 ', 6),
]

# random data
for i in range(100):
    test_line = ''
    # decoder cant't decode the string is 1 characters long
    part_cnt = randint(2, 10)
    for part in range(part_cnt):
        symbol = symbols[randint(0, len(symbols) - 1)]
        test_line += symbol * part_cnt
    test_data.append((test_line, randint(-1, 5)))

if __name__ == '__main__':
    error_count = 0

    res_path = 'barcodes'
    if not os.path.exists(res_path):
        os.mkdir(res_path)

    for test_i, test_value in enumerate(test_data):
        test_text = test_value[0]
        # make text code
        code = main.encode(test_value[0], test_value[1])
        # make png
        img_name = 'barcode' + str(test_i)
        image = convert.to_png(code)
        img_path = os.path.join(res_path, '{}.png'.format(img_name))
        image.save(img_path, 'png')

        # decode
        files = {'file': open(img_path, 'rb')}
        response = requests.post(url="http://zxing.org/w/decode", files=files)
        if not response.text.find('Decode Succeeded') > -1:
            print('decode failed for: {}'.format(test_text))
            break

        decoded_value_raw = response.text[response.text.find('<pre>') + 5: response.text.find('</pre>')]
        decoded_value = html.unescape(decoded_value_raw)

        if test_text == decoded_value:
            print('success: {}'.format(test_text))
        else:
            error_count += 1
            print('error:\n> 1. {0}\n> 2. {1}\n> 3. {2}'.format(test_text, decoded_value, decoded_value_raw))

    print('done, error_count = {}'.format(error_count))
