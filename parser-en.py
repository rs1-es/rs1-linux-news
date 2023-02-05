import feedparser
import datetime
import os
import pytz
import func_timeout

def parseFeed(url, author, homeURL, parseDate, globalFeed):
    d = feedparser.parse(url)
    for entry in d.entries:
        if author in ["DistroWatch", "LWN.net"]:
            entry.published = entry.updated
        dt = 0
        try:
            dt = datetime.datetime.strptime(entry.published, parseDate)
        except ValueError:
            dt = datetime.datetime.strptime(entry.published, "%Y-%m-%dT%H:%M:%S%z")
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
    <html lang="en">
    <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Javascript-free Linux/open source news aggregator">
    <title>RS1 Linux News</title>
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
    <div class="language-bar-item item-active">
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
    <a href="/">NEWS</a>
    </div>
    <div class="topic-bar-item">
    <a href="/videos/">VIDEOS</a>
    </div>
    <div class="topic-bar-item">
    <a href="/more/">MORE</a>
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
    <html lang="en">
    <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Javascript-free Linux/open source news aggregator">
    <title>Videos - RS1 Linux News</title>
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
    <div class="language-bar-item item-active">
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
    <a href="/">NEWS</a>
    </div>
    <div class="topic-bar-item item-active">
    <a href="/videos/">VIDEOS</a>
    </div>
    <div class="topic-bar-item">
    <a href="/more/">MORE</a>
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
    <html lang="en">
    <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Javascript-free Linux/open source news aggregator">
    <title>More - RS1 Linux News</title>
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
    <div class="language-bar-item item-active">
    <a href="/more/">EN</a>
    </div>
    <div class="language-bar-item">
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
    <a href="/">NEWS</a>
    </div>
    <div class="topic-bar-item">
    <a href="/videos/">VIDEOS</a>
    </div>
    <div class="topic-bar-item item-active">
    <a href="/more/">MORE</a>
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

# NEWS
newsFeedsInfo = [
    ["https://9to5linux.com/feed/atom", "9to5Linux", "https://9to5linux.com/", "%Y-%m-%dT%H:%M:%S%z"],
    ["https://linuxiac.com/feed/", "Linuxiac", "https://linuxiac.com/", "%a, %d %b %Y %H:%M:%S %z"],
    ["https://distrowatch.com/news/dw.xml", "DistroWatch", "https://distrowatch.com", "%Y-%m-%dT%H:%M:%S%z"],
    ["https://itsfoss.com/rss/", "It's FOSS", "https://itsfoss.com/", "%a, %d %b %Y %H:%M:%S %Z"],
    ["https://www.gamingonlinux.com/article_rss.php", "GamingOnLinux", "https://www.gamingonlinux.com/", "%a, %d %b %Y %H:%M:%S %z"],
    ["https://www.omgubuntu.co.uk/feed", "OMG! Ubuntu!", "https://www.omgubuntu.co.uk/", "%a, %d %b %Y %H:%M:%S %z"],
    ["https://linuxsecurity.com/linuxsecurity_articles.xml", "LinuxSecurity.com", "https://linuxsecurity.com/", "%a, %d %b %Y %H:%M:%S %z"],
    ["https://debugpointnews.com/feed/", "DebugPoint NEWS", "https://debugpointnews.com/", "%a, %d %b %Y %H:%M:%S %z"],
    ["https://www.phoronix.com/rss.php", "Phoronix", "https://www.phoronix.com/", "%a, %d %b %Y %H:%M:%S %z"],
    ["https://feeds.feedburner.com/Ubuntubuzz", "Ubuntu Buzz!", "https://www.ubuntubuzz.com/", "%Y-%m-%dT%H:%M:%S.%f%z"],
    ["https://linmob.net/feed.xml", "LINMOB.net", "https://linmob.net/", "%Y-%m-%dT%H:%M:%S%z"],
    ["https://www.linux-magazine.com/rss/feed/lmi_news", "Linux Magazine", "https://www.linux-magazine.com/", "%a, %d %b %Y %H:%M:%S %z"],
    ["https://fossforce.com/feed/", "FOSS Force", "https://fossforce.com/", "%a, %d %b %Y %H:%M:%S %z"],
    ["https://fullcirclemagazine.org/feed/", "Full Circle Magazine", "https://fullcirclemagazine.org/", "%a, %d %b %Y %H:%M:%S %z"],
    ["https://linuxgamingcentral.com/posts/index.xml", "Linux Gaming Central", "https://linuxgamingcentral.com/", "%a, %d %b %Y %H:%M:%S %z"],
    ["https://news.opensuse.org/feed.xml", "openSUSE News", "https://news.opensuse.org/", "%a, %d %b %Y %H:%M:%S %z"],
    ["https://www.omglinux.com/feed/", "OMG! Linux", "https://www.omglinux.com/", "%a, %d %b %Y %H:%M:%S %z"],
    ["https://planet.kde.org/index.xml", "Planet KDE", "https://planet.kde.org/", "%a, %d %b %Y %H:%M:%S %z"],
    ["https://lwn.net/headlines/rss", "LWN.net", "https://lwn.net/", "%Y-%m-%dT%H:%M:%S%z"],
    ["https://planet.debian.org/rss20.xml", "Planet Debian", "https://planet.debian.org/", "%a, %d %b %Y %H:%M:%S %z"],
    ["https://tuxphones.com/rss/", "TuxPhones", "https://tuxphones.com/", "%a, %d %b %Y %H:%M:%S %Z"],
    ["https://www.linuxinsider.com/rss-feed", "LinuxInsider", "https://www.linuxinsider.com/", "%a, %d %b %Y %H:%M:%S %z"]
]

#VIDEOS
videosFeedsInfo = [
    ["https://odysee.com/$/rss/@DistroTube:2", "DistroTube", "https://distro.tube/", "%a, %d %b %Y %H:%M:%S %Z"],
    ["https://tube.kockatoo.org/feeds/videos.xml?videoChannelId=5", "Niccolò Ve", "https://tube.kockatoo.org/c/niccolo_ve/videos", "%a, %d %b %Y %H:%M:%S %Z"],
    ["https://odysee.com/$/rss/@Riba-Linux:5", "Riba Linux", "https://odysee.com/@Riba-Linux:5", "%a, %d %b %Y %H:%M:%S %Z"],
    ["https://odysee.com/$/rss/@BrodieRobertson:5", "Brodie Robertson", "https://odysee.com/@BrodieRobertson:5", "%a, %d %b %Y %H:%M:%S %Z"],
    ["https://tilvids.com/feeds/videos.xml?videoChannelId=2775", "Veronica Explains", "https://tilvids.com/c/veronicaexplains_channel/videos", "%a, %d %b %Y %H:%M:%S %Z"],
    ["https://tilvids.com/feeds/videos.xml?videoChannelId=47", "The Linux Experiment", "https://tilvids.com/c/thelinuxexperiment_channel/videos", "%a, %d %b %Y %H:%M:%S %Z"],
    ["https://tilvids.com/feeds/videos.xml?accountId=133224", "Linux User Space", "https://tilvids.com/a/linuxuserspace/videos", "%a, %d %b %Y %H:%M:%S %Z"],
    ["https://framatube.org/feeds/videos.xml?accountId=8178", "Free Software Foundation", "https://framatube.org/a/fsf/videos", "%a, %d %b %Y %H:%M:%S %Z"],
    ["https://video.retroedge.tech/feeds/videos.xml?videoChannelId=4", "RetroEdge.Tech", "https://retroedge.tech/", "%a, %d %b %Y %H:%M:%S %Z"],
    ["https://tilvids.com/feeds/videos.xml?videoChannelId=71", "Linux Lounge", "https://tilvids.com/c/linux_lounge/videos", "%a, %d %b %Y %H:%M:%S %Z"],
    ["https://www.youtube.com/feeds/videos.xml?channel_id=UCxQKHvKbmSzGMvUrVtJYnUA", "Learn Linux TV", "https://www.learnlinux.tv/", "%Y-%m-%dT%H:%M:%S%z"],
    ["https://www.youtube.com/feeds/videos.xml?channel_id=UCoryWpk4QVYKFCJul9KBdyw", "Switched to Linux", "https://switchedtolinux.com/", "%Y-%m-%dT%H:%M:%S%z"],
    ["https://odysee.com/$/rss/@thelinuxcast:4", "The Linux Cast", "https://odysee.com/@thelinuxcast:4", "%a, %d %b %Y %H:%M:%S %Z"],
    ["https://www.youtube.com/feeds/videos.xml?channel_id=UCfX55Sx5hEFjoC3cNs6mCUQ", "The Linux Foundation", "https://www.youtube.com/@LinuxfoundationOrg/videos", "%Y-%m-%dT%H:%M:%S%z"],
    ["https://www.youtube.com/feeds/videos.xml?channel_id=UCNnUnr4gwyNmzx_Bbzvt29g", "LinuxScoop", "https://www.youtube.com/@linuxscoop/videos", "%Y-%m-%dT%H:%M:%S%z"],
    ["https://www.youtube.com/feeds/videos.xml?channel_id=UCc3L72F_yWWr1V1ft_CDpAA", "9to5Linux (Videos)", "https://www.youtube.com/@9to5Linux/videos", "%Y-%m-%dT%H:%M:%S%z"],
    ["https://www.youtube.com/feeds/videos.xml?channel_id=UC1yGcBvdPGxRIMT1yo_bKIQ", "Jake@Linux", "https://www.youtube.com/@JakeLinux/videos", "%Y-%m-%dT%H:%M:%S%z"],
    ["https://www.youtube.com/feeds/videos.xml?channel_id=UCjSEJkpGbcZhvo0lr-44X_w", "TechHut", "https://www.youtube.com/@TechHut/videos", "%Y-%m-%dT%H:%M:%S%z"]
]

#MORE
moreFeedsInfo = [
    ["https://rs1.es/feed.xml", "RS1 Linux Tools", "https://rs1.es/", "%Y-%m-%dT%H:%M:%S%z"],
    ["https://www.linuxlinks.com/feed/", "LinuxLinks", "https://www.linuxlinks.com/", "%a, %d %b %Y %H:%M:%S %z"],
    ["https://www.fosslinux.com/feed", "FOSS Linux", "https://www.fosslinux.com/", "%a, %d %b %Y %H:%M:%S %z"],
    ["https://linuxtldr.com/feed/", "Linux TLDR", "https://linuxtldr.com/", "%a, %d %b %Y %H:%M:%S %z"],
    ["https://trendoceans.com/feed/", "TREND OCEANS", "https://trendoceans.com/", "%a, %d %b %Y %H:%M:%S %z"],
    ["https://www.linuxcapable.com/feed/", "LinuxCapable", "https://www.linuxcapable.com/", "%a, %d %b %Y %H:%M:%S %z"],
    ["https://www.cyberciti.com/atom/atom.xml", "nixCraft", "https://www.cyberciti.biz/", "%Y-%m-%dT%H:%M:%S%z"],
    ["https://www.linux.com/feed/", "Linux.com", "https://www.linux.com/", "%a, %d %b %Y %H:%M:%S %z"],
    ["https://linuxstans.com/feed/", "Linux Stans", "https://linuxstans.com/", "%a, %d %b %Y %H:%M:%S %z"],
    ["https://www.ubuntupit.com/feed/", "UbuntuPIT", "https://www.ubuntupit.com/", "%a, %d %b %Y %H:%M:%S %z"],
    ["https://feeds.feedburner.com/UbuntuhandbookNewsTutorialsHowtosForUbuntuLinux", "UbuntuHandbook", "https://ubuntuhandbook.org/", "%a, %d %b %Y %H:%M:%S %z"],
    ["https://www.tecmint.com/feed/", "Tecmint", "https://www.tecmint.com/", "%a, %d %b %Y %H:%M:%S %z"],
    ["https://opensource.com/feed", "Opensource.com", "https://opensource.com/", "%a, %d %b %Y %H:%M:%S %z"],
    ["https://www.redhat.com/sysadmin/rss.xml", "Red Hat - Enable Sysadmin", "https://www.redhat.com/sysadmin/", "%a, %d %b %Y %H:%M:%S %z"],
    ["https://feeds.feedburner.com/Ostechnix", "OSTechNix", "https://ostechnix.com/", "%a, %d %b %Y %H:%M:%S %z"],
    ["https://fedoramagazine.org/feed/", "Fedora Magazine", "https://fedoramagazine.org/", "%a, %d %b %Y %H:%M:%S %z"],
    ["https://www.debugpoint.com/feed/", "DebugPoint.com", "https://www.debugpoint.com/", "%a, %d %b %Y %H:%M:%S %z"],
    ["https://www.howtoforge.com/feed.rss", "HowtoForge", "https://www.howtoforge.com/", "%a, %d %b %Y %H:%M:%S %z"],
    ["https://thisweek.gnome.org/index.xml", "This Week in GNOME", "https://thisweek.gnome.org/", "%a, %d %b %Y %H:%M:%S %z"],
    ["https://ubuntu.com/blog/feed", "Ubuntu Blog", "https://ubuntu.com/blog", "%a, %d %b %Y %H:%M:%S %z"],
    ["https://www-gem.bearblog.dev/feed/", "www-gem words", "https://www-gem.bearblog.dev/", "%Y-%m-%dT%H:%M:%S.%f%z"],
    ["https://linuxhint.com/feed/", "Linux Hint", "https://linuxhint.com/", "%a, %d %b %Y %H:%M:%S %z"],
    ["https://www.linuxuprising.com/feeds/posts/default", "Linux Uprising", "https://www.linuxuprising.com/", "%Y-%m-%dT%H:%M:%S.%f%z"],
    ["https://boilingsteam.com/feed/", "Boiling Steam", "https://boilingsteam.com/", "%a, %d %b %Y %H:%M:%S %z"]
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

mainProcess("news", newsFeedsInfo, newsFeeds, "./public")
mainProcess("videos", videosFeedsInfo, videosFeeds, "./public/videos")
mainProcess("more", moreFeedsInfo, moreFeeds, "./public/more")


#testParse("https://fosslife.com/rss/")
