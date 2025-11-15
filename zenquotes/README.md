ZenQuotes Helper
=================

`zenqoutes.py` fetches quotes from the [ZenQuotes API](https://zenquotes.io/) and prints either the quote of the day or a random entry. Quotes are cached locally for the current day so repeated calls stay fast and offline-friendly.

Installation
------------

1. Copy `zenqoutes.py` into your Hyde scripts directory:
	 - If `$XDG_CONFIG_HOME` is set, use `$XDG_CONFIG_HOME/hyde/scripts`.
	 - Otherwise copy to `~/.config/hyde/scripts`.
	 - Example:

		 ```fish
		 mkdir -p ~/.config/hyde/scripts
		 cp zenqoutes.py ~/.config/hyde/scripts/zenquotes.py
		 chmod +x ~/.config/hyde/scripts/zenquotes.py
		 ```

2. Ensure the script is executable so `hyde-shell` can run it.

Usage
-----

- `hyde-shell zenquotes today` – prints the deterministic quote selected for the current day.
- `hyde-shell zenquotes random` – prints a random quote from the cached (or freshly fetched) list.
- `hyde-shell zenquotes --help` – shows the CLI usage string.

Sample
------

```
hyde-shell zenquotes today
When you have to make a choice and don't make it, that is in itself a choice. - William James

hyde-shell zenquotes --help
Usage: zenquotes.py [today|random]
```

Debug Mode
----------

Add `--debug` after the subcommand (for example `hyde-shell zenquotes today --debug`) to enable verbose logging using Loguru. Debug output goes to stderr.

Caching
-------

Quotes are cached in `zenquotes_cache.json` under `$XDG_RUNTIME_DIR` (falls back to `/tmp`). A fresh API request is only made when the cache is missing or older than the current calendar day.
