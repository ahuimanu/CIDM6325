from collections.abc import Iterable

from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed

from .models import Post


class LatestPostsBase(Feed):
    title = "Latest Posts"
    link = "/blog/"
    description = "The 10 most recent posts"

    def items(self) -> Iterable[Post]:  # type: ignore[override]
        return Post.objects.published()[:10]

    def item_title(self, item: Post) -> str:  # type: ignore[override]
        return item.title

    def item_description(self, item: Post) -> str:  # type: ignore[override]
        # Use first ~200 chars as a lightweight description/excerpt
        return (item.body or "")[:200]

    def item_link(self, item: Post) -> str:  # type: ignore[override]
        return item.get_absolute_url()

    def item_pubdate(self, item: Post):  # type: ignore[override]
        return item.publish_date


class LatestPostsRSSFeed(LatestPostsBase):
    title = "Latest Posts (RSS)"


class LatestPostsAtomFeed(LatestPostsBase):
    feed_type = Atom1Feed
    subtitle = LatestPostsBase.description
    title = "Latest Posts (Atom)"
