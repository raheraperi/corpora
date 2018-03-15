# -*- coding: utf-8 -*-

from django.conf.urls import url, include
# from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import ugettext_lazy as _

from django.contrib import admin
from django.contrib.sitemaps.views import sitemap

from corpora.views import views
from django.views.generic import RedirectView
# from people.views import profile_redirect
from rest_framework.documentation import include_docs_urls

from corpus.views.stats_views import RecordingStatsView
from corpus.views.views import StatsView
from people.views import stats_views
from people.views import views as people_views

from django.views.decorators.cache import cache_page

urlpatterns = [

    url(r'^$', cache_page(60 * 60)(views.home), name='home'),
    url(r'^privacy', cache_page(60 * 60)(views.privacy), name='privacy'),

    url(r'^', include('corpus.urls', namespace='corpus')),

    url(r'^i18n/', include('django.conf.urls.i18n')),

    url(r'^admin/', admin.site.urls),
    url(r'^account/', include('allauth.urls')),
    url(r'^accounts/', include('allauth.urls')),

    url(r'^signup/',
        cache_page(60 * 5)(
            RedirectView.as_view(
                permanent=False,
                query_string=True,
                url='/accounts/signup')),
        name='signup'),

    url(r'^login/',
        cache_page(60 * 5)(
            RedirectView.as_view(
                permanent=False,
                query_string=True,
                url='/accounts/login')),
        name='login'),

    # url(r'^$', cache_on_auth(settings.SHORT_CACHE)(views.home), name='home'),

    url(_(r'^people/'), include('people.urls', namespace='people')),
    # url(r'^people/profile', profile_redirect, name='profile-backwards-comp'),

    url(r'^rules/$',
        RedirectView.as_view(
            permanent=True,
            url='/competition/rules'),
        name='rules-redirect'),

    url(_(r'^competition/rules'),
        cache_page(60 * 60)(
            views.rules),
        name='rules'),

    url(_(r'^competition/help'),
        cache_page(60 * 60)(
            people_views.Help.as_view()),
        name='competition_help'),

    url(_(r'^competition/user_leaderboard'),
        cache_page(60 * 10)(
            stats_views.PeopleRecordingStatsView.as_view()),
        name='user_leaderboard'),

    url(_(r'^competition/group/(?P<pk>\d+)'),
        cache_page(60 * 10)(
            stats_views.GroupStatsView.as_view()),
        name='competition_group'),

    url(_(r'^competition'),
        cache_page(60 * 10)(
            people_views.Competition.as_view()),
        name='competition'),

    url(_(r'^stats/person'),
        stats_views.PersonRecordingStatsView.as_view(),
        name='stats_person'),

    # url(_(r'^stats/people$'),
    #     cache_page(60 * 10)(
    #         stats_views.PeopleRecordingStatsView.as_view()),
    #     name='stats_people'),

    url(_(r'^stats/groups$'),
        cache_page(60 * 10)(
            stats_views.GroupsStatsView.as_view()),
        name='stats_groups'),

    url(_(r'^stats/recordings'),
        RecordingStatsView.as_view(),
        name='stats_recordings'),

    url(_(r'^stats/$'),
        cache_page(60 * 60)(
            StatsView.as_view()),
        name='stats'),


    # url(r'^$', cache_on_auth(settings.SHORT_CACHE)(views.home), name='home'),

    url(r'^', include('corpora.urls_api', namespace='api')),
    url(r'^docs/', include_docs_urls(title='Corpora API')),

    # url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
    #     name='django.contrib.sitemaps.views.sitemap')

]



# I think it's better we store language preference in cookie and not do url redirects
# urlpatterns += i18n_patterns(
#     url( _(r'^people/'), include('people.urls', namespace='people')),
# )
# prefix_default_language=True