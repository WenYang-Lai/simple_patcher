# Simple Patcher

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
        'padding': one byte (string)
        'padding_length': how many byte padding (hex)
    }
    """

```
