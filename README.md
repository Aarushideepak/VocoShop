# KiranaVoice – AI-Powered Voice Assistant for Kirana Stores

KiranaVoice is a voice-based inventory and order management assistant designed for small retail shops in India.

It allows shopkeepers to interact with their inventory using natural voice commands instead of manually entering data.

## Features

- Voice input using Gnani Prisma Speech-to-Text.
- Voice responses using Gnani Timbre Text-to-Speech.
- Supports Kannada and English commands.
- Check product availability and prices.
- Add and reduce inventory stock.
- Process customer purchases with confirmation.
- Maintain order history.
- Cancel orders and restore inventory.
- Track daily sales.
- Identify low-stock products.
- Store inventory, orders, and sales using SQLite.

## Technology Stack

- Python
- SQLite
- Gnani Prisma STT
- Gnani Timbre TTS
- SoundDevice
- SoundFile
- Python-dotenv

## Project Structure

- `main.py` – Application configuration and API key loading.
- `voice_assistant.py` – Voice input and speech recognition.
- `assistant.py` – Command processing and business logic.
- `speech.py` – Text-to-speech generation and audio playback.
- `inventory.py` – Inventory management.
- `orders.py` – Order creation, history, and cancellation.
- `sales.py` – Sales recording and daily sales calculations.
- `kirana.db` – SQLite database.
- `.env` – Environment configuration and API key.

## Setup and Installation

1. Install Python and VS Code.
2. Clone or download this project.
3. Open the project folder in VS Code.
4. Create and activate a virtual environment.

```bash
python -m venv venv
venv\Scripts\activate
```

5. Install dependencies.

```bash
pip install -r requirements.txt
```

6. Add your Gnani API key to the `.env` file.

```env
GNANI_API_KEY=your_api_key_here
```

7. Start the voice assistant.

```bash
python voice_assistant.py
```

## How It Works

1. The shopkeeper speaks a command.
2. Gnani Prisma converts speech into text.
3. The application identifies the requested operation.
4. Python processes the command and updates the SQLite database when required.
5. Gnani Timbre generates a spoken response.

## Example Commands

- Check rice stock.
- Add two kg rice.
- Sell three kg rice.
- Show orders.
- Cancel order four.
- Check low stock.
- Show daily sales.

## Purpose

KiranaVoice aims to make inventory and order management simpler and more accessible for small shopkeepers through natural voice interaction.
