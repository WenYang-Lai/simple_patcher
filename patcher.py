from pwn import *
import sys
import json

out_file = ''
in_file = ''
patch_config = ''


class patcher:
    # type = [ 'TEXT', 'SYMTAB' ]
    # data_type = [ 'ASM', 'PRINTABLE', 'NONPRINTABLE' ]


    """
    patch = {
        element = [

        ]
    }

    element = {
        'type': type as above (string)
        'symbol': sym_name (string)
        'context': amd64, i386, etc (string)
        'offset': offset (hex)
        'data_type': data_type (string)
        'data': byte string (string)
        'padding': one byte (string)
        'padding_length': how many byte padding (hex)
    }
    """

    def __init__(self, elf, config):
        self.in_elf = ELF(elf)
        self.config = json.load(open(config))

    def patch_TEXT(self, element):
        addr = int(element['offset'], 16)
        patch_type = str(element['data_type'])
        padding_len = int(element['padding_length'], 16)
        patch = ''

        if patch_type == 'PRINTABLE':
            patch = str(element['data'])
        elif patch_type == 'ASM':
            context.arch = str(element['context'])
            patch = asm(str(element['data']))
        elif patch_type == 'NONPRINTABLE':
            patch = element['data'].decode('string_escape')


        # write patch code
        patch_len = len(patch)
        self.in_elf.write(addr, patch)

        if padding_len > 0:
            padding = element['padding'].decode('string_escape')*padding_len
            print(padding)
            self.in_elf.write(addr+patch_len, padding)


    def patch_SYMTAB(self, element):
        raise NotImplemented()

    def patch(self):
        for element in self.config['element']:
            if element['type'] == 'TEXT':
                self.patch_TEXT(element)
            elif element['type'] == 'SYMTAB':
                self.patch_SYMTAB(element)



    def output(self, out_path):
        self.in_elf.save(out_path)


if __name__ == '__main__':
    for para in sys.argv[1:]:
        if '-i' in para:
            in_file = para[para.index('=')+1:]
            out_file = in_file + '.patched'
        elif '-config' in para:
            patch_config = para[para.index('=')+1:]
        elif '-o' in para:
            out_file = para[para.index('=')+1:]

    if in_file != '' and patch_config != '':

        p = patcher(in_file, patch_config)
        p.patch()
        p.output(out_file)

