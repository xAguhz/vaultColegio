---
tipo: fuente
tema: MHS
titulo_video: "¿Por qué Anthropic se está metiendo en el hardware? (MHS explicado)"
canal: IoT Lab
url: https://www.youtube.com/watch?v=3hxdHem70gw
publicado: 2026-11-01
duracion: "29:21"
idioma: es
origen_texto: subtítulos automáticos de YouTube (es-orig), corregidos a mano en nombres propios
tags: [fuente, transcripcion]
---

# Transcripción — MHS explicado (IoT Lab)

> [!info] Sobre este texto
> Subtítulos automáticos de YouTube, agrupados en bloques de ~30 s. Cada marca de tiempo abre el video en ese segundo.
> Se corrigieron errores del reconocimiento de voz: *Claudia → Claude*, *Antropic/Antrópica → Anthropic*, *Cuera → QuEra*,
> *"la gente" → "el agente"* (13:25, 23:31, 25:30, donde el sentido lo pide) y *"dentro del robot" → "dentro de LeRobot"* (23:31). Se quitaron marcas como [música].
> El resto queda tal cual, con la oralidad del autor.

Volver a [[00 Inicio]] · Resumen: [[01 Resumen del video]]

### [00:00](https://www.youtube.com/watch?v=3hxdHem70gw&t=0s)

Llego un poco tarde a este vídeo, pero Anthropic sacó hace unos meses algo que puede ser bastante importante, aunque no lo parezca. Y lo curioso es que no estamos hablando de un nuevo modelo de inteligencia artificial, estamos hablando de un estándar. Se llama Model Hardware Standard, que probablemente lo veréis con las siglas MHS. Pero antes de explicar qué es, pensad durante un momento en algo bastante cotidiano. Imaginad que entráis en una habitación llena de aparatos. Hay una cámara, un robot, una báscula, un microscopio, un sensor de temperatura, una máquina que mueve líquidos de un recipiente a otro, etcétera. Vosotros podéis mirar cada aparato y más o menos entender qué es.

### [00:34](https://www.youtube.com/watch?v=3hxdHem70gw&t=34s)

Veis una cámara y sabéis que sirve para ver imágenes. Veis una báscula y entenderéis que mide peso. Y veis un robot y entendéis que puede moverse. Pues bien, una inteligencia artificial no lo tiene tan fácil. Necesita alguna manera de saber qué dispositivo tiene delante, qué información puede obtener de él, qué órdenes puede darle y qué cosas no debería hacer. Y aquí aparece precisamente el problema que intenta resolver MHS. La idea de Anthropic es crear una especie de lenguaje común entre las inteligencias artificiales y las máquinas. Una manera estándar de explicar a una inteligencia artificial, esto es una cámara, puedes pedirle una imagen. O esto es un robot y puedes moverlo hasta aquí. O incluso, esto es un sensor y puedes preguntarle qué temperatura está midiendo. Incluso, esta acción no la puedes ejecutar porque sería peligroso. Hacer que una inteligencia artificial puede encontrarse con una máquina, descubrir qué puede hacer con ella y sobre todo

### [01:21](https://www.youtube.com/watch?v=3hxdHem70gw&t=81s)

saber cómo interactuar con ella, sin tener que aprender desde cero un sistema completamente distinto cada vez. Ahora bien, esto no quiere decir que Claude pueda meterse en una fábrica, detectar las máquinas que hay y pueda controlarlas automáticamente. De hecho, estamos bastante lejos de eso. Y por eso justo quería hacer este vídeo, para no caer en el titular de la inteligencia artificial ya controla el hardware. Quiero que entendáis qué se está haciendo, cómo se está haciendo y qué se ha hecho ya en escenarios reales. Anthropic presentó públicamente Model Hardware Standard el 27 de agosto de 2026. Sí, lo sé, llego un poco tarde. El proyecto nació como una colaboración entre Anthropic y el campus de investigación HHMI Janelia. Y ahora mismo se encuentra en una research preview bastante limitada. Es decir, todavía no estamos ante una tecnología terminada y preparada para instalar tranquilamente en cualquier fábrica. Se está probando con laboratorios, empresas

### [02:08](https://www.youtube.com/watch?v=3hxdHem70gw&t=128s)

de robótica, fabricantes y organizaciones relacionadas con investigación científica y fabricación avanzada. Entre las compañías que ya están empezando a trabajar con esta tecnología, aparecen nombres bastante comunes como Raspberry Pi o Universal Robots. La intención durante esta primera fase es probar el estándar, encontrar problemas, estudiar especialmente todo lo relacionado con seguridad y más adelante convertirlo en open source. Pero para entender por qué Anthropic cree que necesitamos algo así, tenemos que hablar de un problema que existe desde mucho antes de la inteligencia artificial. Las máquinas no hablan todas el mismo idioma. Imaginad que entramos en un laboratorio. Tenemos un brazo robótico de un fabricante, una cámara de otro, una máquina que mueve líquidos, un microscopio, varios sensores. Desde fuera todos parecen simplemente aparatos electrónicos, pero cuando intentamos

### [02:55](https://www.youtube.com/watch?v=3hxdHem70gw&t=175s)

controlarlos desde un ordenador descubrimos el problema. Cada uno funciona de una manera distinta. El fabricante del robot quizá nos dé un programa concreto para controlarlo. La cámara, en cambio, puede venir con su propio software. El microscopio, en cambio, puede necesitar otro. Un sensor quizá envíe información usando un protocolo determinado. Y puede que otra máquina tenga un programa creado hace 20 años que solamente funciona pulsando botones en una pantalla. Pues si para una persona esto ya puede ser algo incómodo, para un sistema que quiere controlar 10, 20 o 100 dispositivos distintos, se convierte en un problema bastante serio, ya que cada fabricante crea su propia forma de controlarlos. Y cuando queremos conectar equipos diferentes, tenemos que construir pequeños traductores entre un sistema y otros. En informática, esos caminos suelen aparecer en forma de APIs, SDKs, protocolos o programas específicos. Los nombres pueden sonar bastante técnicos,

### [03:43](https://www.youtube.com/watch?v=3hxdHem70gw&t=223s)

pero la idea es sencilla. Una API, por ejemplo, es básicamente una manera que ofrece un programa para que otro programa pueda pedirle cosas. En vez de que una persona pulse con el ratón el botón de una cámara para hacer una foto. Una API podría permitirlo con otro programa enviando una orden que significa haz una foto. Un SDK también es normalmente un conjunto de herramientas que un fabricante entrega a los desarrolladores para que puedan crear software que trabaje con su dispositivo. Y por otro lado, un protocolo define las reglas que siguen dos equipos para intercambiar información. El problema en sí aparece cuando tenemos muchos dispositivos y cada uno tiene sus propias reglas.

### [04:17](https://www.youtube.com/watch?v=3hxdHem70gw&t=257s)

Ahora, imaginad que queremos poner una inteligencia artificial por encima de todos ellos. La IA no solamente necesita encontrar la forma de enviar una orden. También tiene que comprender qué significa esa orden. Tiene que saber qué puede hacer cada máquina, qué información puede leer, qué parámetros puede cambiar, incluso qué límites tiene, por no mencionar qué acciones pueden ser peligrosas. Pero también tiene que saber qué pasos deberían ocurrir antes que otros. Y esto último es especialmente relevante cuando dejamos el mundo del software y pasamos al mundo físico. Porque en un ordenador podemos borrar un archivo por error, pero en una máquina podemos mover un robot contra una persona, o podemos calentar algo demasiado, podemos abrir una válvula que debería estar cerrada, incluso hacer girar un motor cuando alguien está trabajando sobre él. Todo esto en sí tiene consecuencias físicas.

### [05:02](https://www.youtube.com/watch?v=3hxdHem70gw&t=302s)

Jugamos con la vida de las personas muchas veces. Así que MHS intenta crear una estructura común para describir todo eso. La forma más sencilla de imaginarlo, pues es pensar en un traductor. Abajo tenemos la máquina real. Imaginaos, pues un robot, una cámara, un microscopio, un sensor, lo que sea. Esa máquina sigue funcionando exactamente con la tecnología que ya tenía, y MHS no obliga a cambiarla. Lo que colocaríamos entre la máquina y la inteligencia artificial es una pieza de software que Anthropic llama driver MHS. Ese driver hace de traductor. Imaginad que tenemos un robot cuyo fabricante dice, "Para mover el brazo tienes que llamar a esta función concreta de mi software." La inteligencia artificial no tendría porqué conocer todos los detalles internos de ese fabricante. El driver puede traducir una orden más genérica a la traducción exacta que entiende ese robot. En sí, es una idea bastante parecida a lo que ocurre cuando conectamos una

### [05:50](https://www.youtube.com/watch?v=3hxdHem70gw&t=350s)

impresora a un ordenador. Vosotros pulsáis imprimir, no necesitáis saber qué señales eléctricas tiene que enviar Windows a cada motor que mueve el papel. Hay software por debajo que traduce esa intención a las órdenes que entiende la impresora. Pues con MHS la filosofía es bastante parecida, aunque aplicada a máquinas que pueden ser muchísimo más complejas. Anthropic habla, por ejemplo, de operaciones muy básicas como read y write, leer algo o cambiar algo. Supongamos que tenemos un sensor de temperatura. La inteligencia artificial podría querer leer su valor. Para ella, la acción podría ser algo tan simple como quiero saber la temperatura, pero debajo puede estar ocurriendo algo bastante más técnico. Quizá ese sensor funciona con Modbus, quizá hay que preguntar por un registro concreto y quizá el número que devuelve necesita convertirse después a grados Celsius. El agente en sí no debería necesitar

### [06:37](https://www.youtube.com/watch?v=3hxdHem70gw&t=397s)

conocer necesariamente todos esos detalles. El driver se encargaría de hacer esa traducción. Y aquí tenemos una diferencia clave. MHS no hace desaparecer la tecnología que ya existe. Una máquina Modbus seguirá funcionando con Modbus. Un robot seguirá teniendo su API. Y una cámara seguirá teniendo su propio sistema. Alguien sigue teniendo que preparar la integración. Lo que MHS intenta es que, una vez hecha esa integración, todo lo que está por encima vea esos equipos de una manera muy parecida. Y para entender por qué esto puede ser interesante, pensad en vuestros ordenadores. Cuando conectáis un ratón USB de una marca u otra, normalmente vuestro ordenador entiende que aquello es un ratón. No necesitáis aprender una forma completamente nueva de mover un cursor cada vez que cambies de fabricante. Con las máquinas industriales estamos muchísimo más lejos

### [07:24](https://www.youtube.com/watch?v=3hxdHem70gw&t=444s)

de tener algo tan sencillo. Un robot industrial puede ser completamente diferente a otro. Una cámara industrial puede tener su propia forma de control. MHS intenta acercarnos, al menos conceptualmente, a una situación en la que una inteligencia artificial pueda descubrir ciertas capacidades de esos equipos mediante una estructura común. Pero hay otra parte todavía más interesante, porque conocer los comandos de una máquina realmente no es suficiente. Imaginad que os entrego el mando a distancia de una excavadora. Vosotros sabéis qué botón sirve para levantar el brazo, moverse hacia delante, hacia atrás, aplicar fuerza, digamos todo lo que se puede hacer. Pero que sepáis eso no significa que sepáis utilizar una excavadora de forma segura.

### [08:02](https://www.youtube.com/watch?v=3hxdHem70gw&t=482s)

Todavía os faltaría muchísimo contexto. Por ejemplo, cuánto pesa, cuánto puede cargar, hasta dónde llega el brazo, puede girar si hay una persona al lado, qué ocurre si levantamos demasiado peso, qué movimientos están prohibidos, etcétera. Y con inteligencia artificial pasa exactamente lo mismo. Saber qué botón puede pulsar es una parte del problema, pero entender qué significa pulsar ese botón es una cosa completamente distinta. Por eso MHS también intenta describir características y restricciones del dispositivo. Imaginemos un brazo robótico. Desde software podemos acceder a la posición de los motores, podemos conocer su velocidad, incluso mandarlo a una posición, pero puede existir información que no aparezca directamente en una API. Por ejemplo, cuánto peso puede levantar, qué recorrido físico tiene, qué zona no debería atravesar. MHS permite añadir este tipo de información

### [08:49](https://www.youtube.com/watch?v=3hxdHem70gw&t=529s)

mediante etiquetas que incluso pueden escribirse con lenguaje natural. A partir de ahí se genera una especie de ficha de la máquina. Una ficha pensada para que un sistema pueda entender qué dispositivo es, qué sabe hacer, qué puede medir, qué podemos cambiar y qué límites tiene. Esta parte es clave, porque no estamos intentando simplemente conectar una IA con una máquina. Estamos intentando que pueda interpretar qué clase de máquina tiene delante. Y todo esto conecta con una tecnología de Anthropic que seguramente algunos conoceréis, de hecho probablemente muchos si estáis viendo este vídeo, que se llama MCP, Model Context Protocol.

### [09:23](https://www.youtube.com/watch?v=3hxdHem70gw&t=563s)

MCP apareció precisamente para que los modelos de inteligencia artificial pudieran conectarse con herramientas externas. Por ejemplo, una IA podría acceder mediante MCP a un calendario o a una base de datos, a una aplicación o incluso a un buscador. MHS comparte parte de esa filosofía, pero está pensado para otro mundo, que es el mundo físico. Anthropic explica que MHS podía apoyarse en MCP como una de las formas mediante las que un agente accede al hardware, pero no debería ser la única. También puede trabajar mediante línea de comandos o directamente desde código. Y hay otro detalle que conviene dejar claro. Aunque Anthropic está detrás del proyecto, MHS está planteado como model agnostic, es decir, la idea no es que solamente Claude pueda trabajar con estas máquinas. Conceptualmente, otros modelos podrían hacerlo también,

### [10:10](https://www.youtube.com/watch?v=3hxdHem70gw&t=610s)

tal y como hicieron con MCP. Hasta aquí tenemos la teoría, pero lo interesante de esta tecnología es saber qué se está haciendo ya en el mundo físico, en el mundo real, y ya han realizado varios experimentos con esto. Os quiero explicar un ejemplo donde se aplicó MHS para que entendáis claramente el caso de uso y por qué tiene tanto sentido MHS. Querían automatizar un experimento de laboratorio. Para hacerlo, necesitaban coordinar diferentes máquinas, un manipulador de líquidos, un lector de placas, un brazo robótico y varias cámaras. Y todo estaba repartido entre tres ordenadores distintos. Sobre el papel, parece relativamente sencillo.

### [10:43](https://www.youtube.com/watch?v=3hxdHem70gw&t=643s)

Una máquina hace una tarea, después otra hace la siguiente, después el robot mueve algo y continuamos. El problema vuelve a ser el mismo. Cada equipo se controla de una forma completamente diferente. El brazo robótico funcionaba mediante un sistema que recibía archivos. En cambio, el manipulador de líquidos tenía una interfaz antigua basada en ActiveX y COM. Y el lector de placas ni siquiera tenía una API moderna que pudiera llamar directamente. Tenían que manejar una interfaz gráfica. Así que imagínate intentar automatizar vuestra casa si para encender cada bombilla necesitáis una aplicación diferente. Una marca funcionase enviando archivos, otra solamente pudieras manejarla pulsando botones en una pantalla y otra necesitase comandos completamente distintos. Eso era, salvando las distancias claramente, parte del problema. Con MHS desarrollaron drivers para estos

### [11:31](https://www.youtube.com/watch?v=3hxdHem70gw&t=691s)

equipos. Cada driver hacía de traductor entre una máquina concreta y la capa común. Después colocar una capa de orquestación por encima. Orquestar, para que nos entendamos, significa simplemente coordinar las acciones. Primero hace esto, cuando termine mueve aquello, después mide esto y si el resultado es correcto continúa. Gracias a esa arquitectura, un agente podría trabajar con todo ese proceso sin tener que tratar cada máquina como un mundo completamente separado. Y el resultado, pues fue bastante llamativo. Consiguieron pasar de tener el equipamiento preparado, pero sin esa automatización, a obtener una curva de dilución completamente en 8 horas.

### [12:06](https://www.youtube.com/watch?v=3hxdHem70gw&t=726s)

Dentro de esas 8 horas hubo incluso una repetición autónoma del experimento. Según el propio equipo, conseguir una automatización funcional equivalente mediante el enfoque tradicional con un proveedor normalmente habría requerido varias semanas. Y lo mejor de todo es que esas pruebas también indican que se podrían hacer tres veces más rápido de lo que se podían haber hecho manualmente. Aquí conviene no transformar el dato en algo que no es. Esto no significa que cualquier vaya a pasar de necesitar tres meses para integrar algo a horas. Realmente estamos hablando de un experimento concreto, en una situación determinada, con unas máquinas en concreto y los datos aparecen dentro de la propia presentación del proyecto. Pero el ejemplo sirve para el problema que quieren atacar. Cuando conectamos sistemas distintos, una parte enorme del trabajo consiste simplemente en conseguir que A pueda hablar con B, después que B pueda hablar con C y

### [12:53](https://www.youtube.com/watch?v=3hxdHem70gw&t=773s)

después que C entienda lo que devuelve A. Son pequeñas piezas de software que muchas veces se conocen como código pegamento porque literalmente sirven para pegar unos sistemas con otros. MHS lo que va a intentar es crear cierta estructura común para reducir parte de ese caos. Y hay otro experimento que me parece incluso más interesante porque enseña algo diferente. Durante las pruebas pusieron a Claude a trabajar con un sistema óptico. El agente podía cambiar la posición de un láser. Después observaba mediante una cámara qué había ocurrido con el haz y realizaba otro ajuste. Volvía a mirar y continuaba.

### [13:25](https://www.youtube.com/watch?v=3hxdHem70gw&t=805s)

Pensad en cómo ajustaríais vosotros un cuadro que está torcido. Lo movéis un poco, os alejáis, lo miráis, si sigue torcido lo corregís y volvéis a mirar. En sí no tenéis desde el principio una fórmula matemática perfecta que os dice exactamente cuántos milímetros hay que moverlo. Probáis, observáis el resultado y corregís. Pues el agente estaba haciendo algo parecido. Observaba, hacía un cambio, comprobaba qué había ocurrido, corregía y volvía a probar. Pero lo más interesante llegó después. Una vez que Claude encontró una manera de realizar el procedimiento, convirtió lo aprendido en un código. Lo que hizo es generar un script determinista capaz de realizar la alineación sin necesitar que el modelo estuviera pensando continuamente durante cada paso. Y esta diferencia me parece algo fundamental para entender cómo podría encajar la inteligencia artificial en máquinas reales. Cuando imaginamos esta IA controlando un robot o una máquina, eh

### [14:14](https://www.youtube.com/watch?v=3hxdHem70gw&t=854s)

probablemente se nos viene a la cabeza a ChatGPT decidiendo cada milisegundo hacia dónde tiene que tirar, moviendo por ejemplo el motor hacia una dirección u otra. Pero realmente no tiene por qué funcionar así. La inteligencia artificial puede estar en una capa superior. Puede probar, puede analizar resultados, buscar buenos parámetros, desarrollar un procedimiento. Y cuando encuentra una solución, esa solución puede convertirse en código tradicional. Código que siempre sigue las mismas reglas. A eso nos referimos cuando hablamos de código determinista. Si ocurre A, haces B. Si el sensor supera este valor, haces C.

### [14:48](https://www.youtube.com/watch?v=3hxdHem70gw&t=888s)

No hay un modelo que esté improvisando una respuesta nueva cada vez. Esto se ve todavía más claro en otro experimento. Lo realizó QuEra Computing. QuEra desarrolla ordenadores cuánticos basados en átomos neutros. Dentro de sus sistemas trabajan con láseres cuya frecuencia tiene que mantenerse extremadamente estable. Para alguien que no venga de este mundo, podéis imaginarlo como intentar mantener constantemente una radio exactamente sintonizada en la misma frecuencia. Si os desviáis demasiado, perderéis la señal. En el caso de estos láseres, cuando el sistema se desvía, puede perder lo que llaman el clock. Y recuperar ese estado requiere volver a ajustar diferentes partes del sistema.

### [15:24](https://www.youtube.com/watch?v=3hxdHem70gw&t=924s)

Según QuEra, cuando esto ocurría, una persona experta podía tardar entre 5 y 10 minutos en recuperarlo. Y ya habían intentado automatizarlo antes. Un equipo de ingenieros había trabajado durante meses desarrollando un script específico. Y eso que hicieron conseguía recuperar el láser aproximadamente un 58% de las veces y tardaba unos 150 segundos por intento. Así que le plantearon el problema a Claude mediante MHS. Pero de nuevo vuelvo otra vez al papel No querían dejar a Claude permanentemente al mando del láser. Querían que Claude desarrollase un programa capaz de resolver el problema, nada más. Durante las pruebas provocaban diferentes perturbaciones. El agente hacía cambios, ejecutaba el script, comprobaba qué había ocurrido y modificaba el código. Ese ciclo se repitió cientos de veces durante esa noche. Al terminar, el resultado era un

### [16:11](https://www.youtube.com/watch?v=3hxdHem70gw&t=971s)

programa normal, un programa determinista. Después probaron ese programa por separado y provocaron 700 perturbaciones. Pues esto que hizo consiguió recuperar correctamente el clock en 695. Eso supone un 99,3% de éxito. Y en los casos más complicados tardaba aproximadamente entre 10 y 14 segundos frente a los varios minutos que podía necesitar un operador humano. Pero el dato más interesante para mí no es solo ese 99,3%, es donde queda la inteligencia artificial, ya que Claude no está controlando cada microsegundo del láser. Claude lo que ha participado es en el desarrollo del controlador. Lo que hizo fue probar, corregir, actuar y generó código. Y finalmente lo que queda trabajando sobre la máquina, al fin y al cabo, pues es un programa convencional.

### [16:52](https://www.youtube.com/watch?v=3hxdHem70gw&t=1012s)

Se explica también que ese controlador queda desde una capa totalmente superior. El control extremadamente rápido del láser, al fin y al cabo, sigue funcionando por debajo. Y esta arquitectura empieza a tener muchísimo más sentido cuando pensamos en máquinas industriales. Imagínate un coche. El sistema que controla los frenos tiene que reaccionar en tiempos extremadamente pequeños. No queremos enviar una pregunta a un modelo de lenguaje cada vez que necesitamos aumentar ligeramente la presión de frenado. Hay funciones que necesitan ser rápidas, predecibles y estar muy controladas. Estas funciones pueden seguir existiendo exactamente donde están. La IA, en cambio, puede trabajar en otro nivel, analizando, supervisando, buscando ajustes, planificando o incluso desarrollando nuevos procedimientos. Esta separación también desmonta una idea que aparece muchas veces cuando hablamos de IA y automatización. No hace falta sustituir

### [17:40](https://www.youtube.com/watch?v=3hxdHem70gw&t=1060s)

un PLC por un modelo de lenguaje. Un PLC puede seguir encargándose de controlar una máquina. Un variador puede seguir controlando un motor. MHS intenta actuar en otra capa, una capa donde un agente puede comprender qué dispositivos existen y qué posibilidades tiene cada uno. Pero cuando dejamos que la inteligencia artificial se incluya dentro del hardware, aparece aquí un problema bastante grave y es la seguridad, ya que hay una diferencia bastante grande en que ChatGPT se equivoque dándote una respuesta por un chat o incluso escribiendo un código mal que al fin y al cabo va a hacer que una aplicación se caiga, a que la inteligencia artificial se equivoque con controlando una máquina que pesa toneladas, donde, pues, muchas veces hay vidas en juego y personas trabajando alrededor de ella. En el mundo físico, los errores tienen consecuencias físicas y eso es muy importante. Por eso, MHS

### [18:27](https://www.youtube.com/watch?v=3hxdHem70gw&t=1107s)

contempla la posibilidad de declarar límites e interlocks. Un interlock es, básicamente, una protección. Imagínate una lavadora. Mientras está funcionando, la puerta queda bloqueada. No confiamos en que el usuario recuerde que no debería abrirla. La propia máquina impide hacerlo. Eso es una forma sencilla de entender un interlock. En maquinaria ocurre algo parecido. Podemos crear reglas que, físicamente o desde el sistema, impidan ciertas operaciones. La idea es que la seguridad no dependa únicamente de que la inteligencia artificial recuerde una instrucción escrita en algún sitio. Puede haber límites extremos que directamente no le permitan ejecutar determinadas acciones.

### [19:02](https://www.youtube.com/watch?v=3hxdHem70gw&t=1142s)

Pero incluso poniendo límites, tenemos un problema bastante profundo. Los modelos actuales pueden saber muchísimo de cómo funciona el mundo físico sin realmente comprenderlo, al menos como lo hace una persona como tú o yo. Ya hay otro experimento que lo muestra bastante bien. Estaban trabajando con Claude y MHS para automatizar un procedimiento de laboratorio en el que tenían que manipular líquidos. Algunas muestras eran viscosas. Pensad en la diferencia entre mover agua y mover miel. Los dos son líquidos, pero físicamente no se comportan igual. Las muestras viscosas podrían generar espuma y burbujas. Y una pequeña burbuja, que para nosotros puede parecer insignificante, puede estropear una medición. Una pipeta puede creer que ha aspirado una determinada cantidad de líquido cuando una parte de lo que ha aspirado era aire. Un sensor puede interpretar mal el nivel.

### [19:48](https://www.youtube.com/watch?v=3hxdHem70gw&t=1188s)

Y todo eso puede acabar afectando al experimento. Claude comenzó trabajando con parámetros bastante genéricos. Esos parámetros provocaron problemas de burbujas en algunas muestras viscosas. Y ahí apareció una limitación bastante interesante. El modelo sabía trabajar con el software. Sabía interpretar datos. Podía manejar las herramientas. Pero faltaba parte de ese conocimiento físico que tiene una persona que lleva años haciendo el mismo procedimiento. Porque hay una diferencia entre saber en teoría que un líquido puede generar burbujas y haber pipeteado miles de muestras hasta desarrollar una intuición sobre cómo se comportan. Anthropic usa precisamente ese caso para reconocer que los modelos actuales todavía tienen limitaciones cuando hablamos de razonamiento físico. Y creo que este ejemplo ayuda muchísimo a colocar a MHS en su sitio. Una inteligencia artificial

### [20:36](https://www.youtube.com/watch?v=3hxdHem70gw&t=1236s)

puede leer millones de documentos sobre motores, bombas, robots, láseres, máquinas hidráulicas. Pero leer sobre una máquina durante años y trabajar con esa máquina durante, yo que sé, 15 años, pues realmente no es lo mismo. Un técnico, por ejemplo, puede simplemente con el sonido que hace un motor saber si ese motor está fallando. Puede incluso tocar una carcasa y detectar, pues que hay una vibración extraña. Y todo ese conocimiento es muy difícil dejarlo enmarcado y plasmado en un documento. Por eso Anthropic sigue hablando de supervisión experta. MHS todavía está en una fase experimental. De hecho, lo sacaron en agosto. Este vídeo no lo estoy sacando para nada cuando lanzaron este documento, todavía han pasado meses y no se ha dicho nada. Al menos de momento no estamos en el punto de instalar una inteligencia artificial en una máquina industrial y dejarla sola,

### [21:23](https://www.youtube.com/watch?v=3hxdHem70gw&t=1283s)

ni de broma. Que no quiere decir que no pueda salir algún cambio imprevisto que pues cambie todo y al final pues se pueda adaptar mucho más fácil y esta inteligencia artificial se adapte al hardware como ya lo hace a través del software. Hay también otra limitación bastante sencilla de entender. MHS necesita alguna puerta digital por la que entrar. Imaginad una máquina industrial fabricada hace 40 años. Tiene botones, palancas, motores, relés, pero no tiene ordenador, no tiene conexión de red, ni software que podamos controlar, ni ninguna interfaz digital.

### [21:55](https://www.youtube.com/watch?v=3hxdHem70gw&t=1315s)

MHS no puede aparecer mágicamente y empezar a controlarla. Primero necesitaríamos alguna manera de conectar esa máquina con el mundo digital. Quizá añadiendo sensores, instalando un controlador, conectándola a otro sistema, pero tiene que existir algún cambio. En equipos más modernos ese camino puede ser una API, un SDK, un protocolo industrial, un programa, incluso una interfaz gráfica. Lo que ya te he comentado antes. Anthropic reconoce que una de las líneas de trabajo está precisamente en poder trabajar con una mayor variedad de equipos que no tienen buenas interfaces programables. Y todo esto lleva a la parte que más me interesa ya que tiene esa relación con el IoT y como sabéis pues este canal es de IoT, hablamos de ello. Porque MHS toca una pregunta que se lleva haciendo durante años en el internet de las cosas. ¿Cómo hacemos que miles de dispositivos diferentes puedan convivir en el mismo sistema? Pensad en

### [22:43](https://www.youtube.com/watch?v=3hxdHem70gw&t=1363s)

una casa inteligente. Tenemos bombillas, termostatos, sensores de presencia, persianas, etc. Cada fabricante puede tener su aplicación, su nube, su manera de enviar órdenes. Y cualquiera que haya intentado montar un sistema domótico mezclando muchas marcas sabe que esto puede convertirse rápidamente en un pequeño caos. Ahora llevad ese problema a una fábrica. En vez de 10 dispositivos, podemos tener cientos o miles. Y en vez de bombillas, tenemos robots, bombas, motores, sensores, PLCs. Es el tipo de ecosistema donde una capa común empieza a tener sentido. Por ahora, muchos experimentos en MHS están relacionados con ciencia, biología, microscopía, ordenadores cuánticos, robótica, pero ya empiezan a aparecer señales en otras direcciones. Hugging Face está trabajando para añadir soporte de MHS dentro de LeRobot, su ecosistema

### [23:31](https://www.youtube.com/watch?v=3hxdHem70gw&t=1411s)

de robótica. Raspberry Pi también está trabajando en integraciones después de realizar pruebas con un driver para sus cámaras. Y aquí es donde podemos imaginar hacia dónde podría ir algo así. Tenemos una Raspberry Pi, una cámara, un brazo robótico, varios sensores. Cada dispositivo sigue funcionando con su propia tecnología. El sensor puede comunicarse mediante un protocolo. Y la cámara tiene su librería. También el robot tiene su API. Pero todos pueden exponer hacia arriba una descripción que un agente sea capaz de interpretar. Entonces, será cuando el agente pueda descubrir, "Oye, mira, tengo una cámara. La cámara puede capturar imágenes. Tengo un sensor de temperatura. Y ahora mismo mide 28 grados. También tengo un brazo robótico.

### [24:11](https://www.youtube.com/watch?v=3hxdHem70gw&t=1451s)

Puede recoger este objeto. Pero no puede entrar en esta zona, ya que tengo una máquina que solamente puede arrancar cuando esta puerta esté cerrada." A partir de ahí, empieza a ser posible coordinar dispositivos diferentes. Por ejemplo, la cámara detecta que ha llegado una pieza. El agente consulta el estado de la máquina. Comprueba que está preparada. Coordina el robot que mueve la pieza y la máquina realiza su proceso. Un sensor va a comprobar el resultado y el agente, al final, decide cuál es el siguiente paso. Esto es solo una forma sencilla de imaginarnos la idea. No significa que MHS pueda ya instalarse en cualquier línea de producción para hacer exactamente esto, pero nos ayuda a entender qué tipo de problemas se intenta resolver. Quiere que una inteligencia artificial pueda mirar un conjunto de equipos y tener una especie de mapa de capacidades. Eso empieza a parecerse bastante a añadir una capa de inteligencia sobre un sistema IoT, pero

### [24:58](https://www.youtube.com/watch?v=3hxdHem70gw&t=1498s)

tampoco significa que vayamos a sustituir todo lo que ya existe. Los PLC no desaparecen, OPC UA tampoco, Modbus tampoco, ni mucho menos los sistemas de control en tiempo real. Una buena analogía que podríamos hacer es la de un jefe de cocina. Un jefe de cocina coordina lo que sucede dentro de un restaurante, decide qué plato hay que preparar, comprueba si falta algo, organiza tareas, pero claramente no sustituye físicamente a un horno, ni al frigorífico, ni al cuchillo, ni tampoco a la persona que está cocinando. Una capa de agentes podría jugar un papel parecido a esto, coordinar sistemas que ya existen. Los controladores que son rápidos y sobre todo deterministas siguen trabajando en la parte de abajo y el agente trabaja a otro nivel. Lo que está haciendo es coordinar, supervisar en una capa mucho más arriba. Por lo tanto, podrá analizar resultados, configurar operaciones, modificar algunos parámetros cuando tenga sentido

### [25:46](https://www.youtube.com/watch?v=3hxdHem70gw&t=1546s)

hacerlo. Probablemente, y esto ya es mi punto de vista, la inteligencia artificial aplicada al mundo físico pasará no tanto por quitar toda la tecnología que tenemos y hacer algo de cero, sino en que la IA entienda mucho mejor las capas que ya tenemos disponibles. Y luego aparece la gran incógnita. Realmente MHS va a poder convertirse en un estándar. Pues bueno, esto realmente no lo sabemos. Hay una dificultad muy muy muy grande para que todos los fabricantes de robots, cámaras, sensores, equipos industriales lleguen a un consenso de que hay que aplicar ese estándar. De hecho, pensad en algo tan conocido como un USB, algo que seguramente todos conocéis. A día de hoy estamos conectando por USB dispositivos casi sin pensarlo, pero esta tecnología solo es útil porque miles de fabricantes decidieron que

### [26:34](https://www.youtube.com/watch?v=3hxdHem70gw&t=1594s)

había que aplicarla. Se convirtió en un estándar, siguieron todos las mismas reglas. Pues con MHS tendría que ocurrir algo parecido, pero a otro nivel, no necesariamente con conectores físicos, sino de la forma de exponer y describir las funcionalidades que tiene un hardware. Por lo tanto, empresas de automatización, fabricantes, compañías de robótica, laboratorios, todos estos tendrían que implementarlo, pero sobre todo encontrar un valor lo suficientemente grande como para realmente llevarlo a cabo. Y como digo, estamos en una fase muy inicial, todo es experimental. Anthropic está trabajando en ello con esos primeros clientes, primeros, bueno, voluntarios que se ofrecen para poner toda esta tecnología en marcha y ver, como digo, como siempre, ¿no? Detectar los problemas que van surgiendo, corregirlos, qué nivel de seguridad tienen que implementar para que esto no colapse, etcétera. Así que

### [27:21](https://www.youtube.com/watch?v=3hxdHem70gw&t=1641s)

obviamente a día de hoy no diría que este es el estándar oficial para integrar inteligencia artificial y hardware, quizá al final nunca sale, quizá sale otro mejor, no lo sabemos, pero por todo lo que estoy leyendo y cómo avanza en general la inteligencia artificial, tiene bastante sentido que esto acabe sucediendo, al menos a medio corto plazo. Lo que sí me parece bastante interesante es el problema que está intentando resolver, porque si miramos cómo ha evolucionado la inteligencia artificial durante los últimos años, se ve una progresión bastante clara. Primero teníamos modelos que solamente podían hablar.

### [27:52](https://www.youtube.com/watch?v=3hxdHem70gw&t=1672s)

Les preguntabas algo y respondían. Después aprendieron a trabajar con herramientas, buscar información, ejecutar código, consultar bases de datos, manejar aplicaciones. Y con los agentes estamos empezando a pasar de una inteligencia artificial que simplemente responde a una inteligencia artificial que también puede hacer cosas. El siguiente paso parece bastante lógico, pasar del mundo digital al mundo físico, sensores, cámaras, robots, máquinas. El problema es que el mundo físico es muchísimo más desordenado. No existe una única API para todas las máquinas del planeta y un largo etcétera de problemas. Así que quizás antes de pensar en robots humanoides controlados con inteligencia artificial, tenemos que solucionar algo bastante menos ¿Cómo le explicamos a una IA qué es una máquina, lo que puede hacer y qué límites tiene? Y eso en esencia es lo que pretende Model Hardware Standard.

### [28:40](https://www.youtube.com/watch?v=3hxdHem70gw&t=1720s)

Después tendremos que ver si la industria al final decide adoptarlo. Puede que MHS consiga ser una pieza muy relevante en todo este sistema, o puede que no, pero al menos la pregunta que plantea me resulta bastante interesante. Si dentro de unos años queremos que la inteligencia artificial actúe con miles de máquinas que son diferentes entre sí, ¿cómo va a saber qué puede hacer cada una? Porque quizá una de las piezas más importantes para adoptar la inteligencia artificial con el hardware nuevo pasa por ponerlo dentro de un robot que sea completamente autónomo y quizá pase por ser algo mucho menos llamativo que eso.

### [29:12](https://www.youtube.com/watch?v=3hxdHem70gw&t=1752s)

Te dejo por aquí otro vídeo de inteligencia artificial relacionado con el mundo físico que probablemente te interese. Así que nos vemos por ahí. Hasta el siguiente vídeo.
