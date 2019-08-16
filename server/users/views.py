from random import choice
from datetime import datetime, timedelta
import re

from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth import get_user_model, login, authenticate, logout
# from django.contrib.auth.models import User
from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib import messages

from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializer import SmsSerializer,UserRegSerializer
from .models import VerifyCode,ImageCode
from .smsprovider import YunPian
from .makeimage import GetImageCode
from .forms import AuthenticateForm, UserCreateForm, UserChangeForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from django.contrib.auth.decorators import login_required

APIKEY = settings.APIKEY

class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username)|Q(mobile=username))
            if user.check_password(password):
                return user

        except Exception as e:
            return None


class ImageCodeView(APIView):
    '''
    获得图片验证码
    '''
    def get(self, request, *args, **kwargs):
        codedict = GetImageCode()
        codeid = codedict.get('code_id',0)
        reight_text = codedict.get('right_text',0)
        reight_text = reight_text.replace(' ','')
        imagemodel = ImageCode(codeid=codeid, code= reight_text)
        imagemodel.save()
        re_dict = {'imagepath':'/media/codeimage/'+codeid+'.png','codeid':codeid}
        return Response(re_dict, status=status.HTTP_201_CREATED)


class SmsCodeViewset(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    发送短信验证码
    """
    serializer_class = SmsSerializer

    def generate_code(self):
        """
        生成四位数字的验证码
        :return:
        """
        seeds = "1234567890"
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))
        return "".join(random_str)

    def codecheck(self,code, codeid):
        '''
        验证图片验证码，防止恶意用户狂注册
        :param code: 用户填写的验证码
        :param codeid: 验证码ID
        :return:
        '''
        five_mintes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
        right_code = ImageCode.objects.filter(codeid=codeid)
        # lte 小于等于 gte 大于等于
        tright_code = right_code.filter(add_time__gte=five_mintes_ago)
        if not tright_code:
            return 2
        if right_code:
            if str(right_code[0]).lower() != str(code).lower():
                return 0
        else:
            return 0

        return 1


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # 序列化和验证
        serializer.is_valid(raise_exception=True)
        mobile = serializer.validated_data['mobile']
        data = request.data
        imagecode = request.data.get('code',0)
        imagecodeid = request.data.get('codeid',0)

        image_c = self.codecheck(code=imagecode, codeid=imagecodeid)

        if image_c ==2:
            return Response(data={'error':'图片验证码超时'}, status=status.HTTP_400_BAD_REQUEST)
        elif image_c == 0:
            return Response(data={'error': '图片验证码错误'}, status=status.HTTP_400_BAD_REQUEST)
        yun_pian = YunPian(APIKEY)

        code = self.generate_code()

        sms_status = yun_pian.send_sms(code=code, mobile=mobile)

        if sms_status["code"] != 0:
            return Response({
                "data":'error'
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            code_record = VerifyCode(code=code, mobile=mobile)
            code_record.save()
            return Response({
                "data":'success'
            }, status=status.HTTP_201_CREATED)


def signup_view(request, user_form=None, incomplete_form=None):
    """
    View responsible for sign up (without facebook authorization)
    :param user_form: for to validate input data and create new user (UserProfile and User)
    :type user_form: `UserCreateForm()`
    :param incomplete_form: (temporary) variable that determines whether the user_form contains errors
    :type incomplete_form: `string`
    """
    if request.method == 'POST' and incomplete_form is None:
        user_form = UserCreateForm(data=request.POST)
        if user_form.is_valid():
            username = user_form.clean_username()
            password = user_form.clean_password2()
            user_form.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('library')
        else:
            messages.error(request, "Form invalid")
            return signup_view(request, user_form=user_form, incomplete_form=True)
    
    if incomplete_form is None or not incomplete_form:
        user_form = UserCreateForm()
    
    return render(request, 'signup.html', {'user_form': user_form})

def logout_view(request):
    logout(request)
    return redirect('library')

def signin_view(request, auth_form=None):
    if request.user.is_authenticated:
        redirect('library')
    if request.method == 'POST':
        form = AuthenticateForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('library')
        else:
            auth_form = auth_form or AuthenticateForm()
            return render(request, 'signin.html', {'auth_form': auth_form})
    auth_form = AuthenticateForm()
    return render(request, 'signin.html', {'auth_form': auth_form})

@login_required
def edituser_view(request, user_form=None, incomplete_form=None):
    if request.method == 'POST' and incomplete_form is None:
        user_form = UserChangeForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
        else:
            messages.error(request, "Form invalid")
            return edituser_view(request, user_form=user_form, incomplete_form=True)        
    
    return render(request, 'settings.html', {'user_form': user_form})

@login_required
def changepassword_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('changepassword_view')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'changepassword.html', {
        'form': form
    })