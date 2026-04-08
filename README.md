<div align="center">

# 🔥 Pyromodify

**Elegant, Modern & Asynchronous Telegram MTProto API Framework**

*A powerful fork of Pyrogram with built-in conversation handling, Pyromod-style flows, and modern Telegram Bot API support.*

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![PyPI](https://img.shields.io/pypi/v/pyromodify?style=for-the-badge&logo=pypi&logoColor=white&color=blue)](https://pypi.org/project/pyromodify/)
[![License](https://img.shields.io/badge/License-LGPL--3.0-green?style=for-the-badge)](COPYING.lesser)
[![Telegram](https://img.shields.io/badge/Community-Telegram-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/SnowballAI)

---

<p>
  <a href="#-features">Features</a> •
  <a href="#-installation">Installation</a> •
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-conversation-flow">Conversations</a> •
  <a href="#-handler-reference">Handlers</a> •
  <a href="#-project-structure">Structure</a> •
  <a href="#-license">License</a>
</p>

</div>

---

## ✨ Features

<table>
  <tr>
    <td align="center" width="25%">
      <br>⚡<br><b>Async-First</b><br>
      <sub>Fully asynchronous architecture built on <code>asyncio</code> for high‑performance I/O</sub>
    </td>
    <td align="center" width="25%">
      <br>💬<br><b>Conversation Flow</b><br>
      <sub>Built‑in Pyromod‑style <code>ask()</code>, <code>listen()</code>, and step handlers for interactive dialogs</sub>
    </td>
    <td align="center" width="25%">
      <br>🤖<br><b>Dual Mode</b><br>
      <sub>Seamlessly works with both <b>user accounts</b> and <b>bot accounts</b> via MTProto</sub>
    </td>
    <td align="center" width="25%">
      <br>🛡️<br><b>Type‑Safe</b><br>
      <sub>Comprehensive type hints across all core modules for IDE autocomplete & safety</sub>
    </td>
  </tr>
  <tr>
    <td align="center" width="25%">
      <br>🎯<br><b>20+ Handlers</b><br>
      <sub>Message, callback, inline, reaction, story, poll, payment, and more event handlers</sub>
    </td>
    <td align="center" width="25%">
      <br>📦<br><b>Rich Types</b><br>
      <sub>Full coverage of Telegram types — messages, media, keyboards, business, stories</sub>
    </td>
    <td align="center" width="25%">
      <br>🔐<br><b>Crypto Layer</b><br>
      <sub>Built‑in encryption with optional <code>PyTgCrypto</code> and <code>uvloop</code> acceleration</sub>
    </td>
    <td align="center" width="25%">
      <br>📝<br><b>Sphinx Docs</b><br>
      <sub>Auto-generated API reference with Sphinx, Furo theme, and copy‑button support</sub>
    </td>
  </tr>
</table>

---

## 📦 Installation

### Stable Release

```bash
pip install pyromodify
```

### Development Version

```bash
pip install git+https://github.com/Snowball-01/Pyromodify.git
```

### With Performance Extras

```bash
pip install "pyromodify[fast]"
```

> **Note:** The `fast` extra installs [`PyTgCrypto`](https://github.com/pyrogram/tgcrypto) for accelerated crypto operations and [`uvloop`](https://github.com/MagicStack/uvloop) for a faster event loop (Linux/macOS only).

---

## 🚀 Quick Start

### Bot Example

```python
from pyrogram import Client, filters

app = Client(
    "my_bot",
    api_id=123456,
    api_hash="your_api_hash",
    bot_token="123456:ABCDEF"
)


@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await message.reply(
        "👋 **Hello!** Welcome to my bot.\n"
        "Powered by **Pyromodify**."
    )


app.run()
```

### Userbot Example

```python
from pyrogram import Client, filters

app = Client(
    "my_account",
    api_id=123456,
    api_hash="your_api_hash"
)


@app.on_message(filters.me & filters.command("ping", prefixes="."))
async def ping(client, message):
    await message.edit_text("🏓 **Pong!**")


app.run()
```

---

## 💬 Conversation Flow

One of Pyromodify's standout features is its built‑in conversation support — no extra plugins required.

### `ask()` — Prompt and Wait

```python
@app.on_message(filters.command("survey"))
async def survey(client, message):
    # Ask a question and wait for the user's response
    response = await message.chat.ask("What is your name?")
    name = response.text

    response = await message.chat.ask(f"Nice to meet you, {name}! How old are you?")
    age = response.text

    await message.reply(f"✅ Got it! **{name}**, age **{age}**.")
```

### `listen()` — Wait for Any Update

```python
@app.on_message(filters.command("wait"))
async def wait_example(client, message):
    await message.reply("Send me a photo within 30 seconds!")

    response = await client.listen(
        chat_id=message.chat.id,
        filters=filters.photo,
        timeout=30
    )
    await response.reply("📸 Photo received!")
```

### `wait_for_callback_query()` — Inline Button Response

```python
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

@app.on_message(filters.command("choose"))
async def choose(client, message):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Option A", callback_data="a"),
         InlineKeyboardButton("Option B", callback_data="b")]
    ])
    await message.reply("Pick one:", reply_markup=keyboard)

    cb = await client.wait_for_callback_query(message.chat.id)
    await cb.answer(f"You picked: {cb.data.upper()}", show_alert=True)
```

### `register_next_step_handler()` — Step‑Based Flows

```python
@app.on_message(filters.command("multistep"))
async def step_one(client, message):
    await message.reply("Step 1: Send your email address.")
    client.register_next_step_handler(message, step_two)

async def step_two(client, message):
    email = message.text
    await message.reply(f"Got **{email}**. Now send your phone number.")
    client.register_next_step_handler(message, step_three)

async def step_three(client, message):
    phone = message.text
    await message.reply(f"✅ Registration complete! Phone: **{phone}**")
```

---

## 🎛️ Handler Reference

Pyromodify ships with **20+ event handlers** covering every Telegram update type:

| Handler | Decorator | Description |
|:--------|:----------|:------------|
| `MessageHandler` | `@on_message` | New incoming/outgoing messages |
| `EditedMessageHandler` | `@on_edited_message` | Edited messages |
| `DeletedMessagesHandler` | `@on_deleted_messages` | Deleted messages |
| `CallbackQueryHandler` | `@on_callback_query` | Inline button presses |
| `InlineQueryHandler` | `@on_inline_query` | Inline mode queries |
| `ChosenInlineResultHandler` | `@on_chosen_inline_result` | Chosen inline results |
| `ChatMemberUpdatedHandler` | `@on_chat_member_updated` | Chat member status changes |
| `ChatJoinRequestHandler` | `@on_chat_join_request` | Join requests |
| `MessageReactionUpdatedHandler` | `@on_message_reaction_updated` | Message reactions |
| `MessageReactionCountUpdatedHandler` | `@on_message_reaction_count_updated` | Reaction count changes |
| `StoryHandler` | `@on_story` | Stories |
| `PollHandler` | `@on_poll` | Poll updates |
| `UserStatusHandler` | `@on_user_status` | Online/offline status |
| `ConversationHandler` | — | Pyromod conversation flow |
| `PreCheckoutQueryHandler` | `@on_pre_checkout_query` | Pre-checkout payment queries |
| `ShippingQueryHandler` | `@on_shipping_query` | Shipping queries |
| `PurchasedPaidMediaHandler` | `@on_bot_purchased_paid_media` | Purchased paid media |
| `BusinessBotConnectionHandler` | `@on_bot_business_connection` | Business bot connections |
| `RawUpdateHandler` | `@on_raw_update` | Raw MTProto updates |
| `DisconnectHandler` | `@on_disconnect` | Client disconnect events |

---

## 🏗️ Project Structure

```
Pyromodify/
├── pyrogram/                    # Core library
│   ├── client.py                # Main Client class
│   ├── dispatcher.py            # Update dispatcher engine
│   ├── filters.py               # Message & update filters
│   ├── sync.py                  # idle() & compose() utilities
│   ├── utils.py                 # Internal helpers
│   ├── file_id.py               # Telegram file ID parser
│   ├── handlers/                # 20+ event handlers
│   │   ├── message_handler.py
│   │   ├── callback_query_handler.py
│   │   ├── conversation_handler.py
│   │   └── ...
│   ├── methods/                 # Client API methods
│   │   ├── messages/            # Send, edit, delete messages
│   │   ├── chats/               # Chat management
│   │   ├── users/               # User info & actions
│   │   ├── bots/                # Bot-specific methods
│   │   ├── pyromod/             # ask(), listen(), step handlers
│   │   ├── decorators/          # @on_message, @on_callback, ...
│   │   ├── stickers/            # Sticker operations
│   │   ├── stories/             # Stories
│   │   ├── business/            # Business features
│   │   └── ...
│   ├── types/                   # Telegram type definitions
│   │   ├── messages_and_media/  # Message, Photo, Video, ...
│   │   ├── user_and_chats/      # User, Chat, ChatMember, ...
│   │   ├── bots_and_keyboards/  # InlineKeyboard, ReplyKeyboard
│   │   ├── inline_mode/         # InlineQuery, InlineResult
│   │   ├── pyromod/             # Listener, Identifier
│   │   └── ...
│   ├── enums/                   # Enumerations (ChatType, ParseMode, ...)
│   ├── errors/                  # Telegram error mapping
│   ├── connection/              # TCP/Transport layer
│   ├── session/                 # MTProto session management
│   ├── storage/                 # SQLite session storage
│   ├── crypto/                  # Encryption utilities
│   ├── parser/                  # HTML & Markdown parsers
│   └── raw/                     # Auto-generated TL schema bindings
├── compiler/                    # TL schema & docs compilers
│   ├── api/                     # API schema compiler
│   ├── errors/                  # Error code compiler
│   └── docs/                    # Documentation compiler
├── tests/                       # Test suite (pytest)
├── docs/                        # Sphinx documentation source
├── pyproject.toml               # Project metadata & build config
├── hatch_build.py               # Custom Hatch build hook
├── Makefile                     # Development shortcuts
├── COPYING                      # GPL-3.0 license
├── COPYING.lesser               # LGPL-3.0 license
└── NOTICE                       # Attribution notice
```

---

## ⚙️ Requirements

| Requirement | Details |
|:------------|:--------|
| **Python** | `>= 3.9` (CPython or PyPy) |
| **API Credentials** | `api_id` + `api_hash` from [my.telegram.org](https://my.telegram.org) |
| **Bot Token** | From [@BotFather](https://t.me/BotFather) *(for bot mode only)* |

### Core Dependencies

| Package | Purpose |
|:--------|:--------|
| `pyaes` | AES encryption (<=1.6.1) |
| `pysocks` | SOCKS proxy support (<=1.7.1) |

### Optional Extras

```bash
# Speed boost (PyTgCrypto + uvloop)
pip install "pyromodify[fast]"

# Documentation generation
pip install "pyromodify[docs]"

# Development tools (pytest, hatch, twine)
pip install "pyromodify[dev]"
```

---

## 📖 Documentation

Full API documentation is built with [Sphinx](https://www.sphinx-doc.org/) using the [Furo](https://pradyunsg.me/furo/) theme.

### Build Locally

```bash
# Create virtual environment & install deps
make venv

# Generate API reference + build HTML docs
make docs

# Live-reload mode for development
make docs-live
```

The generated docs will be available at `docs/build/html/index.html`.

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

```bash
# Clone the repository
git clone https://github.com/Snowball-01/Pyromodify.git
cd Pyromodify

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest
```

---

## 📄 License

Pyromodify is licensed under the **GNU Lesser General Public License v3.0 (LGPL-3.0)**.

This means you can:
- ✅ Use it in proprietary projects
- ✅ Modify and distribute it
- ⚠️ Changes to the library itself must remain open-source

See [`COPYING`](COPYING) and [`COPYING.lesser`](COPYING.lesser) for full terms.

---

## 🔗 Links

<div align="center">

[![GitHub](https://img.shields.io/badge/Source_Code-GitHub-181717?style=for-the-badge&logo=github)](https://github.com/Snowball-01/Pyromodify)
[![Issues](https://img.shields.io/badge/Bug_Reports-Issues-red?style=for-the-badge&logo=github)](https://github.com/Snowball-01/Pyromodify/issues)
[![Telegram](https://img.shields.io/badge/Community-Telegram-26A5E4?style=for-the-badge&logo=telegram)](https://t.me/SnowballAI)
[![PyPI](https://img.shields.io/badge/Package-PyPI-3775A9?style=for-the-badge&logo=pypi&logoColor=white)](https://pypi.org/project/pyromodify/)

</div>

---

<div align="center">

**Made with ❤️ by the [Snowball-01](https://github.com/Snowball-01) team**

*If you find Pyromodify useful, consider giving it a ⭐ on GitHub!*

</div>
