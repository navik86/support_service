from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import identify_hasher, make_password
from django.contrib.auth.models import GroupManager, Permission
from django.db import models
from django.db.models import BooleanField


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, name=None, full_name=None,
                    is_active=True, is_staff=None, is_admin=None):
        if not email:
            raise ValueError('User must have an email address')
        if not password:
            raise ValueError('The user must enter a password')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.staff = is_staff
        user.admin = is_admin
        user.active = is_active
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, name=None):
        user = self.create_user(email, name=name, password=password,
                                is_staff=True, is_admin=True)
        return user

    def create_staffuser(self, email, password=None, name=None):
        user = self.create_user(email, name=name, password=password,
                                is_staff=True, is_admin=False)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(unique=True, max_length=255, verbose_name='e-mail')
    name = models.CharField(max_length=255, blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Полное имя')
    admin = models.BooleanField(default=False, verbose_name='Админ')
    staff = models.BooleanField(default=False, verbose_name='Стафф')
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    support = BooleanField(default=False, verbose_name='Саппорт специалист')

    group = models.ForeignKey('UserGroup', on_delete=models.PROTECT,
                              verbose_name='Группы пользователей',
                              null=True
                              )

    # The field by which the authorization will take place
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_name(self):
        if self.name:
            return self.name
        return self.email

    def get_full_name(self):
        if self.full_name:
            return self.full_name
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        if self.admin:
            return True
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    def save(self, *args, **kwargs):
        try:
            _alg = identify_hasher(self.password)
        except ValueError:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)


class UserGroup(models.Model):
    """
Adding user groups to set permissions
    """
    name = models.CharField(max_length=150, unique=True)
    permissions = models.ManyToManyField(
        Permission,
        verbose_name='permissions',
        blank=True,
    )

    objects = GroupManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'group'
        verbose_name_plural = 'groups'