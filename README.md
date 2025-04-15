# 🗂️ Task Manager 1.1

**Task Manager 1.1** je vylepšená verzia jednoduchého správcu úloh vytvoreného v Pythone.  
Úlohy sa už neukladajú len do pamäťového zoznamu, ale trvalo do **MySQL databázy**, čo umožňuje skutočnú CRUD funkcionalitu – vytvárať, čítať, aktualizovať a mazať úlohy.

---

## ✨ Čo som implementoval

- Odstránil som používanie zoznamu v pamäti (`ulohy = []`) a nahradil ho trvalým uložením v MySQL databáze.
- Pridal som automatické vytvorenie databázy `task_manager_1_1` (ak ešte neexistuje) priamo v kóde.
- Vytvoril som tabuľku `ulohy` s atribútmi:
  - `id`, `nazov`, `popis`, `stav`, `datum_vytvoreni`
- Implementoval som kompletné CRUD operácie:
  - `Create` – Pridanie úlohy
  - `Read` – Zobrazenie aktívnych úloh (iba Nezahájená alebo Prebieha)
  - `Update` – Zmena stavu úlohy na *Prebieha* alebo *Hotová*
  - `Delete` – Odstránenie úlohy podľa ID
- Pridal som validáciu vstupov (názov a popis musia byť vyplnené).
- Pripojenie k databáze a vytvorenie štruktúry je automatizované – netreba ručne vytvárať databázu ani tabuľku.
- Upravil som konzolové menu podľa požiadaviek zadania – obsahuje všetkých 5 možností:
  1. **Pridať novú úlohu** – umožňuje vložiť názov a popis (s validáciou).
  2. **Zobraziť úlohy** – vypíše všetky aktívne úlohy (stav: Nezahájená alebo Prebieha).
  3. **Aktualizovať úlohu** – umožňuje zmeniť stav úlohy na *Prebieha* alebo *Hotová*.
  4. **Odstrániť úlohu** – zmaže úlohu podľa jej ID z databázy.
  5. **Ukončiť program** – korektne ukončí beh aplikácie a uzatvorí spojenie s databázou.

---

## 🔁 Porovnanie s predchádzajúcou verziou:

| Funkcia            | Verzia 1.0                     | Verzia 1.1                                         |
|--------------------|-------------------------------|----------------------------------------------------|
| Ukladanie úloh     | do zoznamu v pamäti            | do MySQL databázy (trvalé)                         |
| Validácia vstupov  | neexistovala                   | názov aj popis sú povinné                          |
| Aktualizácia stavu | neexistovala                   | možnosť zmeniť stav úlohy                          |
| Odstránenie úlohy  | podľa poradia v zozname        | podľa ID v databáze                                |
| Pripojenie k DB    | žiadne                         | automatické + vytvára databázu a tabuľku           |
| Konzolové menu     | 4 možnosti                     | 5 možností, plné CRUD, konzistentné správy         |

---

## 🧰 Použité technológie

- Python 3
- MySQL databáza
- `mysql-connector-python`
- MySQL Workbench (voliteľne – na vizuálnu kontrolu údajov)

---

## ▶️ Ako projekt spustiť

1. **Uisti sa, že máš spustený MySQL server** (napr. cez XAMPP alebo MySQL Workbench)
2. Nainštaluj knižnicu `mysql-connector-python` (ak ešte nie je):
-pip install mysql-connector-python
3. Otvor súbor `task_manager_1_1.py` a uprav prihlasovacie údaje, ak používaš iné (napr. `user="root", password="tvojeheslo"`).
4. Spusti skript: python task_manager_1_1.py
5. ✅ Pri prvom spustení sa databáza `task_manager_1_1` aj tabuľka `ulohy` automaticky vytvoria – netreba nič ručne vytvárať.

---

## 🧪 Bonus

Môžeš si overiť záznamy cez MySQL Workbench:
```sql
USE task_manager_1_1;
SELECT * FROM ulohy;
