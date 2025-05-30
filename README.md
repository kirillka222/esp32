# Kirill Dolda ESP32 Project

## Описание
Проект моделирует виртуальный дрон, отправляющий координаты через WebSocket, визуализируя данные в окне PyGame.

## Структура
- sender.py — имитирует ESP32, отправляет координаты
- receiver.py — ретрансляция сообщений между sender и visualizer
- visualizer.py — визуализатор положения дрона

## Запуск
1. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
2. В терминале запустите receiver:
   ```bash
   python receiver.py
   ```
3. Во втором терминале запустите sender:
   ```bash
   python sender.py
   ```
4. В третьем — визуализатор:
   ```bash
   python visualizer.py
   ```

   ## Запуск через онлайн-эмулятор
   Для запуска main.py и diagram.json из папки wokwi, необходимо вставить код на платформе https://wokwi.com/
