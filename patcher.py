from pwn import *
import sys
import json

out_file = ''
in_file = ''
patch_config = ''


class patcher:
    # type = [ 'TEXT', 'SYMTAB', 'HIJACK']
    # data_type = [ 'ASM', 'BYTE', ]

    """
    patch = {
        element = [
        ]
    }

    element = {
        'type': 'TEXT'
        'offset': offset (hex)
        'data_type': data_type (string)
        'data': byte string (string)
        'padding': one byte (string, Must NONPRINTABLE style)
        'padding_length': how many byte padding (hex)
    }
    element = {
        'type': 'SYMTAB'
        'symbol': sym_name (string)
        'data_type': data_type (string)
        'data': byte string (string)
    }
    element = {
        'type': 'HIJACK'
        'trampoline_offset': (hex)
        'target_offset': (hex)
        'data_type': data_type (string)
        'data': byte string (string)
        'padding': one byte (NONPRINTABLE, for target_offset !!! )
        'padding_length': (hex)
    }
    """

    def __init__(self, elf, config):
        self.in_elf = ELF(elf)
        self.config = json.load(open(config))
        context.arch = self.in_elf.arch

    def patch_padding(self, addr, byte, length):
        padding = byte*length
        print(padding)
        self.in_elf.write(addr, padding)


    def patch_addr(self, addr, element):
        patch_type = str(element['data_type'])
        patch = ''

        if patch_type == 'ASM':
            patch = asm(str(element['data']))
        elif patch_type == 'BYTE':
            patch = element['data'].decode('string_escape')


        # write patch code
        patch_len = len(patch)
        self.in_elf.write(addr, patch)

        return patch_len

    """
    # Given offset of ELF, and patch it
    """
    def patch_TEXT(self, element):
        addr = int(element['offset'], 16)
        padding_len = int(element['padding_length'], 16)
        patched_length = self.patch_addr(addr, element)
        if padding_len > 0:
            byte = element['padding'].decode('string_escape')
            self.patch_padding(addr+patched_length, byte, padding_len)

    """
    # Pick up first found string in ELF
    # and replace it.
    """
    def patch_SYMTAB(self, element):
        symbol = str(element['symbol'])
        addr = list(self.in_elf.search(symbol))
        if addr != []:
            self.patch_addr(addr[0], element)
        else:
            raise Exception('Can not found string %s' % symbol)

    def patch_HIJACK(self, element):
        trampoline_addr = int(element['trampoline_offset'], 16)
        target_addr = int(element['target_offset'], 16)
        patched_length = self.patch_addr(trampoline_addr, element)
        padding_len = int(element['padding_length'], 16)

        # jump back
        jmp_back_addr = trampoline_addr + patched_length
        jmp_offset = target_addr+5 - (jmp_back_addr+5)
        self.in_elf.write(jmp_back_addr, '\xe9' + struct.pack('<i', jmp_offset))

        # jump entry
        jmp_offset = trampoline_addr - (target_addr+5)
        self.in_elf.write(target_addr, '\xe9' + struct.pack('<i', jmp_offset))

        if padding_len > 0:
            byte = element['padding'].decode('string_escape')
            self.patch_padding(target_addr+5, byte, padding_len)


    def patch(self):
        for element in self.config['element']:
            if element['type'] == 'TEXT':
                self.patch_TEXT(element)
            elif element['type'] == 'SYMTAB':
                self.patch_SYMTAB(element)
            elif element['type'] == 'HIJACK':
                self.patch_HIJACK(element)



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

