from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    GenericAPIView,
    get_object_or_404,
)

from employees.api.permissions import IsGroupEmployeeOnly
from employees.models import Employee
from employees.api.serializers import (
    EmployeeSerializer,
    RegisterSerializer,
    LoginSerializer,
    LogoutSerializer,
)


class EmployeeView(ListAPIView):
    """View to representation employees info"""
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = (IsGroupEmployeeOnly, )


class EmployeeLevelView(ModelViewSet):
    """View to representation employees info by level"""
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = (IsGroupEmployeeOnly, )

    def get_queryset(self):
        return self.queryset.filter(level=self.kwargs["level"])


class RegisterView(CreateAPIView):
    """View to manage log-out post-request"""
    queryset = Employee.objects.all()
    permission_classes = ([IsAdminUser | IsGroupEmployeeOnly])
    serializer_class = RegisterSerializer


class LoginView(TokenViewBase):
    """
    View to manage log-in post-request.
    Returns tokens in the response
    """
    serializer_class = LoginSerializer


class LogoutView(GenericAPIView):
    """View to manage log-out post-request"""
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data={"logout": "access"},
                        status=status.HTTP_200_OK)


class EmployeeInfoView(ModelViewSet):
    """View to representation Authenticated employee info"""
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = (IsAuthenticated, )

    def get_object(self):
        return get_object_or_404(self.queryset, pk=self.request.user.id)
