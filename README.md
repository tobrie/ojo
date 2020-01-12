# ojo
Ojo watches websites and notifies you when they change. Either via [Telegram](https://telegram.org/) or via an rss feed served by ojo (not yet implemented). It is also possible to use [XPaths](https://en.wikipedia.org/wiki/XPath) to only watch a subelement.

## Installation
Install the required python packages
```bash
pip install -r ojo/requirements.txt
```

Configure telegram (Optional)
```bash
export TG_TOKEN="12345678" # <- bot token
export TG_CHATID="" # <- chat_id from the Telegram API
```

Run it
```bash
python -m ojo 
```

## Adding websites
```bash
python -m ojo add
```
Or better yet, use an sqlite editor.

## Finding XPaths
XPaths can can be obtained with most modern browsers as follows
1. Press Ctrl+Shift+C
2. Select the element whose XPath you need
3. In the element inspector right click on the highlighted element and select "Copy" > "XPath"
Most XPaths can however be a simplified and thus become more robust to changes in the page structure.

Example: To be notified when the [xkcd webcomic](https://xkcd.com)'s title changes, you can use the combination of "https://xkcd.com" (the url) and "//div[@id='ctitle']" (an XPath to the title).

This code is experimental. Feel free to improve.
