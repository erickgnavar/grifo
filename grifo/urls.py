from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', 'main.views.home'),
	url(r'^g/', include('main.urls')),
	url(r'^admin/', include(admin.site.urls)),
)

handler_500 = 'main.views.error_500'
handler_404 = 'main.views.error_404'

from django.conf import settings

# if settings.DEBUG:
if True:
	urlpatterns += patterns('',
		(r'^media/(?P<path>.*)$', 'django.views.static.serve',
			{'document_root': settings.MEDIA_ROOT}),
	)