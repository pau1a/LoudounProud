"""Download stock photos from Lorem Picsum for articles that lack hero images."""

import hashlib
import io
import time
import urllib.request

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from apps.articles.models import Article

WIDTH, HEIGHT = 1200, 675  # 16:9


class Command(BaseCommand):
    help = "Download stock photos from Lorem Picsum for articles without hero images."

    def add_arguments(self, parser):
        parser.add_argument(
            "--replace",
            action="store_true",
            help="Replace existing hero images too",
        )

    def handle(self, *args, **options):
        if options["replace"]:
            articles = Article.objects.filter(status="published")
        else:
            articles = Article.objects.filter(status="published", hero_image="")

        count = 0
        for article in articles:
            slug_hash = hashlib.md5(article.slug.encode()).hexdigest()[:8]

            # Use a stable seed from the slug hash so the same article
            # always gets the same image (idempotent).
            seed = int(slug_hash, 16) % 1000
            url = f"https://picsum.photos/seed/{seed}/{WIDTH}/{HEIGHT}"

            self.stdout.write(f"  Fetching: {article.title[:55]}...")
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "LoudounProud/1.0"})
                with urllib.request.urlopen(req, timeout=30) as resp:
                    image_data = resp.read()
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"  FAIL: {e}"))
                continue

            article.hero_image.save(
                f"hero_{slug_hash}.jpg",
                ContentFile(image_data),
                save=False,
            )
            Article.objects.filter(pk=article.pk).update(hero_image=article.hero_image)

            count += 1
            self.stdout.write(self.style.SUCCESS(f"  OK: {article.title[:55]}"))

            # Be polite to the API
            time.sleep(0.5)

        self.stdout.write(self.style.SUCCESS(f"\nDownloaded {count} hero image(s)."))
