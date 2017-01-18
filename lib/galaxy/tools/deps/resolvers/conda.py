"""
This is still an experimental module and there will almost certainly be backward
incompatible changes coming.
"""

import logging
import os

import galaxy.tools.deps.installable

from ..conda_util import (
    build_isolated_environment,
    cleanup_failed_install,
    CondaContext,
    CondaTarget,
    install_conda,
    install_conda_target,
    installed_conda_targets,
    is_conda_target_installed,
    USE_PATH_EXEC_DEFAULT,
)
from ..resolvers import (
    Dependency,
    DependencyException,
    DependencyResolver,
    InstallableDependencyResolver,
    ListableDependencyResolver,
    NullDependency,
)


DEFAULT_BASE_PATH_DIRECTORY = "_conda"
DEFAULT_CONDARC_OVERRIDE = "_condarc"
DEFAULT_ENSURE_CHANNELS = "conda-forge,r,bioconda,iuc"

log = logging.getLogger(__name__)


class CondaDependencyResolver(DependencyResolver, ListableDependencyResolver, InstallableDependencyResolver):
    dict_collection_visible_keys = DependencyResolver.dict_collection_visible_keys + ['conda_prefix', 'versionless', 'ensure_channels', 'auto_install']
    resolver_type = "conda"

    def __init__(self, dependency_manager, **kwds):
        self.versionless = _string_as_bool(kwds.get('versionless', 'false'))
        self.dependency_manager = dependency_manager

        def get_option(name):
            return self._get_config_option(name, dependency_manager, config_prefix="conda", **kwds)

        # Conda context options (these define the environment)
        conda_prefix = get_option("prefix")
        if conda_prefix is None:
            conda_prefix = os.path.join(
                dependency_manager.default_base_path, DEFAULT_BASE_PATH_DIRECTORY
            )

        self.conda_prefix_parent = os.path.dirname(conda_prefix)

        # warning is related to conda problem discussed in https://github.com/galaxyproject/galaxy/issues/2537, remove when that is resolved
        conda_prefix_warning_length = 50
        if len(conda_prefix) >= conda_prefix_warning_length:
            log.warning("Conda install prefix '%s' is %d characters long, this can cause problems with package installation, consider setting a shorter prefix (conda_prefix in galaxy.ini)" % (conda_prefix, len(conda_prefix)))

        condarc_override = get_option("condarc_override")
        if condarc_override is None:
            condarc_override = os.path.join(
                dependency_manager.default_base_path, DEFAULT_CONDARC_OVERRIDE
            )

        copy_dependencies = _string_as_bool(get_option("copy_dependencies"))
        conda_exec = get_option("exec")
        debug = _string_as_bool(get_option("debug"))
        ensure_channels = get_option("ensure_channels")
        use_path_exec = get_option("use_path_exec")
        if use_path_exec is None:
            use_path_exec = USE_PATH_EXEC_DEFAULT
        else:
            use_path_exec = _string_as_bool(use_path_exec)
        if ensure_channels is None:
            ensure_channels = DEFAULT_ENSURE_CHANNELS

        conda_context = CondaContext(
            conda_prefix=conda_prefix,
            conda_exec=conda_exec,
            debug=debug,
            ensure_channels=ensure_channels,
            condarc_override=condarc_override,
            use_path_exec=use_path_exec,
            copy_dependencies=copy_dependencies
        )
        self.ensure_channels = ensure_channels

        # Conda operations options (these define how resolution will occur)
        auto_install = _string_as_bool(get_option("auto_install"))
        self.auto_init = _string_as_bool(get_option("auto_init"))
        self.conda_context = conda_context
        self.disabled = not galaxy.tools.deps.installable.ensure_installed(conda_context, install_conda, self.auto_init)
        self.auto_install = auto_install
        self.copy_dependencies = copy_dependencies

    def clean(self, **kwds):
        return self.conda_context.exec_clean()

    def resolve(self, name, version, type, **kwds):
        # Check for conda just not being there, this way we can enable
        # conda by default and just do nothing in not configured.
        if not os.path.isdir(self.conda_context.conda_prefix):
            return NullDependency(version=version, name=name)

        if type != "package":
            return NullDependency(version=version, name=name)

        exact = not self.versionless or version is None
        if self.versionless:
            version = None

        conda_target = CondaTarget(name, version=version)
        is_installed = is_conda_target_installed(
            conda_target, conda_context=self.conda_context
        )

        job_directory = kwds.get("job_directory", None)
        if not is_installed and self.auto_install and job_directory:
            is_installed = self.install_dependency(name=name, version=version, type=type)

        if not is_installed:
            return NullDependency(version=version, name=name)

        # Have installed conda_target and job_directory to send it to.
        # If dependency is for metadata generation, store environment in conda-metadata-env
        if kwds.get("metadata", False):
            conda_env = "conda-metadata-env"
        else:
            conda_env = "conda-env"

        if job_directory:
            conda_environment = os.path.join(job_directory, conda_env)
        else:
            conda_environment = None

        return CondaDependency(
            self.conda_context,
            conda_environment,
            exact,
            name,
            version
        )

    def list_dependencies(self):
        for install_target in installed_conda_targets(self.conda_context):
            name = install_target.package
            version = install_target.version
            yield self._to_requirement(name, version)

    def install_dependency(self, name, version, type, **kwds):
        "Returns True on (seemingly) successfull installation"
        if type != "package":
            log.warning("Cannot install dependencies of type '%s'" % type)
            return False

        if self.versionless:
            version = None

        conda_target = CondaTarget(name, version=version)

        is_installed = is_conda_target_installed(
            conda_target, conda_context=self.conda_context
        )

        if is_installed:
            return is_installed

        return_code = install_conda_target(conda_target, conda_context=self.conda_context)
        if return_code != 0:
            is_installed = False
        else:
            # Recheck if installed
            is_installed = is_conda_target_installed(
                conda_target, conda_context=self.conda_context
            )
        if not is_installed:
            log.debug("Removing failed conda install of {}, version '{}'".format(name, version))
            cleanup_failed_install(conda_target, conda_context=self.conda_context)

        return is_installed

    @property
    def prefix(self):
        return self.conda_context.conda_prefix


class CondaDependency(Dependency):
    dict_collection_visible_keys = Dependency.dict_collection_visible_keys + ['environment_path', 'name', 'version']
    dependency_type = 'conda'
    cacheable = True

    def __init__(self, conda_context, environment_path, exact, name=None, version=None):
        self.activate = conda_context.activate
        self.conda_context = conda_context
        self.environment_path = environment_path
        self._exact = exact
        self._name = name
        self._version = version
        self.cache_path = None

    @property
    def exact(self):
        return self._exact

    @property
    def name(self):
        return self._name

    @property
    def version(self):
        return self._version

    def build_cache(self, cache_path):
        self.set_cache_path(cache_path)
        self.build_environment()

    def set_cache_path(self, cache_path):
        self.cache_path = cache_path
        self.environment_path = cache_path

    def build_environment(self):
        env_path, exit_code = build_isolated_environment(
            CondaTarget(self.name, self.version),
            path=self.environment_path,
            copy=self.conda_context.copy_dependencies,
            conda_context=self.conda_context,
        )
        if exit_code:
            if len(os.path.abspath(self.environment_path)) > 79:
                # TODO: remove this once conda_build version 2 is released and packages have been rebuilt.
                raise DependencyException("Conda dependency failed to build job environment. "
                                          "This is most likely a limitation in conda. "
                                          "You can try to shorten the path to the job_working_directory.")
            raise DependencyException("Conda dependency seemingly installed but failed to build job environment.")

    def shell_commands(self, requirement):
        if not self.cache_path:
            # Build an isolated environment if not using a cached dependency manager
            self.build_environment()
        return """[ "$CONDA_DEFAULT_ENV" = "%s" ] || . %s '%s' > conda_activate.log 2>&1 """ % (
            self.environment_path,
            self.activate,
            self.environment_path
        )


def _string_as_bool( value ):
    return str( value ).lower() == "true"


__all__ = ('CondaDependencyResolver', 'DEFAULT_ENSURE_CHANNELS')
