from typing import Annotated

from dishka.entities.depends_marker import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import Depends as FromFastAPI
from fastapi.security import OAuth2PasswordBearer

from app.core.config import config
from app.domain.auth.dto import AuthDto
from app.domain.common.usecases import Services

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f'{config.auth.api_url}/signin')


@inject
async def get_current_user(
    token: Annotated[str, FromFastAPI(oauth2_scheme)],
    service: FromDishka[Services],
) -> AuthDto | None:
    return await service.auth.current_user_by_token(token)


CurrentUser = Annotated[AuthDto, FromFastAPI(get_current_user)]
