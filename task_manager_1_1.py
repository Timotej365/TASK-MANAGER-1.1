import mysql.connector
from mysql.connector import Error

# Pripojenie + vytvorenie databázy ak ešte neexistuje
def pripojenie_db():
    try:
        # Najprv pripojenie k serveru bez DB
        spojenie = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1111"
        )
        kurzor = spojenie.cursor()
        kurzor.execute("CREATE DATABASE IF NOT EXISTS task_manager_1_1")
        spojenie.commit()
        kurzor.close()
        spojenie.close()

        # Potom sa pripojíme už k vytvorenej databáze
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

# Vytvorenie tabuľky ulohy
def vytvor_tabulku(spojenie):
    try:
        cursor = spojenie.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ulohy (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nazov VARCHAR(255) NOT NULL,
                popis TEXT,
                stav ENUM('Nezahájená', 'Prebieha', 'Hotová') DEFAULT 'Nezahájená',
                datum_vytvoreni DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        spojenie.commit()
        cursor.close()
        print("🧱 Tabuľka 'ulohy' bola pripravená.")
    except Error as e:
        print("❌ Chyba pri vytváraní tabuľky:", e)

# Hlavné menu
def hlavne_menu():
    print("\nSprávca úloh - Hlavné menu")
    print("1. Pridať novú úlohu")
    print("2. Zobraziť úlohy")
    print("3. Aktualizovať úlohu")
    print("4. Odstrániť úlohu")
    print("5. Ukončiť program")
    volba = input("Vyberte možnosť (1-5): ")
    return volba

# Pridanie úlohy
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

# Zobrazenie úloh
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

# Aktualizácia stavu úlohy
def aktualizovat_ulohu(spojenie):
    cursor = spojenie.cursor()
    try:
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

# Odstránenie úlohy
def odstranit_ulohu(spojenie):
    cursor = spojenie.cursor()
    try:
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

        cursor.execute("SELECT * FROM ulohy WHERE id = %s", (id_ulohy,))
        if cursor.fetchone() is None:
            print("❌ Úloha s takým ID neexistuje.")
            return

        cursor.execute("DELETE FROM ulohy WHERE id = %s", (id_ulohy,))
        spojenie.commit()
        print(f"🗑️ Úloha s ID {id_ulohy} bola odstránená.")
    except Error as e:
        print("❌ Chyba pri odstraňovaní úlohy:", e)

# --- Spustenie programu ---
if __name__ == "__main__":
    spojenie = pripojenie_db()
    vytvor_tabulku(spojenie)

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
            spojenie.close()
            break
        else:
            print("❌ Neplatná voľba. Skús znova.")
