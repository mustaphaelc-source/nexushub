#!/usr/bin/env python3
"""
NEXUSHUB CONTENT BOT
Fetches RSS feeds, generates static HTML blog posts with attribution.
"""

import feedparser
import json
import re
import html as html_module
from datetime import datetime, timezone
from pathlib import Path

CONFIG = {
    "output_dir": "../blog",
    "max_posts_per_run": 3,
    "min_word_count": 300,
    "feeds": [
        {"url": "https://feeds.feedburner.com/TechCrunch/", "category": "Technology", "source_name": "TechCrunch"},
        {"url": "https://www.entrepreneur.com/latest.rss", "category": "Business", "source_name": "Entrepreneur"}
    ],
    "site_url": "https://your-domain.com",
    "affiliate_links": {
        "hostinger": "https://www.hostinger.com/?REFCODE=YOUR_AFF_ID"
    }
}

class ContentBot:
    def __init__(self, config):
        self.config = config
        self.output_dir = Path(config["output_dir"])
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.seen_file = self.output_dir / ".seen_urls.json"
        self.seen_urls = self._load_seen()

    def _load_seen(self):
        if self.seen_file.exists():
            with open(self.seen_file, "r") as f:
                return set(json.load(f))
        return set()

    def _save_seen(self):
        with open(self.seen_file, "w") as f:
            json.dump(list(self.seen_urls), f)

    def _slugify(self, text):
        text = html_module.unescape(text)
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'[-\s]+', '-', text)
        return text.lower().strip('-')[:60]

    def _extract_image(self, entry):
        if 'media_content' in entry:
            return entry.media_content[0]['url']
        if 'media_thumbnail' in entry:
            return entry.media_thumbnail[0]['url']
        if 'content' in entry:
            match = re.search(r'src=["\'](https?://[^"\']+\.(?:jpg|jpeg|png|webp))["\']', entry.content[0].value, re.I)
            if match:
                return match.group(1)
        if 'summary' in entry:
            match = re.search(r'src=["\'](https?://[^"\']+\.(?:jpg|jpeg|png|webp))["\']', entry.summary, re.I)
            if match:
                return match.group(1)
        return "https://images.unsplash.com/photo-1519389950473-47ba0277781c?w=800&h=500&fit=crop"

    def _clean_content(self, html_content):
        clean = re.sub(r'<[^>]+>', ' ', html_content)
        clean = html_module.unescape(clean)
        clean = re.sub(r'\s+', ' ', clean).strip()
        return clean

    def _generate_html_post(self, entry, feed_config, slug):
        title = html_module.unescape(entry.title)
        source = feed_config["source_name"]
        category = feed_config["category"]
        image = self._extract_image(entry)

        raw_content = entry.get('summary', entry.get('content', [{'value': ''}])[0]['value'])
        clean_text = self._clean_content(raw_content)
        excerpt = clean_text[:200] + "..." if len(clean_text) > 200 else clean_text

        pub_date = datetime.now(timezone.utc).strftime("%B %d, %Y")
        iso_date = datetime.now(timezone.utc).isoformat()
        site_url = self.config['site_url']
        aff_link = self.config['affiliate_links']['hostinger']

        # Build HTML using format to avoid quote issues
        html_parts = []
        html_parts.append('<!DOCTYPE html>')
        html_parts.append('<html lang="en" dir="ltr">')
        html_parts.append('<head>')
        html_parts.append('    <meta charset="UTF-8">')
        html_parts.append('    <meta name="viewport" content="width=device-width, initial-scale=1.0">')
        html_parts.append(f'    <meta name="description" content="{excerpt[:160].replace(chr(34), chr(34))}">')
        html_parts.append(f'    <meta name="author" content="{source} (Curated by NexusHub)">')
        html_parts.append(f'    <meta property="og:title" content="{title}">')
        html_parts.append(f'    <meta property="og:description" content="{excerpt[:160]}">')
        html_parts.append(f'    <meta property="og:image" content="{image}">')
        html_parts.append('    <meta property="og:type" content="article">')
        html_parts.append('    <meta name="twitter:card" content="summary_large_image">')
        html_parts.append(f'    <link rel="canonical" href="{site_url}/blog/{slug}.html">')
        html_parts.append('    <title>' + title + ' | NexusHub Blog</title>')
        html_parts.append('    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">')
        html_parts.append('    <link rel="stylesheet" href="../css/style.css">')
        html_parts.append('</head>')
        html_parts.append('<body>')
        html_parts.append('    <article class="blog-post">')
        html_parts.append('        <div class="container" style="max-width: 800px; padding: 120px 24px 60px;">')
        html_parts.append('            <div class="blog-post-header">')
        html_parts.append(f'                <span class="section-tag">{category}</span>')
        html_parts.append(f'                <h1 style="font-size: clamp(1.8rem, 4vw, 3rem); margin: 20px 0;">{title}</h1>')
        html_parts.append('                <div class="blog-meta" style="margin-bottom: 32px;">')
        html_parts.append(f'                    <span>Source: <a href="{entry.link}" target="_blank" rel="nofollow">{source}</a></span>')
        html_parts.append('                    <span>&bull;</span>')
        html_parts.append(f'                    <span>{pub_date}</span>')
        html_parts.append('                </div>')
        html_parts.append('            </div>')
        html_parts.append('            <div class="blog-post-image" style="border-radius: 24px; overflow: hidden; margin-bottom: 40px;">')
        html_parts.append(f'                <img src="{image}" alt="{title}" style="width: 100%; height: auto; display: block;">')
        html_parts.append('            </div>')
        html_parts.append('            <div class="blog-post-content" style="font-size: 1.1rem; line-height: 1.8; color: var(--text-secondary);">')
        html_parts.append(f'                <p><strong>Originally published by {source}.</strong> This is a curated summary with our analysis and recommendations.</p>')
        html_parts.append(f'                <p>{clean_text[:800]}</p>')
        html_parts.append('                <p><em>Continue reading the full article at the original source for complete details.</em></p>')
        html_parts.append('                <div class="original-source" style="margin: 40px 0; padding: 24px; background: rgba(255,255,255,0.03); border-radius: 16px; border-left: 3px solid var(--accent-cyan);">')
        html_parts.append(f'                    <p style="margin: 0; font-size: 0.95rem;"><strong>Original Source:</strong> <a href="{entry.link}" target="_blank" rel="nofollow" style="color: var(--accent-cyan);">{entry.link}</a></p>')
        html_parts.append('                    <p style="margin: 8px 0 0; font-size: 0.85rem; color: var(--text-muted);">This article is curated with attribution. All rights belong to the original publisher.</p>')
        html_parts.append('                </div>')
        html_parts.append('                <div class="affiliate-insert" style="margin: 40px 0; padding: 32px; background: linear-gradient(135deg, rgba(0,212,170,0.05), rgba(168,85,247,0.05)); border-radius: 16px; text-align: center;">')
        html_parts.append('                    <h3 style="margin-bottom: 16px;">Recommended Tool for This Topic</h3>')
        html_parts.append('                    <p style="margin-bottom: 20px;">Build your own automated platform with reliable hosting.</p>')
        html_parts.append(f'                    <a href="{aff_link}" target="_blank" rel="nofollow sponsored" class="btn btn-primary btn-glow">Get Hostinger Deal &rarr;</a>')
        html_parts.append('                </div>')
        html_parts.append('            </div>')
        html_parts.append('            <div class="blog-post-footer" style="margin-top: 60px; padding-top: 40px; border-top: 1px solid rgba(255,255,255,0.05);">')
        html_parts.append('                <a href="../index.html#blog" class="btn btn-secondary">&larr; Back to Blog</a>')
        html_parts.append('            </div>')
        html_parts.append('        </div>')
        html_parts.append('    </article>')
        html_parts.append('    <script src="../js/main.js"></script>')
        html_parts.append('</body>')
        html_parts.append('</html>')

        return "\n".join(html_parts)

    def run(self):
        posts_created = 0

        for feed_config in self.config["feeds"]:
            if posts_created >= self.config["max_posts_per_run"]:
                break

            print(f"\nFetching: {feed_config['source_name']}")

            try:
                feed = feedparser.parse(feed_config["url"])

                if feed.bozo:
                    print(f"   Warning: {feed.bozo_exception}")

                for entry in feed.entries[:5]:
                    if posts_created >= self.config["max_posts_per_run"]:
                        break

                    if entry.link in self.seen_urls:
                        continue

                    content = entry.get('summary', '')
                    if len(self._clean_content(content)) < self.config["min_word_count"]:
                        continue

                    slug = self._slugify(entry.title)
                    post_path = self.output_dir / f"{slug}.html"

                    if post_path.exists():
                        self.seen_urls.add(entry.link)
                        continue

                    html_content = self._generate_html_post(entry, feed_config, slug)

                    with open(post_path, "w", encoding="utf-8") as f:
                        f.write(html_content)

                    self.seen_urls.add(entry.link)
                    posts_created += 1

                    print(f"   Created: {slug}.html")

            except Exception as e:
                print(f"   Error: {e}")
                continue

        self._save_seen()
        print(f"\nDone! Created {posts_created} new post(s).")
        return posts_created

if __name__ == "__main__":
    bot = ContentBot(CONFIG)
    bot.run()
