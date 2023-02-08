import feedparser
import datetime
import os
import pytz
import func_timeout

def parseFeed(url, author, homeURL, parseDate, globalFeed):
    d = feedparser.parse(url)
    for entry in d.entries:
        if author in ["TOOLinux"]:
            entry.published = entry.updated
        dt = 0
        try:
            dt = datetime.datetime.strptime(entry.published, parseDate)
        except ValueError:
            print(entry.published + " does not follow " + parseDate)
            continue
        entry.published = dt.isoformat()
        globalFeed.append([entry.title, entry.link, entry.published, author, homeURL, dt.timestamp()])

def testParse(url):
    d = feedparser.parse(url)
    for entry in d.entries:
        print(entry.title, entry.link, entry.published)

def sortFeeds(feed):
    return sorted(feed, key=lambda entry: entry[5], reverse=True)

def limitFeeds(feed):
    return feed[0:150]

def createEntries(file, entries):
    file.write("<div class=\"post-list\">\n")
    for entry in entries:
        dtentry = datetime.datetime.fromisoformat(entry[2])
        tz = pytz.timezone("UTC")
        dtentry = dtentry.astimezone(tz)
        file.write("<div class=\"post-item\">\n")
        file.write("<a target=\"_blank\" href=\"%s\">\n" %entry[1])
        file.write("<h2>%s</h2>\n" %(entry[0]))
        file.write("</a>\n")
        file.write("<a target=\"_blank\" href=\"%s\">%s</a>\n" %(entry[4], entry[3]))
        file.write("<time datetime=\"%s\">%s</time>\n" %(entry[2], dtentry.strftime('%a, %d %b %Y %H:%M')))
        file.write("</div>\n")
    file.write("</div>\n")

def createHTMLHome(file, entries):
    template1 = """<!DOCTYPE html>
    <html lang="fr">
    <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Agrégateur de nouvelles Linux/open source sans Javascript.">
    <title>Français - RS1 Linux News</title>
    <link rel="shortcut icon" href="/favicon.png" type="image/png">
    <link rel="stylesheet" href="/main.css?v=20230126_1630">
    </head>
    <body>
    <div class="topbar">
    <div class="main-title">
    <a href="/"><h1>RS1 Linux News</h1></a>
    </div>
    <div class="topbar-links">
    <div class="topbar-link-item">
    <a href="/about.html">About</a>
    </div>
    </div>
    </div>
    <div class="filter-bar">
    <div class="language-bar">
    <div class="language-bar-title">
    <span>Language:</span>
    </div>
    <div class="language-bar-item">
    <a href="/">EN</a>
    </div>
    <div class="language-bar-item">
    <a href="/es/">ES</a>
    </div>
    <div class="language-bar-item">
    <a href="/de/">DE</a>
    </div>
    <div class="language-bar-item other-div">
    <span>...</span>
    <div class="other-languages">
    <div class="language-bar-item no-hover">
    <span>&nbsp;</span>
    </div>
    <div class="language-bar-item item-active">
    <a href="/fr/">FR</a>
    </div>
    <div class="language-bar-item">
    <a href="/pt/">PT</a>
    </div>
    </div>
    </div>
    </div>
    <div class="topic-bar">
    <div class="topic-bar-title">
    <span>Topic:</span>
    </div>
    <div class="topic-bar-item item-active">
    <a href="/fr/">NEWS</a>
    </div>
    <div class="topic-bar-item">
    <a href="/fr/videos/">VIDEOS</a>
    </div>
    <div class="topic-bar-item">
    <a href="/fr/more/">MORE</a>
    </div>
    </div>
    </div>"""
    file.write(template1)
    createEntries(file, entries)
    template2 = """<footer>
    <a href="/"><h2>RS1 Linux News</h2></a>
    <div class="footer-content">
    <div>
    <p>Javascript-free Linux/open source news aggregator.</p>
    <p>Linux is a registered trademark of Linus Torvalds.</p>
    </div>
    </div>
    </footer>
    </body>
    </html>"""
    file.write(template2)

def createHTMLVideos(file, entries):
    template1 = """<!DOCTYPE html>
    <html lang="fr">
    <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Agrégateur de nouvelles Linux/open source sans Javascript.">
    <title>Videos (Français) - RS1 Linux News</title>
    <link rel="shortcut icon" href="/favicon.png" type="image/png">
    <link rel="stylesheet" href="/main.css?v=20230126_1630">
    </head>
    <body>
    <div class="topbar">
    <div class="main-title">
    <a href="/"><h1>RS1 Linux News</h1></a>
    </div>
    <div class="topbar-links">
    <div class="topbar-link-item">
    <a href="/about.html">About</a>
    </div>
    </div>
    </div>
    <div class="filter-bar">
    <div class="language-bar">
    <div class="language-bar-title">
    <span>Language:</span>
    </div>
    <div class="language-bar-item">
    <a href="/videos/">EN</a>
    </div>
    <div class="language-bar-item">
    <a href="/es/videos/">ES</a>
    </div>
    <div class="language-bar-item">
    <a href="/de/videos/">DE</a>
    </div>
    <div class="language-bar-item other-div">
    <span>...</span>
    <div class="other-languages">
    <div class="language-bar-item no-hover">
    <span>&nbsp;</span>
    </div>
    <div class="language-bar-item item-active">
    <a href="/fr/videos/">FR</a>
    </div>
    <div class="language-bar-item">
    <a href="/pt/videos/">PT</a>
    </div>
    </div>
    </div>
    </div>
    <div class="topic-bar">
    <div class="topic-bar-title">
    <span>Topic:</span>
    </div>
    <div class="topic-bar-item">
    <a href="/fr/">NEWS</a>
    </div>
    <div class="topic-bar-item item-active">
    <a href="/fr/videos/">VIDEOS</a>
    </div>
    <div class="topic-bar-item">
    <a href="/fr/more/">MORE</a>
    </div>
    </div>
    </div>"""
    file.write(template1)
    createEntries(file, entries)
    template2 = """<footer>
    <a href="/"><h2>RS1 Linux News</h2></a>
    <div class="footer-content">
    <div>
    <p>Javascript-free Linux/open source news aggregator.</p>
    <p>Linux is a registered trademark of Linus Torvalds.</p>
    </div>
    </div>
    </footer>
    </body>
    </html>"""
    file.write(template2)

def createHTMLMore(file, entries):
    template1 = """<!DOCTYPE html>
    <html lang="fr">
    <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Agrégateur de nouvelles Linux/open source sans Javascript.">
    <title>More (Français) - RS1 Linux News</title>
    <link rel="shortcut icon" href="/favicon.png" type="image/png">
    <link rel="stylesheet" href="/main.css?v=20230126_1630">
    </head>
    <body>
    <div class="topbar">
    <div class="main-title">
    <a href="/"><h1>RS1 Linux News</h1></a>
    </div>
    <div class="topbar-links">
    <div class="topbar-link-item">
    <a href="/about.html">About</a>
    </div>
    </div>
    </div>
    <div class="filter-bar">
    <div class="language-bar">
    <div class="language-bar-title">
    <span>Language:</span>
    </div>
    <div class="language-bar-item">
    <a href="/more/">EN</a>
    </div>
    <div class="language-bar-item">
    <a href="/es/more/">ES</a>
    </div>
     <div class="language-bar-item item-active">
    <a href="/de/more/">DE</a>
    </div>
    <div class="language-bar-item other-div">
    <span>...</span>
    <div class="other-languages">
    <div class="language-bar-item no-hover">
    <span>&nbsp;</span>
    </div>
    <div class="language-bar-item item-active">
    <a href="/fr/more/">FR</a>
    </div>
    <div class="language-bar-item">
    <a href="/pt/more/">PT</a>
    </div>
    </div>
    </div>
    </div>
    <div class="topic-bar">
    <div class="topic-bar-title">
    <span>Topic:</span>
    </div>
    <div class="topic-bar-item">
    <a href="/fr/">NEWS</a>
    </div>
    <div class="topic-bar-item">
    <a href="/fr/videos/">VIDEOS</a>
    </div>
    <div class="topic-bar-item item-active">
    <a href="/fr/more/">MORE</a>
    </div>
    </div>
    </div>"""
    file.write(template1)
    createEntries(file, entries)
    template2 = """<footer>
    <a href="/"><h2>RS1 Linux News</h2></a>
    <div class="footer-content">
    <div>
    <p>Javascript-free Linux/open source news aggregator.</p>
    <p>Linux is a registered trademark of Linus Torvalds.</p>
    </div>
    </div>
    </footer>
    </body>
    </html>"""
    file.write(template2)

#NEWS
newsFeedsInfo = [
    ["https://www.toolinux.com/spip.php?page=backend", "TOOLinux", "https://www.toolinux.com/", "%Y-%m-%dT%H:%M:%S%z"],
    ["https://linuxfr.org/news.atom", "LinuxFr.org", "https://linuxfr.org/", "%Y-%m-%dT%H:%M:%S%z"]
]

#VIDEOS
videosFeedsInfo = [
    ["https://www.youtube.com/feeds/videos.xml?channel_id=UCs_AZuYXi6NA9tkdbhjItHQ", "xavki", "https://www.youtube.com/channel/UCs_AZuYXi6NA9tkdbhjItHQ/videos", "%Y-%m-%dT%H:%M:%S%z"],
    ["https://www.youtube.com/feeds/videos.xml?channel_id=UCq6OWb0pyhv5qPtCINJgdxA", "LinuxInFrench", "https://www.youtube.com/channel/UCq6OWb0pyhv5qPtCINJgdxA/videos", "%Y-%m-%dT%H:%M:%S%z"],
    ["https://www.youtube.com/feeds/videos.xml?channel_id=UC5M4fqmqLNJaBey0W_ylCSA", "Actualia", "https://www.youtube.com/@Actualia66/videos", "%Y-%m-%dT%H:%M:%S%z"],
    ["https://www.youtube.com/feeds/videos.xml?channel_id=UC7VqJVFvk75-B0uKg4MWfpw", "Cardiac TuX", "https://www.youtube.com/@Cardiacman/videos", "%Y-%m-%dT%H:%M:%S%z"]

]

#MORE
moreFeedsInfo = [
    ["https://www.numetopia.fr/feed/", "Numétopia", "https://www.numetopia.fr/", "%a, %d %b %Y %H:%M:%S %z"]
]

newsFeeds = []
videosFeeds = []
moreFeeds = []

def mainProcess(section, feedInfo, joinFeed, path):
    for feed in feedInfo:
        print(feed[1])
        try:
            func_timeout.func_timeout(10, parseFeed, args=(feed[0], feed[1], feed[2], feed[3], joinFeed))
        except func_timeout.FunctionTimedOut:
            pass
    print("- %s feeds parsed -" %section)

    joinFeedSorted = sortFeeds(joinFeed)
    joinFeedSorted = limitFeeds(joinFeedSorted)

    if os.path.exists(path) == False:
        os.makedirs(path)

    htmlFile = open(path + "/index.html", "w")
    if section == "news":
        createHTMLHome(htmlFile, joinFeedSorted)
    elif section == "videos":
        createHTMLVideos(htmlFile, joinFeedSorted)
    elif section == "more":
        createHTMLMore(htmlFile, joinFeedSorted)
    htmlFile.close()
    print(path + "/index.html saved")

mainProcess("news", newsFeedsInfo, newsFeeds, "./public/fr")
mainProcess("videos", videosFeedsInfo, videosFeeds, "./public/fr/videos")
mainProcess("more", moreFeedsInfo, moreFeeds, "./public/fr/more")

#testParse("https://www.omgubuntu.co.uk/feed")
