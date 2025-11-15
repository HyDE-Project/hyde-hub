#!/usr/bin/env python

# !/usr/bin/env bash
# -*- coding: utf-8 -*-
'''exec' "${XDG_STATE_HOME:-$HOME/.local/state}/hyde/pip_env/bin/python" "$0" "$@"
' '''

import os
import json
import sys

DEBUG_MODE = "--debug" in sys.argv
if DEBUG_MODE:
    from loguru import logger
    logger.remove()
    logger.add(
        sys.stderr, 
        level="DEBUG", 
        format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | <cyan>{message}</cyan>",
        colorize=True
    )
    sys.argv.remove("--debug")
else:
    class MockLogger:
        def debug(self, msg): pass
        def info(self, msg): pass
        def error(self, msg): pass
    logger = MockLogger()

def get_cache_path():
    runtime_dir = os.environ.get("XDG_RUNTIME_DIR", "/tmp")
    return os.path.join(runtime_dir, "zenquotes_cache.json")

def is_cache_valid(cache_path):
    if not os.path.exists(cache_path):
        logger.debug(f"Cache file does not exist: {cache_path}")
        return False
    try:
        with open(cache_path, "r") as f:
            data = json.load(f)
        import datetime
        today = datetime.date.today().isoformat()
        is_valid = data.get("date") == today
        logger.debug(f"Cache validation: {is_valid} (cached: {data.get('date')}, today: {today})")
        return is_valid
    except Exception as e:
        logger.debug(f"Cache validation failed: {e}")
        return False

def load_quotes_from_cache(cache_path):
    with open(cache_path, "r") as f:
        return json.load(f).get("quotes", [])

def save_quotes_to_cache(cache_path, quotes):
    import datetime
    cache_data = {
        "date": datetime.date.today().isoformat(),
        "quotes": quotes
    }
    with open(cache_path, "w") as f:
        json.dump(cache_data, f, indent=2)

def fetch_quotes_from_api():
    import requests
    logger.debug("Fetching quotes from API")
    try:
        response = requests.get("https://zenquotes.io/api/quotes", timeout=10)
        response.raise_for_status()
        quotes = [f'{item["q"]} - {item["a"]}' for item in response.json()]
        logger.debug(f"Fetched {len(quotes)} quotes")
        return quotes
    except requests.RequestException as e:
        logger.error(f"API request failed: {e}")
        return []

def get_daily_quote(quotes):
    if not quotes:
        return None
    import datetime
    day_of_year = datetime.date.today().timetuple().tm_yday
    return quotes[day_of_year % len(quotes)]

def get_random_quote(quotes):
    import random
    return random.choice(quotes) if quotes else None

def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("today", "random"):
        print("Usage: zenquotes.py [today|random]")
        sys.exit(1)

    mode = sys.argv[1]
    cache_path = get_cache_path()

    if is_cache_valid(cache_path):
        quotes = load_quotes_from_cache(cache_path)
    else:
        logger.info("Fetching fresh quotes from ZenQuotes API...")
        quotes = fetch_quotes_from_api()
        if quotes:
            save_quotes_to_cache(cache_path, quotes)
        else:
            logger.error("Failed to fetch quotes and no valid cache found")
            sys.exit(1)

    quote = get_daily_quote(quotes) if mode == "today" else get_random_quote(quotes)
    
    if quote:
        print(quote)
    else:
        logger.error("No quotes available after processing")
        sys.exit(1)

if __name__ == "__main__":
    main()
