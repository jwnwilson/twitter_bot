"""
twitter_bot URL Configuration
"""
from django.conf.urls import include, url, patterns
from django.contrib import admin

urlpatterns = patterns('',
        url(r'^admin/', include(admin.site.urls)),
        url(r'', include('social_auth.urls')),
    )

urlpatterns += patterns('twitter_bot.views',
        url(r'^$', 'home', name='home'),
        url(r'^hash_tag_battle/', 'hash_tag_battle', name='hash_tag_battle'),
    )

