# CSV-analys i Jupyter Notebook

## Mål
Bygga en Jupyter-notebook som läser CSV-data, besvarar användarens frågor om datan (till exempel medelvärde, max och min) och hämtar data från en extern källa via ett API som endast accepterar CSV.

## Metod
1. Läsa in exempeldatan `employees.csv` (15 anställda) med pandas
2. Skapa klassen `CSVAnalyzer` med metoder för att analysera datan: `info()`, `calculate()`, `group_by()` och `answer()`
3. Hämta CSV-data från en länk med klassen `CSVFetcher` (requests) som kontrollerar länken, statuskod, innehållstyp och storlek och avvisar allt som inte är CSV (till exempel JSON och HTML)
4. Köra ett Flask-API (`/analyze` och `/ask`) i en bakgrundstråd i notebooken och anropa det från en klient med `requests`
5. Visualisera resultat med matplotlib

Så här kör du projektet:

```
pip install notebook pandas requests flask matplotlib
jupyter notebook
```

Öppna `csv_analyzer.ipynb` och kör cellerna uppifrån och ner med `Shift + Enter`. Celler markerade **(interactive)** låter dig skriva egna frågor, och med `quit` går du vidare.

## Resultat
Resultat för `employees.csv` (15 rader, kolumnerna `name`, `department`, `age`, `salary`, `experience`):

1. Medelvärde för lön (`average salary`): 64 733,33
2. Summa av lön (`sum salary`): 971 000
3. Median för lön (`median salary`): 60 000
4. Högsta ålder (`max age`): 50
5. Lägsta erfarenhet (`min experience`): 2 år

Medellön per avdelning (`average salary by department`):

| Avdelning | Medellön |
|---|---|
| IT | 83 750 |
| Finance | 66 666,67 |
| Sales | 57 500 |
| Marketing | 53 000 |
| HR | 50 000 |

API:et avvisar data som inte är CSV. En JSON-fil gav felet `Only CSV data is accepted (got: application/json)`, en saknad fil gav statuskod 404 och en länk som `ftp://...` avvisades som ogiltig.

## Analys
Resultatet visar att IT har den högsta medellönen och HR den lägsta i exempeldatan. Medianen (60 000) ligger under medelvärdet (64 733), vilket tyder på att några höga löner, till exempel inom IT, drar upp snittet. Datan är påhittad exempeldata, så siffrorna säger inget om verkliga löner.

Projektet visar också hur samma analysklass kan användas på tre sätt: direkt på en lokal fil, på data som hämtas från en länk och via ett API. Valideringen i `CSVFetcher` gör att programmet ger tydliga felmeddelanden i stället för att krascha när datan inte är CSV.

## Reflektion
Det svåraste var att få servrarna att fungera inuti notebooken. Filservern (port 8000) och API:et (port 5000) körs i bakgrundstrådar, och om en port redan är upptagen eller cellerna körs i fel ordning slutar det fungera. Därför lade jag till en cell som stoppar båda servrarna. Nästa gång skulle jag lägga till automatiska tester och en lista över tillåtna domäner i API:et, eftersom det annars hämtar vilken länk som helst, samt stöd för frågor som `count by department`.

## GitHub-länk
https://github.com/<ditt-användarnamn>/<repo-namn>
