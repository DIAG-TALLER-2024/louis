# Louis - Bot Tributario

Un ejemplo de un bot tributario que responde dudas basándose en la [Ley 824](https://www.bcn.cl/leychile/navegar?idNorma=6368).

Esta es una prueba de concepto de RAG para el Taller de desarrollo de una aplicación con IA generativa del [Diplomado en Inteligencia Artificial Generativa](https://educacioncontinua.uc.cl/programas/diplomado-en-inteligencia-artificial-generativa/) de la PUC.

## Instrucciones para desarrollar localmente

### Instalación

Una vez descargado el proyecto, crear Virtual environment:

```sh
python3 -m venv venv
```

Activarlo:

```sh
source venv/bin/activate
```

Instalar dependencias:

```sh
pip install -r requirements.txt
```

### Agregar variables de entorno

Necesitarás una [API KEY de OpenAI](https://platform.openai.com/). Una vez la tengas, crea un archivo `.env` y agrégala:

```bash
# .env
OPENAI_API_KEY=""
```

### Ejecución

Una vez ya lo instalaste, recuerda activar el Virtual Env:

```sh
source venv/bin/activate
```

Y luego ya puedes ejecutar el proyecto localmente con

```sh
flask run --debug
```

## Probar el bot

En Postman, puedes hacer un POST a `http://127.0.0.1:5000/chat`, enviando como JSON lo siguiente:

```json
{
    "question": "cómo se clasifica la venta de dólares?"
}
```

Y una posible respuesta es:

```json
{
    "answer": "La venta de dólares se clasifica, generalmente, como una ganancia de capital. Esto es cuando compras dólares a un precio y luego los vendes a un precio más alto, obteniendo un beneficio. Si esta actividad es parte de un negocio habitual, podría considerarse parte de las rentas mencionadas en el artículo 20 N° 5, y sería sujeto a impuestos según las normas aplicables. Si es ocasional, podría tener un trato diferente. Lo importante es tener claro cómo, cuándo y por cuánto se realizó la transacción."
}
```

Luego si haces un follow-up:

```json
{
    "question": "y esto cómo se declara?"
}
```

Debería responderte decente:

```json
{
    "answer": "Las utilidades o pérdidas cambiarias se declaran en la declaración anual de impuestos. Debes llevar un registro claro de estas operaciones. Un contador puede ayudarte a hacerlo correctamente."
}
```

Y esto ocurre gracias a la función `contextualize` (archivo query.py) que transforma la pregunta de `"y esto cómo se declara?"` a `¿Cómo se clasifica la venta de dólares?`, de manera de que al hacer la búsqueda de Chroma DB busque el contexto "correcto".
