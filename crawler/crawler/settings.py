# Scrapy settings for crawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'crawler'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['crawler.spiders']
NEWSPIDER_MODULE = 'crawler.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

REDIRECT_MAX_TRIES = 0
DOWNLOAD_DELAY = 0.25

def setup_django_env(path): 
    import imp 
    from django.core.management import setup_environ 
    f, filename, desc = imp.find_module('settings', [path]) 
    project = imp.load_module('settings', f, filename, desc) 
    print "Setting django environment: ", project
    setup_environ(project) 
    
setup_django_env('../tutorial')