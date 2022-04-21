import os
import importlib
from ripda.conf import global_settings


class Settings:
    """
    importa para execução as configurações definidas no aplicativo.
    """

    SETTINGS_MODULE: str = ''

    def __init__(self) -> None:
        for setting in dir(global_settings):
            if setting.isupper():
                setattr(self, setting, getattr(global_settings, setting))

        self.SETTINGS_MODULE = os.environ.get('RIPDA_SETTINGS_MODULE', None)

        if self.SETTINGS_MODULE is not None:

            mod = importlib.import_module(self.SETTINGS_MODULE)

            tuple_settings = (
                'BLOCKCHAIN_NODES',
            )

            for setting in dir(mod):
                if setting.isupper():

                    setting_value = getattr(mod, setting)

                    if hasattr(setting_value, 'as_posix'):
                        setting_value = setting_value.as_posix()

                    if setting in tuple_settings and not isinstance(
                            setting_value, (list, tuple)
                    ):
                        raise ValueError(
                            "The %s setting must be a list or a tuple." % setting
                        )

                    setattr(self, setting, setting_value)


settings = Settings()
