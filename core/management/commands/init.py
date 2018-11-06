from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group, Permission
from django.db.utils import IntegrityError
from core.models import Centers, Departaments, Areas, Carrers, Masters
from core.models import Itineraries, Mentions, Skills

class Command(BaseCommand):

    help = 'Inicialización de los valores de la base de datos'
    requires_migrations_checks = True

    GROUPS = [
        'Teachers',
        'Departaments',
        'Centers'
    ]

    CENTERS = [
        "EPSL",
        "CA Telecomunicaciones"
    ]

    DEPARTAMENTS = [
        "Telecomunicaciones"
    ]

    AREAS = [
        {
            "name": "Tecnologías de Telecomunicación",
            "departament": "Telecomunicaciones"
        },
        {
            "name": "Telemática",
            "departament": "Telecomunicaciones"
        }
    ]

    MASTERS = [
        {
            "name": "Máster Universitario en Ingeniería de Telecomunicación",
            "center": "CA Telecomunicaciones",
            "departament": "Telecomunicaciones"
        },
    ]

    CARRERS = [
        {
            "name": "Grado en Ingeniería de Tecnologías de Telecomunicación",
            "center": "EPSL",
            "departament": "Telecomunicaciones",
            "itineraries": {
                "Sistemas de telecomunicación": [
                    {
                        "name": "ST.1",
                        "description": "Capacidad para construir, explotar y gestionar las redes, "
                                       + "servicios, procesos y aplicaciones de telecomunicaciones, "
                                       + "entendidas éstas como sistemas de captación, transporte, "
                                       + "representación, procesado, almacenamiento, gestión y presentación"
                                       + " de información multimedia, desde el punto de vista de los "
                                       + "sistemas de transmisión."
                    },
                    {
                        "name": "ST.2",
                        "description": "Capacidad para aplicar las técnicas en que se basan las redes, "
                                       + "servicios y aplicaciones de telecomunicación tanto en entornos"
                                       + " fijos como móviles, personales, locales o a gran distancia, "
                                       + "con diferentes anchos de banda, incluyendo telefonía, "
                                       + "radiodifusión, televisión y datos, desde el punto de vista "
                                       + "de los sistemas de transmisión."
                    },
                    {
                        "name": "ST.3",
                        "description": "Capacidad de análisis de componentes y sus especificaciones "
                                       + "para sistemas de comunicaciones guiadas y no guiadas."
                    },
                    {
                        "name": "ST.4",
                        "description": "Capacidad para la selección de circuitos, subsistemas y "
                                       + "sistemas de radiofrecuencia, microondas, radiodifusión, "
                                       + "radioenlaces y radiodeterminación."
                    },
                    {
                        "name": "ST.5",
                        "description": "Capacidad para la selección de antenas, equipos y "
                                       + "sistemas de transmisión, propagación de ondas guiadas y "
                                       + "no guiadas, por medios electromagnéticos, de radiofrecuencia "
                                       + "u ópticos y la correspondiente gestión del espacio radioeléctrico "
                                       + "y asignación de frecuencias.",
                    },
                    {
                        "name": "ST.6",
                        "description": "Capacidad para analizar, codificar, procesar y transmitir "
                                       + "información multimedia empleando técnicas de procesado analógico y "
                                       + "digital de señal."
                    }
                ],
                "Sonido e imagen": [
                    {
                        "name": "SI.1",
                        "description": "Capacidad de construir, explotar y gestionar servicios y "
                                       + "aplicaciones de telecomunicaciones, entendidas éstas como "
                                       + "sistemas de captación, tratamiento analógico y digital, "
                                       + "codificación, transporte, representación, procesado, almacenamiento,"
                                       + " reproducción, gestión y presentación de servicios audiovisuales e "
                                       + "información multimedia."
                    },
                    {
                        "name": "SI.2",
                        "description": "Capacidad de analizar, especificar, realizar y mantener "
                                       + "sistemas, equipos, cabeceras e instalaciones de televisión, audio "
                                       + "y vídeo, tanto en entornos fijos como móviles.",
                    },
                    {
                        "name": "SI.3",
                        "description": "Capacidad para realizar proyectos de locales e instalaciones "
                                       + "destinados a la producción y grabación de señales de audio y vídeo.",
                    },
                    {
                        "name": "SI.4",
                        "description": "Capacidad para realizar proyectos de ingeniería acústica "
                                       + "sobre: Aislamiento y acondicionamiento acústico de locales; "
                                       + "instalaciones de megafonía; especificación, análisis y selección "
                                       + "de transductores electroacústicos; sistemas de medida, análisis y "
                                       + "control de ruido y vibraciones; acústica medioambiental; sistemas "
                                       + "de acústica submarina."
                    }
                ]
            },
            "mentions": []
        },
        {
            "name": "Grado en Ingeniería Telemática",
            "center": "EPSL",
            "departament": "Telecomunicaciones",
            "itineraries": {
                "General": [
                    {
                        "name": "TEL1",
                        "description":"Capacidad de construir, explotar y gestionar las "
                                      + "redes, servicios, procesos y aplicaciones de telecomunicaciones"
                                      + ", entendidas éstas como sistemas de captación, transporte,"
                                      + " representación, procesado, almacenamiento, gestión y presentación"
                                      + "  de información multimedia, desde el punto de vista de los "
                                      + "servicios telemáticos."
                    },
                    {
                        "name": "TEL2",
                        "description": "Capacidad para aplicar las técnicas en que se basan las redes, "
                                       + "servicios y aplicaciones telemáticas, tales como "
                                       + "sistemas de gestión, señalización y conmutación, encaminamiento"
                                       + " y enrutamiento, seguridad (protocolos criptográficos, "
                                       + "tunelado, cortafuegos, mecanismos de cobro, de autenticación"
                                       + " y de protección de contenidos), ingeniería de tráfico "
                                       + "(teoría de grafos, teoría de colas y teletráfico) tarificación "
                                       + "y fiabilidad y calidad de servicio, tanto en entornos fijos, "
                                       + "móviles, personales, locales o a gran distancia, con diferentes"
                                       + " anchos de banda, incluyendo telefonía y datos."
                    },
                    {
                        "name": "TEL3",
                        "description": "Capacidad de construir, explotar y gestionar servicios "
                                       + "telemáticos utilizando herramientas analíticas de planificación, "
                                       + "de dimensionado y de análisis."
                    },
                    {
                        "name": "TEL4",
                        "description": "Capacidad de describir, programar, validar y optimizar "
                                       + "protocolos e interfaces de comunicación en los diferentes"
                                       + " niveles de una arquitectura de redes"
                    },
                    {
                        "name": "TEL5",
                        "description": "Capacidad de seguir el progreso tecnológico de transmisión, "
                                       + "telemáticos.conmutación y proceso para mejorar "
                                       + "las redes y servicios"
                    },
                    {
                        "name": "TEL6",
                        "description": "Capacidad de diseñar arquitecturas de redes y servicios "
                                       + "telemáticos."
                    },
                    {
                        "name": "TEL7",
                        "description": "Capacidad de programación de servicios y aplicaciones"
                                       + " telemáticas, en red y distribuidas."
                    }
                ]
            },
            "mentions": []
        },
    ]

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
                self.__undo_init()
            else:
                self.__create_groups(self.GROUPS)
                self.__create_centers(self.CENTERS)
                self.__create_departaments(self.DEPARTAMENTS)
                self.__create_areas(self.AREAS)
                self.__create_masters(self.MASTERS)
                self.__create_carrers(self.CARRERS)
                self.stdout.write("Inicialición creada correctamente")
        except IntegrityError:
            raise CommandError("La inicialización ya ha sido realizada")
        # except:
        #     raise CommandError("Error, revise que todo este correcto")

    def __undo_init(self):
        Group.objects.all().delete()
        Centers.objects.all().delete()
        Departaments.objects.all().delete()
        Areas.objects.all().delete()
        Itineraries.objects.all().delete()
        Mentions.objects.all().delete()
        Skills.objects.all().delete()
        self.stdout.write("Inicialización desecha de forma satisfactoria")

    @staticmethod
    def __create_groups(groups):
        permissions_types = [
            Permission.objects.filter(codename__endswith="projects"),
            Permission.objects.filter(codename__endswith="students"),
            Permission.objects.filter(codename__endswith="tutor2")
        ]
        for group in groups:
            group_created = Group.objects.create(id=groups.index(group)+1, name=group)
            for permssion_list in permissions_types:
                for permission in permssion_list:
                    group_created.permissions.add(permission)

    @staticmethod
    def __create_centers(centers):
        centers_id = 1
        for center in centers:
            Centers.objects.create(id=centers_id, name=center)
            centers_id += 1

    @staticmethod
    def __create_departaments(departaments):
        departaments_id = 1
        for departament in departaments:
            Departaments.objects.create(id=departaments_id, name=departament)
            departaments_id += 1

    @staticmethod
    def __create_areas(areas):
        areas_id = 1
        for area in areas:
            Areas.objects.create(
                id=areas_id,
                name=area["name"],
                departaments_id=Departaments.objects.get(name=area["departament"]).id
            )
            areas_id += 1

    @staticmethod
    def __create_masters(masters):
        masters_id = 1
        for master in masters:
            Masters.objects.create(
                id=masters_id,
                name=master["name"],
                departaments_id=Departaments.objects.get(name=master["departament"]).id,
                centers_id=Centers.objects.get(name=master["center"]).id
            )
            masters_id += 1

    @staticmethod
    def __create_carrers(carrers):
        carrers_id, itineraries_id, mentions_id, skills_id = 1, 1, 1, 1
        for carrer in carrers:
            Carrers.objects.create(
                id=carrers_id,
                name=carrer["name"],
                departaments_id=Departaments.objects.get(name=carrer["departament"]).id,
                centers_id=Centers.objects.get(name=carrer["center"]).id
            )
            for itinerarie in carrer["itineraries"].keys():
                Itineraries.objects.create(
                    id=itineraries_id,
                    name=itinerarie,
                    carrers_id=carrers_id
                )
                for skill in carrer["itineraries"][itinerarie]:
                    Skills.objects.create(
                        id=skills_id,
                        name=skill["name"],
                        text=skill["description"],
                        itineraries_id=itineraries_id
                    )
                    skills_id += 1
                itineraries_id += 1
            for mention in carrer["mentions"]:
                Mentions.objects.create(
                    id=mentions_id,
                    name=mention,
                    carrers_id=carrers_id
                )
                mentions_id += 1
            carrers_id += 1
