__all__ = [
    'PY25', 'ez_setup'
]

import sys

PY25 = sys.version_info[0] == 2 and sys.version_info[1] == 5

if PY25:
    import ez_setup_py25 as ez_setup
