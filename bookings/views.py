import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from .models import FitnessClass, Booking
from .serializers import FitnessClassSerializer, BookingSerializer

logger = logging.getLogger(__name__)


def create_payload(status_bool, message, error=None, data=None):
    return {
        "status": status_bool,
        "message": message,
        "error": error,
        "data": data
    }


class ClassListView(APIView):
    def get(self, request):
        try:
            now = timezone.now()
            classes = FitnessClass.objects.filter(scheduled_at__gte=now).order_by('scheduled_at')
            serializer = FitnessClassSerializer(classes, many=True)
            logger.info(f"Returned {len(classes)} upcoming classes")
            return Response(
                create_payload(True, "Upcoming classes fetched successfully", data=serializer.data),
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Error fetching class list: {str(e)}")
            return Response(
                create_payload(False, "Error fetching classes", error=str(e)),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class BookingView(APIView):
    def post(self, request):
        try:
            class_id = request.data.get('class_id')
            name = request.data.get('client_name')
            email = request.data.get('client_email')

            if not all([class_id, name, email]):
                logger.warning(f"Missing booking fields: {request.data}")
                return Response(
                    create_payload(False, "Missing required fields", error="All fields are required"),
                    status=status.HTTP_400_BAD_REQUEST
                )

            try:
                fitness_class = FitnessClass.objects.get(id=class_id)
            except FitnessClass.DoesNotExist:
                logger.warning(f"Fitness class not found: class_id={class_id}")
                return Response(
                    create_payload(False, "Class not found", error="Invalid class ID"),
                    status=status.HTTP_404_NOT_FOUND
                )

            if fitness_class.available_slots <= 0:
                logger.info(f"Overbooking attempt for class_id={class_id}")
                return Response(
                    create_payload(False, "No slots available", error="Class is fully booked"),
                    status=status.HTTP_400_BAD_REQUEST
                )

            Booking.objects.create(
                fitness_class=fitness_class,
                client_name=name,
                client_email=email
            )
            fitness_class.available_slots -= 1
            fitness_class.save()

            logger.info(f"Booking successful: {name} for class_id={class_id}")
            return Response(
                create_payload(True, "Booking successful"),
                status=status.HTTP_201_CREATED
            )

        except ValidationError as ve:
            logger.warning(f"Validation error during booking: {str(ve)}")
            return Response(
                create_payload(False, "Validation error", error=str(ve)),
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Unexpected error in booking: {str(e)}")
            return Response(
                create_payload(False, "Error creating booking", error=str(e)),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class BookingListView(APIView):
    def get(self, request):
        try:
            email = request.GET.get('email')
            if not email:
                logger.warning("Missing email in booking list request")
                return Response(
                    create_payload(False, "Missing email", error="Email is required as query param"),
                    status=status.HTTP_400_BAD_REQUEST
                )

            bookings = Booking.objects.filter(client_email=email)
            serializer = BookingSerializer(bookings, many=True)
            logger.info(f"Returned {len(bookings)} bookings for email: {email}")
            return Response(
                create_payload(True, "Bookings fetched successfully", data=serializer.data),
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Error fetching bookings: {str(e)}")
            return Response(
                create_payload(False, "Error fetching bookings", error=str(e)),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )