""" 
Generate a Typed Array binary file for js from a cin file,
    the first to forth compositionis can be 30 keys,
    the fifth composition can only be 7 key, 
    the fifth compositions greater than 7, will reduce to 7.

    gen_data is to generate the binary file for a normal cin table with js char code
    gen_quick_data is to generate the binary file for a quick cin table with js char code

    cin_file_name is record the compositions, chinese word, and the js char code,
    as following formate:
    '
    .aad    行    34892
    '

    cin_file_name is record the compositions, chinese word, and the js char code,
    as following formate:
    '
    aa    二元武□□□次□□□    20108,20803,27494,9633,9633,9633,27425,9633,9633,9633

    '

    db_file_name and db_quick_file_name are file path for output database.
"""
fifth_key_list = ['i']
composition_keys = 'qwertyuiopasdfghjkl;zxcvbnm,./'
cin_file_name = "./JsCharCode.txt"
db_file_name = "./ar30.data"
quick_cin_file_name = "./JsCharCode_quick.txt"
quick_db_file_name = "./ar30_quick.data"

def gen_data():
    fin = open(cin_file_name, "r")
    fout = open(db_file_name, "wb")
    for line in fin:
        key, word, value = line.strip().split('\t')
        fout.write(bytes(gen_key(key)))
        fout.write(int(value).to_bytes(2, byteorder='little'))
    fin.close()
    fout.close()

def gen_quick_data():
    fin = open(quick_cin_file_name, "r")
    fout = open(quick_db_file_name, "wb")
    for line in fin:
        key, word, values = line.strip().split('\t')
        fout.write( bytes( gen_key(key)[:2]))
        for value in values.split(','):
            #  replace the char code of empty word (□) to zero
            value_int = 0 if value == '9633' else int(value)
            fout.write(int(value).to_bytes(2, byteorder='little'))
    fin.close()
    fout.close()


def gen_key(compositions):
    """Generate the compositions to a three bytes Key"""
    if len(compositions) > 5:
        raise "Composition can NOT greater than five."
    five_key_code = 0
    if len(compositions) == 5:
        five_key_code = five_key_to_num(compositions[4])
        compositions = compositions[0:4]
    for i in range(4 - len(compositions)):
        compositions += ' '
    first_and_secode = (key_to_num(compositions[0]) + key_to_num(compositions[1]) *32 ) 
    first_byte = first_and_secode & 255    
    second_byte = ( first_and_secode & 768 ) >> 8
    second_byte = second_byte | ( key_to_num(compositions[2]) * 8 )
    third_byte = key_to_num(compositions[3]) | five_key_code * 32
    return first_byte, second_byte, third_byte
    


def key_to_num(key):
    """key in QWERT keboard translate to number"""
    keys = composition_keys
    for i, k in enumerate(keys, 1):
        if key == k:
            return i
    return 0 if key == ' ' else 7

def five_key_to_num(key):
    """The five key index for fifth_key_list,"""
    if key not in fifth_key_list:
       return 0
    else:
       return fifth_key_list.index(key) + 1
       
if __name__ == '__main__':
    print('Starting Test...')
    print('-' * 30)

    print('Test', 'key_to_num', sep='\t')
    assert key_to_num('q') == 1, 'q != 1'
    assert key_to_num('b') == 25, 'b != 25'
    assert key_to_num(' ') == 0, '" " != 0'
    print('{:>30}'.format('pass'))
    print('-' * 30)

    print('Test', 'five_key_to_num',  sep='\t')
    assert len(fifth_key_list) < 7, "The 5th composition only can spesific 6 Key"
    for i, ch in enumerate(fifth_key_list, 1):
        assert five_key_to_num(ch) == i, 'Five Key Error: ' + ch
    assert five_key_to_num(' ') == 0, 'Five Key Error: ' +  "' '"
    print('{:>30}'.format('pass'))
    print('-' * 30)
    
    print('Test', 'gen_key',  sep='\t')
    assert gen_key('') == (0,0,0), "gen_key ' ' error."
    assert gen_key('abcd') == (43, 187, 13), "gen_key 'abcd' error."
    if fifth_key_list:
        assert gen_key('ovke' + fifth_key_list[0]) == (9, 147, 35), "gen_key 'ovkei' error."
    print('{:>30}'.format('pass'))
    print('-' * 30)
