from rest_framework import pagination


class ProgresoPlayerPagination(pagination.CursorPagination):
    page_size = 4
    ordering = "created"
