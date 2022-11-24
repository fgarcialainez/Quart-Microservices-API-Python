import logging

from quart import request, Response
from quart_schema import validate_response

from application.views.base_views import BaseExperienceMethodView
from application.views.customer_views import ExperienceListResponse


class PartnerListExperiencesView(BaseExperienceMethodView):
    """
    TODO - Implement authorization checking auth token permissions, and getting
     the partner_id from the auth token (e.g. JWT) instead of using a query param.
    """

    @validate_response(ExperienceListResponse, 200)
    async def get(self):
        try:
            # Get partner_id param
            partner_id = request.args.get('partner_id', None)

            if not partner_id:
                return Response(response="Missing or invalid 'partner_id' param.", status=400)

            # Get the list of experiences for the partner
            model_list = await self.service.get_experiences_list(partner_id)

            # Return the model list
            return ExperienceListResponse(experiences=model_list)
        except Exception as exc:
            logging.log(logging.ERROR, exc)
            return Response(response=f"Unknown error: {exc}", status=400)


class PartnerUpdateExperienceView(BaseExperienceMethodView):
    """
    TODO - Implement authorization checking auth token permissions, and enabling
     access only to the partner that is the owner of the experience, extracting
     the partner_id from the token (e.g. JWT).
    """
    async def put(self, experience_id: str) -> Response:
        try:
            # Get request body params and validate
            data = await request.json
            available = data.get("available", None)

            if available is None:
                return Response(response="Missing or invalid 'available' param.", status=400)

            # Update the experience
            error_msg = await self.service.update_experience(experience_id, None, available)

            # If failed, return error
            if error_msg:
                return Response(response=error_msg, status=400)

            # Return response
            return Response(response="Updated", status=200)
        except Exception as exc:
            logging.log(logging.ERROR, exc)
            return Response(response=f"Unknown error: {exc}", status=400)


class PartnerGetExperienceView(BaseExperienceMethodView):
    """
    TODO - Implement authorization checking auth token permissions (e.g. JWT), validating
     that the given experience belongs to the partner that is performing the call.
    """

    async def get(self, experience_id: str):
        try:
            # Get the experience
            model = await self.service.get_experience(experience_id)

            if not model:
                return Response(response="The experience doesn't exist.", status=400)

            # Return response
            return model
        except Exception as exc:
            logging.log(logging.ERROR, exc)
            return Response(response=f"Unknown error: {exc}", status=400)
