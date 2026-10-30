import random
from collections import Counter

n = random.randint(5, 10)
m = random.randint(5, 10)
labirint = [['*' for _ in range(m)] for _ in range(n)]
labirint[0][0] = '&'

seen = [[False for _ in range(m)] for _ in range(n)]

def reveal_around(cx, cy):
    """Открывает туман войны в радиусе 1 клетки вокруг (cx, cy)"""
    for i in range(max(0, cx - 1), min(n, cx + 2)):
        for j in range(max(0, cy - 1), min(m, cy + 2)):
            seen[i][j] = True

# Открываем клетки вокруг игрока на старте
reveal_around(0, 0)

inventory = []
gold = 10
debt = 0
loan_taken_total = 0
portal_open = False

LOAN_LIMIT = 1_000_000

# ---------- Показ ----------
def show(labirint):
    print("\n" + "=" * (m * 2 + 3))
    for x, row in enumerate(labirint):
        line = "  "
        for y, cell in enumerate(row):
            line += (cell if seen[x][y] else "?") + " "
        print(line)
    print("=" * (m * 2 + 3))
    print(f"🎒 Инвентарь: {', '.join(inventory) if inventory else 'пусто'}")
    print(f"🪙 Золото: {gold}" + (f"  |  ⚠️ Долг: {debt}" if debt > 0 else ""))
    print(f"🌀 Портал: {'открыт' if portal_open else 'закрыт'}")
    print("Управление: w/a/s/d — шаг, i — инвентарь, q — выход\n")

# ---------- Поиск игрока ----------
def player(labirint):
    for x, row in enumerate(labirint):
        for y, cell in enumerate(row):
            if cell == '&':
                return (x, y)
    return (0, 0)

# ---------- Расстановка ----------
def place(symbol, count):
    placed = 0
    while placed < count:
        x = random.randint(0, n - 1)
        y = random.randint(0, m - 1)
        if labirint[x][y] == '*' and (x, y) != (0, 0):
            labirint[x][y] = symbol
            placed += 1

place('M', 3)
place('C', 4)
place('K', 1)
place('P', 1)
place('$', 1)

# ---------- Лут из сундука ----------
def open_chest():
    global gold
    loot = random.choice([
        'меч',
        'зелье невидимости',
        'камень зачарования',
        'странный камень',
        'золото',
    ])
    if loot == 'золото':
        amount = random.randint(5, 20)
        gold += amount
        print(f"📦 Сундук! Ты нашёл {amount} золота.")
    else:
        inventory.append(loot)
        print(f"📦 Сундук! Ты нашёл: {loot}")

# ---------- Бой с монстром ----------
def fight_monster():
    if 'меч ✦' in inventory:
        print("⚔️ Монстр! Твой зачарованный меч разрубил его. Меч остался цел.")
        return True
    if 'меч' in inventory:
        inventory.remove('меч')
        print("⚔️ Монстр! Ты зарубил его мечом, но меч сломался.")
        return True
    if 'зелье невидимости' in inventory:
        inventory.remove('зелье невидимости')
        print("🧪 Монстр! Ты выпил зелье невидимости и тихо прошёл мимо.")
        return True
    print("💀 Ты наткнулся на монстра без оружия и защиты! Игра окончена.")
    exit()

# ---------- Проверка банкротства ----------
def check_bankrupt():
    if gold <= 0:
        if loan_taken_total >= LOAN_LIMIT:
            print("💀 Ты проиграл всё золото и исчерпал кредитный лимит! Игра окончена.")
            exit()
        else:
            print("💸 У тебя закончилось золото! Возьми кредит в меню казино или уходи.")
            return True
    return False

# ---------- Ввод ставки ----------
def get_bet():
    if check_bankrupt():
        return None
    raw = input("Ставка (Enter — назад): ").strip()
    if raw == "":
        return None
    try:
        bet = int(raw)
    except ValueError:
        print("Нужно ввести число.")
        return 0
    if bet <= 0:
        print("Ставка должна быть больше нуля.")
        return 0
    if bet > gold:
        print(f"У тебя только {gold} золота.")
        return 0
    return bet

# ============ ПОКЕР ============

RANKS = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
SUITS = ['♠','♥','♦','♣']
RANK_VALUE = {r: i for i, r in enumerate(RANKS, start=2)}

HAND_NAMES = {
    8: "Стрит-флеш", 7: "Каре", 6: "Фулл-хаус",
    5: "Флеш", 4: "Стрит", 3: "Тройка",
    2: "Две пары", 1: "Пара", 0: "Старшая карта",
}

def make_deck():
    deck = [(r, s) for r in RANKS for s in SUITS]
    random.shuffle(deck)
    return deck

def hand_str(hand):
    return ' '.join(f"{r}{s}" for r, s in hand)

def evaluate_hand(hand):
    ranks = sorted([RANK_VALUE[r] for r, _ in hand], reverse=True)
    suits = [s for _, s in hand]
    flush = len(set(suits)) == 1
    unique = sorted(set(ranks), reverse=True)

    straight = False
    if len(unique) == 5:
        if unique[0] - unique[-1] == 4:
            straight = True
        elif unique == [14, 5, 4, 3, 2]:
            straight = True
            unique = [5, 4, 3, 2, 1]

    counts = Counter(ranks)
    freq = sorted(counts.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    freqs = [c for _, c in freq]
    ordered = [v for v, _ in freq]

    if straight and flush: return (8, tuple(unique))
    if freqs[0] == 4: return (7, tuple(ordered))
    if freqs[0] == 3 and freqs[1] == 2: return (6, tuple(ordered))
    if flush: return (5, tuple(ranks))
    if straight: return (4, tuple(unique))
    if freqs[0] == 3: return (3, tuple(ordered))
    if freqs[0] == 2 and freqs[1] == 2: return (2, tuple(ordered))
    if freqs[0] == 2: return (1, tuple(ordered))
    return (0, tuple(ranks))

def poker():
    global gold
    print("\n--- ПОКЕР ---")
    print("Тебе и дилеру по 5 карт. Победа — ×2, ничья — возврат.")
    while True:
        bet = get_bet()
        if bet is None:
            return
        if bet == 0:
            continue

        gold -= bet
        deck = make_deck()
        player_hand = [deck.pop() for _ in range(5)]
        dealer_hand = [deck.pop() for _ in range(5)]

        p_cat, p_tie = evaluate_hand(player_hand)
        d_cat, d_tie = evaluate_hand(dealer_hand)

        print(f"\n  Твои карты:   {hand_str(player_hand)}  — {HAND_NAMES[p_cat]}")
        print(f"  Карты дилера: {hand_str(dealer_hand)}  — {HAND_NAMES[d_cat]}")

        if (p_cat, p_tie) > (d_cat, d_tie):
            win = bet * 2
            gold += win
            print(f"🏆 Ты выиграл! +{win}")
        elif (p_cat, p_tie) == (d_cat, d_tie):
            gold += bet
            print(f"🤝 Ничья. Ставка возвращается: {bet}")
        else:
            print(f"💀 Дилер выиграл. Ты потерял {bet}")

        print(f"Баланс: {gold}")
        if check_bankrupt():
            return
        if input("Ещё? (Enter — да, n — нет): ").strip().lower() == 'n':
            return

# ---------- Кредит ----------
def take_loan():
    global gold, debt, loan_taken_total
    remaining = LOAN_LIMIT - loan_taken_total
    print("\n--- КРЕДИТ ---")
    print(f"Доступно для взятия: {remaining} (Всего лимит: {LOAN_LIMIT})")
    if remaining <= 0:
        print("Лимит исчерпан.")
        return
    raw = input("Сколько взять? (Enter — отмена): ").strip()
    if raw == "":
        return
    try:
        amount = int(raw)
    except ValueError:
        print("Нужно число.")
        return
    if not (0 < amount <= remaining):
        print(f"Можно взять от 1 до {remaining}.")
        return
    gold += amount
    debt += amount
    loan_taken_total += amount
    print(f"Ты взял {amount} золота. Текущий долг: {debt}.")

def repay_loan():
    global gold, debt
    if debt <= 0:
        print("У тебя нет долга.")
        return
    print(f"\n--- ВОЗВРАТ ДОЛГА ---")
    print(f"Долг: {debt}, у тебя золота: {gold}")
    raw = input("Сколько вернуть? (Enter — максимум возможного): ").strip()
    if raw == "":
        pay = min(gold, debt)
    else:
        try:
            pay = int(raw)
        except ValueError:
            print("Нужно число.")
            return
    if pay <= 0 or pay > gold:
        print("Некорректная сумма.")
        return
    pay = min(pay, debt)
    gold -= pay
    debt -= pay
    print(f"Ты вернул {pay}. Остаток долга: {debt}.")

# ---------- Рулетка ----------
def roulette():
    global gold
    print("\n--- РУЛЕТКА ---")
    print("  🎰 x2   💀 x0   💎 x3")
    while True:
        bet = get_bet()
        if bet is None:
            return
        if bet == 0:
            continue

        gold -= bet
        result = random.choice(['x2', 'x0', 'x3'])
        if result == 'x2':
            win = bet * 2
            gold += win
            print(f"🎰 Выпало x2! Выигрыш {win}. Баланс: {gold}")
        elif result == 'x3':
            win = bet * 3
            gold += win
            print(f"💎 Выпало x3! Выигрыш {win}. Баланс: {gold}")
        else:
            print(f"💀 Выпало x0. Ты потерял {bet}. Баланс: {gold}")

        if check_bankrupt():
            return
        if input("Ещё? (Enter — да, n — нет): ").strip().lower() == 'n':
            return

# ---------- Слоты ----------
SLOT_SYMBOLS = ['🍒', '🍋', '🔔', '💎', '7️⃣']
SLOT_MULTIPLIERS = {'🍒': 3, '🍋': 4, '🔔': 6, '💎': 10, '7️⃣': 20}

def slots():
    global gold
    print("\n--- СЛОТЫ ---")
    print("  🍒 x3   🍋 x4   🔔 x6   💎 x10   7️⃣ x20  (Два одинаковых — x2)")
    while True:
        bet = get_bet()
        if bet is None:
            return
        if bet == 0:
            continue

        gold -= bet
        reels = [random.choice(SLOT_SYMBOLS) for _ in range(3)]
        if reels[0] == reels[1] == reels[2]:
            mult = SLOT_MULTIPLIERS[reels[0]]
        elif len(set(reels)) == 2:
            mult = 2
        else:
            mult = 0

        win = bet * mult
        gold += win
        print(f"\n  [ {reels[0]} | {reels[1]} | {reels[2]} ]\n")
        if mult == 0:
            print(f"💀 Ничего. Ты потерял {bet}. Баланс: {gold}")
        elif mult == 2:
            print(f"✨ Два одинаковых! Выигрыш {win}. Баланс: {gold}")
        else:
            print(f"🎉 ДЖЕКПОТ x{mult}! Выигрыш {win}. Баланс: {gold}")

        if check_bankrupt():
            return
        if input("Ещё? (Enter — да, n — нет): ").strip().lower() == 'n':
            return

# ---------- Меню казино ----------
def casino():
    global gold
    while True:
        print("\n=== 🎰 КАЗИНО ===")
        print(f"Золото: {gold}" + (f" | ⚠️ Долг: {debt}" if debt > 0 else ""))
        print("  1 — Рулетка")
        print("  2 — Слоты")
        print("  3 — Покер")
        print("  4 — Взять кредит")
        print("  5 — Вернуть долг")
        if 'странный камень' in inventory:
            print("  6 — Продать странный камень (+15 золота)")
        print("  Enter — Выйти в лабиринт")
        choice = input("> ").strip()

        if choice == '1':
            roulette()
        elif choice == '2':
            slots()
        elif choice == '3':
            poker()
        elif choice == '4':
            take_loan()
        elif choice == '5':
            repay_loan()
        elif choice == '6' and 'странный камень' in inventory:
            inventory.remove('странный камень')
            gold += 15
            print("Ты продал странный камень коллекционеру за 15 золота!")
        elif choice == '':
            if debt > 0:
                print(f"\n⚠️ Охрана у дверей: «У тебя долг {debt} золота! Сначала верни (пункт 5), или мы тебя не выпустим!»")
                if gold == 0 and loan_taken_total >= LOAN_LIMIT:
                    print("💀 Тебе нечем платить и кредитов больше не дают. Игра окончена!")
                    exit()
            else:
                print("Ты вышел из казино.")
                return

# ---------- Обработка клетки ----------
def on_enter(cell):
    """Возвращает True, если игрок должен переместиться на эту клетку"""
    if cell == 'M':
        return fight_monster()
    elif cell == 'C':
        open_chest()
        return True
    elif cell == 'K':
        inventory.append('ключ')
        print("🔑 Ты подобрал ключ! Используй его в инвентаре (клавиша i), чтобы открыть портал.")
        return True
    elif cell == '$':
        casino()
        # Возвращаем False, чтобы значок казино '$' не затирался игроком и туда можно было зайти снова
        return False
    elif cell == 'P':
        if portal_open:
            if debt > 0:
                print(f"🌀 Портал перед тобой, но магический барьер не пускает должников (долг: {debt})!")
                return False
            print("🎉 Ты вошёл в открытый портал и прошёл игру! Победа!")
            exit()
        else:
            print("🔒 Портал закрыт. Открой инвентарь (клавиша i) и используй ключ.")
            return False
    return True

# ---------- Движение ----------
def try_move(dx, dy):
    x, y = player(labirint)
    nx, ny = x + dx, y + dy
    if not (0 <= nx < n and 0 <= ny < m):
        print("🧱 Там стена лабиринта!")
        return

    # Открываем клетку, в которую пытаемся шагнуть (чтобы видеть портал или казино)
    seen[nx][ny] = True
    target = labirint[nx][ny]

    if on_enter(target):
        labirint[x][y] = '*'
        labirint[nx][ny] = '&'
        reveal_around(nx, ny)

# ---------- Зачарование ----------
def enchant_sword():
    if 'меч ✦' in inventory:
        print("Твой меч уже зачарован.")
    elif 'меч' not in inventory:
        print("У тебя нет обычного меча для зачарования.")
    elif 'камень зачарования' not in inventory:
        print("Нужен камень зачарования.")
    else:
        inventory.remove('меч')
        inventory.remove('камень зачарования')
        inventory.append('меч ✦')
        print("✨ Ты зачаровал меч! Теперь он никогда не сломается.")

# ---------- Инвентарь ----------
def inventory_menu():
    global portal_open
    if not inventory:
        print("Инвентарь пуст.")
        return
    print("\n--- ИНВЕНТАРЬ ---")
    for i, item in enumerate(inventory, 1):
        print(f"  {i}. {item}")
    sub = input("(u)использовать / (e)зачаровать меч / (s)ортировать / (d)выбросить / Enter — назад: ").strip().lower()
    
    if sub == 's':
        inventory.sort()
        print("Отсортировано.")
    elif sub == 'd':
        try:
            idx = int(input("Номер предмета: ")) - 1
            if 0 <= idx < len(inventory):
                if inventory[idx] == 'ключ':
                    print("Ключ нельзя выбрасывать, иначе не выберешься из лабиринта!")
                else:
                    print("Выброшено:", inventory.pop(idx))
            else:
                print("Неверный номер.")
        except ValueError:
            print("Нужно число.")
    elif sub == 'u':
        try:
            idx = int(input("Номер предмета для использования: ")) - 1
            if 0 <= idx < len(inventory):
                item = inventory[idx]
                if item == 'ключ':
                    inventory.pop(idx)
                    portal_open = True
                    print("🔑 Ты повернул ключ в воздухе — где-то в лабиринте открылся портал!")
                elif item == 'странный камень':
                    print("Красивый блестящий булыжник. Возможно, его купят в казино.")
                else:
                    print(f"Предмет «{item}» применяется автоматически в бою или через другие меню.")
            else:
                print("Неверный номер.")
        except ValueError:
            print("Нужно число.")
    elif sub == 'e':
        enchant_sword()

# ---------- Главный цикл ----------
MOVES = {
    'w': (-1, 0),
    's': (1, 0),
    'a': (0, -1),
    'd': (0, 1),
}

while True:
    show(labirint)
    choose = input("> ").strip().lower()

    if choose in MOVES:
        dx, dy = MOVES[choose]
        try_move(dx, dy)
    elif choose == 'i':
        inventory_menu()
    elif choose == 'q':
        print("Выход из игры.")
        break
    else:
        print("Неизвестная команда. Используй w/a/s/d, i или q.")
