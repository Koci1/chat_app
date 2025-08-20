from rest_framework.pagination import CursorPagination


class MessagePagination(CursorPagination):
    page_size = 100
    ordering = '-timestamp'
    