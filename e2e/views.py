from django.core.management import call_command
from django.http import JsonResponse
from rest_framework.views import APIView


class CallCommandView(APIView):
    def get(self, request, command):
        try:
            data = request.GET.copy()
            arg_or_args = data.get('args', '')

            if 'args' in data:
                data.pop('args')

            arg_or_args = [arg.strip() for arg in arg_or_args.split(',') if arg.strip()]

            call_command(command, *arg_or_args, **data.dict())

            return JsonResponse(status=200, data={})
        except Exception as e:
            print(e)

            return JsonResponse(status=500, data={'error': str(e)})
