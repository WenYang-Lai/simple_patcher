# Simple Patcher

### launch
```
$ python -i=input -o=output -config=config
```

### config format
```
# type = [ 'TEXT', 'SYMTAB', 'LJUMP']
# data_type = [ 'ASM', 'BYTE' ]

"""
patch = {
    element = [
    ]
}
element = {
    'type': type as above (string, required)
    'data_type': data_type (string, required)
    'data': byte string (string, optional)
    'data_path': path to data (string, optional)
    'padding': one byte (string, Must NONPRINTABLE style, required)
    'padding_length': how many byte padding (hex, required)
}
"""
```

### config sample
```
{
    "element": [
        {
            "type": "TEXT",
            "offset": "0xb00",
            "data_type": "ASM",
            "data": "push rdi\npush rsi",
            "padding": "\\x00",
            "padding_length": "1"
        },
        {
            "type": "SYMTAB",
            "symbol": "prctl",
            "offset": "0",
            "data_type": "BYTE",
            "data": "isnan",
            "padding": "\\x00",
            "padding_length": "1"
        },
        {
            "type": "LJUMP",
            "trampoline_offset": "0xb1c",
            "target_offset": "0x9ab",
            "data_type": "ASM",
            "data": "push rdi\n push rax",
            "padding": "\\x00",
            "padding_length": "0"
        }
    ]
}
```
