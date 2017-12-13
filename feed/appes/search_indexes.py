import datetime
from django.utils import timezone
from haystack import indexes
from haystack.fields import CharField

from .models import Myfeed


class MyfeedIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(
        document=True, use_template=True,
        template_name='/home/aptus/rssfeeds/ASLF/feed/templates/search/indexes/myfeed_text.txt')
    title = indexes.EdgeNgramField(model_attr='title')
    slug = indexes.EdgeNgramField(model_attr='slug', null=True)
    description = indexes.EdgeNgramField(model_attr="description", null=True)
    category = indexes.CharField(model_attr='category', null=True, faceted=True)
    main_link = indexes.CharField(model_attr='main_link', null=True, faceted=True)
    sub_link = indexes.CharField(model_attr='sub_link', null=True, faceted=True)
    tag_id = indexes.CharField(model_attr='tag_id', null=True, faceted=True)
    published = indexes.CharField(model_attr='published', null=True, faceted=True)
    updated = indexes.CharField(model_attr='updated', null=True, faceted=True)

    # for auto complete
    content_auto = indexes.EdgeNgramField(model_attr='title')

    # Spelling suggestions
    suggestions = indexes.FacetCharField()

    def get_model(self):
        return Myfeed

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(timestamp__lte=timezone.now())

if __name__ == "__main__":
    MyfeedIndex()
    schedule.every(25).minutes.do(MyfeedIndex)