from ninja import Router
from .shcema import Signin, Signup, ChangePassword, TinyUserSchema

from common.schema import MessageSchema
from ninja import errors
from django.contrib.auth import get_user_model, login, logout
from ninja.security import django_auth


router = Router(tags=["users"])


## http://localhost:8000/api/v1/users
@router.post("/signup", response=MessageSchema)
def signup(request, payload: Signup):
    payload_dict = payload.dict()

    email = payload_dict.get("email")
    password = payload_dict.get("password")
    username = payload_dict.get("username")
    password_confirm = payload_dict.get("password_confirm")

    if password != password_confirm:
        raise errors.ValidationError("저기여 패스워드가 다르자나여!!")

    username = None if username is None else username

    user_exists = get_user_model().objects.filter(email=email).exists()
    if user_exists:
        raise errors.ValidationError("저기여 이미 유저가 있자나여")

    user = get_user_model().objects.create_user(
        email=email,
        password=password,
        username=username,
    )
    login(request, user)

    return {"message": "회원가입 ㅊㅋ"}


## login
@router.post("/signin", response=MessageSchema)
def signin(request, payload: Signin):
    payload_dict = payload.dict()
    email = payload_dict.get("email")
    password = payload_dict.get("password")

    user_exist = get_user_model().objects.filter(email=email).exists()
    if not user_exist:
        raise errors.AuthenticationError("저기여 아아디기 없거나 비밀번호가 틀렸으라")

    user = get_user_model().objects.get(email=email)
    if not user.check_password(password):
        raise errors.AuthenticationError("저기여 아아디기 없거나 비밀번호가 틀렸으라")

    login(request, user)
    return {"message": "로그인 되었으라!"}


@router.get("/me", response={200: TinyUserSchema}, auth=django_auth)
def get_me(request):
    return 200, request.user


## 패스워드 바꾸기
@router.patch("/me/chage_password", auth=django_auth)
def change_password(request, payload: ChangePassword):
    if not request.user.is_authenticated:
        raise errors.AuthenticationError("로그인 해라!")

    payload_dict = payload.dict()
    old_password = payload_dict.get("old_password")
    new_password = payload_dict.get("new_password")
    new_password_confirm = payload_dict.get("new_password_confirm")

    user = request.user
    if not user.check_password(old_password):
        raise errors.AuthenticationError("저기여 아아디기 없거나 비밀번호가 틀렸으라")

    if new_password != new_password_confirm:
        raise errors.ValidationError("저기여 패스워드가 다르자나여!!")

    user.set_password(new_password)
    user.save()

    return {"message": "password change 성공"}


## 로그아웃
@router.post("/signout")
def signout(request):
    logout(request)
    return {"message": "로그아웃!"}
