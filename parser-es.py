import feedparser
import datetime
import os
import pytz
import func_timeout

def parseFeed(url, author, homeURL, parseDate, globalFeed):
    d = feedparser.parse(url)
    for entry in d.entries:
        dt = 0
        try:
            dt = datetime.datetime.strptime(entry.published, parseDate)
        except ValueError:
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
    <html lang="es">
    <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Agregador de noticias sobre Linux y software libre, sin Javascript">
    <title>Español - RS1 Linux News</title>
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
    <div class="language-bar-item item-active">
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
    <div class="language-bar-item">
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
    <a href="/es/">NEWS</a>
    </div>
    <div class="topic-bar-item">
    <a href="/es/videos/">VIDEOS</a>
    </div>
    <div class="topic-bar-item">
    <a href="/es/more/">MORE</a>
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
    <html lang="es">
    <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Agregador de noticias sobre Linux y software libre, sin Javascript">
    <title>Videos (Español) - RS1 Linux News</title>
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
    <div class="language-bar-item item-active">
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
    <div class="language-bar-item">
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
    <a href="/es/">NEWS</a>
    </div>
    <div class="topic-bar-item item-active">
    <a href="/es/videos/">VIDEOS</a>
    </div>
    <div class="topic-bar-item">
    <a href="/es/more/">MORE</a>
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
    <html lang="es">
    <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Agregador de noticias sobre Linux y software libre, sin Javascript">
    <title>More (Español) - RS1 Linux News</title>
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
    <div class="language-bar-item item-active">
    <a href="/es/more/">ES</a>
    </div>
    <div class="language-bar-item">
    <a href="/de/more/">DE</a>
    </div>
    <div class="language-bar-item other-div">
    <span>...</span>
    <div class="other-languages">
    <div class="language-bar-item no-hover">
    <span>&nbsp;</span>
    </div>
    <div class="language-bar-item">
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
    <a href="/es/">NEWS</a>
    </div>
    <div class="topic-bar-item">
    <a href="/es/videos/">VIDEOS</a>
    </div>
    <div class="topic-bar-item item-active">
    <a href="/es/more/">MORE</a>
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
    ["https://feeds.feedburner.com/desdelinuxweb", "Desde Linux", "https://desdelinux.net/", "%a, %d %b %Y %H:%M:%S %z"],
    ["https://elpinguinotolkiano.wordpress.com/feed/", "El Pingüino Tolkiano", "https://elpinguinotolkiano.wordpress.com", "%a, %d %b %Y %H:%M:%S %z"],
    ["https://h4ckseed.wordpress.com/feed/", "h4ckseed", "https://h4ckseed.wordpress.com/", "%a, %d %b %Y %H:%M:%S %z"],
    ["https://feeds.feedburner.com/LinuxAdictos", "Linux Adictos", "https://www.linuxadictos.com/", "%a, %d %b %Y %H:%M:%S %z"],
    ["https://www.muylinux.com/feed/", "MuyLinux", "https://www.muylinux.com/", "%a, %d %b %Y %H:%M:%S %z"],
    ["https://victorhckinthefreeworld.com/feed/", "Victorhck in the free world", "https://victorhckinthefreeworld.com/", "%a, %d %b %Y %H:%M:%S %z"],
    ["https://nksistemas.com/feed/", "NKSistemas", "https://nksistemas.com/", "%a, %d %b %Y %H:%M:%S %z"],
    ["https://www.kdeblog.com/feed", "KDE Blog", "https://www.kdeblog.com/", "%a, %d %b %Y %H:%M:%S %z"],
    ["https://www.linuxparty.es/?format=feed&type=rss", "LinuxParty", "https://www.linuxparty.es/", "%a, %d %b %Y %H:%M:%S %z"],
    ["https://laboratoriolinux.es/?format=feed&type=rss", "Laboratorio Linux", "https://laboratoriolinux.es/", "%a, %d %b %Y %H:%M:%S %z"],
    ["https://feeds.feedburner.com/ubunlog", "Ubunlog", "https://ubunlog.com/", "%a, %d %b %Y %H:%M:%S %z"]
]


#VIDEOS
videosFeedsInfo = [
    ["https://odysee.com/$/rss/@manosymaquinasentrevideos:6", "Manos y Máquinas Entre Vídeos", "https://odysee.com/@manosymaquinasentrevideos:6", "%a, %d %b %Y %H:%M:%S %Z"],
    ["https://fediverse.tv/feeds/videos.xml?videoChannelId=19129", "Atareao (Vídeos)", "https://fediverse.tv/c/atareao/videos", "%a, %d %b %Y %H:%M:%S %Z"],
    ["https://fediverse.tv/feeds/videos.xml?accountId=132878", "MAINKIVI (Vídeos)", "https://fediverse.tv/a/mainkivi/videos", "%a, %d %b %Y %H:%M:%S %Z"],
    ["https://fediverse.tv/feeds/videos.xml?videoChannelId=22590", "Dani Sánchez", "https://fediverse.tv/c/danisanchez.net/videos", "%a, %d %b %Y %H:%M:%S %Z"],
    ["https://www.youtube.com/feeds/videos.xml?channel_id=UC6ImDlcMZukA-pqtIaXqbdA", "Cumpi Linux", "https://cumpi.ga/", "%Y-%m-%dT%H:%M:%S%z"],
    ["https://www.youtube.com/feeds/videos.xml?channel_id=UCl8XUDjAOLc7GNKcDp9Nepg", "Locos por Linux", "https://www.youtube.com/@LocosporLinux/videos", "%Y-%m-%dT%H:%M:%S%z"],
    ["https://www.youtube.com/feeds/videos.xml?channel_id=UCFRuGs1rZJ4oAaLsAjypt7A", "Desde Linux con Amor", "https://www.youtube.com/@DesdeLinuxConAmor/videos", "%Y-%m-%dT%H:%M:%S%z"],
    ["https://www.youtube.com/feeds/videos.xml?channel_id=UCFnFYB2mWAdVwA7Q94AaLPA", "Linux en Casa", "https://www.youtube.com/@LinuxenCasa/videos", "%Y-%m-%dT%H:%M:%S%z"],
    ["https://www.youtube.com/feeds/videos.xml?channel_id=UCgErca6xmDIcaHDnVghHk6w", "Nos Gusta Linux", "https://www.youtube.com/@nosgustalinux/videos", "%Y-%m-%dT%H:%M:%S%z"],
    ["https://www.youtube.com/feeds/videos.xml?channel_id=UCta4Iy4TzMx8Xo0pwpkbWgg", "PatoJAD", "https://www.youtube.com/@PatoJAD/videos", "%Y-%m-%dT%H:%M:%S%z"]
]

#MORE
moreFeedsInfo = [
    ["https://voidnull.es/rss/", "voidNull", "https://voidnull.es/", "%a, %d %b %Y %H:%M:%S %z"],
    ["https://www.ochobitshacenunbyte.com/feed/", "ochobitshacenunbyte", "https://www.ochobitshacenunbyte.com/", "%a, %d %b %Y %H:%M:%S %z"],
    ["https://podcastlinux.com/feed", "Podcast Linux", "https://podcastlinux.com/", "%a, %d %b %Y %H:%M:%S %Z"],
    ["https://mainkivi.info/wordpress/blog/feed/", "MAINKIVI", "https://mainkivi.info/wordpress/blog/", "%a, %d %b %Y %H:%M:%S %z"],
    ["https://ugeek.github.io/feed.xml", "Blog Podcast uGeek", "https://ugeek.github.io/", "%a, %d %b %Y %H:%M %z"],
    ["https://elblogdelazaro.org/index.xml", "El Blog de Lázaro", "https://elblogdelazaro.org/", "%a, %d %b %Y %H:%M:%S %z"],
    ["https://atareao.es/feed/", "Atareao", "https://atareao.es/", "%a, %d %b %Y %H:%M:%S %z"],
    ["https://salmorejogeek.com/feed/", "Salmorejo Geek", "https://salmorejogeek.com/", "%a, %d %b %Y %H:%M:%S %z"],
    ["https://elbinario.net/feed/", "Elbinario", "https://elbinario.net/", "%a, %d %b %Y %H:%M:%S %z"],
    ["https://ubuntuperonista.blogspot.com/feeds/posts/default", "Ubuntu Peronista", "https://ubuntuperonista.blogspot.com/", "%Y-%m-%dT%H:%M:%S.%f%z"],
    ["https://martinezmartinez.eu/feed/", "Blog de informática", "https://martinezmartinez.eu/", "%a, %d %b %Y %H:%M:%S %z"],
    ["https://feeds.feedburner.com/geeklandlinux", "geekland", "https://geekland.eu/", "%a, %d %b %Y %H:%M:%S %z"],
    ["https://myblog.clonbg.es/feedClonbg_es.xml", "Blog de Clonbg", "https://myblog.clonbg.es/", "%a, %d %b %Y %H:%M:%S %z"],
    ["https://cambiatealinux.com/rss", "Cambiate a Linux", "https://cambiatealinux.com/", "%a, %d %b %Y %H:%M:%S %z"],
    ["https://www.bujarra.com/feed/", "Blog Bujarra.com", "https://www.bujarra.com/", "%a, %d %b %Y %H:%M:%S %z"],
    ["https://56k.es/feed/", "56K", "https://56k.es/", "%a, %d %b %Y %H:%M:%S %z"]
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

mainProcess("news", newsFeedsInfo, newsFeeds, "./public/es")
mainProcess("videos", videosFeedsInfo, videosFeeds, "./public/es/videos")
mainProcess("more", moreFeedsInfo, moreFeeds, "./public/es/more")

#testParse("https://www.omgubuntu.co.uk/feed")
