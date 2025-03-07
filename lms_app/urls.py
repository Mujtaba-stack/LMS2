from django.urls import path
from .views import (
    member_list_create, member_detail,
    category_list_create, category_detail,
    book_list_create, book_detail,
    author_list_create, author_detail,
       search_lms,book_borrow,book_reserve,book_return
)

urlpatterns = [
    path('member/', member_list_create, name='member-list-create'),
    path('member/<int:id>/', member_detail, name='member-detail'),

    path('category/', category_list_create, name='category-list-create'),
    path('category/<int:id>/', category_detail, name='category-detail'),

    path('books/', book_list_create, name='book-list-create'),
    path('books/<int:id>/', book_detail, name='book-detail'),
    path('borrow/', book_borrow, name='book-borrow'),
    path('reserve/', book_reserve, name='book-reserve'),
    path('return/', book_return, name='book-return'),

    path('author/', author_list_create, name='author-list-create'),
    path('author/<int:id>/', author_detail, name='author-detail'),
    path('search/', search_lms, name='search_lms_create'),
]

