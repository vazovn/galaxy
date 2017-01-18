"""Integration tests for conda dependency resolution."""
import os
import shutil
from tempfile import mkdtemp

from base import integration_util
from base.api import ApiTestCase

GNUPLOT = {u'version': u'4.6', u'type': u'package', u'name': u'gnuplot'}


class CondaResolutionIntegrationTestCase(integration_util.IntegrationTestCase, ApiTestCase):
    """Test conda dependency resolution through API."""

    framework_tool_and_types = True

    @classmethod
    def handle_galaxy_config_kwds(cls, config):
        cls.conda_tmp_prefix = mkdtemp()
        config["use_cached_dep_manager"] = True
        config["conda_auto_init"] = True
        config["conda_prefix"] = os.path.join(cls.conda_tmp_prefix, 'conda')

    @classmethod
    def tearDownClass(cls):
        """Shutdown Galaxy server and cleanup temp directory."""
        shutil.rmtree(cls.conda_tmp_prefix)
        cls._test_driver.tear_down()
        cls._app_available = False

    def test_dependency_before_install( self ):
        """
        Test that dependency is not installed (response['dependency_type'] == 'null').
        """
        data = GNUPLOT
        create_response = self._get( "dependency_resolvers/dependency", data=data, admin=True )
        self._assert_status_code_is( create_response, 200 )
        response = create_response.json()
        assert response['dependency_type'] is None and response['exact']

    def test_dependency_install( self ):
        """
        Test installation of GNUPLOT dependency.
        """
        data = GNUPLOT
        create_response = self._post( "dependency_resolvers/dependency", data=data, admin=True )
        self._assert_status_code_is( create_response, 200 )
        response = create_response.json()
        assert response['dependency_type'] == 'conda' and response['exact']

    def test_dependency_install_not_exact(self):
        """
        Test installation of gnuplot with a version that does not exist.
        Sh
        """
        data = GNUPLOT.copy()
        data['version'] = '4.9999'
        create_response = self._post("dependency_resolvers/dependency", data=data, admin=True)
        self._assert_status_code_is(create_response, 200)
        response = create_response.json()
        assert response['dependency_type'] == 'conda' and not response['exact']

    def test_dependency_status_installed_exact( self ):
        """
        GET request to dependency_resolvers/dependency with GNUPLOT dependency.
        Should be installed through conda (response['dependency_type'] == 'conda').
        """
        data = GNUPLOT
        create_response = self._get( "dependency_resolvers/dependency", data=data, admin=True )
        self._assert_status_code_is( create_response, 200 )
        response = create_response.json()
        assert response['dependency_type'] == 'conda' and response['exact']

    def test_dependency_status_installed_not_exact( self ):
        """
        GET request to dependency_resolvers/dependency with GNUPLOT dependency.
        Should be installed through conda (response['dependency_type'] == 'conda'),
        but version 4.9999 does not exist.
        """
        data = GNUPLOT.copy()
        data['version'] = '4.9999'
        create_response = self._get( "dependency_resolvers/dependency", data=data, admin=True )
        self._assert_status_code_is( create_response, 200 )
        response = create_response.json()
        assert response['dependency_type'] == 'conda' and not response['exact']

    def test_conda_install_through_tools_api( self ):
        tool_id = 'mulled_example_multi_1'
        endpoint = "tools/%s/install_dependencies" % tool_id
        data = {'id': tool_id}
        create_response = self._post(endpoint, data=data, admin=True)
        self._assert_status_code_is( create_response, 200 )
        response = create_response.json()
        assert any([True for d in response if d['dependency_type'] == 'conda'])
        endpoint = "tools/%s/build_dependency_cache" % tool_id
        create_response = self._post(endpoint, data=data, admin=True)
        self._assert_status_code_is( create_response, 200 )

    def test_conda_clean( self ):
        endpoint = 'dependency_resolvers/clean'
        create_response = self._post(endpoint, data={}, admin=True)
        self._assert_status_code_is(create_response, 200)
        response = create_response.json()
        assert response == "OK"
