from haystack.forms import FacetedSearchForm


class FacetedMyfeedSearchForm(FacetedSearchForm):

    def __init__(self, *args, **kwargs):
        data = dict(kwargs.get("data", []))
        self.categories = data.get('category', [])
        self.main_links = data.get('main_link', [])
        super(FacetedMyfeedSearchForm, self).__init__(*args, **kwargs)

    def search(self):
        sqs = super(FacetedMyfeedSearchForm, self).search()
        if self.categories:
            query = None
            for category in self.categories:
                if query:
                    query += u' OR '
                else:
                    query = u''
                query += u'"%s"' % sqs.query.clean(category)
            sqs = sqs.narrow(u'category_exact:%s' % query)
        if self.main_links:
            query = None
            for main_link in self.main_links:
                if query:
                    query += u' OR '
                else:
                    query = u''
                query += u'"%s"' % sqs.query.clean(main_link)
            sqs = sqs.narrow(u'main_link_exact:%s' % query)
        return sqs
