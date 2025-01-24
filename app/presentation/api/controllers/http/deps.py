from typing import Annotated

from dishka.entities.depends_marker import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import Depends as FromFastAPI
from fastapi.security import OAuth2PasswordBearer

from app.core.config import config
from app.domain.auth.dto import AuthDto
from app.domain.user.dto import UserFullDto
from app.infrastructure.usecases.usecases import Services

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f'{config.auth.api_url}/signin')


@inject
async def get_current_user_auth(
    token: Annotated[str, FromFastAPI(oauth2_scheme)],
    service: FromDishka[Services],
) -> AuthDto | None:
    user_from_token = await service.auth.user_auth_by_token(token)
    return await service.adapters.postgres.auth.get_auth_by_id(user_from_token.id)


@inject
async def get_current_user_full(
    token: Annotated[str, FromFastAPI(oauth2_scheme)],
    service: FromDishka[Services],
) -> UserFullDto | None:
    user_from_token = await service.auth.user_auth_by_token(token)
    return await service.adapters.postgres.user.get_full_by_id(user_from_token.id)


@inject
async def get_current_user_roles(
    token: Annotated[str, FromFastAPI(oauth2_scheme)],
    service: FromDishka[Services],
) -> list[str]:
    user_from_token = await service.auth.user_auth_by_token(token)
    return await service.adapters.postgres.auth.get_user_role_codes_by_id(user_from_token.id)


@inject
async def get_current_user_permissions(
    token: Annotated[str, FromFastAPI(oauth2_scheme)],
    service: FromDishka[Services],
) -> list[str]:
    user_from_token = await service.auth.user_auth_by_token(token)
    return await service.adapters.postgres.auth.get_user_permission_codes_by_id(user_from_token.id)


CurrentUserAuth = Annotated[AuthDto, FromFastAPI(get_current_user_auth)]
CurrentUserFull = Annotated[UserFullDto, FromFastAPI(get_current_user_full)]
CurrentUserRoles = Annotated[UserFullDto, FromFastAPI(get_current_user_roles)]
CurrentUserPermissions = Annotated[UserFullDto, FromFastAPI(get_current_user_permissions)]
