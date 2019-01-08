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
        "Facultad de Ciencias de la Salud",
        "Facultad de Ciencias Experimentales",
        "Facultad de Ciencias Sociales y Jurídicas",
        "Facultad de Humanidades y Ciencias de la Educación",
        "Facultad de Trabajo Social",
        "Escuela Politécnica Superior de Jaén",
        "Escuela Politécnica Superior de Linares",
        "Comisión Academica del Máster de Ingeniería de Telecomunicación"
    ]

    DEPARTAMENTS = [
        "Antropología, Geografía e Historia",
        "Biología Animal, Biología Vegetal y Ecología",
        "Biología Experimental",
        "Ciencias de la Salud",
        "Derecho Civil, Derecho Financiero y Tributario",
        "Derecho Penal, Filosofía del Derecho, Filosofía Moral y Filosofía",
        "Derecho Público",
        "Derecho Público y Común Europeo",
        "Derecho Público y Derecho Privado Especial",
        "Didáctica de la Expresión Musical, Plástica y Corporal",
        "Didáctica de las Ciencias",
        "Economía",
        "Economía Financiera y Contabilidad",
        "Enfermería",
        "Estadística e Investigación Operativa",
        "Filología Española",
        "Filología Inglesa",
        "Física",
        "Geología",
        "Informática",
        "Ingeniería Cartográfica, Geodésica y Fotogrametría",
        "Ingeniería de Telecomunicación",
        "Ingeniería Eléctrica",
        "Ingeniería Electrónica y Automática",
        "Ingeniería Gráfica, Diseño y Proyectos",
        "Ingeniería Mecánica y Minera",
        "Ingeniería Química, Ambiental y de los Materiales",
        "Lenguas y Culturas Mediterráneas",
        "Matemáticas",
        "Organización de Empresas, Marketing y Sociología",
        "Patrimonio Histórico",
        "Pedagogía",
        "Psicología",
        "Química Física y Analítica",
        "Química Inorgánica y Orgánica",
        "Otro",
    ]

    AREAS = [
        {
            "name": "Antropología Social",
            "departament": "Antropología, Geografía e Historia"
        },
        {
            "name": "Análisis Geográfico Regional",
            "departament": "Antropología, Geografía e Historia"
        },
        {
            "name": "Geografía Física",
            "departament": "Antropología, Geografía e Historia"
        },
        {
            "name": "Geografía Humana",
            "departament": "Antropología, Geografía e Historia"
        },
        {
            "name": "Historia Antigua",
            "departament": "Antropología, Geografía e Historia"
        },
        {
            "name": "Historia Moderna",
            "departament": "Antropología, Geografía e Historia"
        },
        {
            "name": "Historia Contemporánea",
            "departament": "Antropología, Geografía e Historia"
        },
        {
            "name": "Botánica",
            "departament": "Biología Animal, Biología Vegetal y Ecología"
        },
        {
            "name": "Ecología",
            "departament": "Biología Animal, Biología Vegetal y Ecología"
        },
        {
            "name": "Fisiología Vegetal",
            "departament": "Biología Animal, Biología Vegetal y Ecología"
        },
        {
            "name": "Zoología",
            "departament": "Biología Animal, Biología Vegetal y Ecología"
        },
        {
            "name": "Biología Celular",
            "departament": "Biología Experimental"
        },
        {
            "name": "Bioquímica y Biología Molecular",
            "departament": "Biología Experimental"
        },
        {
            "name": "Genética",
            "departament": "Biología Experimental"
        },
        {
            "name": "Anatomía y Embrología Humana",
            "departament": "Ciencias de la Salud"
        },
        {
            "name": "Cirugía",
            "departament": "Ciencias de la Salud"
        },
        {
            "name": "Fisiología",
            "departament": "Ciencias de la Salud"
        },
        {
            "name": "Medecina Preventiva y Salud Pública",
            "departament": "Ciencias de la Salud"
        },
        {
            "name": "Inmunología",
            "departament": "Ciencias de la Salud"
        },
        {
            "name": "Microbiología",
            "departament": "Ciencias de la Salud"
        },
        {
            "name": "Fisioterapia",
            "departament": "Ciencias de la Salud"
        },
        {
            "name": "Derecho Civil",
            "departament": "Derecho Civil, Derecho Financiero y Tributario"
        },
        {
            "name": "Derecho Financiero y Tributario",
            "departament": "Derecho Civil, Derecho Financiero y Tributario"
        },
        {
            "name": "Derecho Penal",
            "departament": "Derecho Penal, Filosofía del Derecho, Filosofía Moral y Filosofía"
        },
        {
            "name": "Filosofía del Derecho",
            "departament": "Derecho Penal, Filosofía del Derecho, Filosofía Moral y Filosofía"
        },
        {
            "name": "Filosofía Moral",
            "departament": "Derecho Penal, Filosofía del Derecho, Filosofía Moral y Filosofía"
        },
        {
            "name": "Filosofía",
            "departament": "Derecho Penal, Filosofía del Derecho, Filosofía Moral y Filosofía"
        },
        {
            "name": "Derecho Administrativo",
            "departament": "Derecho Público"
        },
        {
            "name": "Derecho Constitucional",
            "departament": "Derecho Público"
        },
        {
            "name": "Derecho Eclesiástico del Estado",
            "departament": "Derecho Público y Común Europeo"
        },
        {
            "name": "Derecho Internacional Público y Relaciones Internacionales",
            "departament": "Derecho Público y Común Europeo"
        },
        {
            "name": "Derecho Procesal",
            "departament": "Derecho Público y Común Europeo"
        },
        {
            "name": "Derecho Romano",
            "departament": "Derecho Público y Común Europeo"
        },
        {
            "name": "Ciencia Política y de la Administración",
            "departament": "Derecho Público y Derecho Privado Especial"
        },
        {
            "name": "Derecho Internacional Privado",
            "departament": "Derecho Público y Derecho Privado Especial"
        },
        {
            "name": "Derecho Mercantil",
            "departament": "Derecho Público y Derecho Privado Especial"
        },
        {
            "name": "Derecho del Trabajo y de la Seguridad Social",
            "departament": "Derecho Público y Derecho Privado Especial"
        },
        {
            "name": "Historia del Derecho y de las Instituciones",
            "departament": "Derecho Público y Derecho Privado Especial"
        },
        {
            "name": "Dibujo",
            "departament": "Didáctica de la Expresión Musical, Plástica y Corporal"
        },
        {
            "name": "Didáctica de la Expresión Corporal",
            "departament": "Didáctica de la Expresión Musical, Plástica y Corporal"
        },
        {
            "name": "Didáctica de la Expresión Musical",
            "departament": "Didáctica de la Expresión Musical, Plástica y Corporal"
        },
        {
            "name": "Educación Física y Deportiva",
            "departament": "Didáctica de la Expresión Musical, Plástica y Corporal"
        },
        {
            "name": "Música",
            "departament": "Didáctica de la Expresión Musical, Plástica y Corporal"
        },
        {
            "name": "Didáctica de la Expresión Plástica",
            "departament": "Didáctica de la Expresión Musical, Plástica y Corporal"
        },
        {
            "name": "Didáctica de las Matemáticas",
            "departament": "Didáctica de las Ciencias"
        },
        {
            "name": "Didáctica de las Ciencias Experimentales",
            "departament": "Didáctica de las Ciencias"
        },
        {
            "name": "Didáctica de las Ciencias Sociales",
            "departament": "Didáctica de las Ciencias"
        },
        {
            "name": "Economía Aplicada",
            "departament": "Economía"
        },
        {
            "name": "Fundamentos del Análisis Económico",
            "departament": "Economía"
        },
        {
            "name": "Historia e Instituciones Económicas",
            "departament": "Economía"
        },
        {
            "name": "Economía Financiera y Contabilidad",
            "departament": "Economía Financiera y Contabilidad"
        },
        {
            "name": "Enfermería",
            "departament": "Enfermería"
        },
        {
            "name": "Estadística e Investigación Operativa",
            "departament": "Estadística e Investigación Operativa"
        },
        {
            "name": "Didáctica de la Lengua y la Literatura",
            "departament": "Filología Española"
        },
        {
            "name": "Lengua Española",
            "departament": "Filología Española"
        },
        {
            "name": "Lingüística General",
            "departament": "Filología Española"
        },
        {
            "name": "Literatura Española",
            "departament": "Filología Española"
        },
        {
            "name": "Filología Inglesa",
            "departament": "Filología Inglesa"
        },
        {
            "name": "Astronomía y Astrofísica",
            "departament": "Física"
        },
        {
            "name": "Física Aplicada",
            "departament": "Física"
        },
        {
            "name": "Física de la Tierra",
            "departament": "Física"
        },
        {
            "name": "Cristalografía y Mineralogía",
            "departament": "Geología"
        },
        {
            "name": "Edafología y Química Agrícola",
            "departament": "Geología"
        },
        {
            "name": "Estratigrafía",
            "departament": "Geología"
        },
        {
            "name": "Geodinámica Externa",
            "departament": "Geología"
        },
        {
            "name": "Geodinámica Interna",
            "departament": "Geología"
        },
        {
            "name": "Arquitectura y tecnología de computadores",
            "departament": "Informática"
        },
        {
            "name": "Ciencias de la computación e Inteligencia artificial",
            "departament": "Informática"
        },
        {
            "name": "Lenguajes y sistemas informáticos",
            "departament": "Informática"
        },
        {
            "name": "Ingeniería Cartográfica, Geodésica y Fotogrametría",
            "departament": "Ingeniería Cartográfica, Geodésica y Fotogrametría"
        },
        {
            "name": "Ingeniería Telemática",
            "departament": "Ingeniería de Telecomunicación"
        },
        {
            "name": "Teoría de la Señal y Comunicaciones",
            "departament": "Ingeniería de Telecomunicación"
        },
        {
            "name": "Ingeniería Eléctrica",
            "departament": "Ingeniería Eléctrica"
        },
        {
            "name": "Ingeniería Electrónica y Automática",
            "departament": "Ingeniería Electrónica y Automática"
        },
        {
            "name": "Expresión Gráfica en la Ingeniería",
            "departament": "Ingeniería Gráfica, Diseño y Proyectos"
        },
        {
            "name": "Proyectos de Ingeniería",
            "departament": "Ingeniería Gráfica, Diseño y Proyectos"
        },
        {
            "name": "Explotación de Minas",
            "departament": "Ingeniería Mecánica y Minera"
        },
        {
            "name": "Ingeniería de la Construcción",
            "departament": "Ingeniería Mecánica y Minera"
        },
        {
            "name": "Ingeniería de los Procesos de Fabricación",
            "departament": "Ingeniería Mecánica y Minera"
        },
        {
            "name": "Ingeniería Mecánica",
            "departament": "Ingeniería Mecánica y Minera"
        },
        {
            "name": "Máquinas y Motores Térmicos ",
            "departament": "Ingeniería Mecánica y Minera"
        },
        {
            "name": "Mecánica de Fluidos",
            "departament": "Ingeniería Mecánica y Minera"
        },
        {
            "name": "Mecánica de los Medios Continuos y Teoría de Estructuras",
            "departament": "Ingeniería Mecánica y Minera"
        },
        {
            "name": "Prospección e Investigación Minera",
            "departament": "Ingeniería Mecánica y Minera"
        },
        {
            "name": "Ciencia de Materiales e Ingeniería Metalúrgica",
            "departament": "Ingeniería Química, Ambiental y de los Materiales"
        },
        {
            "name": "Ciencia DE Ingeniería Química",
            "departament": "Ingeniería Química, Ambiental y de los Materiales"
        },
        {
            "name": "Tecnologías del Medio Ambiente",
            "departament": "Ingeniería Química, Ambiental y de los Materiales"
        },
        {
            "name": "Estudios Árabes e Islámicos",
            "departament": "Lenguas y Culturas Mediterráneas"
        },
        {
            "name": "Filología Francesa",
            "departament": "Lenguas y Culturas Mediterráneas"
        },
        {
            "name": "Filología Griega",
            "departament": "Lenguas y Culturas Mediterráneas"
        },
        {
            "name": "Filología Latina",
            "departament": "Lenguas y Culturas Mediterráneas"
        },
        {
            "name": "Teoría de la Literatura y Literatura Comparada",
            "departament": "Lenguas y Culturas Mediterráneas"
        },
        {
            "name": "Álgebra",
            "departament": "Matemáticas"
        },
        {
            "name": "Análisis Matemático",
            "departament": "Matemáticas"
        },
        {
            "name": "Geometría y Topología",
            "departament": "Matemáticas"
        },
        {
            "name": "Matemática Aplicada",
            "departament": "Matemáticas"
        },
        {
            "name": "Sociología",
            "departament": "Organización de Empresas, Marketing y Sociología"
        },
        {
            "name": "Organización de Empresas",
            "departament": "Organización de Empresas, Marketing y Sociología"
        },
        {
            "name": "Comercialización e Investigación de Mercados",
            "departament": "Organización de Empresas, Marketing y Sociología"
        },
        {
            "name": "Arqueología",
            "departament": "Patrimonio Histórico"
        },
        {
            "name": "Historia del arte",
            "departament": "Patrimonio Histórico"
        },
        {
            "name": "Historia medieval",
            "departament": "Patrimonio Histórico"
        },
        {
            "name": "Prehistoria",
            "departament": "Patrimonio Histórico"
        },
        {
            "name": "Didáctica y Organización Escolar",
            "departament": "Pedagogía"
        },
        {
            "name": "Métododos de Investigación y Diagnóstico en Educación",
            "departament": "Pedagogía"
        },
        {
            "name": "Teoría e Historia de la Educación",
            "departament": "Pedagogía"
        },
        {
            "name": "Metodología de las Ciencias del Comportamiento",
            "departament": "Psicología"
        },
        {
            "name": "Personalidad, Evaluación y Tratamiento Psicológico",
            "departament": "Psicología"
        },
        {
            "name": "Psicobiología",
            "departament": "Psicología"
        },
        {
            "name": "Psicología Básica",
            "departament": "Psicología"
        },
        {
            "name": "Psicología Evolutiva y de la Educación",
            "departament": "Psicología"
        },
        {
            "name": "Psicología Social",
            "departament": "Psicología"
        },
        {
            "name": "Trabajo Social y Servicios Sociales",
            "departament": "Psicología"
        },
        {
            "name": "Química Analítica",
            "departament": "Química Física y Analítica"
        },
        {
            "name": "Química Física",
            "departament": "Química Física y Analítica"
        },
        {
            "name": "Química Inorgánica y Orgánica",
            "departament": "Química Inorgánica y Orgánica"
        },
        {
            "name": "Otra",
            "departament": "Otro"
        }
    ]

    MASTERS = [
        {
            "name": "Máster Universitario en Ingeniería de Telecomunicación",
            "center": "Comisión Academica del Máster de Ingeniería de Telecomunicación",
            "departaments": [
                "Ingeniería de Telecomunicación",
                "Ingeniería Eléctrica",
                "Ingeniería Electrónica y Automática",
                "Informática"
            ]
        },
    ]

    CARRERS = [
        {
            "name": "Grado en Ingeniería de Tecnologías de Telecomunicación",
            "center": "Escuela Politécnica Superior de Linares",
            "departaments": [
                "Ingeniería de Telecomunicación",
                "Ingeniería Eléctrica",
                "Informática",
                "Matemáticas",
                "Organización de Empresas, Marketing y Sociología",
                "Estadística e Investigación Operativa",
                "Física"
            ],
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
            "center": "Escuela Politécnica Superior de Linares",
            "departaments": [
                "Ingeniería de Telecomunicación",
                "Ingeniería Eléctrica",
                "Informática",
                "Matemáticas",
                "Organización de Empresas, Marketing y Sociología",
                "Estadística e Investigación Operativa",
                "Física"
            ],
            "itineraries": {
                "General (Telematica)": [
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
        {
            "name": "Grado en Ingeniería Química Industrial",
            "center": "Escuela Politécnica Superior de Linares",
            "departaments": [
                "Química Física y Analítica",
                "Química Inorgánica y Orgánica",
                "Informática",
                "Matemáticas",
                "Ingeniería Química, Ambiental y de los Materiales",
                "Estadística e Investigación Operativa",
                "Organización de Empresas, Marketing y Sociología",
                "Física"
            ],
            "itineraries": {
                "General (Química Industrial)": [
                    {
                        "name": "CEQ1",
                        "description": "Conocimientos sobre balances de materia "
                                       + "y energía, biotecnología, "
                                       + "transferencia de materia, operaciones de separación, "
                                       + ", entendidas éstas como sistemas de captación, transporte"
                                       + ", ingeniería de la reacción química, diseño de reactores,"
                                       + " y valorización y transformación de materias "
                                       + "primas y recursos energéticos."
                    },
                    {
                        "name": "CEQ2",
                        "description": "Capacidad para el análisis, diseño, simulación y "
                                       + "optimización de procesos y productos."
                    },
                    {
                        "name": "CEQ3",
                        "description": "Capacidad para el diseño y gestión de procedimientos de "
                                       + "experimentación aplicada, especialmente para la "
                                       + "determinación de propiedades termodinámicas y de transporte, "
                                       + "y modelado de fenómenos y sistemas en el ámbito "
                                       + "de la ingeniería química, sistemas con flujo de fluidos, "
                                       + "transmisión de calor, operaciones de transferencia de materia, "
                                       + "cinética de las reacciones químicas y reactores."
                    },
                    {
                        "name": "CEQ4",
                        "description": "Capacidad para diseñar, gestionar y operar "
                                       + "procedimientos de simulación, control e "
                                       + "instrumentación de procesos químicos."
                    }
                ]
            },
            "mentions": [
                "Meción en Tecnología Industrial y Agroalimentaria",
                "Meción en Medioambiente y Materiales",
                "Sin mención"
            ]
        },
        {
            "name": "Grado Enfermería",
            "center": "Facultad de Ciencias de la Salud",
            "departaments": [
                "Enfermería",
                "Ciencias de la Salud",
                "Biología Experimental",
                "Psicología",
                "Estadística e Investigación Operativa"
            ],
            "itineraries": {
                "General (Enfermería)": [
                    {
                        "name": "EN1",
                        "description": "Conocimientos sobre balances de materia "
                                       + "y energía, biotecnología, "
                                       + "transferencia de materia, operaciones de separación, "
                                       + ", entendidas éstas como sistemas de captación, transporte"
                                       + ", ingeniería de la reacción química, diseño de reactores,"
                                       + " y valorización y transformación de materias "
                                       + "primas y recursos energéticos."
                    },
                    {
                        "name": "EN2",
                        "description": "Capacidad para el análisis, diseño, simulación y "
                                       + "optimización de procesos y productos."
                    },
                    {
                        "name": "EN3",
                        "description": "Capacidad para el diseño y gestión de procedimientos de "
                                       + "experimentación aplicada, especialmente para la "
                                       + "determinación de propiedades termodinámicas y de transporte, "
                                       + "y modelado de fenómenos y sistemas en el ámbito "
                                       + "de la ingeniería química, sistemas con flujo de fluidos, "
                                       + "transmisión de calor, operaciones de transferencia de materia, "
                                       + "cinética de las reacciones químicas y reactores."
                    },
                    {
                        "name": "EN4",
                        "description": "Capacidad para diseñar, gestionar y operar "
                                       + "procedimientos de simulación, control e "
                                       + "instrumentación de procesos químicos."
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
            master_object = Masters.objects.create(
                id=masters_id,
                name=master["name"],
                centers_id=Centers.objects.get(name=master["center"]).id,
            )
            for masters_has_departament in master["departaments"]:
                master_object.departaments.add(
                    Departaments.objects.get(name=masters_has_departament)
                )
            masters_id += 1

    @staticmethod
    def __create_carrers(carrers):
        carrers_id, itineraries_id, mentions_id, skills_id = 1, 1, 1, 1
        for carrer in carrers:
            carrer_object = Carrers.objects.create(
                id=carrers_id,
                name=carrer["name"],
                centers_id=Centers.objects.get(name=carrer["center"]).id,
            )
            for carrers_has_departament in carrer["departaments"]:
                carrer_object.departaments.add(
                    Departaments.objects.get(name=carrers_has_departament)
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
