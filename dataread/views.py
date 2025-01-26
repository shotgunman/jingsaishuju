from django.shortcuts import render
import csv
from django.views.decorators.csrf import csrf_exempt
from .models import Competition
import json
from django.views.decorators.http import require_http_methods
from django.core.exceptions import FieldError
from django.shortcuts import get_list_or_404
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from .models import Users
from .serializers import UserSerializer,CompetitionSerializer
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict

# ----------------------------------- 账户系统 --------------------------------------------------

class RegisterView(APIView):
    """
        RegisterView类用于处理用户的注册请求。

        post方法接收一个包含'username', 'password', 'manager', 和 'real_name'等字段的POST请求，
        并使用UserSerializer将其序列化。如果数据有效，它将会创建一个新的用户实例并返回201状态码。
        如果数据无效，它会返回400状态码和错误信息。
    """
    def post(self, request, format=None):
        """
        处理POST请求，创建新的用户。

        参数:
        request (Request): Django REST framework的Request实例，包含用户发送的数据。
        format (str, 可选): 请求的格式，例如'json'，'xml'等。默认为None。

        返回:
        Response: 包含新创建的用户数据或错误信息的Response实例。
        """
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request, format=None):
        data = request.data
        user = Users.objects.filter(username=data.get('username'),password=data.get('password')).first()
        if user:
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        return Response({"detail": "登录信息不正确"}, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(APIView):
    def get(self, request, pk, format=None):
        user = Users.objects.filter(id=pk).first()
        if user:
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        return Response({"detail": "用户不存在"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk, format=None):
        user = Users.objects.filter(id=pk).first()
        if user:
            data = request.data
            if 'password' in data:
                data['password'] = make_password(data['password'])
            serializer = UserSerializer(user, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "用户不存在"}, status=status.HTTP_404_NOT_FOUND)
# ----------------------------------- 修改数据 --------------------------------------------------
# 创建项目
class Project_Create(APIView):
    def post(self, request, format=None):
        """
            创建或更新一个比赛项目。

            通过POST请求接收一个包含比赛详细信息的JSON数据。如果存在相同的比赛，则更新该比赛。如果不存在，则创建新的比赛。

            Args:
                request (HttpRequest): Django的http请求对象，包含一个JSON数据体，该数据体应包含比赛的详细信息。

            Returns:
                JsonResponse: 包含状态信息的JSON响应，如果成功创建或更新比赛，状态码为201。
            """
        data = request.data
        serializer = CompetitionSerializer(data=data)
        '''
        _, created = Competition.objects.update_or_create(
            year=data['year'],
            name=data['name'],
            competition_level=data['competition_level'],
            award_level=data['award_level'],
            leader_name=data['leader_name'],
            leader_id=data['leader_id'] if data['leader_id'] else None,
            member_name=data['member_name'],
            is_guoyuan=True if data['is_guoyuan'] == 'True' else False
        )
        '''
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Project_Get(APIView):
    def post(self, request, format=None):
        """
            根据给定的字段名和字段值查询并返回所有相关的比赛。

            通过POST请求接收一个包含字段名和字段值的JSON数据。查询数据库中所有字段名为field_name，字段值为field_value的比赛。

            Args:
                request (HttpRequest): Django的http请求对象，包含一个JSON数据体，该数据体应包含字段名和字段值。

            Returns:
                JsonResponse: 包含比赛列表的JSON响应，如果没有找到任何比赛或字段名无效，将返回一个包含错误信息的JSON响应。
            """
        data = request.data.dict()
        try:
            # 使用 filter 来获取所有字段名为 field_name，字段值为 field_value 的比赛
            competitions = Competition.objects.filter(**data)

            # 将比赛转换为可序列化的字典列表
            competitions_list = [model_to_dict(competition) for competition in competitions]

            # 返回 JSON 响应
            return JsonResponse(competitions_list, safe=False)
        except FieldError:
            return JsonResponse({"error": "Invalid field name."}, status=400)

class Project_Del(APIView):
    def post(self, request, format=None):
        """
        根据给定的字段名和字段值查询并删除指定的比赛,然后返回结果。

        通过POST请求接收一个包含给定的字段名和字段值的JSON数据。如果找到了相应的比赛，就删除它。如果没有找到，就返回一个HTTP 404错误。

        Args:
            request (HttpRequest): Django的http请求对象，包含一个JSON数据体，该数据体应包含要删除的比赛的id。

        Returns:
            JsonResponse: 包含状态信息的JSON响应，如果成功删除比赛，返回"deleted"状态；如果没有找到比赛，返回HTTP 404错误。
        """
        data = request.data.dict()
        try:
            # 使用 get_object_or_404 来获取满足条件的比赛
            competitions = Competition.objects.filter(**data)

            # 删除找到的比赛
            competitions.delete()

            # 返回 JSON 响应
            return JsonResponse({"status": "deleted"})
        except FieldError:
            return JsonResponse({"error": "Invalid field name."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

# 调取全部数据
class GetAllCompetitions(APIView):
    """
    一次性从数据库读取所有比赛数据的API函数。
    """
    def get(self, request, format=None):
        """
        一次性获取所有比赛的API接口。

        Args:
            request (HttpRequest): Django的http请求对象。

        Returns:
            JsonResponse: 包含所有比赛数据的JSON响应。
        """
        try:
            # 获取所有比赛的实例
            all_competitions = Competition.objects.all()

            # 序列化所有比赛数据
            competitions_data = CompetitionSerializer(all_competitions, many=True).data

            # 返回 JSON 响应
            return JsonResponse(competitions_data, safe=False)
        except Exception as e:
            # 如果发生错误，返回包含错误信息的JSON响应,返回值为500
            return JsonResponse({"error": str(e)}, status=500)
# -------------------------------上传csv----------------------------------------------
@csrf_exempt
def upload_csv(request):
    """
        上传并处理CSV文件，用于创建或更新比赛项目。

        通过POST请求接收一个CSV文件。文件应包含以下列：year, name, competition_level, award_level, leader_name, leader_id, member_name, is_guoyuan。
        对于每一行，如果存在相同的比赛（基于year和name字段），则更新该比赛。如果不存在，则创建新的比赛。

        Args:
            request (HttpRequest): Django的http请求对象，包含一个CSV文件。

        Returns:
            HttpResponse: 如果CSV文件成功上传并处理，返回一个包含成功消息的HTTP响应。
        """
    csv_file = request.FILES['DATA']
    decoded_file = csv_file.read().decode('utf-8').splitlines()
    reader = csv.DictReader(decoded_file)

    for row in reader:
        _, created = Competition.objects.update_or_create(
            year=row['year'],
            name=row['name'],
            competition_level=row['competition_level'],
            award_level=row['award_level'],
            leader_name=row['leader_name'],
            leader_id=row['leader_id'] if row['leader_id'] else None,
            member_name=row['member_name'],
            is_guoyuan=True if row['is_guoyuan'] == 'True' else False
        )

    return HttpResponse("CSV file uploaded and processed successfully")






