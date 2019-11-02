# Simple Patcher

### launch
```
$ python -i=input -o=output -config=config
```

### config format
```
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
    'padding': one byte (string, Must NONPRINTABLE style)
    'padding_length': how many byte padding (hex)
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
            "data_type": "PRINTABLE",
            "data": "isnan",
            "padding": "\\x00",
            "padding_length": "1"
        }
    ]
}
```
