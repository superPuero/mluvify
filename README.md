# mluvify 

# Dokumentace k softwaru pro analýzu řeči a detekci kognitivního deficitu

Tato dokumentace popisuje analytický systém navržený pro hodnocení spontánního mluveného projevu. Cílem systému je kvantifikovat lingvistické a sémantické vzorce, které slouží jako biomarkery pro detekci kognitivního poklesu, neurodegenerativních onemocnění (např. Alzheimerova choroba, demence) či specifických řečových patologií (afázie).

Metriky jsou rozděleny podle své diskriminační síly na klíčové (primární indikátory patologie), doplňkové a vyřazené.

---

## 1. Klíčové diagnostické metriky (Váha: Vysoká)
Tyto moduly prokázaly v testování nejvyšší schopnost rozlišit zdravý mozek od kognitivně narušeného. Zaměřují se na detekci perseverace (zacyklení) a lexikálního vyčerpání.

### 1.1 Lexikální bohatost (Lexical Richness)
Modul měří velikost aktivní slovní zásoby a schopnost mluvčího neopakovat se.
* **MTLD (Measure of Textual Lexical Diversity):** Nejsilnější a nejspolehlivější parametr modulu. Počítá průměrný počet slov, který mluvčí vyprodukuje, než lexikální bohatost (TTR) klesne pod kritickou hranici 0,72. Je plně imunní vůči celkové délce textu.
  * *Klinický význam:* U zdravých jedinců se hodnoty pohybují vysoko (> 60). Hodnoty pod 30 indikují sémantickou anomii a rychlé vyčerpání slovní zásoby.
* **TTR (Type-Token Ratio):** Poměr unikátních slov (types) ku všem slovům (tokens). Vypočte se jako $TTR = \frac{Types}{Tokens}$.
* **MATTR a HDD:** Pokročilé pravděpodobnostní a klouzavé modely, které potvrzují stabilitu lexikálního profilu.

### 1.2 Míra opakování slov (Lexikální redundance)
* **count_repeated_words:** Metrika vyjadřující procentuální podíl duplicitních slov v textu (na základě lemmatizace).
  * *Klinický význam:* Odhaluje rigidní perseveraci. Zatímco zdravý mluvčí vykazuje přirozenou redundanci gramatických pojiv (kolem 0,20 - 0,30), u pacientů s patologií hodnota přesahuje 0,50 (každé druhé slovo je zopakováno).

### 1.3 Speech Graph (Graf řeči)
Převádí text na orientovaný graf, kde uzly představují unikátní slova a hrany jejich sekvenční napojení. Měří "topologii" myšlenek nezávisle na gramatice.
* **L1 Loops (Smyčky délky 1):** Počet případů, kdy slovo ukazuje samo na sebe (okamžité zopakování, např. „pěšky, pěšky“). Značí silné motorické nebo kognitivní zasekávání.
* **L2 Loops (Smyčky délky 2):** Návrat ke slovu přes jedno jiné slovo (např. „u té, u velké“).
* **Clustering Coefficient:** Měří tvorbu sémantických „bublin“. Vysoká hodnota (např. > 0,10) značí, že mluvčí uvízl v izolovaném shluku slov a nedokáže plynule navázat novým tématem.
* **Density (Hustota):** Měří propletenost sítě pomocí vzorce $Density = \frac{E}{N(N-1)}$ (kde $E$ jsou hrany a $N$ uzly).

---


## 2. Metriky vyřazené z finálního skórování
Během testování bylo zjištěno, že následující metriky zanášejí do výsledků šum, jsou snadno zmanipulovatelné nebo mají pro mluvenou češtinu nízkou diskriminační hodnotu. Jsou součástí kódu, ale nedoporučuje se je využívat pro diagnostiku:

* **Perplexity:** Jazykové modely (LLM) vyhodnocují u zacyklených pacientů perplexitu často jako nízkou (v normě), protože pacienti generují jednoduché, i když zmatené věty. Naopak zdravá a kreativní řeč perplexitu uměle zvyšuje.
* **Detekce nedokončených vět (Incomplete Sentences) a oprav (Repairs):** V mluvené češtině je příliš závislá na kvalitě interpunkce z ASR (Automatic Speech Recognition) modelu a vede k vysoké chybovosti. Lepších výsledků se dosahuje pomocí grafu řeči (smyčky).
* **Podíl obsahových a funkčních slov (POS ratio):** Zacyklený pacient často opakuje podstatná jména, čímž matematicky udržuje normální poměr obsahových slov, i když je řeč fakticky prázdná.
* **Akustické metriky a tempo řeči (Speech Rate, Pauzy):** Průměrná délka pauzy nebo tempo řeči nerozlišuje spolehlivě mezi úzkostným pacientem (který mluví rychle a zmateně) a zdravým člověkem, který dělá přirozené, dlouhé dramatické pauzy při vzpomínání.

---

## 3. Výpočet Kognitivního Deficit Indexu (KDI)
Pro potřeby klasifikace je navržen agregovaný index, který normalizuje a váží nejspolehlivější hodnoty do jednoho skóre.

Návrh koncepčního vzorce kombinuje penalizační koeficienty:

$$KDI = \alpha \cdot P_{MTLD} + \beta \cdot P_{Repetition} + \gamma \cdot P_{Loops} + \delta \cdot P_{Drift}$$

Kde:
* $P_{MTLD}$ je penalizace za kriticky nízkou hodnotu MTLD (např. < 30).
* $P_{Repetition}$ je hodnota přímo z metriky `count_repeated_words`.
* $P_{Loops}$ je penalizace za vysoký výskyt uzlů typu L1.
* $P_{Drift}$ je penalizace za absenci posunu tématu na konci promluvy.

*(Pozn.: Přesné hodnoty vah $\alpha, \beta, \gamma, \delta$ je nutné kalibrovat na větším klinickém datasetu, přičemž nejvyšší váhu by měly nést moduly MTLD a Repetition).*
