# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from paas_wl.platform.auth.permissions import IsInternalAdmin
from paas_wl.platform.system_api.views import SysAppRelatedViewSet
from paas_wl.release_controller.hooks import serializers
from paas_wl.release_controller.hooks.models import Command
from paas_wl.resources import tasks as scheduler_tasks
from paas_wl.resources.actions.exec import interrupt_command
from paas_wl.utils.constants import CommandType
from paas_wl.utils.error_codes import error_codes


class CommandViewSet(SysAppRelatedViewSet):
    model = Command
    serializer_class = serializers.SimpleCommandSerializer
    permission_classes = [IsAuthenticated, IsInternalAdmin]

    def create(self, request, **kwargs):
        slz = serializers.CreateCommandSerializer(data=request.data)
        slz.is_valid(raise_exception=True)
        data = slz.validated_data

        app = self.get_app()
        build = app.build_set.get(pk=data.pop("build"))
        type_ = CommandType(data.pop("type"))

        command = app.command_set.new(
            type_=type_,
            command=data["command"],
            build=build,
            operator=data["operator"],
        )

        scheduler_tasks.run_command.delay(
            command.uuid, stream_channel_id=data.get("stream_channel_id"), extra_envs=data.get("extra_envs", {})
        )
        return Response(serializers.SimpleCommandSerializer(command).data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        app = self.get_app()

        command = get_object_or_404(app.command_set, pk=self.kwargs["uuid"])
        return Response(serializers.CommandWithLogsSerializer(command).data)

    def user_interrupt(self, request, **kwargs):
        """Interrupt a user command"""
        app = self.get_app()

        command = get_object_or_404(app.command_set, pk=self.kwargs["uuid"])
        if not command.check_interruption_allowed():
            raise error_codes.INTERRUPTION_NOT_ALLOWED
        if not interrupt_command(command):
            raise error_codes.INTERRUPTION_FAILED.f("指令可能已执行完毕.")
        return Response({})
