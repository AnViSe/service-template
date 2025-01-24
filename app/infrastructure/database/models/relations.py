from sqlalchemy import Column, ForeignKey, Table

from .base import Base

# roles_perms = Table(
#     'roles_perms',
#     Base.metadata,
#     Column('role_id', ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True, comment='Код роли'),
#     Column('perm_id', ForeignKey('permissions.id', ondelete='CASCADE'), primary_key=True, comment='Код разрешения'),
# )

users_roles = Table(
    'users_roles',
    Base.metadata,
    Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), primary_key=True, comment='Код пользователя'),
    Column('role_id', ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True, comment='Код роли'),
)

users_perms = Table(
    'users_perms',
    Base.metadata,
    Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), primary_key=True, comment='Код пользователя'),
    Column('perm_id', ForeignKey('permissions.id', ondelete='CASCADE'), primary_key=True, comment='Код разрешения'),
)
