import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import time
import random
import threading

# Replace with your real token
TOKEN = "8275211887:AAEYI8754Zs8iA_h4ciCtpYz8vrpwrEQx5k"
ADMIN_ID = 7827532625  # Your admin ID
bot = telebot.TeleBot(TOKEN)

# Store user data and analytics
user_data = {}
analytics = {
    'total_users': 0,
    'commands_used': {},
    'button_clicks': {}
}

# Helper function to create beautiful buttons
def create_inline_keyboard(buttons, row_width=2):
    markup = InlineKeyboardMarkup(row_width=row_width)
    for button in buttons:
        if 'url' in button:
            markup.add(InlineKeyboardButton(button['text'], url=button['url']))
        else:
            markup.add(InlineKeyboardButton(button['text'], callback_data=button['callback_data']))
    return markup

def create_reply_keyboard(buttons, row_width=2, resize_keyboard=True):
    markup = ReplyKeyboardMarkup(row_width=row_width, resize_keyboard=resize_keyboard)
    for button_row in buttons:
        row_buttons = [KeyboardButton(button) for button in button_row]
        markup.add(*row_buttons)
    return markup

# Track user activity
def track_activity(user_id, command=None, button=None):
    if user_id not in user_data:
        user_data[user_id] = {
            'first_seen': time.time(),
            'commands_used': {},
            'last_active': time.time(),
            'points': 0  # Gamification: points for interactions
        }
        analytics['total_users'] += 1
    
    user_data[user_id]['last_active'] = time.time()
    
    if command:
        if command not in analytics['commands_used']:
            analytics['commands_used'][command] = 0
        analytics['commands_used'][command] += 1
        
        if command not in user_data[user_id]['commands_used']:
            user_data[user_id]['commands_used'][command] = 0
        user_data[user_id]['commands_used'][command] += 1
        user_data[user_id]['points'] += 10  # Award points
    
    if button:
        if button not in analytics['button_clicks']:
            analytics['button_clicks'][button] = 0
        analytics['button_clicks'][button] += 1
        user_data[user_id]['points'] += 5  # Award points for buttons

# Send message with typing action (ultra-fast for seamless experience)
def send_message_with_typing(chat_id, text, reply_markup=None, parse_mode=None):
    bot.send_chat_action(chat_id, 'typing')
    time.sleep(0.1)  # Ultra-fast typing simulation for quick responses
    return bot.send_message(chat_id, text, reply_markup=reply_markup, parse_mode=parse_mode)

# /start command with warm, inviting welcome + buttons
@bot.message_handler(commands=['start'])
def start_handler(message):
    track_activity(message.from_user.id, '/start')
    
    # Warm, friendly welcome message with emojis and clear formatting
    welcome_text = """
🌟 *Hello and Welcome to TKINGBEAST!* 🌟

🔥 *Unlock the Secrets of Gold Trading with Our Pro eBook* 🔥

Imagine turning market insights into steady profits on XAU/USD – all with simple, proven steps! 

💎 *Here's what awaits you:*
✅ Easy-to-follow entry and exit rules
✅ Real-life chart examples to guide you
✅ Smart risk management to protect your gains
✅ Over 10 inspiring trade stories

We're excited to help you start your trading journey. Pick an option below – it's that simple! 😊⚡
    """
    
    buttons = [
        {'text': "🛒 Get the eBook ($100)", 'url': "https://crypto-pay-kappa.vercel.app/"},
        {'text': "📘 eBook Details", 'callback_data': "bookinfo"},
        {'text': "💬 Chat with Us", 'url': "t.me/tkingbeast"},
        {'text': "⭐ Real Stories", 'callback_data': "testimonials"},
        {'text': "💰 Easy Payments", 'callback_data': "payment_options"},
        {'text': "🎲 Quick Fun Quiz", 'callback_data': "quiz_start"}  # Engaging fun feature
    ]
    
    markup = create_inline_keyboard(buttons, row_width=2)
    
    # Send welcoming message (text-first for speed; photo optional)
    try:
        # If you have a welcome image, uncomment below
        # bot.send_photo(message.chat.id, photo=open('welcome.jpg', 'rb'), caption=welcome_text, reply_markup=markup, parse_mode='Markdown')
        send_message_with_typing(message.chat.id, welcome_text, reply_markup=markup, parse_mode='Markdown')
    except Exception as e:
        print(f"Error sending photo: {e}")
        send_message_with_typing(message.chat.id, welcome_text, reply_markup=markup, parse_mode='Markdown')
    
    # Add intuitive quick-reply keyboard for effortless navigation
    quick_reply_buttons = [
        ['📘 Details', '💰 Price'],
        ['🛒 Start Now', '💬 Help', '🎲 Quiz']
    ]
    reply_markup = create_reply_keyboard(quick_reply_buttons)
    send_message_with_typing(message.chat.id, "What would you like to explore first? 😊", reply_markup=reply_markup)

# /help command with empathetic, clear guidance
@bot.message_handler(commands=['help'])
def help_handler(message):
    track_activity(message.from_user.id, '/help')
    
    help_text = """
🤝 *We're Here to Make This Easy for You!*

No worries – we've got your back with friendly support on:
• Buying and accessing your eBook
• Any payment questions
• Trading strategy tips
• Bot navigation help

*Simple Ways to Reach Us:*
• WhatsApp: [Tap to Chat](https://wa.me/251905243667?text=Hi%20TKINGBEAST%20team%2C%20I%20need%20a%20little%20help%21)
• Email: support@tkingbeast21@gmail.com
• Telegram: @TKingBeast_Support (t.me/tkingbeast)

*Quick Answers:*
• Delivery time? → Right away after we confirm your payment! 🚀
• Payments? → Secure crypto (USDT on Polygon, TRC20, BEP20, etc.)
• Refunds? → Unfortunately, no refunds once purchased

Feel free to ask anything – we're smiling and ready to assist! 😊
    """
    send_message_with_typing(message.chat.id, help_text, parse_mode='Markdown')

# /bookinfo command with approachable, benefit-focused details
@bot.message_handler(commands=['bookinfo'])
def bookinfo_handler(message):
    track_activity(message.from_user.id, '/bookinfo')
    
    book_info = """
📘 *Discover TKINGBEAST's Gold Trading eBook – Your Friendly Guide to Success*

*Why You'll Love It:*
• *Real Results:* High win rates when you stay patient and disciplined on XAU/USD
• *Gold-Only Focus:* Tailored just for gold trading – no distractions!
• *Affordable Joy:* Just $100 for lifetime access (read offline after one easy login)
• *Beginner-to-Pro:* Perfect for anyone ready to build confidence

*Inside the Pages:*
✅ Crystal-clear entry/exit steps
✅ Annotated charts from live trades
✅ Gentle risk tips to keep you safe
✅ 10+ stories of wins to inspire you
✅ Mindset boosts for calm trading
✅ Quick setup for custom tools

*Ideal For You If:*
• You're eager for reliable profits
• Signals feel overwhelming – this empowers you!
• You want to truly understand gold's moves

Plus, free chats with us after you join! Let's make trading fun together. 🌟
    """
    
    buttons = [
        {'text': "🛒 Grab It Now ($100)", 'url': "https://crypto-pay-kappa.vercel.app/"},
        {'text': "💰 Payment Guide", 'callback_data': "payment_options"},
        {'text': "📞 Quick Question?", 'url': "https://wa.me/251905243667?text=Hi%20TKINGBEAST%2C%20tell%20me%20more%20about%20the%20eBook!"}
    ]
    
    markup = create_inline_keyboard(buttons, row_width=1)
    send_message_with_typing(message.chat.id, book_info, reply_markup=markup, parse_mode='Markdown')

# /price command with transparent, reassuring info
@bot.message_handler(commands=['price'])
def price_handler(message):
    track_activity(message.from_user.id, '/price')
    
    price_text = """
💵 *Straightforward Pricing – No Surprises!*

*Your Investment:* $100 (one easy, one-time payment)

*What You Gain:*
• Full eBook access (offline-ready after login)
• Instant delivery to your device
• Ongoing friendly support

*Hassle-Free Payments:*
• Crypto magic with USDT (Polygon, TRC20, BEP20, and more)
• Super-secure and speedy processing

🌟 *Sweet Deal:* The first 50 explorers get an exclusive discount – hurry! 

Value like this? It's a steal for the skills you'll build. 😊
    """
    
    buttons = [
        {'text': "🛒 Secure Checkout", 'url': "https://crypto-pay-kappa.vercel.app/"},
        {'text': "💬 Payment Buddy", 'url': "https://wa.me/251905243667?text=Hi%20TKINGBEAST%2C%20walk%20me%20through%20payment%3F"}
    ]
    
    markup = create_inline_keyboard(buttons)
    send_message_with_typing(message.chat.id, price_text, reply_markup=markup, parse_mode='Markdown')

# /payment command with step-by-step kindness
@bot.message_handler(commands=['payment'])
def payment_handler(message):
    track_activity(message.from_user.id, '/payment')
    
    payment_text = """
🚀 *Your Smooth Path to Payment – We've Made It a Breeze!*

We love crypto for its speed and safety – here's how:

*Choose Your Vibe:*
• Polygon (fast & cheap!)
• TRC20
• BEP20 (and others welcome)

*Gentle Steps:*
1️⃣ Tap 'Payment Portal' below – super secure!
2️⃣ Pick your network and send exactly $100 USDT (or add a fun tip 😊)
3️⃣ Snap a quick screenshot of your transaction
4️⃣ Share it with our team (link in support)
5️⃣ Boom! eBook lands in your DMs instantly 🎉

*Pro Tip:* Match the chain to avoid any hiccups – we're here if needed!

Happy paying – you're one step closer to gold wins! 🌈
    """
    
    buttons = [
        {'text': "🌐 Payment Portal", 'url': "https://crypto-pay-kappa.vercel.app/"},
        {'text': "💬 Payment Pal", 'url': "https://wa.me/251905243667?text=Hi%20TKINGBEAST%2C%20payment%20help%20please!"}
    ]
    
    markup = create_inline_keyboard(buttons)
    send_message_with_typing(message.chat.id, payment_text, reply_markup=markup, parse_mode='Markdown')

# /buy command with encouraging, bite-sized steps
@bot.message_handler(commands=['buy'])
def buy_handler(message):
    track_activity(message.from_user.id, '/buy')
    
    buy_text = """
💰 *Let's Get You Started – 5 Super-Easy Steps to Your eBook!*

You're making a smart move – here's the gentle guide:

1️⃣ *Tap 'Payment Portal'* – Head to our safe spot
2️⃣ *Pick Your Network* – Polygon, TRC20, BEP20... you choose!
3️⃣ *Send $100 USDT* – Exact amount (tip optional for good karma 😉)
4️⃣ *Share Proof* – Quick screenshot via form or support
5️⃣ *Enjoy Instantly!* – eBook delivered with a smile 🚀

Stuck anywhere? Our support button is your friend!

Excited for your trading glow-up? Let's do this! ✨
    """
    
    buttons = [
        {'text': "🚀 Payment Portal", 'url': "https://crypto-pay-kappa.vercel.app/"},
        {'text': "📝 Proof Form", 'url': "https://docs.google.com/forms/d/e/1FAIpQLSdZASavTBeRJmSSfIn7fRC1D2enutnqPEPRuCsFCGO33JhcEA/viewform"},
        {'text': "💬 Buy Buddy", 'url': "https://wa.me/251905243667?text=Hi%20TKINGBEAST%2C%20help%20with%20my%20purchase!"}
    ]
    
    markup = create_inline_keyboard(buttons, row_width=1)
    send_message_with_typing(message.chat.id, buy_text, reply_markup=markup, parse_mode='Markdown')

# /support command with warm, accessible options
@bot.message_handler(commands=['support'])
def support_handler(message):
    track_activity(message.from_user.id, '/support')
    
    support_text = """
💬 *Your Friendly Support Squad Awaits!*

We love chatting and solving things together:
• Purchase or payment ease
• eBook delivery magic
• Trading curiosity
• Anything on your mind

*Easy Connections:*
• WhatsApp: [Say Hi!](https://wa.me/251905243667?text=Hello%20TKINGBEAST%20friends%2C%20how%20can%20I%20help%20today%3F)
• Email: support@tkingbeast21@gmail.com
• Telegram: t.me/tkingbeast

*Our Promise:* Quick replies – often in minutes during the day, always within 24 hours. You're never alone! 😊
    """
    
    send_message_with_typing(message.chat.id, support_text, parse_mode='Markdown')

# /terms command with clear, reassuring language
@bot.message_handler(commands=['terms'])
def terms_handler(message):
    track_activity(message.from_user.id, '/terms')
    
    terms_text = """
📜 *Our Simple Terms – Transparency First!*

When you join us, it's all about trust:

*Your Rights:*
• Just for you (no sharing needed – it's personal!)
• One cozy license per purchase
• Dream big, but no reselling without a chat

*No-Worries Policy:*
• Refunds: No, since it's digital and instant – but we're here for any fixes!

*Important Note:*
• Trading's an adventure with risks – protect yourself
• Wins aren't promised, but tools are!
• We're guides, not guarantors of gold

*Dive Deeper:* Full details [here](https://read-liard.vercel.app/)

Happy exploring – questions? Just ask! 🌟
    """
    
    send_message_with_typing(message.chat.id, terms_text, parse_mode='Markdown')

# /testimonials command with uplifting, relatable stories
@bot.message_handler(commands=['testimonials'])
def testimonials_handler(message):
    track_activity(message.from_user.id, '/testimonials')
    
    testimonials = [
        {
            'name': 'Kidus 🌟',
            'text': 'This eBook flipped my gold game! Recouped costs in days – pure joy.',
            'profit': '+$1,240'
        },
        {
            'name': 'Solomon 😊',
            'text': 'As a newbie, the steps felt like a warm hug. So clear and doable!',
            'profit': '+$890'
        },
        {
            'name': 'Mike T. 🚀',
            'text': 'Discipline unlocked – steady wins for months. Life-changing stuff!',
            'profit': '+$3,150'
        },
        {
            'name': 'Sami K. 💫',
            'text': 'Top investment ever. Team's support? Like family. Grateful!',
            'profit': '+$2,100'
        },
        {
            'name': 'Alex R. ✨',
            'text': 'From confused to confident. Charts make sense now – wow!',
            'profit': '+$720'
        }
    ]
    
    testimonial = random.choice(testimonials)
    
    testimonial_text = f"""
⭐ *A Heartwarming Win Story* ⭐

*{testimonial['name']}* shares: "{testimonial['text']}"

*Their Sparkle:* {testimonial['profit']}

Your turn to shine? We're cheering you on! 🎊
    """
    
    buttons = [
        {'text': "🛒 Join the Winners", 'url': "https://crypto-pay-kappa.vercel.app/"},
        {'text': "📘 Peek Inside", 'callback_data': "bookinfo"}
    ]
    
    markup = create_inline_keyboard(buttons)
    send_message_with_typing(message.chat.id, testimonial_text, reply_markup=markup, parse_mode='Markdown')

# /tip command: Uplifting, bite-sized wisdom
@bot.message_handler(commands=['tip'])
def tip_handler(message):
    track_activity(message.from_user.id, '/tip')
    tips = [
        "💡 *Gentle Reminder:* Discipline is your superpower – trust the plan, and wins follow! 🌱",
        "📈 *Easy Win:* Stop-losses are like seatbelts – always buckle up for safety. 🛡️",
        "🧠 *Growth Hack:* Log your trades like a diary. Reflections turn lessons into gold! 📓",
        "⚡ *Flow Tip:* Ride the trend wave – it's smoother than swimming upstream. 🌊",
        "🎯 *Patience Magic:* High-quality setups are worth the wait. Good things bloom slowly! 🌸",
        "🔥 *Mindset Boost:* Every trade teaches – celebrate the learning, not just the profit. 🏆",
        "💎 *Pro Secret:* Small, consistent steps build empires. Start tiny, dream big! 🚀"
    ]
    tip = random.choice(tips)
    send_message_with_typing(message.chat.id, f"🛡️ *A Little Trading Sunshine* 🛡️\n\n{tip}", parse_mode='Markdown')

# /joke command: Light-hearted laughs to brighten the day
@bot.message_handler(commands=['joke'])
def joke_handler(message):
    track_activity(message.from_user.id, '/joke')
    jokes = [
        "Why did the trader marry the chart? It had all the right curves! 😂📊",
        "What's a trader's fave exercise? Running profits! 🏃‍♂️💰",
        "Trader to market: 'Stop breaking my heart!' Market: 'It's just a dip – hug it out.' 💕📉",
        "Why don't traders play hide and seek? Good luck hiding from volatility! 😜",
        "Chart walks into a bar... Bartender: 'Why the long wick?' 📈🍸"
    ]
    joke = random.choice(jokes)
    send_message_with_typing(message.chat.id, f"😆 *A Chuckle for Your Charts* 😆\n\n{joke}\n\nHope that sparked a smile! 🌟", parse_mode='Markdown')

# Enhanced /quiz command: Dynamic, ever-unique fun with expanded pool for freshness
@bot.message_handler(commands=['quiz'])
def quiz_handler(message):
    track_activity(message.from_user.id, '/quiz')
    # Larger, diverse pool for uniqueness – random pick ensures fresh experience every time
    questions = [
        {
            "q": "What's the real MVP in trading – beyond any hot tip?",
            "options": ["A: Pure luck", "B: Rock-solid discipline", "C: Lightning speed"],
            "ans": "B"
        },
        {
            "q": "True or False: It's smart to risk money you can't afford to wave goodbye?",
            "options": ["A: True – go big!", "B: False – play safe"],
            "ans": "B"
        },
        {
            "q": "In gold trading, what's your best buddy for protection?",
            "options": ["A: A crystal ball", "B: Stop-loss orders", "C: Coffee breaks"],
            "ans": "B"
        },
        {
            "q": "Quick: Trade with the flow or fight it?",
            "options": ["A: Fight for glory", "B: Flow with the trend"],
            "ans": "B"
        },
        {
            "q": "Patience in trading is like...?",
            "options": ["A: Boring wait", "B: Your secret weapon"],
            "ans": "B"
        },
        {
            "q": "True or False: Journaling trades boosts your skills?",
            "options": ["A: False – too much work", "B: True – magic growth tool"],
            "ans": "B"
        },
        {
            "q": "What's key for XAU/USD wins?",
            "options": ["A: Daily trades", "B: High-probability setups"],
            "ans": "B"
        },
        {
            "q": "Risk management: Cap it at what % of your account?",
            "options": ["A: 50% – all in!", "B: 1-2% – steady sails"],
            "ans": "B"
        },
        {
            "q": "Emotions in trading: Friend or foe?",
            "options": ["A: Best guide ever", "B: Sneaky foe – stay cool"],
            "ans": "B"
        },
        {
            "q": "Bonus for consistency?",
            "options": ["A: Wild guesses", "B: A solid plan"],
            "ans": "B"
        }
    ]
    q = random.choice(questions)  # Always unique – fresh question each time!
    user_data[message.from_user.id]['current_quiz'] = q  # Store gently for check
    markup = InlineKeyboardMarkup(row_width=1)
    for opt in q['options']:
        markup.add(InlineKeyboardButton(opt, callback_data=f"quiz_{opt.replace(' ', '_').replace('-', '_')}"))  # Safer data
    send_message_with_typing(message.chat.id, f"🧠 *Fun Trading Brain Teaser!* 🧠\n\n{q['q']}\n\nTap your guess – no pressure, just play! 😊", reply_markup=markup)

# Handle button callbacks with smooth, positive feedback
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "bookinfo":
        track_activity(call.from_user.id, button="bookinfo_callback")
        bookinfo_handler(call.message)
    elif call.data == "testimonials":
        track_activity(call.from_user.id, button="testimonials_callback")
        testimonials_handler(call.message)
    elif call.data == "payment_options":
        track_activity(call.from_user.id, button="payment_options_callback")
        payment_handler(call.message)
    elif call.data == "quiz_start":
        track_activity(call.from_user.id, button="quiz_start")
        quiz_handler(call.message)
    elif call.data.startswith("quiz_"):
        track_activity(call.from_user.id, button="quiz_answer")
        user_id = call.from_user.id
        if user_id in user_data and 'current_quiz' in user_data[user_id]:
            q = user_data[user_id]['current_quiz']
            # Extract selected option more robustly
            selected = call.data.split("_", 1)[1].replace('_', ' ').replace(' ', '')  # Clean up
            correct_letter = q['ans'][0].upper()
            if selected.startswith(correct_letter):
                user_data[user_id]['points'] += 50
                bot.edit_message_text("🎉 Yay! Spot on – you're a natural! +50 points to your trading glow. 🌟", call.message.chat.id, call.message.message_id)
                send_message_with_typing(call.message.chat.id, f"Total sparkle points: {user_data[user_id]['points']}\n\nFancy another? /quiz 😊")
            else:
                bot.edit_message_text(f"😄 Close one! It was {q['ans']}. Every guess levels you up! Keep shining. ✨", call.message.chat.id, call.message.message_id)
            del user_data[user_id]['current_quiz']
        bot.answer_callback_query(call.id)
    
    bot.answer_callback_query(call.id)

# Handle quick reply buttons with forgiving, intuitive matching
@bot.message_handler(func=lambda message: True)
def handle_quick_replies(message):
    text = message.text.lower().strip()
    
    if any(word in text for word in ['book info', 'details', 'info', 'ebook']):
        track_activity(message.from_user.id, button="bookinfo_quick")
        bookinfo_handler(message)
    elif any(word in text for word in ['price', 'cost', 'how much']):
        track_activity(message.from_user.id, button="price_quick")
        price_handler(message)
    elif any(word in text for word in ['buy now', 'purchase', 'get it', 'buy']):
        track_activity(message.from_user.id, button="buy_quick")
        buy_handler(message)
    elif any(word in text for word in ['support', 'help', 'question', 'issue']):
        track_activity(message.from_user.id, button="support_quick")
        support_handler(message)
    elif any(word in text for word in ['quiz', 'question', 'test', 'fun']):
        track_activity(message.from_user.id, button="quiz_quick")
        quiz_handler(message)
    else:
        # Warm fallback for any curveballs
        track_activity(message.from_user.id, button="unknown_message")
        fallback_text = """
🤖 *Hi There! I'm Your TKINGBEAST Guide* 🌟

Eager to help with trading treasures! Try:
• /bookinfo for eBook magic
• /price for the scoop
• /buy to jump in
• /support for a chat
• /tip, /joke, or /quiz for smiles & smarts!

Or tap a button below – easy peasy! 😊
        """
        
        quick_reply_buttons = [
            ['📘 Details', '💰 Price'],
            ['🛒 Start Now', '💬 Help', '🎲 Quiz']
        ]
        reply_markup = create_reply_keyboard(quick_reply_buttons)
        send_message_with_typing(message.chat.id, fallback_text, reply_markup=reply_markup)

# Admin command: Insightful stats with gamification highlights
@bot.message_handler(commands=['stats'], func=lambda message: message.from_user.id == ADMIN_ID)
def stats_handler(message):
    stats_text = f"""
📊 *Bot Insights – Let's Celebrate the Wins!*

*Total Explorers:* {analytics['total_users']}
*Top Commands (High-Fives):*
"""
    
    for cmd, count in sorted(analytics['commands_used'].items(), key=lambda x: x[1], reverse=True)[:5]:
        stats_text += f"• {cmd}: {count}\n"
    
    stats_text += "\n*Button Buzz:*\n"
    for btn, count in sorted(analytics['button_clicks'].items(), key=lambda x: x[1], reverse=True)[:5]:
        stats_text += f"• {btn}: {count}\n"
    
    # Gamification joy
    total_points = sum(user['points'] for user in user_data.values())
    avg_points = total_points / len(user_data) if user_data else 0
    stats_text += f"\n*Fun Factor:* Average Points: {avg_points:.0f} – Users are leveling up! 🏆"
    
    send_message_with_typing(message.chat.id, stats_text, parse_mode='Markdown')

# /points: Encouraging personal progress check
@bot.message_handler(commands=['points'])
def points_handler(message):
    track_activity(message.from_user.id, '/points')
    points = user_data.get(message.from_user.id, {}).get('points', 0)
    send_message_with_typing(message.chat.id, f"🏆 *Your Personal Trading Stars:* {points}\n\nYou've earned these through curiosity – quizzes are point parties! Keep glowing. 💫\n\nMore? Dive into /quiz or /tip!")

# Gentle periodic nudges for re-engagement
def send_updates():
    for user_id, data in user_data.items():
        if time.time() - data['last_active'] > 86400:  # 24 hours quiet?
            try:
                update_text = """
🌟 *A Sunny Reminder Just for You!*

We spotted your interest in gold trading awesomeness. 

First 10 friends get 10% off – your perfect nudge? 

👉 [Tap for Your Deal](https://crypto-pay-kappa.vercel.app/)

No rush – we're here when you're ready! 😊
                """
                send_message_with_typing(user_id, update_text, parse_mode='Markdown')
            except Exception as e:
                print(f"Update whisper failed for {user_id}: {e}")

# Soft scheduling for those caring check-ins
def schedule_updates():
    while True:
        time.sleep(86400)  # Gentle 24-hour rhythm
        send_updates()

# Spark the update magic in the background
update_thread = threading.Thread(target=schedule_updates)
update_thread.daemon = True
update_thread.start()

# Launch into the world!
if __name__ == "__main__":
    print("🤖 TKINGBEAST Bot Awakening... 🌟")
    print("✨ Turbocharged with unique quizzes, lightning speed, and heartwarming vibes!")
    print("📊 Analytics flowing, points sparkling – ready to delight!")
    bot.infinity_polling()
