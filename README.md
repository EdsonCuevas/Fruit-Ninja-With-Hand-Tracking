<div align="center">

# 🍉 Fruit Ninja con Seguimiento de Mano

Cutting fruits con tu dedo índice y cámara web. Evita bombas, suma puntos y corre contra el reloj.

<img src="docs/demo/demo.gif" alt="Demostración en GIF" width="640" />

<br/>

![Python](https://img.shields.io/badge/Python-3.9–3.11-blue) ![Plataformas](https://img.shields.io/badge/OS-Windows%20%7C%20macOS%20%7C%20Linux-informational) ![Cámara](https://img.shields.io/badge/Requiere-C%C3%A1mara%20Web-orange)

</div>

## 👥 Integrantes
- [Edson Leonardo Felix Cuevas](https://github.com/EdsonCuevas)
- [Alfredo Elizaldi Romero](https://github.com/elizaldi14)
- [Gustavo Ceja Ayala](https://github.com/Gusceja12)
- [Adrian Lopez Flores](https://github.com/FREENKILLA)
- [Gabriel Valencia Barrios](https://github.com/Gaboard)

---

## 📑 Tabla de contenidos
- ✨ Características
- 🧩 Tecnologías
- 📦 Requisitos
- 🚀 Instalación
- ▶️ Ejecución
- 🎮 Controles
- 🔧 Configuración rápida
- 🧪 Personalización
- 🖼️ Capturas y demo
- 🛠️ Troubleshooting
- ❓ FAQ
- 📈 Rendimiento
- 🗺️ Roadmap
- 🤝 Contribuir
- 📜 Licencia

---

## ✨ Características
- Seguimiento del dedo índice en tiempo real (Mediapipe + OpenCV).
- Mecánicas de corte y explosión con feedback visual inmediato.
- HUD con score, timer y vidas siempre visible.
- Pantallas de inicio, pausa y fin de juego.
- Assets listos para usar y fáciles de extender.

## 🧩 Tecnologías
- Pygame — renderizado y loop principal.
- OpenCV — captura de vídeo y preprocesamiento.
- Mediapipe — landmarks de mano, índice como cursor.

## 📦 Requisitos
- Python 3.9–3.11.
- Cámara web funcional.
- Windows, macOS o Linux.

## 📦 Dependencias de Python
Estas son las librerías utilizadas por el proyecto:

- `pygame` — motor de juego y audio.
- `opencv-python` — captura de vídeo y procesamiento de imágenes.
- `mediapipe` — detección de la mano y landmarks.

Instalación recomendada:

```bash
pip install "pygame>=2.1" "opencv-python>=4.7" "mediapipe==0.10.*"
```

Comprobación rápida:

```bash
python -c "import pygame, cv2, mediapipe as mp; print('OK')"
```

Notas de compatibilidad:
- `mediapipe` no soporta oficialmente Python 3.12; usa 3.9–3.11.
- Si la instalación falla, asegúrate de tener `pip` actualizado: `python -m pip install --upgrade pip`.

## 🚀 Instalación
1. Clona el repositorio.
2. Crea y activa un entorno virtual.
   - Windows:
     ```bash
     python -m venv venv
     .\venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
3. Actualiza `pip` e instala dependencias:
   ```bash
   python -m pip install --upgrade pip
   pip install pygame opencv-python mediapipe
   ```

## 📚 Instalación de librerías de Python
Con el entorno virtual activo, instala las librerías necesarias.

- Instalación rápida (todas juntas):
  ```bash
  pip install pygame opencv-python mediapipe
  ```

- Instalación por librería:
  ```bash
  pip install pygame
  pip install sys
  pip install opencv-python
  pip install mediapipe
  ```

- Verificar instalación:
  ```bash
  python -c "import pygame, cv2, mediapipe as mp; print('OK')"
  ```

Si encuentras errores con Mediapipe, asegúrate de usar Python 3.9–3.11 y tener actualizado `pip`.

## ▶️ Ejecución
```bash
python handtracking.py
```

## 🎮 Controles
| Acción | Tecla |
|-------|------|
| Comenzar | `ESPACIO` |
| Pausar/Continuar | `ESC` |
| Reiniciar | `R` |

## 🔧 Configuración rápida
- Resolución / FPS: `WIDTH, HEIGHT` y `FPS` en `handtracking.py:16–17`.
- Duración: `GAME_TIME` en `handtracking.py:18`.
- Vidas: `player_lives` en `handtracking.py:12`.
- Frutas: `fruits` en `handtracking.py:14` (requiere sprites en `images/`).

## 🧪 Personalización
- Añade nuevas frutas agregando su nombre en `fruits` y proveyendo:
  - `images/<fruta>.png` y `images/half_<fruta>.png`.
- Cambia la detección de mano ajustando:
  - `Hands(max_num_hands=1, min_detection_confidence=0.7)` en `handtracking.py:43`.
- Modifica velocidad y físicas en `generate_random_fruits()` `handtracking.py:77–88`.

## 🛠️ Troubleshooting
- La cámara no inicia: cierra apps que la usen (Zoom, Teams, etc.).
- Pantalla negra: verifica que `back.jpg` exista y que la cámara funciona.
- Error de Mediapipe: usa Python 3.9–3.11 (3.12 no soportado oficialmente).
- macOS: concede permisos de cámara en Preferencias del Sistema.

## ❓ FAQ
- ¿Puedo usar el mouse en vez de la mano? No, el juego usa el dedo índice como cursor (puedes extenderlo en código).
- ¿Cómo ajusto la sensibilidad? Modifica `min_detection_confidence` en `handtracking.py:43`.
- ¿Se puede jugar en pantalla completa? Cambia el modo de display en `pygame.display.set_mode()` `handtracking.py:22`.

## 📈 Rendimiento
- Reduce `FPS` `handtracking.py:17` si tu equipo es lento.
- Optimiza imágenes (PNG comprimidos, dimensiones acordes a `60x60`).
- Mantén `max_num_hands=1` para menor costo de cómputo.

## 🗺️ Roadmap
- [ ] Sonidos de corte y explosión.
- [ ] Dificultades y power-ups.
- [ ] Tabla de puntuaciones persistente.
- [ ] Soporte multihand / multiplayer local.

## 🤝 Contribuir
- Haz un fork y crea un branch descriptivo.
- Envía PRs pequeños con cambios claros.
- Incluye capturas si modificas UI/UX.

## 📜 Licencia
Por definir.