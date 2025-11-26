from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'documents', views.DocumentViewSet)
router.register(r'entities', views.EntityViewSet)
router.register(r'relationships', views.RelationshipViewSet)

# 获取路由器生成的所有URL模式
urlpatterns = [
    path('', include(router.urls)),
]

# 添加知识图谱相关的自定义端点
urlpatterns += [
    path('knowledge-graph/', views.knowledge_graph_data, name='knowledge-graph-data'),
    path('entity-subgraph/<int:entity_id>/', views.entity_subgraph, name='entity-subgraph'),
]

urlpatterns += [
    path('management/', views.api_management_panel, name='api-management'),
    path('management/entities/', views.entity_management, name='entity-management'),
    path('management/relationships/', views.relationship_management, name='relationship-management'),
]