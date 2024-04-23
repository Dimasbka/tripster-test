from django.contrib import admin
from publications.models import *

# Register your models here.


# --------------------------------------------------------------------Publication
class PublicationAdmin(admin.ModelAdmin):
    # нужно для инициализации Autocomplete полей
    autocomplete_fields = [
        "user",
    ]
    search_fields = ("name",)

    list_display = ["id", "text", "user", "publish_date", "rating", "votes"]
    list_display_links = ["id", "text", "user", "publish_date", "rating", "votes"]
    save_on_top = True


admin.site.register(Publication, PublicationAdmin)


# --------------------------------------------------------------- PublicationVote
class PublicationVoteAdmin(admin.ModelAdmin):
    # нужно для инициализации Autocomplete полей
    autocomplete_fields = [
        "user",
        "publication",
    ]
    #    search_fields = ( 'user__email', 'publication__', )

    list_display = ["user", "publication", "vote"]
    list_display_links = ["user", "publication", "vote"]
    list_filter = ("vote",)
    save_on_top = True


admin.site.register(PublicationVote, PublicationVoteAdmin)
