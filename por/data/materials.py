from por.meta.schema import Material


materials = [
    {
        "code": "BM.01",
        "interaction": "Unir",
        "year": 2026,
        "authors": "Heidi Jalkh and Nadya Suvorova",
        "name": "Conchas marinas trituradas (cholgas, navajas y ostras) con biopolímero de algas.",
        "material_origin": "Ultramarinos (AR)",
        "description": (
            "Pieza por pieza, esta esfera-rompecabezas cobra existencia. Fabricada con "
            "biocerámica de conchas marinas, moldeada a temperatura ambiente, fragmentos de "
            "lo antiguo se unifican mediante un aglutinante de algas. Tres módulos "
            "entrelazados que una vez unidos, forman una geometría perfecta: una orbe "
            "reimaginada capaz de rodar, detenerse y recuperar su equilibrio."
        ),
    },
    {
        "code": "GM.02",
        "interaction": "Crecer",
        "year": 2026,
        "authors": "Heidi Jalkh and Nadya Suvorova",
        "name": "Bioaglomerado de micelio de Pycnoporus sanguineus y Ganoderma lucidum",
        "fungus_inoculation": (
            "Dr. Leonardo M. Majul, Lab. de Micología Experimental y Liquenología "
            "(INMIBO-UBA)"
        ),
        "description": (
            "En un movimiento suave, este hábitat tambaleante acuna un mundo vivo en su "
            "núcleo. Dentro de este vientre cinético, el hongo se expanden lentamente y se "
            "entreteje, nutriendo un cuerpo compartido en expansión. Lo que comienza como un "
            "simple recipiente se convierte en un santuario silencioso donde la vida se "
            "congrega y crece siguiendo el pulso de una forma en constante transformación."
        ),
    },
    {
        "code": "MC.03",
        "interaction": "Magnetizar",
        "year": 2026,
        "authors": "Heidi Jalkh and Nadya Suvorova",
        "name": "Compuesto de caucho siliconado con partículas de aleación de neodimio-hierro-boro (NdFeB)",
        "material_origin": (
            "Dr Ahmet Demirörs (CH), Material Science Department, Complex Materials Group, "
            "ETH Zurich"
        ),
        "source_url": "https://advanced.onlinelibrary.wiley.com/doi/full/10.1002/advs.202102510",
        "description": (
            "Sobre una superficie inmóvil, filamentos de silicona magnetizados se mecen al "
            "unísono. Impulsados por un flujo magnético, estos cilios artificiales desplazan "
            "pequeños objetos de una hebra a otra mediante un movimiento ondulante, como si "
            "flotaran sobre una multitud.Un sistema de transporte sofisticado, donde ondas de  "
            "energía trasladan la materia a través de un suave relevo sincronizado."
        ),
    },
    {
        "code": "AS.04",
        "interaction": "Tensar",
        "year": 2026,
        "authors": "Heidi Jalkh and Nadya Suvorova",
        "name": "Estructura auxética de goma eva",
        "collaborators": "Dr. Lorenzo Guiducci, Matters of Activity (DE)",
        "source_url": "https://www.degruyterbrill.com/document/doi/10.1515/9783110714883-007/html?lang=en&srsltid=AfmBOoo9wxIljnyrYrmJaGI8kRl3NtZ8VYouM8-AUtRgN3BviMpitVGa",
        "description": (
            "Una trama en forma de moñitos cortada en una lámina elástica oculta una "
            "transformación compleja. Bajo tensión, las geometrías auxéticas se expanden, ya "
            "sea curvándose hacia arriba o enrollándose, replegándose hacia adentro como un "
            "tatú carreta para levantar una esfera, este movimientos se da únicamente a través "
            "de la forma. En lugar de apoderarse de su objetivo, el material lo envuelve "
            "suavemente, asegurándolo y liberándolo mediante una deformación inteligente que "
            "evoca el instinto de un organismo vivo."
        ),
    },
    {
        "code": "MF.05",
        "interaction": "Atraer",
        "year": 2026,
        "authors": "Heidi Jalkh and Nadya Suvorova",
        "name": "Polvo de acero",
        "material_origin": "Apheros AG (CH), Material Science Department, Complex Materials Group, ETH Zurich",
        "source_url": "https://advanced.onlinelibrary.wiley.com/doi/full/10.1002/adma.202207181",
        "description": (
            "A través de un escenario magnético, esponjas metálicas pisan y se deslizan en "
            "una caminata lunar perpetua. Guiadas por un campo magnético rotatorio, se "
            "adhieren, trepan y derivan de maneras que parecen desafiar la gravedad, escalando "
            "planos verticales con una gracia sin esfuerzo. Es una coreografía palpitante: una "
            "secuencia fluida de atracción, entrega y ascenso."
        ),
    },
]

materials = [Material(**m) for m in materials]
material_map = {m.code: m for m in materials}
