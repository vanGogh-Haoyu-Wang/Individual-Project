# SMOP
## 1. Check Python version
```
// vangogh@vangoghs-MacBook-Pro ~ % python3 --version

pip3 --version

Python 3.14.5

pip 26.1.1 from /Library/Frameworks/Python.framework/Versions/3.14/lib/python3.14/site-packages/pip (python 3.14)
```

## 2. Change Python version & Check Again
### 2.1 Change Version
```
vangogh@vangoghs-MacBook-Pro ~ % brew install python@3.11

Inspect the formula dependency plan before installing with `brew install --ask`.

Enable ask mode by setting `HOMEBREW_ASK=1`.

Hide these hints with `HOMEBREW_NO_ENV_HINTS=1` (see `man brew`).

==> **Fetching downloads for:** **python@3.11**

✔︎ Bottle Manifest python@3.11 (3.11.15_1)                                                    Downloaded   26.2KB/ 26.2KB

✔︎ Bottle python@3.11 (3.11.15_1)                                                             Downloaded   15.6MB/ 15.6MB

==> **Pouring python@3.11--3.11.15_1.arm64_tahoe.bottle.tar.gz**

==> **/opt/homebrew/Cellar/python@3.11/3.11.15_1/bin/python3.11 -Im ensurepip**

==> **/opt/homebrew/Cellar/python@3.11/3.11.15_1/bin/python3.11 -Im pip install -v --no-index --upgrade --isolated --targe**

==> **Caveats**

Python is installed as

  /opt/homebrew/bin/python3.11

  

Unversioned and major-versioned symlinks `python`, `python3`, `python-config`, `python3-config`, `pip`, `pip3`, etc. pointing to

`python3.11`, `python3.11-config`, `pip3.11` etc., respectively, are installed into

  /opt/homebrew/opt/python@3.11/libexec/bin

  

You can install Python packages with

  pip3.11 install <package>

They will install into the site-package directory

  /opt/homebrew/lib/python3.11/site-packages

  

`idle3.11` requires tkinter, which is available separately:

  brew install python-tk@3.11

  

gdbm (`dbm.gnu`) is no longer included in this formula, but it is available separately:

  brew install python-gdbm@3.11

`dbm.ndbm` changed database backends in Homebrew Python 3.11.

If you need to read a database from a previous Homebrew Python created via `dbm.ndbm`,

you'll need to read your database using the older version of Homebrew Python and convert to another format.

`dbm` still defaults to `dbm.gnu` when it is installed.

  

If you do not need a specific version of Python, and always want Homebrew's `python3` in your PATH:

  brew install python3

  

For more information about Homebrew and Python, see: https://docs.brew.sh/Homebrew-and-Python

==> **Summary**

🍺  /opt/homebrew/Cellar/python@3.11/3.11.15_1: 3,306 files, 64.9MB

==> **Running `brew cleanup python@3.11`...**

Disable this behaviour by setting `HOMEBREW_NO_INSTALL_CLEANUP=1`.

Hide these hints with `HOMEBREW_NO_ENV_HINTS=1` (see `man brew`).
```
### 2.2 Check Again
```
vangogh@vangoghs-MacBook-Pro ~ % /opt/homebrew/bin/python3.11 --version

Python 3.11.15
vangogh@vangoghs-MacBook-Pro ~ %
```
## 3. Create independent environment
### 3.1 Try to create
```
vangogh@vangoghs-MacBook-Pro ~ % mkdir ~/smop-test
cd ~/smop-test

python3.11 -m venv venv
source venv/bin/activate

(venv) vangogh@vangoghs-MacBook-Pro ~ %
```
### 3.2 Upgrade pip
```
(venv) vangogh@vangoghs-MacBook-Pro smop-test % pip install --upgrade pip setuptools wheel

Requirement already satisfied: pip in ./venv/lib/python3.11/site-packages (26.1)

Collecting pip

  Using cached pip-26.1.1-py3-none-any.whl.metadata (4.6 kB)

Requirement already satisfied: setuptools in ./venv/lib/python3.11/site-packages (82.0.1)

Collecting wheel

  Using cached wheel-0.47.0-py3-none-any.whl.metadata (2.3 kB)

Collecting packaging>=24.0 (from wheel)

  Using cached packaging-26.2-py3-none-any.whl.metadata (3.5 kB)

Using cached pip-26.1.1-py3-none-any.whl (1.8 MB)

Using cached wheel-0.47.0-py3-none-any.whl (32 kB)

Using cached packaging-26.2-py3-none-any.whl (100 kB)

Installing collected packages: pip, packaging, wheel

  Attempting uninstall: pip

    Found existing installation: pip 26.1

    Uninstalling pip-26.1:

      Successfully uninstalled pip-26.1

Successfully installed packaging-26.2 pip-26.1.1 wheel-0.47.0
```
### 3.3 Install SMOP reliance
```

(venv) vangogh@vangoghs-MacBook-Pro smop-test % pip install numpy networkx ply

Collecting numpy

  Downloading numpy-2.4.6-cp311-cp311-macosx_14_0_arm64.whl.metadata (6.6 kB)

Collecting networkx

  Downloading networkx-3.6.1-py3-none-any.whl.metadata (6.8 kB)

Collecting ply

  Downloading ply-3.11-py2.py3-none-any.whl.metadata (844 bytes)

Downloading numpy-2.4.6-cp311-cp311-macosx_14_0_arm64.whl (5.5 MB)

   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 5.5/5.5 MB 24.4 MB/s  0:00:00

Downloading networkx-3.6.1-py3-none-any.whl (2.1 MB)

   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.1/2.1 MB 52.0 MB/s  0:00:00

Downloading ply-3.11-py2.py3-none-any.whl (49 kB)

Installing collected packages: ply, numpy, networkx

Successfully installed networkx-3.6.1 numpy-2.4.6 ply-3.11

(venv) vangogh@vangoghs-MacBook-Pro
```
### 3.4 Install SMOP
```
(venv) vangogh@vangoghs-MacBook-Pro smop-test % pip install smop

Collecting smop

  Downloading smop-0.41.tar.gz (87 kB)

  Installing build dependencies ... done

  Getting requirements to build wheel ... done

  Preparing metadata (pyproject.toml) ... done

Requirement already satisfied: ply in ./venv/lib/python3.11/site-packages (from smop) (3.11)

Requirement already satisfied: numpy in ./venv/lib/python3.11/site-packages (from smop) (2.4.6)

Collecting scipy (from smop)

  Downloading scipy-1.17.1-cp311-cp311-macosx_14_0_arm64.whl.metadata (62 kB)

Requirement already satisfied: networkx in ./venv/lib/python3.11/site-packages (from smop) (3.6.1)

Downloading scipy-1.17.1-cp311-cp311-macosx_14_0_arm64.whl (20.3 MB)

   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 20.3/20.3 MB 26.9 MB/s  0:00:00

Building wheels for collected packages: smop

  Building wheel for smop (pyproject.toml) ... done

  Created wheel for smop: filename=smop-0.41-py3-none-any.whl size=49265 sha256=46f871b25986e75de765755bc4ce7393792a225b2661a129572a17e5258b1173

  Stored in directory: /Users/vangogh/Library/Caches/pip/wheels/3d/44/9f/1cb56e08e06b1cc047be93dc7ead2f9b8eddb3efa0d9d31353

Successfully built smop

Installing collected packages: scipy, smop

Successfully installed scipy-1.17.1 smop-0.41
```
## 4. Test
```
(venv) vangogh@vangoghs-MacBook-Pro smop-test % smop --help

usage: 

  

    smop [OPTIONS] [FILE1.m FILE2.m ...]

  

SMOP is Small Matlab and Octave to Python compiler, it takes MATLAB

files and translates them to Python.  The names of the resulting files

are derived from the names of the source files unless explicitly set

with -o .

  

positional arguments:

  file.m

  

options:

  -h, --help            show this help message and exit

  -A, --no-analysis     

                        skip analysis

  -B, --no-backend      

                        omit code generation

  -C, --no-comments     

                        discard multiline comments

  -D DEBUG, --debug DEBUG

                        Colon-separated codes.

                        M Main

                        L Lex

                        P Parse

  -E, --delete-on-error

                        By default, broken ".py" files are kept alive to allow their

                        examination and debugging. Sometimes we want the opposite behavior

  -g PATTERN, --glob-pattern PATTERN

                        Apply unix glob pattern to the input file list or to files. For

                        example -g 'octave-4.0.2/*.m

  -H, --no-header       

                        use it if you plan to concatenate the generated files

  -L, --debug-lexer     

                        enable built-in debugging tools

  -N, --no-numbers      

                        discard line-numbering information

  -o FILE.py, --output FILE.py

                        Write the results to FILE.py.  Use -o- to send the results to the

                        standard output.  If not specified explicitly, output file names are

                        derived from input file names by replacing ".m" with ".py".  For example,

                            $ smop FILE1.m FILE2.m FILE3.m

                        generates files FILE1.py FILE2.py and FILE3.py

  -P, --debug-parser    

                        enable built-in debugging tools

  -R, --no-resolve      

                        omit name resolution

  -S, --strict          

                        stop after first syntax error (by default compiles other .m files)

  -T, --testing-mode    

                        support special "testing" percent-bang comments used to write Octave

                        test suite.  When disabled, behaves like regular comments

  -x FILE1.m,FILE2.m,FILE3.m, --exclude FILE1.m,FILE2.m,FILE3.m

                        comma-separated list of files to ignore

  -V, --version         show program's version number and exit

  -v, --verbose

  -Z ARCHIVE.tar, --archive ARCHIVE.tar

                        Read ".m" files from the archive; ignore other files.  Accepted

                        format: "tar".  Accepted compression: "gzip", "bz2".

  

Example:

    $ wget ftp://ftp.gnu.org/gnu/octave/octave-4.0.2.tar.gz

    $ smop -a octave-4.0.2.tar.gz -g '*/scripts/*.m'

    $ ls -1 *.py | wc

    $ python -m py_compile *.py

    $ ls -1 *.pyc | wc
```
## 5. Test Transfer 
### 5.1 Create test file
```
(venv) vangogh@vangoghs-MacBook-Pro smop-test % nano test.m

a = 1;
b = 2;
c = a + b
```
### 5.2 Test the file
```
(venv) vangogh@vangoghs-MacBook-Pro smop-test % smop test.m

WARNING: Token 'CLASSDEF' defined, but not used

WARNING: Token 'END_UNEXPECTED' defined, but not used

WARNING: There are 2 unused tokens

Generating LALR tables

/Users/vangogh/smop-test/venv/lib/python3.11/site-packages/ply/lex.py:760: FutureWarning: Possible nested set at position 65

  c = re.compile('(?P<%s>%s)' % (fname, _get_regex(f)), self.reflags)

/Users/vangogh/smop-test/venv/lib/python3.11/site-packages/ply/lex.py:498: FutureWarning: Possible nested set at position 118

  lexre = re.compile(regex, reflags)

str

Traceback (most recent call last):

  File "/Users/vangogh/smop-test/venv/lib/python3.11/site-packages/smop/main.py", line 66, in main

    G = resolve.resolve(stmt_list)

        ^^^^^^^^^^^^^^^^^^^^^^^^^^

  File "/Users/vangogh/smop-test/venv/lib/python3.11/site-packages/smop/resolve.py", line 54, in resolve

    u = G.node[n]["ident"]

        ^^^^^^

AttributeError: 'DiGraph' object has no attribute 'node'

Errors: 1
``` 
### 5.3 Downgrade networkx to 1.11

- API not fit caused by "G.node" which deleted by networkx 3.6.1
``` 
(venv) vangogh@vangoghs-MacBook-Pro smop-test % pip uninstall networkx -y

pip install "networkx<2.0"

Found existing installation: networkx 3.6.1

Uninstalling networkx-3.6.1:

  Successfully uninstalled networkx-3.6.1

Collecting networkx<2.0

  Downloading networkx-1.11-py2.py3-none-any.whl.metadata (1.5 kB)

Collecting decorator>=3.4.0 (from networkx<2.0)

  Downloading decorator-5.3.1-py3-none-any.whl.metadata (3.9 kB)

Downloading networkx-1.11-py2.py3-none-any.whl (1.3 MB)

   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.3/1.3 MB 21.2 MB/s  0:00:00

Downloading decorator-5.3.1-py3-none-any.whl (10 kB)

Installing collected packages: decorator, networkx

Successfully installed decorator-5.3.1 networkx-1.11

(venv) vangogh@vangoghs-MacBook-Pro
``` 
### 5.4 Test SMOP
``` 
(venv) vangogh@vangoghs-MacBook-Pro smop-test % smop test.m

Traceback (most recent call last):

  File "/Users/vangogh/smop-test/venv/bin/smop", line 3, in <module>

    from smop.main import main

  File "/Users/vangogh/smop-test/venv/lib/python3.11/site-packages/smop/main.py", line 17, in <module>

    from . import resolve

  File "/Users/vangogh/smop-test/venv/lib/python3.11/site-packages/smop/resolve.py", line 22, in <module>

    import networkx as nx

  File "/Users/vangogh/smop-test/venv/lib/python3.11/site-packages/networkx/__init__.py", line 84, in <module>

    import networkx.generators

  File "/Users/vangogh/smop-test/venv/lib/python3.11/site-packages/networkx/generators/__init__.py", line 5, in <module>

    from networkx.generators.classic import *

  File "/Users/vangogh/smop-test/venv/lib/python3.11/site-packages/networkx/generators/classic.py", line 21, in <module>

    from networkx.algorithms.bipartite.generators import complete_bipartite_graph

  File "/Users/vangogh/smop-test/venv/lib/python3.11/site-packages/networkx/algorithms/__init__.py", line 12, in <module>

    from networkx.algorithms.dag import *

  File "/Users/vangogh/smop-test/venv/lib/python3.11/site-packages/networkx/algorithms/dag.py", line 2, in <module>

    from fractions import gcd

ImportError: cannot import name 'gcd' from 'fractions' (/opt/homebrew/Cellar/python@3.11/3.11.15_1/Frameworks/Python.framework/Versions/3.11/lib/python3.11/fractions.py)
``` 
### 5.5 Try to downgrade to Python 3.8
- Fixed the " ```DiGraph has no attribute 'node'``` " problem
- Appear another compatibility problem:" ```ImportError: cannot import name 'gcd' from 'fractions'```" Caused by networkx 1.11 is too old and rely on "```from fractions import gcd```"
- Pyhthon 3.9+ deleted ```fractions.gcd```, so SMOP need Old networkx, old networkx need Old Python.
```
(venv) vangogh@vangoghs-MacBook-Pro smop-test % brew install python@3.8

✔︎ JSON API formula.jws.json                                                                  Downloaded   32.5MB/ 32.5MB

✔︎ JSON API cask.jws.json                                                                     Downloaded   15.7MB/ 15.7MB

Warning: No available formula with the name "python@3.8". Did you mean python@3.9, python@3.14, python@3.13, python@3.12, python@3.11, python@3.10 or python-yq?

==> **Searching for similarly named formulae and casks...**

==> **Formulae**

python@3.9 (deprecated)       python@3.13                   **python@3.11** **✔**                 python-yq

python@3.14                   **python@3.12** **✔**                 python@3.10

  

To install python@3.9 (deprecated), run:

  brew install python@3.9 (deprecated)

(venv) vangogh@vangoghs-MacBook-Pro smop-test % /opt/homebrew/bin/python3.8 --version

zsh: no such file or directory: /opt/homebrew/bin/python3.8
```
### 5.6 fix networkx 1.11
- Python 3.8 was no more offered.
- Change "```from fractions import gcd```" to "```from math import gcd```" manually.
```
(venv) vangogh@vangoghs-MacBook-Pro smop-test % nano ~/smop-test/venv/lib/python3.11/site-packages/networkx/algorithms/dag.py

(venv) vangogh@vangoghs-MacBook-Pro smop-test % smop test.m

/Users/vangogh/smop-test/venv/lib/python3.11/site-packages/ply/lex.py:760: FutureWarning: Possible nested set at position 65

  c = re.compile('(?P<%s>%s)' % (fname, _get_regex(f)), self.reflags)

/Users/vangogh/smop-test/venv/lib/python3.11/site-packages/ply/lex.py:498: FutureWarning: Possible nested set at position 118

  lexre = re.compile(regex, reflags)

str

str

str

str

str
```
### 5.7 Check the file
- Five "```str```"is the debug output.
```
(venv) vangogh@vangoghs-MacBook-Pro smop-test % ls

test.m test.py venv

(venv) vangogh@vangoghs-MacBook-Pro smop-test % cat test.py

# Generated with SMOP  0.41

from libsmop import *

# test.m

  

    a=1

# test.m:1

    b=2

# test.m:2

    c=a + b

# test.m:3**%**
```
## 6. Save the environment

```
(venv) vangogh@vangoghs-MacBook-Pro smop-test % pip freeze > requirements.txt
```

```
(venv) vangogh@vangoghs-MacBook-Pro smop-test % cat requirements.txt

decorator==5.3.1

networkx==1.11

numpy==2.4.6

packaging==26.2

ply==3.11

scipy==1.17.1

smop==0.41
```

```
(venv) vangogh@vangoghs-MacBook-Pro smop-test % cp ~/smop-test/venv/lib/python3.11/site-packages/networkx/algorithms/dag.py \

~/smop-test/dag.py.backup
```

```
(venv) vangogh@vangoghs-MacBook-Pro smop-test % cd ~

tar -czf smop-working-env.tar.gz smop-test
```

## 7. Create a launch script
### 7.1 Create and Root 
```
vangogh@vangoghs-MacBook-Pro ~ % nano ~/smop-test/start_smop.sh

#!/bin/zsh

cd ~/smop-test
source venv/bin/activate
```
- give root
```
vangogh@vangoghs-MacBook-Pro ~ % chmod +x ~/smop-test/start_smop.sh
```
### 7.2 Launch check
```
vangogh@vangoghs-MacBook-Pro ~ % ~/smop-test/start_smop.sh

(venv)vangogh@vangoghs-MacBook-Pro ~ %
```

## 8. Verify SMOP
```
(venv) vangogh@vangoghs-MacBook-Pro ~ % which python

/Users/vangogh/smop-test/venv/bin/python

(venv) vangogh@vangoghs-MacBook-Pro ~ % smop --help                                       

usage: 

  

    smop [OPTIONS] [FILE1.m FILE2.m ...]

  

SMOP is Small Matlab and Octave to Python compiler, it takes MATLAB

files and translates them to Python.  The names of the resulting files

are derived from the names of the source files unless explicitly set

with -o .

  

positional arguments:

  file.m

  

options:

  -h, --help            show this help message and exit

  -A, --no-analysis     

                        skip analysis

  -B, --no-backend      

                        omit code generation

  -C, --no-comments     

                        discard multiline comments

  -D DEBUG, --debug DEBUG

                        Colon-separated codes.

                        M Main

                        L Lex

                        P Parse

  -E, --delete-on-error

                        By default, broken ".py" files are kept alive to allow their

                        examination and debugging. Sometimes we want the opposite behavior

  -g PATTERN, --glob-pattern PATTERN

                        Apply unix glob pattern to the input file list or to files. For

                        example -g 'octave-4.0.2/*.m

  -H, --no-header       

                        use it if you plan to concatenate the generated files

  -L, --debug-lexer     

                        enable built-in debugging tools

  -N, --no-numbers      

                        discard line-numbering information

  -o FILE.py, --output FILE.py

                        Write the results to FILE.py.  Use -o- to send the results to the

                        standard output.  If not specified explicitly, output file names are

                        derived from input file names by replacing ".m" with ".py".  For example,

                            $ smop FILE1.m FILE2.m FILE3.m

                        generates files FILE1.py FILE2.py and FILE3.py

  -P, --debug-parser    

                        enable built-in debugging tools

  -R, --no-resolve      

                        omit name resolution

  -S, --strict          

                        stop after first syntax error (by default compiles other .m files)

  -T, --testing-mode    

                        support special "testing" percent-bang comments used to write Octave

                        test suite.  When disabled, behaves like regular comments

  -x FILE1.m,FILE2.m,FILE3.m, --exclude FILE1.m,FILE2.m,FILE3.m

                        comma-separated list of files to ignore

  -V, --version         show program's version number and exit

  -v, --verbose

  -Z ARCHIVE.tar, --archive ARCHIVE.tar

                        Read ".m" files from the archive; ignore other files.  Accepted

                        format: "tar".  Accepted compression: "gzip", "bz2".

  

Example:

    $ wget ftp://ftp.gnu.org/gnu/octave/octave-4.0.2.tar.gz

    $ smop -a octave-4.0.2.tar.gz -g '*/scripts/*.m'

    $ ls -1 *.py | wc

    $ python -m py_compile *.py

    $ ls -1 *.pyc | wc
```

## 9. Verify in VS Code
![[截屏2026-05-19 19.14.06.png]]
```
vangogh@vangoghs-MacBook-Pro ~ % which smop
smop not found
vangogh@vangoghs-MacBook-Pro ~ % ls ~
Applications            Downloads               Music                   PyCharmMiscProject
Desktop                 Library                 Pictures                smop-test
Documents               Movies                  Public                  smop-working-env.tar.gz
vangogh@vangoghs-MacBook-Pro ~ % ls ~/smop-test
dag.py.backup           start_smop.sh           test.py
requirements.txt        test.m                  venv
vangogh@vangoghs-MacBook-Pro ~ % source ~/smop-test/venv/bin/activate
(venv) vangogh@vangoghs-MacBook-Pro ~ % which smop
/Users/vangogh/smop-test/venv/bin/smop
(venv) vangogh@vangoghs-MacBook-Pro ~ % 

```

# Cookiecutter
```
vangogh@vangoghs-MacBook-Pro ~ % pip3 --version

pip 26.1.1 from /Library/Frameworks/Python.framework/Versions/3.14/lib/python3.14/site-packages/pip (python 3.14)

vangogh@vangoghs-MacBook-Pro ~ % pip3 install cookiecutter

WARNING: Cache entry deserialization failed, entry ignored

Collecting cookiecutter

  Downloading cookiecutter-2.7.1-py3-none-any.whl.metadata (7.3 kB)

Collecting binaryornot>=0.4.4 (from cookiecutter)

  Downloading binaryornot-0.6.0-py3-none-any.whl.metadata (2.9 kB)

Collecting Jinja2<4.0.0,>=2.7 (from cookiecutter)

  Downloading jinja2-3.1.6-py3-none-any.whl.metadata (2.9 kB)

WARNING: Cache entry deserialization failed, entry ignored

Collecting click<9.0.0,>=7.0 (from cookiecutter)

  Using cached click-8.4.0-py3-none-any.whl.metadata (2.6 kB)

WARNING: Cache entry deserialization failed, entry ignored

Collecting pyyaml>=5.3.1 (from cookiecutter)

  Downloading pyyaml-6.0.3-cp314-cp314-macosx_11_0_arm64.whl.metadata (2.4 kB)

Collecting python-slugify>=4.0.0 (from cookiecutter)

  Downloading python_slugify-8.0.4-py2.py3-none-any.whl.metadata (8.5 kB)

WARNING: Cache entry deserialization failed, entry ignored

Collecting requests>=2.23.0 (from cookiecutter)

  Using cached requests-2.34.2-py3-none-any.whl.metadata (4.8 kB)

Collecting arrow (from cookiecutter)

  Downloading arrow-1.4.0-py3-none-any.whl.metadata (7.7 kB)

WARNING: Cache entry deserialization failed, entry ignored

Collecting rich (from cookiecutter)

  Using cached rich-15.0.0-py3-none-any.whl.metadata (18 kB)

Collecting MarkupSafe>=2.0 (from Jinja2<4.0.0,>=2.7->cookiecutter)

  Downloading markupsafe-3.0.3-cp314-cp314-macosx_11_0_arm64.whl.metadata (2.7 kB)

Collecting text-unidecode>=1.3 (from python-slugify>=4.0.0->cookiecutter)

  Downloading text_unidecode-1.3-py2.py3-none-any.whl.metadata (2.4 kB)

WARNING: Cache entry deserialization failed, entry ignored

Collecting charset_normalizer<4,>=2 (from requests>=2.23.0->cookiecutter)

  Downloading charset_normalizer-3.4.7-cp314-cp314-macosx_10_15_universal2.whl.metadata (40 kB)

WARNING: Cache entry deserialization failed, entry ignored

Collecting idna<4,>=2.5 (from requests>=2.23.0->cookiecutter)

  Using cached idna-3.15-py3-none-any.whl.metadata (7.7 kB)

WARNING: Cache entry deserialization failed, entry ignored

Collecting urllib3<3,>=1.26 (from requests>=2.23.0->cookiecutter)

  Using cached urllib3-2.7.0-py3-none-any.whl.metadata (6.9 kB)

WARNING: Cache entry deserialization failed, entry ignored

Collecting certifi>=2023.5.7 (from requests>=2.23.0->cookiecutter)

  Using cached certifi-2026.4.22-py3-none-any.whl.metadata (2.5 kB)

Collecting python-dateutil>=2.7.0 (from arrow->cookiecutter)

  Downloading python_dateutil-2.9.0.post0-py2.py3-none-any.whl.metadata (8.4 kB)

Collecting tzdata (from arrow->cookiecutter)

  Downloading tzdata-2026.2-py2.py3-none-any.whl.metadata (1.4 kB)

WARNING: Cache entry deserialization failed, entry ignored

Collecting six>=1.5 (from python-dateutil>=2.7.0->arrow->cookiecutter)

  Using cached six-1.17.0-py2.py3-none-any.whl.metadata (1.7 kB)

WARNING: Cache entry deserialization failed, entry ignored

Collecting markdown-it-py>=2.2.0 (from rich->cookiecutter)

  Using cached markdown_it_py-4.2.0-py3-none-any.whl.metadata (7.4 kB)

WARNING: Cache entry deserialization failed, entry ignored

Collecting pygments<3.0.0,>=2.13.0 (from rich->cookiecutter)

  Using cached pygments-2.20.0-py3-none-any.whl.metadata (2.5 kB)

WARNING: Cache entry deserialization failed, entry ignored

Collecting mdurl~=0.1 (from markdown-it-py>=2.2.0->rich->cookiecutter)

  Using cached mdurl-0.1.2-py3-none-any.whl.metadata (1.6 kB)

Downloading cookiecutter-2.7.1-py3-none-any.whl (41 kB)

Using cached click-8.4.0-py3-none-any.whl (116 kB)

Downloading jinja2-3.1.6-py3-none-any.whl (134 kB)

Downloading binaryornot-0.6.0-py3-none-any.whl (14 kB)

Downloading markupsafe-3.0.3-cp314-cp314-macosx_11_0_arm64.whl (12 kB)

Downloading python_slugify-8.0.4-py2.py3-none-any.whl (10 kB)

Downloading pyyaml-6.0.3-cp314-cp314-macosx_11_0_arm64.whl (173 kB)

Using cached requests-2.34.2-py3-none-any.whl (73 kB)

Downloading charset_normalizer-3.4.7-cp314-cp314-macosx_10_15_universal2.whl (309 kB)

Using cached idna-3.15-py3-none-any.whl (72 kB)

Using cached urllib3-2.7.0-py3-none-any.whl (131 kB)

Using cached certifi-2026.4.22-py3-none-any.whl (135 kB)

Downloading text_unidecode-1.3-py2.py3-none-any.whl (78 kB)

Downloading arrow-1.4.0-py3-none-any.whl (68 kB)

Downloading python_dateutil-2.9.0.post0-py2.py3-none-any.whl (229 kB)

Using cached six-1.17.0-py2.py3-none-any.whl (11 kB)

Using cached rich-15.0.0-py3-none-any.whl (310 kB)

Using cached pygments-2.20.0-py3-none-any.whl (1.2 MB)

Using cached markdown_it_py-4.2.0-py3-none-any.whl (91 kB)

Using cached mdurl-0.1.2-py3-none-any.whl (10.0 kB)

Downloading tzdata-2026.2-py2.py3-none-any.whl (349 kB)

Installing collected packages: text-unidecode, urllib3, tzdata, six, pyyaml, python-slugify, pygments, mdurl, MarkupSafe, idna, click, charset_normalizer, certifi, binaryornot, requests, python-dateutil, markdown-it-py, Jinja2, rich, arrow, cookiecutter

Successfully installed Jinja2-3.1.6 MarkupSafe-3.0.3 arrow-1.4.0 binaryornot-0.6.0 certifi-2026.4.22 charset_normalizer-3.4.7 click-8.4.0 cookiecutter-2.7.1 idna-3.15 markdown-it-py-4.2.0 mdurl-0.1.2 pygments-2.20.0 python-dateutil-2.9.0.post0 python-slugify-8.0.4 pyyaml-6.0.3 requests-2.34.2 rich-15.0.0 six-1.17.0 text-unidecode-1.3 tzdata-2026.2 urllib3-2.7.0

vangogh@vangoghs-MacBook-Pro ~ % cookiecutter --version

Cookiecutter 2.7.1 from /Library/Frameworks/Python.framework/Versions/3.14/lib/python3.14/site-packages (Python 3.14.5 (v3.14.5:5607950ef23, May 10 2026, 07:38:09) [Clang 21.0.0 (clang-2100.0.123.102)])

vangogh@vangoghs-MacBook-Pro ~ % cookiecutter https://github.com/neuroinformatics-unit/python-cookiecutter

  [1/9] full_name **(Python developer)**:
```