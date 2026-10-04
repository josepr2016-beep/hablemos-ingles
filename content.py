"""Contenido por niveles (Inicial, Básico, Intermedio). Para agregar más, copie un bloque y cambie los textos.

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

_L1 = [
    ("Hola y adiós", "👋", [
        ("Hello!", "¡Hola!"),
        ("Good morning.", "Buenos días."),
        ("Good night.", "Buenas noches."),
        ("Thank you.", "Gracias."),
        ("Yes, please.", "Sí, por favor."),
        ("No, thank you.", "No, gracias."),
        ("I'm sorry.", "Lo siento."),
        ("Goodbye!", "¡Adiós!"),
    ], [
        ("A", "Hello! Good morning.", "¡Hola! Buenos días."),
        ("B", "Good morning.", "Buenos días."),
        ("A", "Do you want some juice?", "¿Quieres jugo?"),
        ("B", "Yes, please.", "Sí, por favor."),
        ("A", "Here you go.", "Aquí tienes."),
        ("B", "Thank you. Goodbye!", "Gracias. ¡Adiós!"),
    ]),
    ("Colores", "🎨", [
        ("It's red.", "Es rojo."),
        ("It's blue.", "Es azul."),
        ("The sun is yellow.", "El sol es amarillo."),
        ("The tree is green.", "El árbol es verde."),
        ("I like pink.", "Me gusta el rosado."),
        ("Black and white.", "Negro y blanco."),
        ("I have two hands.", "Tengo dos manos."),
        ("What color is it?", "¿De qué color es?"),
    ], [
        ("A", "Look at the sun. What color is it?", "Mira el sol. ¿De qué color es?"),
        ("B", "The sun is yellow.", "El sol es amarillo."),
        ("A", "And the tree?", "¿Y el árbol?"),
        ("B", "The tree is green.", "El árbol es verde."),
        ("A", "What color do you like?", "¿Qué color te gusta?"),
        ("B", "I like pink.", "Me gusta el rosado."),
    ]),
    ("Animales", "🐶", [
        ("This is a dog.", "Este es un perro."),
        ("The cat is small.", "El gato es pequeño."),
        ("I see a bird.", "Veo un pájaro."),
        ("The lion is big.", "El león es grande."),
        ("Look, a duck!", "¡Mira, un pato!"),
        ("I like my dog.", "Me gusta mi perro."),
        ("The fish is in the water.", "El pez está en el agua."),
        ("It's a horse.", "Es un caballo."),
    ], [
        ("A", "What is this?", "¿Qué es esto?"),
        ("B", "This is a dog.", "Este es un perro."),
        ("A", "Is the cat big?", "¿El gato es grande?"),
        ("B", "No. The cat is small.", "No. El gato es pequeño."),
        ("A", "What do you see?", "¿Qué ves?"),
        ("B", "I see a bird.", "Veo un pájaro."),
    ]),
    ("Vamos a jugar", "🧸", [
        ("This is my ball.", "Esta es mi pelota."),
        ("Let's play!", "¡Vamos a jugar!"),
        ("I have a bike.", "Tengo una bicicleta."),
        ("It's my turn.", "Es mi turno."),
        ("I want to play.", "Quiero jugar."),
        ("Come with me.", "Ven conmigo."),
        ("I'm happy.", "Estoy feliz."),
        ("Look at me!", "¡Mírame!"),
    ], [
        ("A", "Hi! What do you want to do?", "¡Hola! ¿Qué quieres hacer?"),
        ("B", "I want to play.", "Quiero jugar."),
        ("A", "What is this?", "¿Qué es esto?"),
        ("B", "This is my ball.", "Esta es mi pelota."),
        ("A", "Great! Let's play!", "¡Genial! ¡Vamos a jugar!"),
        ("B", "It's my turn. I'm happy.", "Es mi turno. Estoy feliz."),
    ]),
]

_L3 = [
    ("Planes", "📅", [
        ("What are you going to do this weekend?", "¿Qué vas a hacer este fin de semana?"),
        ("I'm going to visit my grandparents.", "Voy a visitar a mis abuelos."),
        ("We went to the beach last month.", "Fuimos a la playa el mes pasado."),
        ("I didn't have time to call you.", "No tuve tiempo de llamarte."),
        ("Would you like to come with us?", "¿Te gustaría venir con nosotros?"),
        ("That sounds like a great idea.", "Suena como una gran idea."),
        ("I'll let you know tomorrow.", "Te aviso mañana."),
        ("I had a really good time.", "La pasé muy bien."),
    ], [
        ("A", "What are you going to do this weekend?", "¿Qué vas a hacer este fin de semana?"),
        ("B", "I'm going to visit my grandparents.", "Voy a visitar a mis abuelos."),
        ("A", "Nice. We are going to the beach. Would you like to come with us?", "Qué bien. Vamos a la playa. ¿Te gustaría venir con nosotros?"),
        ("B", "That sounds like a great idea.", "Suena como una gran idea."),
        ("A", "Can you tell me today?", "¿Me puedes decir hoy?"),
        ("B", "I'll let you know tomorrow.", "Te aviso mañana."),
    ]),
    ("Trabajo", "💼", [
        ("What do you do for a living?", "¿A qué te dedicas?"),
        ("I work in an office downtown.", "Trabajo en una oficina en el centro."),
        ("I've been working here for five years.", "Llevo cinco años trabajando aquí."),
        ("I have a meeting this afternoon.", "Tengo una reunión esta tarde."),
        ("Could you send me the report?", "¿Me podrías enviar el informe?"),
        ("I'm sorry, I'm running late.", "Lo siento, voy tarde."),
        ("Let me check and get back to you.", "Déjame revisar y te respondo."),
        ("I need to finish this before Friday.", "Necesito terminar esto antes del viernes."),
    ], [
        ("A", "What do you do for a living?", "¿A qué te dedicas?"),
        ("B", "I work in an office downtown.", "Trabajo en una oficina en el centro."),
        ("A", "How long have you worked there?", "¿Cuánto tiempo llevas trabajando ahí?"),
        ("B", "I've been working here for five years.", "Llevo cinco años trabajando aquí."),
        ("A", "Could you send me the report today?", "¿Me podrías enviar el informe hoy?"),
        ("B", "Let me check and get back to you.", "Déjame revisar y te respondo."),
    ]),
    ("Viajes", "✈️", [
        ("I'd like to book a room for two nights.", "Quisiera reservar una habitación por dos noches."),
        ("What time does the flight leave?", "¿A qué hora sale el vuelo?"),
        ("Could you tell me where the gate is?", "¿Me podría decir dónde está la puerta de embarque?"),
        ("I have a reservation under my name.", "Tengo una reserva a mi nombre."),
        ("Is breakfast included?", "¿El desayuno está incluido?"),
        ("How long does it take to get there?", "¿Cuánto se demora en llegar?"),
        ("I think I left my bag on the bus.", "Creo que dejé mi maleta en el bus."),
        ("Can you recommend a good restaurant?", "¿Me puede recomendar un buen restaurante?"),
    ], [
        ("A", "Good evening. How can I help you?", "Buenas noches. ¿En qué le puedo ayudar?"),
        ("B", "I have a reservation under my name.", "Tengo una reserva a mi nombre."),
        ("A", "Yes, here it is. A room for two nights.", "Sí, aquí está. Una habitación por dos noches."),
        ("B", "Is breakfast included?", "¿El desayuno está incluido?"),
        ("A", "Yes, it is. Anything else?", "Sí, está incluido. ¿Algo más?"),
        ("B", "Can you recommend a good restaurant?", "¿Me puede recomendar un buen restaurante?"),
    ]),
    ("Salud y problemas", "🩺", [
        ("I don't feel very well.", "No me siento muy bien."),
        ("I have a headache.", "Tengo dolor de cabeza."),
        ("I need to see a doctor.", "Necesito ver a un médico."),
        ("How long have you felt like this?", "¿Hace cuánto te sientes así?"),
        ("You should get some rest.", "Deberías descansar un poco."),
        ("My phone isn't working.", "Mi teléfono no funciona."),
        ("Could you speak more slowly, please?", "¿Podría hablar más despacio, por favor?"),
        ("I didn't understand the last part.", "No entendí la última parte."),
    ], [
        ("A", "Hello. What seems to be the problem?", "Hola. ¿Cuál parece ser el problema?"),
        ("B", "I don't feel very well. I have a headache.", "No me siento muy bien. Tengo dolor de cabeza."),
        ("A", "How long have you felt like this?", "¿Hace cuánto te sientes así?"),
        ("B", "Could you speak more slowly, please?", "¿Podría hablar más despacio, por favor?"),
        ("A", "Of course. You should get some rest and drink water.", "Claro. Deberías descansar y tomar agua."),
        ("B", "Thank you. I need to see a doctor.", "Gracias. Necesito ver a un médico."),
    ]),
]

# Niveles. Los identificadores (a, u, c) no deben cambiarse: el progreso guardado depende de ellos.
LEVELS = [
    {"id": 1, "name": "Inicial", "emoji": "🌱", "desc": "Desde cero. Frases muy cortas, ideal para niños."},
    {"id": 2, "name": "Básico", "emoji": "🌿", "desc": "Frases sencillas para el día a día."},
    {"id": 3, "name": "Intermedio", "emoji": "🌳", "desc": "Frases más largas y conversaciones reales."},
]

UNITS = []
for prefix, level, raw in (("a", 1, _L1), ("u", 2, _RAW), ("c", 3, _L3)):
    for n, (title, emoji, phrases, lines) in enumerate(raw, start=1):
        uid = f"{prefix}{n}"
        UNITS.append({
            "id": uid,
            "level": level,
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
