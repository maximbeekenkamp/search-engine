Search Project:
Maxim Beekenkamp

We have zero known bugs.

The user should first type in python3 <index.py filepath> <wiki filepath> <titles filepath> 
<docs filepath> <words filepath>. This will run the indexer on the input wiki and output the 
contents of the id to titles dictionary in the titles txt file, the pagerankprime dictionary in the
docs txt file, and the words to rel dictionary in the words txt file. 
Then the user should input python3 <query.py filepath> [--pagerank] <titles filepath> <docs filepath> 
<words filepath> where [--pagerank] is an optional argument allowing the user to toggle between no 
pagerank and pagerank. This launches the REPL. The user can then enter a word / phrase and the top 10
(if possible) most relevant documents will be returned. This process can be repeated ad infinitum or 
until the user types in the keyword "quit".

The index.py consists of three main parts: a parser, which populates all our dictionaries and parses the
input xml file, a relevancy algorithm, which calculates the tf*idf for each word in the corpus, and the 
pagerank algorithm, which calulates the pagerank for each link after convergence. 

The query consists of four main parts: a repl, which prompts the user to provide a search input, a parser,
which turns this user input into a list for our scores, and two score algorithms one for with pagerank and
one for without pagerank. 

These two components comunicate via the file_io program which allows our indexing to be pre computed in the 
indexer and then be referenced (without calculations) in our query.

System Testing:

If the user inputs an invalid file we will raise a FileNotFoundError with the statement "Input error."
If the user inputs an invalid number of inputs we will raise an AttributeError with the statement
"Invalid inputs." for query and "Invalid number of inputs. There must be exactly four inputs." for 
index.

We have reasonable confidence that our query is functioning as expected due to comparison
with the provided TA results in the MedWiki google doc. 

For baseball without pagerank we got:
oakland athlet
minor league basebal
miami marlin
fantasy sport
kenesaw mountain landi
out
october 30
january 7
hub
february 2

All 10 of these are found within the top 20 of the TA query. These are also the exact same
top 10 in the same order.

For baseball with pagerank we got:
netherland
ohio
kenesaw mountain landi
minor league basebal
february 2
illinoi
pennsylvania
kansa
louisiana
michigan

All 10 of these are found within the top 20 of the TA query.

For the fire without pagerank we got:
firewall (construction)
pale fir
ride the lightn
g?tterd?mmerung
fsb
keiretsu
hephaestu
kab-500kr
izabella scorupco
justin martyr

All 10 of these are found within the top 20 of the TA query. These are also the exact same
top 10 in the same order.

For fire with pagerank we got:
hinduism
empress suiko
justin martyr
new amsterdam
nazi germani
planet
guam
falklands war
hephaestu
hermann g?r

All 10 of these are found within the top 20 of the TA query.

For cats without pagerank we got:
kattegat
kiritimati
morphology (linguistics)
northern mariana island
lynx
freyja
politics of lithuania
isle of man
nirvana (uk band)
john ambrose flem

All 10 of these are found within the top 20 of the TA query. These are also the exact same
top 10 in the same order.

For cats with pagerank we got:
netherland
pakistan
hong kong
portug
morphology (linguistics)
northern mariana island
normandi
george berkeley
illinoi
pope

All 10 of these are found within the top 20 of the TA query.

For United States without pagerank we got:
federated states of micronesia
imperial unit
joul
knowledge aided retrieval in activity context
imperialism in asia
elbridge gerri
martin van buren
pennsylvania
finite-state machin
louisiana

All 10 of these are found within the top 20 of the TA query. These are also the exact same
top 10 in the same order.

For United States with pagerank we got:
netherland
pakistan
monarch
portug
govern
nazi germani
illinoi
ohio
norway
michigan

8 of these are found within the top 20 of the TA query.

For united without pagerank we got:
imperial unit
joul
gauss (unit)
imperialism in asia
knowledge aided retrieval in activity context
inch
elbridge gerri
fsb
martin van buren
los angeles international airport

All 10 of these are found within the top 20 of the TA query. These are also the exact same
top 10 in the same order.

For united with pagerank we got:
netherland
pakistan
portug
monarch
norway
franklin d. roosevelt
nazi germani
illinoi
ohio
govern

9 of these are found within the top 20 of the TA query.