#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_app.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Django import edilemedi. Yüklü olduğundan ve "
            "PYTHONPATH ortam değişkeninde tanımlı olduğundan emin misiniz? Sanal "
            "ortamı aktifleştirdiniz mi?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
