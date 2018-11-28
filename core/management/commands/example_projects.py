from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from core.models import Masters, Carrers, Itineraries, Mentions, Skills
from core.models import Departaments, Areas, Tutor2
from login.models import Students
from tfgs.models import Tfgs
from tfms.models import Tfms

class Command(BaseCommand):

    help = 'Crea un listado de usuarios en base de datos'
    requires_migrations_checks = True

    TFGS = [
        {
            "title": "Estudio sobre el uso de las redes definidas "
                     + " por software en las redes de sensores",
            "type": Tfgs.TYPE_ESPECIFIC,
            "mode": Tfgs.MODE_ING_PROYECT,
            "is_team": False,
            "objectives": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                          + "Ut vel luctus sem, non vehicula erat. Donec sit amet lacus sapien. "
                          + "Fusce lobortis ipsum id arcu faucibus, quis porttitor libero "
                          + "scelerisque.",
            "methodology": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                           + "Ut vel luctus sem, non vehicula erat. Donec sit amet lacus sapien. "
                           + "Fusce lobortis ipsum id arcu faucibus, quis porttitor libero "
                           + "scelerisque.",
            "docs_and_forms": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                              + "Ut vel luctus sem, non vehicula erat. Donec sit amet lacus sapien."
                              + " Fusce lobortis ipsum id arcu faucibus, quis porttitor libero "
                              + "scelerisque.",
            "departament_validation": None,
            "center_validation": None,
            "tutor1": "jccuevas",
            "tutor2": None,
            "itinerarie": "General (Telematica)",
            "mention": None,
            "carrer": "Grado en Ingeniería Telemática",
            "skills": [
                "TEL3",
                "TEL1",
                "TEL6"
            ],
            "student": [
                {
                    "name": "Antonio Jesús León-Sanchez",
                    "dni": "77346412A",
                    "phone": "658325022",
                    "email": "ajls0003@red.ujaen.es",
                }
            ]
        },
        {
            "title": "Diseño e implementación de un protocolo "
                     + "de comunicaciones entre sensores IoT y una plataforma cloud.",
            "type": Tfgs.TYPE_GENERAL,
            "mode": Tfgs.MODE_EXP_THEORETICAL,
            "is_team": False,
            "objectives": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                          + "Ut vel luctus sem, non vehicula erat. Donec sit amet lacus sapien. "
                          + "Fusce lobortis ipsum id arcu faucibus, quis porttitor libero "
                          + "scelerisque.",
            "methodology": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                           + "Ut vel luctus sem, non vehicula erat. Donec sit amet lacus sapien. "
                           + "Fusce lobortis ipsum id arcu faucibus, quis porttitor libero "
                           + "scelerisque.",
            "docs_and_forms": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                              + "Ut vel luctus sem, non vehicula erat. Donec sit amet lacus sapien."
                              + " Fusce lobortis ipsum id arcu faucibus, quis porttitor libero "
                              + "scelerisque.",
            "departament_validation": None,
            "center_validation": None,
            "tutor1": "fnavarro",
            "tutor2": None,
            "itinerarie": "General (Telematica)",
            "mention": None,
            "carrer": "Grado en Ingeniería Telemática",
            "skills": [
                "TEL2",
                "TEL3",
                "TEL5"
            ],
            "student": [
                {
                    "name": "González-Ginés, María L.",
                    "dni": "77243312A",
                    "phone": "654325022",
                    "email": "mlgg0002@red.ujaen.es",
                }
            ]
        },
        {
            "title": "Aplicación móvil para la gestión de envío de avisos "
                     + "y notificaciones para colegios de enseñanza infantil y primaria.",
            "type": Tfgs.TYPE_GENERAL,
            "mode": Tfgs.MODE_EXP_THEORETICAL,
            "is_team": False,
            "objectives": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                          + "Ut vel luctus sem, non vehicula erat. Donec sit amet lacus sapien. "
                          + "Fusce lobortis ipsum id arcu faucibus, quis porttitor libero "
                          + "scelerisque.",
            "methodology": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                           + "Ut vel luctus sem, non vehicula erat. Donec sit amet lacus sapien. "
                           + "Fusce lobortis ipsum id arcu faucibus, quis porttitor libero "
                           + "scelerisque.",
            "docs_and_forms": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                              + "Ut vel luctus sem, non vehicula erat. Donec sit amet lacus sapien."
                              + " Fusce lobortis ipsum id arcu faucibus, quis porttitor libero "
                              + "scelerisque.",
            "departament_validation": None,
            "center_validation": None,
            "tutor1": "jccuevas",
            "tutor2": None,
            "itinerarie": "General (Telematica)",
            "mention": None,
            "carrer": "Grado en Ingeniería Telemática",
            "skills": [
                "TEL1",
                "TEL3",
                "TEL7"
            ],
            "student": [
                {
                    "name": "Fernández-Piñas-Padial, José L.",
                    "dni": "77255312A",
                    "phone": "654935022",
                    "email": "jlfpp0008@red.ujaen.es",
                }
            ]
        },
        {
            "title": "Control de acceso a dependencias seguro basado en "
                     + "NFC para terminales Android con sistema de gestión",
            "type": Tfgs.TYPE_ESPECIFIC,
            "mode": Tfgs.MODE_TECHNICAL_STUDY,
            "is_team": True,
            "objectives": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                          + "Ut vel luctus sem, non vehicula erat. Donec sit amet lacus sapien. "
                          + "Fusce lobortis ipsum id arcu faucibus, quis porttitor libero "
                          + "scelerisque.",
            "methodology": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                           + "Ut vel luctus sem, non vehicula erat. Donec sit amet lacus sapien. "
                           + "Fusce lobortis ipsum id arcu faucibus, quis porttitor libero "
                           + "scelerisque.",
            "docs_and_forms": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                              + "Ut vel luctus sem, non vehicula erat. Donec sit amet lacus sapien."
                              + " Fusce lobortis ipsum id arcu faucibus, quis porttitor libero "
                              + "scelerisque.",
            "departament_validation": None,
            "center_validation": None,
            "tutor1": "jccuevas",
            "tutor2": None,
            "itinerarie": "General (Telematica)",
            "mention": None,
            "carrer": "Grado en Ingeniería Telemática",
            "skills": [
                "TEL1",
                "TEL2",
                "TEL5"
            ],
            "student": [
                {
                    "name": "Moya-Fernández, Francisco-A.",
                    "dni": "775355312A",
                    "phone": "654935852",
                    "email": "afmf00041@red.ujaen.es",
                },
                {
                    "name": "Rebollo-Calvo, Eva",
                    "dni": "77251312A",
                    "phone": "654935522",
                    "email": "erc0009@red.ujaen.es",
                }
            ]
        },
        {
            "title": "DESLIEGUE DE UNA RED MANET PARA LA CAPTURA DE LA"
                     + " SEÑAL RADIADA POR EMISORES BLUETOOTH LE EN ENTORNOS DE MICROLOCALIZACIÓN",
            "type": Tfgs.TYPE_ESPECIFIC,
            "mode": Tfgs.MODE_TECHNICAL_STUDY,
            "is_team": False,
            "objectives": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                          + "Ut vel luctus sem, non vehicula erat. Donec sit amet lacus sapien. "
                          + "Fusce lobortis ipsum id arcu faucibus, quis porttitor libero "
                          + "scelerisque.",
            "methodology": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                           + "Ut vel luctus sem, non vehicula erat. Donec sit amet lacus sapien. "
                           + "Fusce lobortis ipsum id arcu faucibus, quis porttitor libero "
                           + "scelerisque.",
            "docs_and_forms": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                              + "Ut vel luctus sem, non vehicula erat. Donec sit amet lacus sapien."
                              + " Fusce lobortis ipsum id arcu faucibus, quis porttitor libero "
                              + "scelerisque.",
            "departament_validation": None,
            "center_validation": None,
            "tutor1": "ajyuste",
            "tutor2": None,
            "itinerarie": "Sistemas de telecomunicación",
            "mention": None,
            "carrer": "Grado en Ingeniería de Tecnologías de Telecomunicación",
            "skills": [
                "ST.1",
                "ST.3",
                "ST.4"
            ],
            "student": [
                {
                    "name": "Nsogo-Nsa, Samuel Ela",
                    "dni": "77298312A",
                    "phone": "654931592",
                    "email": "esnn0003@red.ujaen.es",
                }
            ]
        },
        {
            "title": "DESARROLLO DE UN ALGORITMO BASADO EN REDES NEURONALES "
                     + "PARA LA DETECCIÓN AUTOMÁTICA DEL TIPO DE INSTRUMENTO MUSICAL",
            "type": Tfgs.TYPE_GENERAL,
            "mode": Tfgs.MODE_ING_PROYECT,
            "is_team": False,
            "objectives": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                          + "Ut vel luctus sem, non vehicula erat. Donec sit amet lacus sapien. "
                          + "Fusce lobortis ipsum id arcu faucibus, quis porttitor libero "
                          + "scelerisque.",
            "methodology": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                           + "Ut vel luctus sem, non vehicula erat. Donec sit amet lacus sapien. "
                           + "Fusce lobortis ipsum id arcu faucibus, quis porttitor libero "
                           + "scelerisque.",
            "docs_and_forms": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                              + "Ut vel luctus sem, non vehicula erat. Donec sit amet lacus sapien."
                              + " Fusce lobortis ipsum id arcu faucibus, quis porttitor libero "
                              + "scelerisque.",
            "departament_validation": None,
            "center_validation": None,
            "tutor1": "ajyuste",
            "tutor2": None,
            "itinerarie": "Sonido e imagen",
            "mention": None,
            "carrer": "Grado en Ingeniería de Tecnologías de Telecomunicación",
            "skills": [
                "SI.2",
                "SI.3",
                "SI.4"
            ],
            "student": [
                {
                    "name": "Gálvez-Gómez, Joaquín",
                    "dni": "77598312A",
                    "phone": "634931592",
                    "email": "jgg00019@red.ujaen.es",
                }
            ]
        }
    ]
    TFMS = [
        {
            "title": "Estrategias inteligentes de planificación en Cloud Computing",
            "type": Tfms.TYPE_UNI,
            "objectives": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                          + "Ut vel luctus sem, non vehicula erat. Donec sit amet lacus sapien. "
                          + "Fusce lobortis ipsum id arcu faucibus, quis porttitor libero "
                          + "scelerisque.",
            "methodology": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                           + "Ut vel luctus sem, non vehicula erat. Donec sit amet lacus sapien. "
                           + "Fusce lobortis ipsum id arcu faucibus, quis porttitor libero "
                           + "scelerisque.",
            "docs_and_forms": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                              + "Ut vel luctus sem, non vehicula erat. Donec sit amet lacus sapien."
                              + " Fusce lobortis ipsum id arcu faucibus, quis porttitor libero "
                              + "scelerisque.",
            "language": "Inglish",
            "knowledge": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
                         + "Ut vel luctus sem, non vehicula erat. Donec sit amet lacus sapien."
                         + " Fusce lobortis ipsum id arcu faucibus, quis porttitor libero "
                         + "scelerisque.",
            "departament_validation": None,
            "center_validation": None,
            "tutor1": "jccuevas",
            "tutor2": None,
            "master": "Máster Universitario en Ingeniería de Telecomunicación",
            "student": [
                {
                    "name": "Rodríguez-Reche, Rafael-Rudesindo",
                    "dni": "775312312A",
                    "phone": "643935852",
                    "email": "rrrr0002@red.ujaen.es",
                }
            ]
        }
    ]
    def add_arguments(self, parser):
        parser.add_argument(
            "--delete",
            action="store_true",
            dest="delete",
            help="revierte la inicialización"
        )

    def handle(self, *args, **options):
        # try:
            if options["delete"]:
                self.__delete()
            else:
                self.__create_tfgs(self.TFGS)
                self.__create_tfms(self.TFMS)
                self.stdout.write("Proyectos de ejemplo creados correctamente")
        # except IntegrityError:
        #     raise CommandError("La inicialización ya ha sido realizada")
        # except:
        #     raise CommandError("Error, revise que todo este correcto")

    def __delete(self):
        Tfgs.objects.all().delete()
        Tfms.objects.all().delete()
        Students.objects.all().delete()
        Tutor2.objects.all().delete()
        self.stdout.write("Proyectos eliminados correctamente")

    @staticmethod
    def __create_tfgs(tfgs):
        for tfg in tfgs:
            tutor2 = None
            if tfg["tutor2"] is not None:
                tutor2 = Tutor2.objects.create(
                    name=tfg["tutor2"]["name"],
                    center=tfg["tutor2"]["center"],
                    departament=tfg["tutor2"]["departament"],
                    area=tfg["tutor2"]["area"]
                )
            tfg_item = Tfgs.objects.create(
                title=tfg["title"],
                type=tfg["type"],
                mode=tfg["mode"],
                is_team=tfg["is_team"],
                objectives=tfg["objectives"],
                methodology=tfg["methodology"],
                docs_and_forms=tfg["docs_and_forms"],
                departament_validation=tfg["departament_validation"],
                center_validation=tfg["center_validation"],
                tutor1_id=User.objects.get(username=tfg["tutor1"]).id,
                tutor2=tutor2,
                itineraries_id=Itineraries.objects.get(name=tfg["itinerarie"]).id
                if tfg["itinerarie"] is not None else None,
                mentions_id=Mentions.objects.get(name=tfg["mention"]).id
                if tfg["mention"] is not None else None,
                carrers_id=Carrers.objects.get(name=tfg["carrer"]).id
            )
            for student in tfg["student"]:
                Students.objects.create(
                    name=student["name"],
                    dni=student["dni"],
                    phone=student["phone"],
                    email=student["email"],
                    tfgs_id=tfg_item.id
                )
            for skill in tfg["skills"]:
                tfg_item.skills.add(Skills.objects.get(name=skill))

    @staticmethod
    def __create_tfms(tfms):
        for tfm in tfms:
            tutor2 = None
            if tfm["tutor2"] is not None:
                tutor2 = Tutor2.objects.create(
                    name=tfm["tutor2"]["name"],
                    departament=Departaments.objects.get(name=tfm["tutor2"]["departament"]).id,
                    area=Areas.objects.get(name=tfm["tutor2"]["area"]).id
                )
            tfm_item = Tfms.objects.create(
                title=tfm["title"],
                type=tfm["type"],
                objectives=tfm["objectives"],
                methodology=tfm["methodology"],
                docs_and_forms=tfm["docs_and_forms"],
                language=tfm["language"],
                knowledge=tfm["knowledge"],
                departament_validation=tfm["departament_validation"],
                center_validation=tfm["center_validation"],
                tutor1_id=User.objects.get(username=tfm["tutor1"]).id,
                tutor2=tutor2,
                masters_id=Masters.objects.get(name=tfm["master"]).id
            )
            for student in tfm["student"]:
                Students.objects.create(
                    name=student["name"],
                    dni=student["dni"],
                    phone=student["phone"],
                    email=student["email"],
                    tfms_id=tfm_item.id
                )
