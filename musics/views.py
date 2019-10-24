from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Music, Artist, Comment
from .serializers import MusicSerializer, ArtistSerializer, CommentSerializer, ArtistDetailSerializer
# Create your views here.

@api_view(['GET'])
def music_list(request):
    #만약에 artist_pk 가 query params로 넘어온다면 필터링한 값만 응답하고 
    params = {}
    artist_pk = request.GET.get('artist_pk')
    
    if artist_pk:
        params['artist_id'] = artist_pk

    # 그렇지 않다면 전체 응답한다.
    musics = Music.objects.filter(**params)
    #json파일로 변환하여 줘야한다. 
    serializer = MusicSerializer(musics, many=True)
    return Response(serializer.data)


# @api_view(['GET'])
# def music_detail(request, music_pk):
#     music = get_object_or_404(Music, pk=music_pk)
#     serializer = MusicSerializer(music)
#     return Response(serializer.data)

@api_view(['GET', 'PUT', 'DELETE',])
def music_detail_delete_update(request, music_pk):
    music = get_object_or_404(Music, pk=music_pk)
    if request.method =='PUT':
        serializer = MusicSerializer(data=request.data, instance=music)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

    elif request.method =='DELETE':
        music.delete()
        return Response({'message':'Comment has been deleted!'})

    else:
        serializer = MusicSerializer(music)
    return Response(serializer.data)


@api_view(['GET'])
def artist_list(request):
    artists = Artist.objects.all()
    serializer = ArtistSerializer(artists, many=True)
    return Response(serializer.data)




@api_view(['GET', 'PUT', 'DELETE',])
def artist_detail_update_delete(request, artist_pk):
    artist = get_object_or_404(Artist, pk=artist_pk)

    if request.method =='PUT':
        serializer = ArtistSerializer(data=request.data, instance=artist)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

    elif request.method =='DELETE':
        artist.delete()
        return Response({'message':'Comment has been deleted!'})

    else:
        serializer = ArtistDetailSerializer(artist)
    return Response(serializer.data)



@api_view(['GET'])
def comment_list(request):
    comments = Comment.objects.all()
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)


# @api_view(['GET'])
# def comment_detail(request, comment_pk):
#     comment = get_object_or_404(Comment, pk=comment_pk)
#     serializer = CommentSerializer(comment)
#     return Response(serializer.data)


@api_view(['POST'])
def comments_create(request, music_pk):
    # print(request.data)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True): # 검증에 실패하면 400 Bad Request오류를 발생
        serializer.save(music_id=music_pk)
    return Response(serializer.data)


@api_view(['DELETE', 'PUT'])
def comments_update_and_delete(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.method =='PUT':
        serializer = CommentSerializer(data=request.data, instance=comment)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)

    else: # DELETE
        comment.delete()
        return Response({'message':'Comment has been deleted!'})

