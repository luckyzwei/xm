#coding=utf-8

from django.utils.deprecation import MiddlewareMixin
import logging

logger = logging.getLogger("all")
slogger = logging.getLogger("scripts")
class LogException(MiddlewareMixin):
    def process_exception(self, request, exception):
        slogger.exception(exception)
