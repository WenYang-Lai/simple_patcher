# Simple Patcher

### launch
```
$ python patcher.py -i=input -o=output -config=config
```

### config
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
    'offset': offset (hex)
    'data_type': data_type (string)
    'data': byte string (string)
    'padding': one byte (string, Must NONPRINTABLE style)
    'padding_length': how many byte padding (hex)
}
"""

```
