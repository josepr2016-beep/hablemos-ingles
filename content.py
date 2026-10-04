"""Contenido de nivel básico. Para agregar más, copie un bloque y cambie los textos.

Cada tema tiene frases (inglés, español) y una conversación.
En la conversación, "A" es la aplicación y "B" es la persona que practica.
"""

_RAW = [
    ("Saludos", "👋", [
        ("Hi, how are you?", "Hola, ¿cómo estás?"),
        ("I'm fine, thank you.", "Estoy bien, gracias."),
        ("What's your name?", "¿Cómo te llamas?"),
        ("Nice to meet you.", "Mucho gusto."),
        ("Where are you from?", "¿De dónde eres?"),
        ("I'm from Colombia.", "Soy de Colombia."),
        ("Can you repeat that, please?", "¿Puedes repetir, por favor?"),
        ("See you tomorrow.", "Nos vemos mañana."),
    ], [
        ("A", "Hi! How are you?", "¡Hola! ¿Cómo estás?"),
        ("B", "I'm fine, thank you.", "Estoy bien, gracias."),
        ("A", "Where are you from?", "¿De dónde eres?"),
        ("B", "I'm from Colombia.", "Soy de Colombia."),
        ("A", "Nice to meet you!", "¡Mucho gusto!"),
        ("B", "Nice to meet you too. See you tomorrow.", "Mucho gusto también. Nos vemos mañana."),
    ]),
    ("Familia y casa", "🏠", [
        ("This is my family.", "Esta es mi familia."),
        ("I have two brothers.", "Tengo dos hermanos."),
        ("My mother is at home.", "Mi mamá está en casa."),
        ("We live in a small house.", "Vivimos en una casa pequeña."),
        ("Where is the bathroom?", "¿Dónde está el baño?"),
        ("The kitchen is over there.", "La cocina está allá."),
        ("I love my family.", "Amo a mi familia."),
        ("Who is that?", "¿Quién es ese?"),
    ], [
        ("A", "Do you have brothers or sisters?", "¿Tienes hermanos o hermanas?"),
        ("B", "Yes, I have two brothers.", "Sí, tengo dos hermanos."),
        ("A", "Where do you live?", "¿Dónde vives?"),
        ("B", "We live in a small house.", "Vivimos en una casa pequeña."),
        ("A", "Who is at home now?", "¿Quién está en casa ahora?"),
        ("B", "My mother is at home.", "Mi mamá está en casa."),
    ]),
    ("Comida", "🍎", [
        ("I'm hungry.", "Tengo hambre."),
        ("I would like some water, please.", "Quisiera un poco de agua, por favor."),
        ("Can I have the menu?", "¿Me da el menú?"),
        ("I like chicken and rice.", "Me gusta el pollo con arroz."),
        ("What do you want to eat?", "¿Qué quieres comer?"),
        ("The food is very good.", "La comida está muy buena."),
        ("How much is it?", "¿Cuánto es?"),
        ("The check, please.", "La cuenta, por favor."),
    ], [
        ("A", "Hello! What do you want to eat?", "¡Hola! ¿Qué quieres comer?"),
        ("B", "I like chicken and rice.", "Me gusta el pollo con arroz."),
        ("A", "Anything to drink?", "¿Algo de tomar?"),
        ("B", "I would like some water, please.", "Quisiera un poco de agua, por favor."),
        ("A", "Here you go.", "Aquí tienes."),
        ("B", "Thank you. The food is very good.", "Gracias. La comida está muy buena."),
    ]),
    ("Rutina diaria", "⏰", [
        ("I wake up early.", "Me despierto temprano."),
        ("I take a shower every morning.", "Me ducho todas las mañanas."),
        ("I go to work by bus.", "Voy al trabajo en bus."),
        ("What time is it?", "¿Qué hora es?"),
        ("It's time to go to bed.", "Es hora de ir a la cama."),
        ("I'm very tired today.", "Estoy muy cansado hoy."),
        ("What are you doing?", "¿Qué estás haciendo?"),
        ("I'm doing my homework.", "Estoy haciendo mi tarea."),
    ], [
        ("A", "What time do you wake up?", "¿A qué hora te despiertas?"),
        ("B", "I wake up early.", "Me despierto temprano."),
        ("A", "How do you go to work?", "¿Cómo vas al trabajo?"),
        ("B", "I go to work by bus.", "Voy al trabajo en bus."),
        ("A", "What are you doing now?", "¿Qué estás haciendo ahora?"),
        ("B", "I'm doing my homework.", "Estoy haciendo mi tarea."),
    ]),
    ("En la calle", "🚌", [
        ("Excuse me, where is the bank?", "Disculpe, ¿dónde está el banco?"),
        ("Go straight and turn left.", "Siga derecho y gire a la izquierda."),
        ("Is it far from here?", "¿Está lejos de aquí?"),
        ("It's near the park.", "Está cerca del parque."),
        ("I need a taxi.", "Necesito un taxi."),
        ("How do I get to the airport?", "¿Cómo llego al aeropuerto?"),
        ("I'm lost. Can you help me?", "Estoy perdido. ¿Me puede ayudar?"),
        ("Thank you for your help.", "Gracias por su ayuda."),
    ], [
        ("A", "Can I help you?", "¿Le puedo ayudar?"),
        ("B", "Excuse me, where is the bank?", "Disculpe, ¿dónde está el banco?"),
        ("A", "Go straight and turn left.", "Siga derecho y gire a la izquierda."),
        ("B", "Is it far from here?", "¿Está lejos de aquí?"),
        ("A", "No, it's near the park.", "No, está cerca del parque."),
        ("B", "Thank you for your help.", "Gracias por su ayuda."),
    ]),
    ("Compras", "🛍️", [
        ("How much does this cost?", "¿Cuánto cuesta esto?"),
        ("It's too expensive.", "Es demasiado caro."),
        ("Do you have a bigger size?", "¿Tiene una talla más grande?"),
        ("I'm just looking, thanks.", "Solo estoy mirando, gracias."),
        ("I'll take it.", "Me lo llevo."),
        ("Can I pay with a card?", "¿Puedo pagar con tarjeta?"),
        ("Where can I buy shoes?", "¿Dónde puedo comprar zapatos?"),
        ("I need a new jacket.", "Necesito una chaqueta nueva."),
    ], [
        ("A", "Hello! Can I help you?", "¡Hola! ¿Le puedo ayudar?"),
        ("B", "I need a new jacket.", "Necesito una chaqueta nueva."),
        ("A", "This one is very nice.", "Esta es muy bonita."),
        ("B", "How much does this cost?", "¿Cuánto cuesta esto?"),
        ("A", "It's forty dollars.", "Cuesta cuarenta dólares."),
        ("B", "I'll take it. Can I pay with a card?", "Me lo llevo. ¿Puedo pagar con tarjeta?"),
    ]),
]

UNITS = []
for n, (title, emoji, phrases, lines) in enumerate(_RAW, start=1):
    uid = f"u{n}"
    UNITS.append({
        "id": uid,
        "title": title,
        "emoji": emoji,
        "phrases": [
            {"id": f"{uid}p{i}", "en": en, "es": es}
            for i, (en, es) in enumerate(phrases, start=1)
        ],
        "dialogue": {"id": f"{uid}d", "lines": [list(line) for line in lines]},
    })

# Pares de sonidos que suelen confundir los hispanohablantes.
_PAIRS = [
    ("ship", "sheep", "En 'ship' la vocal es corta y relajada. En 'sheep' es larga, como sonriendo."),
    ("live", "leave", "'live' es corta; 'leave' es larga: liiiv."),
    ("this", "these", "'this' termina en s suave y vocal corta; 'these' es larga y termina en z."),
    ("cat", "cut", "En 'cat' abre bien la boca; en 'cut' es un sonido corto, casi una 'a' apagada."),
    ("very", "berry", "Para la 'v' los dientes de arriba tocan el labio de abajo. La 'b' junta los dos labios."),
    ("vote", "boat", "'vote' empieza con dientes en el labio; 'boat' con los labios cerrados."),
    ("three", "tree", "Para 'th' saca un poco la lengua entre los dientes y sopla."),
    ("think", "sink", "'think' lleva la lengua entre los dientes; 'sink' es una 's' normal."),
    ("they", "day", "En 'they' la lengua toca los dientes y vibra; 'day' es una 'd' seca."),
    ("chair", "share", "'chair' es como la 'ch' del español; 'share' es más suave, como pidiendo silencio: shhh."),
    ("watch", "wash", "'watch' termina en 'ch'; 'wash' termina en 'shhh'."),
    ("yellow", "jello", "'yellow' empieza suave como una 'i'; 'jello' empieza fuerte, como 'dch'."),
]
PAIRS = [{"id": f"m{i}", "a": a, "b": b, "tip": tip} for i, (a, b, tip) in enumerate(_PAIRS, start=1)]
