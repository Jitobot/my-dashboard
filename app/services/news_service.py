from xml.etree import ElementTree

import httpx

NHK_RSS_URL = "https://www.nhk.or.jp/rss/news/cat0.xml"


async def fetch_news(max_items: int = 10) -> list[dict]:
    async with httpx.AsyncClient(follow_redirects=True) as client:
        res = await client.get(NHK_RSS_URL, timeout=10)
        res.raise_for_status()

    root = ElementTree.fromstring(res.text)
    items = root.findall(".//item")

    news = []
    for item in items[:max_items]:
        title = item.findtext("title", "")
        link = item.findtext("link", "")
        pub_date = item.findtext("pubDate", "")
        news.append({
            "title": title,
            "link": link,
            "pub_date": pub_date,
        })
    return news
