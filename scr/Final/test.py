import pytest
import os
from dparser import Parser

def test_telegram_bot_token_is_exists():
    assert os.getenv('YOUR_TELEGRAM_BOT_TOKEN', "") != ""

if __name__ == '__main__':
    main()
