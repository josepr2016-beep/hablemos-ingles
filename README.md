# Hablemos Inglés

Aplicación web familiar para aprender inglés hablado y escuchado (cinco niveles, de Inicial a Avanzado).
Flask + Postgres, pensada para desplegar en Render. Funciona en celular y computador.

## Qué hace

- **Práctica de hoy**: sesión corta que mezcla frases para repasar y frases nuevas (repaso espaciado).
- **Hablar**: escuchar la frase, repetirla y ver qué palabras se entendieron y cuáles no.
- **Escuchar**: oír la frase sin verla y armarla con fichas.
- **Conversar**: diálogo guiado por turnos con la aplicación.
- **Sonidos difíciles**: pares como ship/sheep o three/tree, para entrenar el oído.
- Perfiles por persona, con racha de días y puntos.

## Voz

Usa la voz y el reconocimiento de voz del navegador, sin costo.
Para que califique la pronunciación se necesita Chrome o Edge (computador y Android) o Safari (iPhone),
y que la página se abra por HTTPS (Render lo da) o en `localhost`.

## Probar en el computador

    pip install -r requirements.txt
    python app.py

Abrir http://localhost:5000 en Chrome. Sin `DATABASE_URL` usa un archivo SQLite local.

## Desplegar en Render

Subir el repositorio a GitHub y en Render elegir **New > Blueprint**; `render.yaml` crea el servicio y la base de datos.

## Agregar contenido

Editar `content.py`: copiar un bloque de tema y cambiar las frases y la conversación.
