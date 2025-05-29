# 🛒 telegram_bot_shop_tracker

A Telegram bot to manage shopping lists categorized by stores. Supports adding, deleting, and viewing items using convenient inline keyboards.

---

## 🚀 Features

- Store selection
- Add and remove items
- View current list
- FSM navigation between input stages
- Can be used by a small group to collaboratively manage shared shopping lists
- **Note:** Currently uses a JSON file as a temporary database. This means it is suitable for small-scale or shared group use only.  
  **Planned:** Migration to a real database (e.g., SQLite) to support full multi-user functionality.

---

## 🛠 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/telegram-shop-tracker.git
   cd telegram-shop-tracker

2. Install dependencies:
    pip install -r requirements.txt

3. Create a .env file in the root directory and add your bot token:
    BOT_TOKEN=your_bot_token_here

4. Run the bot:
    python main.py

## License

This project is licensed under the MIT License.

