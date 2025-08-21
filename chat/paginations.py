from rest_framework.pagination import CursorPagination


class MessagePagination(CursorPagination):
    page_size = 40
    ordering = '-timestamp'
    