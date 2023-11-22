from rest_framework.views import APIView
from apps.mediation.models import Mediator, Mediation
from apps.core.responses import CustomResponse
from apps.mediation.models import Mediator, Mediation
from apps.mediation.serializers import MediatorSerializer, MediationSerializer
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle


class MediatorList(APIView):
    """
    List all mediators.
    """

    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    @extend_schema(
        responses={200: MediatorSerializer(many=True)},
        request=MediatorSerializer,
        tags=["mediation"],
    )
    def get(self, request, format=None):
        mediators = Mediator.objects.all()
        serializer = MediatorSerializer(mediators, many=True)
        if serializer.is_valid():
            return CustomResponse.success(
                status_code=status.HTTP_200_OK,
                detail="Mediators retrieved successfully",
                data=serializer.data,
            )
        return CustomResponse.error(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mediators not retrieved",
            data=serializer.errors,
        )


class MediatorDetail(APIView):
    """
    Retrieve a mediator instance.
    """

    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    @extend_schema(
        responses={200: MediatorSerializer},
        request=MediatorSerializer,
        tags=["mediation"],
    )
    def get(self, request, pk, format=None):
        try:
            mediator = Mediator.objects.get(pk=pk)
        except Mediator.DoesNotExist:
            return CustomResponse.error(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mediator not found",
                data={},
            )
        serializer = MediatorSerializer(mediator)
        return CustomResponse.success(
            status_code=status.HTTP_200_OK,
            detail="Mediator retrieved successfully",
            data=serializer.data,
        )


class CreateMediator(APIView):
    """
    Create a new mediator instance.
    """

    # permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    @extend_schema(
        responses={200: MediatorSerializer},
        request=MediatorSerializer,
        tags=["mediation"],
    )
    def post(self, request, format=None):
        serializer = MediatorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return CustomResponse.success(
                status_code=status.HTTP_201_CREATED,
                detail="Mediator created successfully",
                data=serializer.data,
            )
        return CustomResponse.error(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mediator not created",
            data=serializer.errors,
        )


class DeleteMediator(APIView):
    """
    Delete a mediator instance.
    """

    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    @extend_schema(
        responses={200: MediatorSerializer},
        request=MediatorSerializer,
        tags=["mediation"],
    )
    def delete(self, request, pk, format=None):
        try:
            mediator = Mediator.objects.get(pk=pk)
        except Mediator.DoesNotExist:
            return CustomResponse.error(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mediator not found",
                data={},
            )
        mediator.delete()
        return CustomResponse.success(
            status_code=status.HTTP_200_OK,
            detail="Mediator deleted successfully",
            data={},
        )


class MediationList(APIView):
    """
    List all mediations.
    """

    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    @extend_schema(
        responses={200: MediationSerializer(many=True)},
        request=MediationSerializer,
        tags=["mediation"],
    )
    def get(self, request, format=None):
        mediations = Mediation.objects.all()
        serializer = MediationSerializer(mediations, many=True)
        if serializer.is_valid():
            return CustomResponse.success(
                status_code=status.HTTP_200_OK,
                detail="Mediations retrieved successfully",
                data=serializer.data,
            )
        return CustomResponse.error(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mediations not retrieved",
            data=serializer.errors,
        )


class CreateMediation(APIView):
    """
    Create a new mediation instance.
    """

    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    @extend_schema(
        responses={200: MediationSerializer},
        request=MediationSerializer,
        tags=["mediation"],
    )
    def post(self, request, format=None):
        serializer = MediationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return CustomResponse.success(
                status_code=status.HTTP_201_CREATED,
                detail="Mediation created successfully",
                data=serializer.data,
            )
        return CustomResponse.error(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mediation not created",
            data=serializer.errors,
        )


class UpdateMediation(APIView):
    """
    Update a mediation instance.
    """

    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    @extend_schema(
        responses={200: MediationSerializer},
        request=MediationSerializer,
        tags=["mediation"],
    )
    def put(self, request, pk, format=None):
        try:
            mediation = Mediation.objects.get(pk=pk)
        except Mediation.DoesNotExist:
            return CustomResponse.error(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mediation not found",
                data={},
            )
        serializer = MediationSerializer(mediation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return CustomResponse.success(
                status_code=status.HTTP_200_OK,
                detail="Mediation updated successfully",
                data=serializer.data,
            )
        return CustomResponse.error(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mediation not updated",
            data=serializer.errors,
        )


class MediationDetail(APIView):
    """
    Retrieve a mediation instance.
    """

    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    @extend_schema(
        responses={200: MediationSerializer},
        request=MediationSerializer,
        tags=["mediation"],
    )
    def get(self, request, pk, format=None):
        try:
            mediation = Mediation.objects.get(pk=pk)
        except Mediation.DoesNotExist:
            return CustomResponse.error(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mediation not found",
                data={},
            )
        serializer = MediationSerializer(mediation)
        return CustomResponse.success(
            status_code=status.HTTP_200_OK,
            detail="Mediation retrieved successfully",
            data=serializer.data,
        )


class DeleteMediation(APIView):
    """
    Delete a mediation instance.
    """

    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    @extend_schema(
        responses={200: MediationSerializer},
        request=MediationSerializer,
        tags=["mediation"],
    )
    def delete(self, request, pk, format=None):
        try:
            mediation = Mediation.objects.get(pk=pk)
        except Mediation.DoesNotExist:
            return CustomResponse.error(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Mediation not found",
                data={},
            )
        mediation.delete()
        return CustomResponse.success(
            status_code=status.HTTP_200_OK,
            detail="Mediation deleted successfully",
            data={},
        )
