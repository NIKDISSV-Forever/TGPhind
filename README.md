# TGPhind

Find the article you need *([telegra.ph](https://telegra.ph/)/[te.legra.ph](https://te.legra.ph/)/[graph.org](https://graph.org/))*
----------

## Установка:


### Linux / Termux:

*Any: ```apt```, ```pkg```, ```dpkg```*

```apt upgrade -y && apt update -y```

```apt install git python -y```

```git clone https://github.com/NIKDISSV-Forever/TGPhind/```

```cd TGPhind```


### Windows / MacOS:

**Python:** [Downdload](https://www.python.org/downloads/) (*Intsall PATH*)

**Git:** [Download](https://git-scm.com/downloads)

### cmd:

```git clone https://github.com/NIKDISSV-Forever/TGPhind/```

```cd TGPhind```



## Запуск:


### cmd / PowerShell:

```py main.py``` **query** *-ARGV*


### Linux Terminal:

```python3 main.py``` **query** *-ARGV*

## query:

*Any text* **and** *[...]* - *For templating text*


**exampl[e es ing]** *(Specified through any " \t\n\r\v\f")*

**A search will be made for 4 options, these are**
: "exampl", "example", "examples", "exampling"

**The range of characters is indicated by _"-"_**

**g[a-z]d**

**any letter of the English alphabet between _g_ and _d_, _27_ options in total.**
: 'gad', 'gbd', 'gcd', 'gd', 'gdd', 'ged', 'gfd', 'ggd', 'ghd', 'gid', 'gjd', 'gkd', 'gld', 'gmd', 'gnd', 'god', 'gpd', 'gqd', 'grd', 'gsd', 'gtd', 'gud', 'gvd', 'gwd', 'gxd', 'gyd', 'gzd'


## -ARGV:

**-mm**
: month range *(Specified through "-")*

**-dd**
: days range *(Specified through "-")*

**-fd**
: folder with found results *(default **found**)*

**-opnRes**
: Open the file with the results.

**-noOut**
: Removes printing anything on the screen *(Except for the banner)*

**-noMirrors**
: No mirrors will be recorded. *only telegra.ph*

**--**
: Does not remove the **-** sign in transcription.
