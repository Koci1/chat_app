from rest_framework.pagination import CursorPagination


class MessagePagination(CursorPagination):

    """
    Za ucitavanje historije poruka koristimo cursor paginaciju
    """

    page_size = 40
    ordering = '-timestamp'
    