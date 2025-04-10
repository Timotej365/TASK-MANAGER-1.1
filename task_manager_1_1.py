import mysql.connector
from mysql.connector import Error


def pripojenie_db():
    try:
        spojenie = mysql.connector.connect(
            host="localhost",
            user="root",         
            password="1111",    
            database="task_manager_1_1"       
        )

        if spojenie.is_connected():
            print("✅ Pripojenie k databáze prebehlo úspešne.")
            return spojenie

    except Error as e:
        print("❌ Chyba pri pripájaní k databáze:", e)
        exit()

# Na začiatku programu
spojenie = pripojenie_db()  # ← takto si zavoláme funkciu a spojenie si uložíme

# Funkcia hlavného menu – vráti voľbu používateľa ako text (napr. "1", "2", ...)
def hlavne_menu():
    print("\nSprávca úloh - Hlavné menu")
    print("1. Pridať novú úlohu")
    print("2. Zobraziť úlohy")
    print("3. Aktualizovať úlohu")
    print("4. Odstrániť úlohu")
    print("5. Ukončiť program")
    volba = input("Vyberte možnosť (1-5): ")
    return volba

# Funkcia na pridanie novej úlohy – validácia v krokoch
def pridat_ulohu(spojenie):
    cursor = spojenie.cursor()

    while True:
        nazov = input("Zadaj názov úlohy: ").strip()
        if not nazov:
            print("❌ Názov úlohy nesmie byť prázdny. Skús to znova.")
        else:
            break

    while True:
        popis = input("Zadaj popis úlohy: ").strip()
        if not popis:
            print("❌ Popis úlohy nesmie byť prázdny. Skús to znova.")
        else:
            break

    try:
        sql = "INSERT INTO ulohy (nazov, popis) VALUES (%s, %s)"
        hodnoty = (nazov, popis)
        cursor.execute(sql, hodnoty)
        spojenie.commit()
        print(f"✅ Úloha „{nazov}“ bola úspešne pridaná do databázy.")
    except Error as e:
        print("❌ Chyba pri ukladaní úlohy:", e)


# Funkcia na zobrazenie všetkých úloh
def zobrazit_ulohy(spojenie):
    cursor = spojenie.cursor()

    try:
        sql = "SELECT id, nazov, popis, stav FROM ulohy WHERE stav IN ('Nezahájená', 'Prebieha')"
        cursor.execute(sql)
        vysledky = cursor.fetchall()

        if len(vysledky) == 0:
            print("ℹ️ Zoznam úloh je prázdny alebo sú všetky úlohy hotové.")
        else:
            print("\n📝 Aktívne úlohy:")
            for id, nazov, popis, stav in vysledky:
                print(f"#{id} | {nazov} – {popis} [{stav}]")

    except Error as e:
        print("❌ Chyba pri načítaní úloh:", e)

# Funkcia na aktualizovanie úloh
def aktualizovat_ulohu(spojenie):
    cursor = spojenie.cursor()

    try:
        # Zobrazíme všetky úlohy s ID, názvom a stavom
        cursor.execute("SELECT id, nazov, stav FROM ulohy")
        ulohy = cursor.fetchall()

        if len(ulohy) == 0:
            print("📭 Zoznam úloh je prázdny.")
            return

        print("\n🛠️ Úlohy na aktualizáciu:")
        for id, nazov, stav in ulohy:
            print(f"#{id} | {nazov} [{stav}]")

        vyber = input("Zadaj ID úlohy, ktorej stav chceš zmeniť: ")
        if not vyber.isdigit():
            print("❌ Neplatné ID.")
            return

        id_ulohy = int(vyber)
        cursor.execute("SELECT * FROM ulohy WHERE id = %s", (id_ulohy,))
        if cursor.fetchone() is None:
            print("❌ Úloha s týmto ID neexistuje.")
            return

        print("Vyber nový stav:")
        print("1. Prebieha")
        print("2. Hotová")
        volba = input("Zadaj možnosť (1-2): ")

        if volba == "1":
            novy_stav = "Prebieha"
        elif volba == "2":
            novy_stav = "Hotová"
        else:
            print("❌ Neplatná voľba.")
            return

        cursor.execute("UPDATE ulohy SET stav = %s WHERE id = %s", (novy_stav, id_ulohy))
        spojenie.commit()
        print(f"✅ Stav úlohy s ID {id_ulohy} bol zmenený na '{novy_stav}'.")

    except Error as e:
        print("❌ Chyba pri aktualizácii úlohy:", e)


# Funkcia na odstránenie vybranej úlohy podľa poradia
def odstranit_ulohu(spojenie):
    cursor = spojenie.cursor()

    try:
        # Zobraz úlohy ako pri zobrazení
        cursor.execute("SELECT id, nazov, popis FROM ulohy")
        ulohy = cursor.fetchall()

        if len(ulohy) == 0:
            print("📭 Zoznam úloh je prázdny.")
            return

        print("\n🗑️ Úlohy dostupné na odstránenie:")
        for id, nazov, popis in ulohy:
            print(f"#{id} | {nazov} – {popis}")

        vyber = input("Zadaj ID úlohy, ktorú chceš odstrániť: ")

        if not vyber.isdigit():
            print("❌ Zadal si neplatné ID.")
            return

        id_ulohy = int(vyber)

        # Over, či úloha s daným ID existuje
        cursor.execute("SELECT * FROM ulohy WHERE id = %s", (id_ulohy,))
        if cursor.fetchone() is None:
            print("❌ Úloha s takým ID neexistuje.")
            return

        # Odstránenie
        cursor.execute("DELETE FROM ulohy WHERE id = %s", (id_ulohy,))
        spojenie.commit()
        print(f"🗑️ Úloha s ID {id_ulohy} bola odstránená.")

    except Error as e:
        print("❌ Chyba pri odstraňovaní úlohy:", e)


# --- HLAVNÝ CYKLUS PROGRAMU ---

# Cyklus sa opakuje, kým používateľ nezvolí možnosť "4"
while True:
    volba = hlavne_menu()

    if volba == "1":
        pridat_ulohu(spojenie)
    elif volba == "2":
        zobrazit_ulohy(spojenie)
    elif volba == "3":
        aktualizovat_ulohu(spojenie)
    elif volba == "4":
        odstranit_ulohu(spojenie)
    elif volba == "5":
        print("👋 Program sa ukončuje...")
        break
    else:
        print("❌ Neplatná voľba. Skús znova.")
