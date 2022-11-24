import logging
from quart import request, Response
from application.views.base_views import BaseExperienceMethodView


class AdminUpdateExperienceView(BaseExperienceMethodView):
    """
    TODO - Implement authorization checking auth token permissions
     (e.g. JWT), and enabling access to admin users only.
    """
    async def put(self, experience_id: str) -> Response:
        try:
            # Get request body params and validate
            data = await request.json
            capacity = data.get("capacity", None)

            if capacity is None:
                return Response(response="Missing or invalid 'capacity' param.", status=400)

            # Update the experience
            error_msg = await self.service.update_experience(experience_id, capacity, None)

            # If failed, return error
            if error_msg:
                return Response(response=error_msg, status=400)

            # Return response
            return Response(response="Updated", status=200)
        except Exception as exc:
            logging.log(logging.ERROR, exc)
            return Response(response=f"Unknown error: {exc}", status=400)
