from rest_framework import pagination


class ProgresoPersonPagination(pagination.CursorPagination):
    page_size = 4
    ordering = "created"
