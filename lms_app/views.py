from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from rest_framework import status
from .models import Member, Category, Book, Author
from .serializers import (
    MemberSerializer, CategorySerializer, BookSerializer, 
    AuthorSerializer
)

@api_view(['GET', 'POST'])
def member_list_create(request):
    if request.method == 'GET':
        members = Member.objects.all()
        serializer = MemberSerializer(members, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = MemberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PATCH', 'DELETE'])
def member_detail(request, id):
    member = get_object_or_404(Member, id=id)
    if request.method == 'GET':
        serializer = MemberSerializer(member)
        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = MemberSerializer(member, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        member.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def category_list_create(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PATCH', 'DELETE'])
def category_detail(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def book_list_create(request):
    try:
        if request.method == 'GET':
            books = Book.objects.all()
            serializer = BookSerializer(books, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            serializer = BookSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print("Exception: ", e)
    if request.method == 'GET':
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['PATCH'])
def book_detail(request):
    if request.method == 'PATCH':
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['PATCH'])
def book_status(request, book_id):  
    try:
        book = Book.objects.get(book_id=book_id)
    except Book.DoesNotExist:
        return Response({"error":"Book not found"},status=status.HTTP_404_NOT_FOUND)
    data = request.data
    if 'book_status' in data:
        book.book_status = data['book_status']
        book.save()
        return Response({"error":"book status updated!", "book_status":book.book_status},status=status.HTTP_200_OK)
    else:
        return Response({"error":"book status field is required"},status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def book_borrow(request):
    member_id = request.data.get('member_id')
    book_id = request.data.get('book_id')
    if not all([member_id, book_id]):
        return Response({'error': 'Enter the valid info'}, status=status.HTTP_400_BAD_REQUEST)
    member = get_object_or_404(Member, pk=member_id)
    book = get_object_or_404(Book, pk=book_id)
    if book.book_status != 'Available':
        return Response({'error': 'Book is not available for borrow'}, status=status.HTTP_400_BAD_REQUEST)
    book.member.add(member)
    book.book_status = 'Borrow'
    book.save()
    return Response({'message': f'Book "{book.book_title}" is borrowed by {member.member_full_name}.'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def book_reserve(request):
    member_id = request.data.get('member_id')
    book_id = request.data.get('book_id')
    if not all([member_id, book_id]):
        return Response({'error': 'Enter the valid info'}, status=status.HTTP_400_BAD_REQUEST)
    member = get_object_or_404(Member, pk=member_id)
    book = get_object_or_404(Book, pk=book_id)
    if book.book_status != 'Available':
        return Response({'error': 'Book is not available for reservation'}, status=status.HTTP_400_BAD_REQUEST)
    if book.book_status == 'Reserved':
        return Response({'error': 'This book is already reserved by another member.'}, status=status.HTTP_400_BAD_REQUEST)
    book.book_status = 'Reserved'
    book.save()
    return Response({'message': f'Book "{book.book_title}" is reserved by {member.member_full_name}.'}, status=status.HTTP_200_OK)



@api_view(['POST'])
def book_return(request):
    member_id = request.data.get('member_id')
    book_id = request.data.get('book_id')
    if not all([member_id, book_id]):
        return Response({'error': 'Enter the valid info'}, status=status.HTTP_400_BAD_REQUEST)
    member = get_object_or_404(Member, pk=member_id)
    book = get_object_or_404(Book, pk=book_id)
    if member not in book.member.all():
        return Response({'error': 'This book is not borrowed by the member.'}, status=status.HTTP_400_BAD_REQUEST)
    book.member.remove(member)
    book.book_status = 'Available'
    book.save()  
    return Response({'message': f'Book "{book.book_title}" is return by {member.member_full_name}.'}, status=status.HTTP_200_OK)


    

   
    
    





@api_view(['GET', 'POST'])
def author_list_create(request):
    if request.method == 'GET':
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH', 'DELETE'])
def author_detail(request, id):
    author = get_object_or_404(Author, id=id)
    if request.method == 'GET':
        serializer = AuthorSerializer(author)
        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = AuthorSerializer(author, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        author.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

@api_view(['GET'])
def search_lms(request):
    query = request.GET.get('query', '')
    books = Book.objects.filter(Q(book_title__icontains=query))
    members = Member.objects.filter(Q(member_full_name__icontains=query) |Q(member_Email__icontains=query) |Q(member_department__icontains=query) |Q(member_city__icontains=query) |Q(member_age__icontains=query))
    categories = Category.objects.filter(Q(category_name__icontains=query))
    authors = Author.objects.filter(Q(author_name__icontains=query))

    response = {
        "books": BookSerializer(books, many=True).data,
        "members": MemberSerializer(members, many=True).data,
        "categories": CategorySerializer(categories, many=True).data,
        "authors": AuthorSerializer(authors, many=True).data,
                
    }
    
    return Response(response,status=status.HTTP_200_OK)
