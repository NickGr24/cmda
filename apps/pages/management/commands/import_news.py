"""
Import news articles from startup.chisinau.md/noutati/
Fetches all pages, downloads images, creates News records.
"""
import os
import re
from datetime import datetime
from io import BytesIO
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from apps.pages.models import News

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
    'Accept-Encoding': 'gzip, deflate',
}
BASE_URL = 'https://startup.chisinau.md'
NEWS_URL = f'{BASE_URL}/category/comunicate-de-presa/'


class Command(BaseCommand):
    help = 'Import news from startup.chisinau.md/noutati/'

    def handle(self, *args, **options):
        articles = []

        # Collect article links from all pages
        for page_num in range(1, 10):
            url = NEWS_URL if page_num == 1 else f'{NEWS_URL}page/{page_num}/'
            self.stdout.write(f'Fetching list page {page_num}: {url}')

            try:
                resp = requests.get(url, headers=HEADERS, timeout=30)
            except Exception as e:
                self.stdout.write(f'  Page {page_num} fetch error: {e}, stopping.')
                break
            if resp.status_code != 200:
                self.stdout.write(f'  Page {page_num} returned {resp.status_code}, stopping.')
                break

            soup = BeautifulSoup(resp.text, 'html.parser')
            items = soup.select('.blog-posts .item')
            if not items:
                # Try alternative selectors
                items = soup.select('article') or soup.select('.post')
            if not items:
                self.stdout.write(f'  No articles found on page {page_num}, stopping.')
                break

            for item in items:
                link_tag = item.find('a', href=True)
                if not link_tag:
                    continue
                article_url = link_tag['href']
                if not article_url.startswith('http'):
                    article_url = urljoin(BASE_URL, article_url)

                # Get thumbnail image
                img_tag = item.find('img')
                thumb_url = ''
                if img_tag:
                    thumb_url = img_tag.get('src', '') or img_tag.get('data-src', '')

                # Get date from the card
                date_el = item.select_one('.date')
                date_text = ''
                if date_el:
                    date_text = date_el.get_text(strip=True)

                # Get title
                title_el = item.find('h4') or item.find('h3') or item.find('h2')
                title = title_el.get_text(strip=True) if title_el else ''

                # Get excerpt
                excerpt_el = item.find('p')
                excerpt = excerpt_el.get_text(strip=True) if excerpt_el else ''

                articles.append({
                    'url': article_url,
                    'thumb_url': thumb_url,
                    'date_text': date_text,
                    'title': title,
                    'excerpt': excerpt,
                })

            self.stdout.write(f'  Found {len(items)} articles on page {page_num}')

        self.stdout.write(f'\nTotal articles found: {len(articles)}')

        # Process each article
        created_count = 0
        for i, art in enumerate(articles, 1):
            title = art['title']
            if not title:
                self.stdout.write(f'  [{i}] Skipping article with no title: {art["url"]}')
                continue

            slug = slugify(title)[:500]
            if News.objects.filter(slug=slug).exists():
                self.stdout.write(f'  [{i}] Already exists: {title[:60]}')
                continue

            self.stdout.write(f'  [{i}] Processing: {title[:60]}...')

            # Parse date (MM/DD/YYYY format)
            published_date = self._parse_date(art['date_text'])

            # Fetch full article content
            content, featured_img_url = self._fetch_article(art['url'])

            # Prefer thumbnail from listing page (unique per article),
            # fallback to article page's featured image (often a site-wide default)
            img_url = art['thumb_url'] or featured_img_url

            # Create News object
            news = News(
                title=title,
                slug=slug,
                excerpt=art['excerpt'][:500] if art['excerpt'] else '',
                content=content,
                published_date=published_date,
                source_url=art['url'],
            )

            # Download and attach image
            if img_url:
                try:
                    img_resp = requests.get(img_url, headers=HEADERS, timeout=30)
                    if img_resp.status_code == 200:
                        ext = self._get_extension(img_url, img_resp.headers.get('content-type', ''))
                        filename = f'{slug[:80]}{ext}'
                        news.image.save(filename, ContentFile(img_resp.content), save=False)
                except Exception as e:
                    self.stdout.write(f'    Image download failed: {e}')

            news.save()
            created_count += 1
            self.stdout.write(self.style.SUCCESS(f'    Created: {title[:60]}'))

        self.stdout.write(self.style.SUCCESS(f'\nDone! Created {created_count} news articles.'))

    def _parse_date(self, date_text):
        """Parse date from MM/DD/YYYY or other formats."""
        if not date_text:
            return datetime(2023, 1, 1).date()

        # Remove any non-date characters (SVG icon text etc.)
        date_text = re.sub(r'[^\d/.\-]', '', date_text).strip()

        for fmt in ('%m/%d/%Y', '%d/%m/%Y', '%Y-%m-%d', '%d.%m.%Y'):
            try:
                return datetime.strptime(date_text, fmt).date()
            except ValueError:
                continue

        self.stdout.write(f'    Could not parse date: "{date_text}", using default')
        return datetime(2023, 1, 1).date()

    def _fetch_article(self, url):
        """Fetch full article content and featured image."""
        try:
            resp = requests.get(url, headers=HEADERS, timeout=30)
            if resp.status_code != 200:
                return '', ''

            soup = BeautifulSoup(resp.text, 'html.parser')

            # The article text lives in .section-blog .container as direct
            # <p> / <ul> / <ol> / <img> children, before <h3>Alte Noutăți</h3>
            content = ''
            container = soup.select_one('.section-blog .container')
            if container:
                # First, remove "Alte Noutăți" sections and everything after
                for h3 in container.find_all('h3'):
                    if 'nout' in h3.get_text().lower():
                        # Remove this h3 and all following siblings
                        for sib in list(h3.find_next_siblings()):
                            sib.decompose()
                        h3.decompose()
                        break

                # Also clean inside nested wrappers (blog-single-wrapper)
                for wrapper in container.find_all(class_='blog-single-wrapper'):
                    for h3 in wrapper.find_all('h3'):
                        if 'nout' in h3.get_text().lower():
                            for sib in list(h3.find_next_siblings()):
                                sib.decompose()
                            h3.decompose()
                            break

                # Remove related-posts sections
                for el in container.find_all(class_=re.compile(r'related|swiper', re.I)):
                    el.decompose()
                # Remove stray related-post links (a tags with .info/.date inside)
                for a_tag in container.find_all('a', recursive=False):
                    if a_tag.find(class_='info') or a_tag.find(class_='date'):
                        a_tag.decompose()

                parts = []
                for el in container.children:
                    if not hasattr(el, 'name') or el.name is None:
                        continue
                    # Skip the h1 title (already stored separately)
                    if el.name == 'h1':
                        continue
                    # Skip page-header-image (already shown as hero)
                    if el.name == 'img' and 'page-header-image' in el.get('class', []):
                        continue
                    # Skip standalone links (related post cards)
                    if el.name == 'a':
                        continue
                    # Keep paragraphs, lists, images, blockquotes, wrappers
                    if el.name in ('p', 'ul', 'ol', 'blockquote', 'figure', 'img', 'div'):
                        # Also clean related links inside wrappers
                        for a_tag in el.find_all('a'):
                            if a_tag.find(class_='info') or a_tag.find(class_='date'):
                                a_tag.decompose()
                        html = str(el).strip()
                        if html:
                            parts.append(html)
                content = '\n'.join(parts)

            # Get featured image
            featured_img = ''
            og_img = soup.find('meta', property='og:image')
            if og_img:
                featured_img = og_img.get('content', '')
            if not featured_img:
                for img in soup.find_all('img'):
                    src = img.get('src', '')
                    if src and 'wp-content/uploads' in src:
                        featured_img = src
                        break

            return content, featured_img

        except Exception as e:
            self.stdout.write(f'    Error fetching article: {e}')
            return '', ''

    def _get_extension(self, url, content_type):
        """Get file extension from URL or content-type."""
        # Try from URL
        path = url.split('?')[0]
        if '.' in path.split('/')[-1]:
            ext = '.' + path.split('/')[-1].split('.')[-1].lower()
            if ext in ('.jpg', '.jpeg', '.png', '.webp', '.gif'):
                return ext

        # From content-type
        ct_map = {
            'image/jpeg': '.jpg',
            'image/png': '.png',
            'image/webp': '.webp',
            'image/gif': '.gif',
        }
        return ct_map.get(content_type, '.jpg')
