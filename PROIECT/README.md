# MDS Jetpack
Jocul a fost gândit și creat de echipa: Culea Ionel Alexandru, Hodoroabă Ștefan Emanuel, Lazăr Mihai, Niculae Tiberiu Constantin.

## Descrierea proiectului
Aplicația constă într-un joc de tip "endless runner", cu grafica 2D, ce este asemănător cu jocul Jetpack Joyride.

În jocul nostru, scopul este să ajungi cât mai departe, strângând în același timp și un număr cât mai mare de bănuți, suma dintre metri parcurși și numărul de bănuți strânși reprezentând scorul final.

După terminarea numărului de vieți, cât timp s-au acumulat cel puțin 200 de bănuți, jucătorul va avea oportunitatea de a cumpăra o viață în plus. Prelungindu-și timpul de joc.

Aplicația este dezvoltată în limbajul Python, pentru sistemul de operare Windows.

## Demo
Demo-ul jocului nostru poate fi gasit [aici](https://www.youtube.com/watch?v=e4r82uQ2hro).

## User stories
User stories reprezintă niște probleme ridicate de oameni pe care aplicația noastră le rezolvă.

Împreună, am reușit să compunem următoarele 10:

1. Jocul va fi de tip "Endless runner".
2. Jocul va conține diverse obstacole ce vor apărea în mod aleatoriu și vor încheia sesiunea de joc în momentul coliziunii cu jucătorul.
3. În cazul în care jocul se încheie prin coliziunea cu un obstacol, jucătorul poate continua sesiunea de joc dacă acesta mai are "vieți".
4. Jocul va crește în dificultate pe măsură ce scorul crește.
5. Pe parcursul jocului, jucătorul poate colecta monede ce îl vor ajuta să cumpere vieți. La finalul jocului, monedele rămase vor contribui la scor.
6. La finalul jocului, jucătorul va putea să-și salveze scorul.
7. Sesiunea de joc va avea opțiunea de pauză.
8. Aplicația va avea o secțiune de instrucțiuni ce arată controalele, descrie desfășurarea jocului și scopul acestuia.
9. Aplicația va putea fi pusă pe mute atât din meniul principal, cât și din timpul jocului.
10. Aplicația va avea o secțiune de High Scores.

## Teste automate
Testele sunt făcute cu framework-ul unittest din Python. Testele concepute de noi se împart în două categorii: teste de pe partea de framework a aplicației și teste pentru logica aplicației. Fiecare test verifică o anumită funcționalitate a framework-ului, respectiv a aplicației și sunt independente între ele.

Fiecare gamă de teste – teste ce pot fi grupate – este pusă în câte o clasă, cu o denumire oarecare, dar care moștenește clasa unittest.TestCase. Fiecare metodă a claselor definite de noi, exceptând câteva metode mai speciale, reprezintă un test. Fiecare denumire de metodă-test trebuie să înceapă cu ”test_”, altfel nu e luată în considerare la procesul de testare. Scopul unei metode-test este să facă assert-uri, adică să facă efectiv verificarea relevantă metodei testate (de preferat, fiecare metodă să aibă un singur assert).

Metodele speciale folosite de noi sunt:

•	setUp() și tearDown(), metode ce se apelează la fiecare test, setUp inainte de test, iar tearDown dupa test

•	setUpClass() și tearDownClass(), metode ce se apelează la începutul, respectiv la sfârșitul rulării testelor din acea clasă

Aceste metode speciale funcționează precum constructorii și destructorii.

Pentru a defini testele mai rapid, în același folder sunt un modul cu constante și un folder cu resurse, pe care le folosim de mai multe ori.

Pentru a rula testele, folosim script-ul run_tests.py. Acesta parseaza directoarele cu module de teste (unittest.TestLoader) și apoi le apelează (unittest.TextTestRunner).

## Bug reporting
Au fost întâlnite următoarele bug-uri:

1. Atunci când se apela funcția PlayNewScene(), scena se schimba, dar aplicația se bloca.
2. Textul unui buton atașat la RenderedObject nu se află pe buton.
3. La o primă încărcare, meniul funcționează așa cum trebuie, însă dacă este încărcat din nou, niciunul dintre butoane nu funcționează.

Aceste bug-uri au fost sesizate în secțiunea Issues, de pe platforma GitHub și au fost rezolvate în commit-uri ulterioare.

## Build tool
Pentru a realiza aplicația, s-a folosit programul Visual Studio Code al celor de la Microsoft. Pentru a face build aplicației, ca să putem exporta sub formă de executabil, am folosit un pachet Python numit PyInstaller.

## Refactoring
Inițial, interfața prin care cumperi vieți era încorporată în clasa GameSession, clasă ce presupune jocul efectiv. Ulterior, această interfață a fost mutată într-un modul separat.

## Design patterns
În procesul de dezvoltare a aplicației noastre, am folosit următoarele concepte de Design pattern:

•	Singleton (clasele App, EventsManager, UpdateScheduler)

•	Observer, modul de funcționare al claselor EventsManager și UpdateScheduler: înregistrez metode în acele clase ce urmează să fie apelate atunci când apar evenimente (EventManager) sau când apare un nou frame al aplicatiei (UpdateScheduler)

## Diagrama UML
![UML](https://github.com/bestman4111/Laborator-MDS/blob/main/PROIECT/diagrama/diagrama.png)
