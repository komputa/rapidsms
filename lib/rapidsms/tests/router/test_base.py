from nose.tools import assert_equals, assert_raises

from django.utils.functional import curry
from django.core.exceptions import ImproperlyConfigured

from rapidsms.apps.base import AppBase
from rapidsms.router import get_router
from rapidsms.router.base import BaseRouter


class MockRouter(object):
    pass


def test_get_router():
    assert_raises(ImproperlyConfigured, get_router,
                  'rapidsms.tests.test_router.BadClassName')
    assert_raises(ImproperlyConfigured, get_router,
                  'rapidsms.tests.bad_module.MockRouter')
    assert_equals(get_router('rapidsms.tests.router.test_base.MockRouter'),
                  MockRouter)


def test_router_calls_all_app_phases():
    class MockMsg(object):
        connection = None
        text = ''
        handled = False

    class MockApp(AppBase):
        start_phases = ["start"]
        incoming_phases = ["filter", "parse", "handle", "default", "cleanup"]
        outgoing_phases = ["outgoing"]
        stop_phases = ["stop"]
        called_phases = []

        def _append_phase(self, phase, *args, **kwargs):
            self.called_phases.append(phase)
            return False

        def __init__(self, router):
            phases = self.start_phases + self.incoming_phases +\
                     self.outgoing_phases + self.stop_phases
            for phase in phases:
                setattr(self, phase, curry(self._append_phase, phase))
            super(MockApp, self).__init__(router)

    router = BaseRouter()
    app = MockApp(router)
    router.apps.append(app)
    router.incoming(MockMsg())
    assert_equals(app.called_phases, app.incoming_phases)
    app.called_phases = []
    router.outgoing(MockMsg())
    assert_equals(app.called_phases, app.outgoing_phases)
    app.called_phases = []
    router.start()
    assert_equals(app.called_phases, app.start_phases)
    app.called_phases = []
    router.stop()
    assert_equals(app.called_phases, app.stop_phases)
