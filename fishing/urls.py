from django.urls import path
from fishing.views import sync_pull, sync_catches, sync_sessions

urlpatterns = [
    path("sync/", sync_pull),
    path("sync/sessions/", sync_sessions),
    path("sync/catches/", sync_catches),
]


# Pike: 196696ed-1a51-4d99-bc8a-c41aacaaaadd
# Trout: 48b44751-40e8-4f75-b7db-176590e0d822
# Chub: 75aeafc1-1646-46b3-9b91-83e8f7bebb94
# Barbel: f07ea577-3056-4919-9098-fab6c7e59e67