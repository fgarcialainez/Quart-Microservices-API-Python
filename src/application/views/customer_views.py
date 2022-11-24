import logging

from quart import Response, request
from quart_schema import validate_response

from application.views.base_views import BaseExperienceMethodView, ExperienceListResponse


class CustomerListExperiencesView(BaseExperienceMethodView):
    """
    TODO - Implement authorization checking auth token permissions, and enabling
     access only to the customer users that are registered in the system.
    """

    @validate_response(ExperienceListResponse, 200)
    async def get(self):
        try:
            # Get the list of experiences
            model_list = await self.service.get_experiences_list()

            # Return the model list
            return ExperienceListResponse(experiences=model_list)
        except Exception as exc:
            logging.log(logging.ERROR, exc)
            return Response(response=f"Unknown error: {exc}", status=400)


class CustomerBookExperienceView(BaseExperienceMethodView):
    """
    TODO - Implement authorization checking auth token permissions, and enabling access
     only to the customer users that are registered in the system. Extract customer_id
     from the token (e.g. JWT), passing it to the partners API in the purchase service call.
    """

    async def post(self) -> Response:
        try:
            # Get request params and perform validation
            data = await request.json
            experience_id = data.get("experience_id", None)
            quantity = data.get("quantity", None)

            if not experience_id or quantity is None or quantity <= 0:
                return Response(
                    response="Missing or invalid 'experience_id' and/or 'quantity' params.",
                    status=400
                )

            # Book the experience
            error_msg = await self.service.book_experience(experience_id, quantity)

            # If failed, return error
            if error_msg:
                return Response(response=error_msg, status=400)

            return Response(response="Booked", status=200)
        except Exception as exc:
            logging.log(logging.ERROR, exc)
            return Response(response=f"Unknown error: {exc}", status=400)
