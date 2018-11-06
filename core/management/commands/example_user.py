from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User, Group
from django.db.utils import IntegrityError
from login.models import Userinfos
from core.models import Centers, Departaments, Areas

class Command(BaseCommand):

    help = 'Crea un listado de usuarios en base de datos'
    requires_migrations_checks = True

    USUARIOS = {
        "Teachers": [
            {
                "username": "jccuevas",
                "email": "jccuevas@ujaen.es",
                "password": "prueba123?",
                "first_name": "Juan Carlos",
                "last_name": "Cuevas",
                "departament": "Telecomunicaciones",
                "area": "Telemática"
            },
            {
                "username": "fnavarro",
                "email": "fnavarro@ujaen.es ",
                "password": "prueba123?",
                "first_name": "Francisco Javier",
                "last_name": "Sanchez-Roselly",
                "departament": "Telecomunicaciones",
                "area": "Telemática"
            },
            {
                "username": "ajyuste",
                "email": "ajyuste@ujaen.es",
                "password": "prueba123?",
                "first_name": "Antonio Jesús",
                "last_name": "Yuste",
                "departament": "Telecomunicaciones",
                "area": "Tecnologías de Telecomunicación"
            }
        ],
        "Departaments": [
            {
                "username": "teleco",
                "email": "teleco@ujaen.es",
                "password": "prueba123?",
                "departament": "Telecomunicaciones"
            },
        ],
        "Centers": [
            {
                "username": "epsl",
                "email": "epsl@ujaen.es",
                "password": "prueba123?",
                "center": "EPSL",
            },
            {
                "username": "cateleco",
                "email": "cateleco@ujaen.es",
                "password": "prueba123?",
                "center": "CA Telecomunicaciones",
            }
        ]
    }
    def add_arguments(self, parser):
        parser.add_argument(
            "--delete",
            action="store_true",
            dest="delete",
            help="revierte la inicialización"
        )

    def handle(self, *args, **options):
        try:
            if options["delete"]:
                self.__delete()
            else:
                self.__create_users(self.USUARIOS)
                self.stdout.write("Usuarios creados correctamente")
        except IntegrityError:
            raise CommandError("La inicialización ya ha sido realizada")
        except:
            raise CommandError("Error, revise que todo este correcto")

    def __delete(self):
        User.objects.all().delete()
        self.stdout.write("Usuarios eliminados correctamente")

    def __create_users(self, users):
        self.__create_teachers(users["Teachers"])
        self.__create_departaments(users["Departaments"])
        self.__create_centers(users["Centers"])

    @staticmethod
    def __create_teachers(teachers):
        teacher_group = Group.objects.get(name="Teachers")
        for teacher in teachers:
            user = User.objects.create_user(
                username=teacher["username"],
                email=teacher["email"],
                password=teacher["password"],
                first_name=teacher["first_name"],
                last_name=teacher["last_name"]
            )
            teacher_group.user_set.add(user)
            Userinfos.objects.create(
                departaments_id=Departaments.objects.get(name=teacher["departament"]).id,
                areas_id=Areas.objects.get(name=teacher["area"]).id,
                auth_id=user.id
            )

    @staticmethod
    def __create_departaments(departaments):
        departament_group = Group.objects.get(name="Departaments")
        for departament in departaments:
            user = User.objects.create_user(
                username=departament["username"],
                email=departament["email"],
                password=departament["password"],
            )
            departament_group.user_set.add(user)
            Userinfos.objects.create(
                departaments_id=Departaments.objects.get(name=departament["departament"]).id,
                auth_id=user.id
            )


    @staticmethod
    def __create_centers(centers):
        center_group = Group.objects.get(name="Centers")
        for center in centers:
            user = User.objects.create_user(
                username=center["username"],
                email=center["email"],
                password=center["password"],
            )
            center_group.user_set.add(user)
            Userinfos.objects.create(
                centers_id=Centers.objects.get(name=center["center"]).id,
                auth_id=user.id
            )
