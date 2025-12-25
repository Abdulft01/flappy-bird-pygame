# Flappy Bird – Pygame

A Flappy Bird–style 2D game built **from scratch** using Python and Pygame.  
The project was developed incrementally to understand **game loops, physics, collision detection, object-oriented design and asset management**.

> This is a **non-commercial, educational clone** inspired by Flappy Bird.

---

## 🎮 Features
- Physics-based bird movement (gravity & jump)
- Procedurally generated pipes
- Collision detection and game state handling
- Score tracking with increasing difficulty
- Persistent high score stored locally
- Sound effects and background music
- Clean **OOP architecture** (Bird, Pipe, Game classes)
- EXE-ready build using PyInstaller

---

## 🧠 Project Structure
- `Bird` class → handles player movement and physics  
- `Pipe` class → handles obstacle generation, movement, and collisions  
- `Game` class → manages game loop, state, input, rendering and scoring  

The project was refactored step by step from a procedural script into a structured OOP design.

---

## 🕹 Controls
- **SPACE** → Jump  
- **R** → Restart after Game Over  
- **Close window** → Exit game  

---

## 🛠 Tech Stack
- **Python**
- **Pygame**
- **PyInstaller** (for Windows executable)

---

## ▶ How to Run (Source Code)

```bash
pip install pygame
python main.py
