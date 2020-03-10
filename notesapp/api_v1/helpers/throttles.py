from rest_framework.throttling import UserRateThrottle


class UserThrottlePerMinute(UserRateThrottle):
    rate = '10/minute'
