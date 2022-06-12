# MDS Jetpack
Jocul a fost gândit și creat de echipa: Culea Ionel Alexandru, Hodoroabă Ștefan Emanuel, Lazăr Mihai, Niculae Tiberiu Constantin.
<<<<<<< HEAD
=======
=======
# <img align="left" src="https://github.com/bestman4111/Laborator-MDS/blob/main/PROIECT/res/jetpack.png" width="38">MDS Jetpack
Aplicația a fost gândită și creată de echipa formată din: Culea Ionel-Alexandru, Hodoroabă Ștefan-Emanuel, Lazăr Mihai, Niculae Tiberiu-Constantin.

## Descrierea proiectului
Aplicația constă într-un joc de tip "endless runner", cu grafica 2D, ce este asemănător cu jocul Jetpack Joyride.

În jocul nostru, scopul este să ajungi cât mai departe, strângând în același timp și un număr cât mai mare de bănuți, suma dintre metri parcurși și numărul de bănuți strânși reprezentând scorul final.

După terminarea numărului de vieți, cât timp s-au acumulat cel puțin 200 de bănuți, jucătorul va avea oportunitatea de a cumpăra o viață în plus. Prelungindu-și timpul de joc.

Aplicația este dezvoltată în limbajul Python, pentru sistemul de operare Windows.

## Demo
Demo-ul jocului nostru poate fi gasit [aici](https://www.youtube.com/watch?v=e4r82uQ2hro).

## User stories
User stories reprezintă cerințele utilizatorilor cu privire la aplicația dezvoltată.

Cerințele la care aplicația noastră răspunde sunt:

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

Pentru a rula testele, folosim script-ul run_tests.py. Acesta parseaza directoarele ce conțin modulele cu teste, urmând să apeleze testele găsite.

## Bug reporting
O parte din bug-urile sesizate sunt urmatoarele:

1. Atunci când se apela funcția PlayNewScene(), scena se schimba, dar aplicația se bloca.
2. Textul unui buton atașat la RenderedObject nu se află pe buton.
3. La o primă încărcare, meniul funcționează așa cum trebuie, însă dacă este încărcat din nou, niciunul dintre butoane nu funcționează.

Aceste bug-uri au fost sesizate în secțiunea Issues și au fost rezolvate în commit-uri ulterioare.

## Build tool
Pentru a realiza aplicația, s-a folosit programul Visual Studio Code al celor de la Microsoft. Pentru a face build aplicației, ca să putem exporta sub formă de executabil, am folosit un pachet Python numit PyInstaller.

## Refactoring
Inițial, interfața prin care cumperi vieți era încorporată în clasa GameSession, clasă ce presupune jocul efectiv. Ulterior, această interfață a fost mutată într-un modul separat.

## Design patterns
În procesul de dezvoltare a aplicației noastre, am folosit următoarele concepte de Design pattern:

•	Singleton (clasele App, EventsManager, UpdateScheduler)

•	Observer, modul de funcționare al claselor EventsManager și UpdateScheduler: (se înregistrează metode ce urmează să fie apelate în funcție de situație)

## Diagrama UML
<p align="center">
  <img src="https://github.com/bestman4111/Laborator-MDS/blob/main/PROIECT/diagrama.png" width="600">
</p>
>>>>>>> a493dcf (Modificat README)
>>>>>>> 70193d0 (Actualizat README)
