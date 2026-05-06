#!/usr/bin/env python3
"""
NEXUSHUB SITEMAP GENERATOR
==========================
Generates sitemap.xml and updates robots.txt for SEO.
Run after adding new blog posts or products.

Usage:
  python sitemap_gen.py
"""

from datetime import datetime, timezone
from pathlib import Path
import xml.etree.ElementTree as ET

CONFIG = {
    "site_url": "https://your-domain.com",
    "base_dir": "..",
    "pages": [
        {"loc": "/", "priority": "1.0", "changefreq": "daily"},
        {"loc": "/#blog", "priority": "0.9", "changefreq": "daily"},
        {"loc": "/#shop", "priority": "0.8", "changefreq": "weekly"},
        {"loc": "/#affiliate", "priority": "0.8", "changefreq": "daily"},
        {"loc": "/#newsletter", "priority": "0.7", "changefreq": "monthly"},
    ]
}

def generate_sitemap():
    base = Path(CONFIG["base_dir"])
    blog_dir = base / "blog"
    shop_dir = base / "shop"

    urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # Add static pages
    for page in CONFIG["pages"]:
        url = ET.SubElement(urlset, "url")
        ET.SubElement(url, "loc").text = CONFIG["site_url"] + page["loc"]
        ET.SubElement(url, "lastmod").text = today
        ET.SubElement(url, "changefreq").text = page["changefreq"]
        ET.SubElement(url, "priority").text = page["priority"]

    # Add blog posts
    if blog_dir.exists():
        for post in blog_dir.glob("*.html"):
            if post.name.startswith("."):
                continue
            url = ET.SubElement(urlset, "url")
            ET.SubElement(url, "loc").text = f"{CONFIG['site_url']}/blog/{post.name}"
            ET.SubElement(url, "lastmod").text = today
            ET.SubElement(url, "changefreq").text = "weekly"
            ET.SubElement(url, "priority").text = "0.7"

    # Add shop products
    if shop_dir.exists():
        for product in shop_dir.glob("*.html"):
            if product.name.startswith("."):
                continue
            url = ET.SubElement(urlset, "url")
            ET.SubElement(url, "loc").text = f"{CONFIG['site_url']}/shop/{product.name}"
            ET.SubElement(url, "lastmod").text = today
            ET.SubElement(url, "changefreq").text = "weekly"
            ET.SubElement(url, "priority").text = "0.6"

    # Write sitemap
    sitemap_path = base / "sitemap.xml"
    tree = ET.ElementTree(urlset)
    ET.indent(tree, space="  ")
    tree.write(sitemap_path, encoding="utf-8", xml_declaration=True)

    print(f"Generated sitemap.xml with {len(urlset)} URLs")
    return len(urlset)

def update_robots():
    robots_content = f"""User-agent: *
Allow: /
Disallow: /automation/
Disallow: /.github/

Sitemap: {CONFIG['site_url']}/sitemap.xml

# Crawl-delay for polite bots
Crawl-delay: 1
"""
    robots_path = Path(CONFIG["base_dir"]) / "robots.txt"
    with open(robots_path, "w") as f:
        f.write(robots_content)
    print("Updated robots.txt")

if __name__ == "__main__":
    count = generate_sitemap()
    update_robots()
    print(f"\nSEO files updated. Total URLs in sitemap: {count}")
