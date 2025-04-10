# 🗂️ Task Manager 1.1

**Task Manager 1.1** je vylepšená verzia jednoduchého správcu úloh vytvoreného v Pythone.  
Úlohy sa už neukladajú len do pamäťového zoznamu, ale trvalo do **MySQL databázy**, čo umožňuje skutočnú CRUD funkcionalitu – vytvárať, čítať, aktualizovať a mazať úlohy.

---

## ✨ Čo som implementoval

- Odstránil som používanie zoznamu v pamäti (`ulohy = []`) a nahradil ho trvalým uložením v MySQL databáze.
- Vytvoril som tabuľku `ulohy` s atribútmi:
  - `id`, `nazov`, `popis`, `stav`, `datum_vytvorenia`
- Pridal som funkciu `pripojenie_db()` na bezpečné pripojenie k databáze.
- Implementoval som kompletné CRUD operácie:
  - `Create` – Pridanie úlohy
  - `Read` – Zobrazenie aktívnych úloh (iba Nezahájená alebo Prebieha)
  - `Update` – Zmena stavu úlohy na *Prebieha* alebo *Hotová*
  - `Delete` – Odstránenie úlohy podľa ID
- Pridal som validáciu vstupov (názov a popis musia byť vyplnené).
- Upravil som konzolové menu podľa požiadaviek zadania – obsahuje všetkých 5 možností:
  1. **Pridať novú úlohu** – umožňuje vložiť názov a popis (s validáciou).
  2. **Zobraziť úlohy** – vypíše všetky aktívne úlohy (stav: Nezahájená alebo Prebieha).
  3. **Aktualizovať úlohu** – umožňuje zmeniť stav úlohy na *Prebieha* alebo *Hotová*.
  4. **Odstrániť úlohu** – zmaže úlohu podľa jej ID z databázy.
  5. **Ukončiť program** – korektne ukončí beh aplikácie.

## 🔁 Porovnanie s predchádzajúcou verziou:

🔹 Ukladanie úloh:
- 1.0: do pamäťového zoznamu (stratí sa po vypnutí)
- 1.1: do MySQL databázy (trvalé uloženie)

🔹 Validácia vstupov:
- 1.0: mohol si zadať prázdny názov alebo popis
- 1.1: názov aj popis sú povinné

🔹 Aktualizácia stavu:
- 1.0: neexistovala
- 1.1: možnosť zmeniť stav na „Prebieha“ alebo „Hotová“

🔹 Odstránenie úlohy:
- 1.0: vymazanie podľa poradia v zozname
- 1.1: vymazanie podľa ID z databázy

🔹 Konzolové menu:
- 1.0: 4 možnosti (bez aktualizácie a bez validácie)
- 1.1: 5 možností (plné CRUD, validácia, pripojenie k DB)

---

## 🧰 Použité technológie

- Python 3
- MySQL databáza
- `mysql-connector-python`
- MySQL Workbench

---

## ▶️ Ako projekt spustiť

> **ℹ️ Poznámka pre kontrolu:**  
> Projekt vyžaduje lokálnu MySQL databázu.  
> V prípade, že databáza `task_manager_1_1` ešte neexistuje, je potrebné ju vytvoriť podľa pokynov nižšie.  
> Všetky SQL príkazy sú pripravené, stačí ich vložiť do MySQL Workbench.

1. Vytvor databázu `task_manager_1_1` v MySQL.
   CREATE DATABASE task_manager_1_1;
3. V rámci nej vytvor tabuľku `ulohy` pomocou SQL:
   
```sql
CREATE TABLE IF NOT EXISTS ulohy (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nazov VARCHAR(255) NOT NULL,
    popis TEXT NOT NULL,
    stav ENUM('Nezahájená', 'Prebieha', 'Hotová') DEFAULT 'Nezahájená',
    datum_vytvorenia TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

3. V súbore task_manager_1_1.py si uprav prihlasovacie údaje k databáze podľa svojho lokálneho nastavenia (napr. user="root", password="1234").
4. Spusti skript cez terminál pomocou príkazu: python task_manager_1_1.py
