# RS1 Linux News

Javascript-free Linux/open source news aggregator.

This is the source code of https://news.rs1.es. Python script parses feeds (RSS/Atom/RDF), joins them and sorts them by date. There is a script for each language.

### Required Python modules

- feedparser
- datetime
- os
- pytz
- func_timeout

### Generate pages

Simply run the python scripts (e.g.: `python parser-en.py`) periodically and upload files inside "public" to a server, a hosting service, etc.

### Contribute

Create an issue if you want to add a page. Provide the feed link.
