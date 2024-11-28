from dataclasses import dataclass


@dataclass
class Config:
    add_type_ignore: bool = False
    add_using_to_alter_operation: bool = True


_config = Config()


def set_configuration(config: Config):
    global _config
    _config = config


def get_configuration() -> Config:
    return _config
