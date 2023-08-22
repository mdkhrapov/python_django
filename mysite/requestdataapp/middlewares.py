from datetime import datetime, timedelta
from django.http import HttpRequest, HttpResponseForbidden


def set_useragent_on_request_middleware(get_response):
    print("Initial call")
    def middleware(request: HttpRequest):
        print("before get response")
        request.user_agent = request.META["HTTP_USER_AGENT"]
        response = get_response(request)
        print("after get response")
        return response

    return middleware

class CountRequestsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests_count = 0
        self.responses_count = 0
        self.exceptions_count = 0

    def __call__(self, request: HttpRequest):
        self.requests_count += 1
        print("requests_count: ", self.requests_count)
        response = self.get_response(request)
        self.responses_count += 1
        print("responses_count: ", self.responses_count)
        return response

    def process_exception(self, request: HttpRequest, exception: Exception):
        self.exceptions_count += 1
        print("got", self.exceptions_count, "exceptions so far")


class ThrottlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.ip_requests = {}                       # словарь в формате 'IP': время последнего запроса
        self.time_delta = timedelta(seconds=5)      # длина интервала времени

    def __call__(self, request: HttpRequest):
        ip = request.META.get("REMOTE_ADDR")
        time = datetime.now()

        if self.ip_requests.get(ip) == None:
            self.ip_requests[ip] = time
        else:
            saved_time = self.ip_requests[ip]
            self.ip_requests[ip] = time
            time_delta = time - saved_time

            if time_delta < self.time_delta: # если интервал между запросами не превышает self.time_delta секунд
                return HttpResponseForbidden(f"<h2>You send requests very often! {time_delta} since last request</h2>")
        response = self.get_response(request)
        return response