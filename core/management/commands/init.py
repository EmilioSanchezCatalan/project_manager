from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group, Permission
from django.db.utils import IntegrityError
from core.models import Departaments, Areas, Carrers, Itineraries, Mentions, Skills

class Command(BaseCommand):

    help = 'Inicialización de los valores de la base de datos'
    requires_migrations_checks = True

    GROUPS = [
        'Teachers',
        'Departaments',
        'Centers'
    ]

    CENTER_STRUCTURE = {
        "Telecomunicaciones": {
            "Tecnologías de Telecomunicación": {
                "Grado en imagen y sonido": {
                    "Itineraries": {
                        "Sistemas de telecomunicación": [
                            "ST.1 - Capacidad para construir, explotar y gestionar las redes, "
                            + "servicios, procesos y aplicaciones de telecomunicaciones, "
                            + "entendidas éstas como sistemas de captación, transporte, "
                            + "representación, procesado, almacenamiento, gestión y presentación"
                            + " de información multimedia, desde el punto de vista de los "
                            + "sistemas de transmisión."
                            "ST.2 - Capacidad para aplicar las técnicas en que se basan las redes, "
                            + "servicios y aplicaciones de telecomunicación tanto en entornos"
                            + " fijos como móviles, personales, locales o a gran distancia, "
                            + "con diferentes anchos de banda, incluyendo telefonía, "
                            + "radiodifusión, televisión y datos, desde el punto de vista "
                            + "de los sistemas de transmisión.",
                            "ST.3 - Capacidad de análisis de componentes y sus especificaciones "
                            + "para sistemas de comunicaciones guiadas y no guiadas.",
                            "ST.4 - Capacidad para la selección de circuitos, subsistemas y "
                            + "sistemas de radiofrecuencia, microondas, radiodifusión, "
                            + "radioenlaces y radiodeterminación."
                            "ST.5 - Capacidad para la selección de antenas, equipos y "
                            + "sistemas de transmisión, propagación de ondas guiadas y "
                            + "no guiadas, por medios electromagnéticos, de radiofrecuencia "
                            + "u ópticos y la correspondiente gestión del espacio radioeléctrico "
                            + "y asignación de frecuencias.",
                            "ST.6 - Capacidad para analizar, codificar, procesar y transmitir "
                            + "información multimedia empleando técnicas de procesado analógico y "
                            + "digital de señal."
                        ],
                        "Sonido e imagen": [
                            "SI.1 - Capacidad de construir, explotar y gestionar servicios y "
                            + "aplicaciones de telecomunicaciones, entendidas éstas como "
                            + "sistemas de captación, tratamiento analógico y digital, "
                            + "codificación, transporte, representación, procesado, almacenamiento,"
                            + " reproducción, gestión y presentación de servicios audiovisuales e "
                            + "información multimedia.",
                            "SI.2 - Capacidad de analizar, especificar, realizar y mantener "
                            + "sistemas, equipos, cabeceras e instalaciones de televisión, audio "
                            + "y vídeo, tanto en entornos fijos como móviles.",
                            "SI.3 - Capacidad para realizar proyectos de locales e instalaciones "
                            + "destinados a la producción y grabación de señales de audio y vídeo.",
                            "SI.4 - Capacidad para realizar proyectos de ingeniería acústica "
                            + "sobre: Aislamiento y acondicionamiento acústico de locales; "
                            + "instalaciones de megafonía; especificación, análisis y selección "
                            + "de transductores electroacústicos; sistemas de medida, análisis y "
                            + "control de ruido y vibraciones; acústica medioambiental; sistemas "
                            + "de acústica submarina."
                        ]
                    },
                    "Mentions": [],
                },
            },
            "Telemática": {
                "Grado en ingenieria Telemática" :{
                    "Itineraries": {
                        "General":  [
                            "TEL1 - Capacidad de construir, explotar y gestionar las "
                            + "redes, servicios, procesos y aplicaciones de telecomunicaciones"
                            + ", entendidas éstas como sistemas de captación, transporte,"
                            + " representación, procesado, almacenamiento, gestión y presentación"
                            + "  de información multimedia, desde el punto de vista de los "
                            + "servicios telemáticos.",
                            "TEL2 - Capacidad para aplicar las técnicas en que se basan las redes, "
                            + "servicios y aplicaciones telemáticas, tales como "
                            + "sistemas de gestión, señalización y conmutación, encaminamiento"
                            + " y enrutamiento, seguridad (protocolos criptográficos, "
                            + "tunelado, cortafuegos, mecanismos de cobro, de autenticación"
                            + " y de protección de contenidos), ingeniería de tráfico "
                            + "(teoría de grafos, teoría de colas y teletráfico) tarificación "
                            + "y fiabilidad y calidad de servicio, tanto en entornos fijos, "
                            + "móviles, personales, locales o a gran distancia, con diferentes"
                            + " anchos de banda, incluyendo telefonía y datos.",
                            "TEL3 - Capacidad de construir, explotar y gestionar servicios "
                            + "telemáticos utilizando herramientas analíticas de planificación, "
                            + "de dimensionado y de análisis.",
                            "TEL4 - Capacidad de describir, programar, validar y optimizar "
                            + "protocolos e interfaces de comunicación en los diferentes"
                            + " niveles de una arquitectura de redes",
                            "TEL5 - Capacidad de seguir el progreso tecnológico de transmisión, "
                            + "telemáticos.conmutación y proceso para mejorar "
                            + "las redes y servicios ",
                            "TEL6 - Capacidad de diseñar arquitecturas de redes y servicios "
                            + "telemáticos.",
                            "TEL7 - Capacidad de programación de servicios y aplicaciones"
                            + " telemáticas, en red y distribuidas."
                        ]
                    },
                    "Mentions": [],
                }
            }
        }
    }
    def add_arguments(self, parser):
        parser.add_argument(
            "--undo",
            action="store_true",
            dest="undo",
            help="revierte la inicialización"
        )

    def handle(self, *args, **options):
        try:
            if options["undo"]:
                self.__undo_init()
            else:
                self.__create_groups(self.GROUPS)
                self.__create_center_structure(self.CENTER_STRUCTURE)
                self.stdout.write("Inicialición creada correctamente")
        except IntegrityError:
            raise CommandError("La inicialización ya ha sido realizada")
        except:
            raise CommandError("Error, revise que todo este correcto")

    def __undo_init(self):
        Group.objects.all().delete()
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
            group_created = Group.objects.create(name=group)
            for permssion_list in permissions_types:
                for permission in permssion_list:
                    group_created.permissions.add(permission)

    @staticmethod
    def __create_center_structure(structure):
        departaments_id, areas_id, carrers_id, iti_id, mentions_id, skills_id = 1, 1, 1, 1, 1, 1
        for departament in structure.keys():
            Departaments.objects.create(id=departaments_id, name=departament)
            for area in structure[departament].keys():
                Areas.objects.create(id=areas_id, name=area, departaments_id=departaments_id)
                for carrer in structure[departament][area].keys():
                    Carrers.objects.create(id=carrers_id, name=carrer, areas_id=areas_id)
                    for iti in structure[departament][area][carrer]["Itineraries"].keys():
                        Itineraries.objects.create(id=iti_id, name=iti, carrers_id=carrers_id)
                        for skills in structure[departament][area][carrer]["Itineraries"][iti]:
                            Skills.objects.create(id=skills_id, text=skills, itineraries_id=iti_id)
                            skills_id += 1
                        iti_id += 1
                    for mention in structure[departament][area][carrer]["Mentions"]:
                        Mentions.objects.create(id=mentions_id, name=mention, carrers_id=carrers_id)
                        mentions_id += 1
                    carrers_id += 1
                areas_id += 1
            departaments_id += 1
