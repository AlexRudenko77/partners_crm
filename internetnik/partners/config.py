from dataclasses import dataclass
from typing import List

from environs import Env


@dataclass
class DatabaseConfig:
    database: str  # Название базы данных
    db_host: str  # URL-адрес базы данных
    db_user: str  # Username пользователя базы данных
    db_password: str  # Пароль к базе данных


@dataclass
class SecretKeyConfig:
    secret_key: str  # Секретный ключ проекта


@dataclass
class StaticUrlConfig:
    static_url: str  # месторасположение статических файлов



@dataclass
class HostsConfig:
    hosts: List[str]    # Список доменов


@dataclass
class Config:
    django_key: SecretKeyConfig
    db: DatabaseConfig
    static: StaticUrlConfig
    hosts: HostsConfig


def load_config(path: str | None = None) -> Config:
    env: Env = Env()
    env.read_env(path)
    return Config(
        django_key=SecretKeyConfig(
            secret_key=env('SECRET_KEY'),
        ),
        db=DatabaseConfig(
            database=env('DATABASE'),
            db_host=env('DB_HOST'),
            db_user=env('DB_USER'),
            db_password=env('DB_PASSWORD')
        ),
        static=StaticUrlConfig(
            static_url=env('STATIC_URL')
        ),
        hosts=HostsConfig(
            hosts=env.list('ALLOWED_HOSTS', subcast=str)
        )
    )
