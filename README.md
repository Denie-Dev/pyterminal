# [Pyterminal](https://github.com/Denie-Dev/pyterminal)
A small, lightweight terminal built on python.
## Commands
Use help to check current commands.
```
af   - append (to) files                       | af {file/path} {text}
cf   - copy files                              | cf {file1} {file2}
cs   - clear screen                            | cs
cwd  - current woking directory                | cwd
df   - delete files                            | df {file/path}
ds   - device specification                    | ds
help - help                                    | help
md   - make directory                          | md {dir/path}
mf   - make  files                             | mf {file/part}
ot   - output text                             | ot {text}
rev  - read enviormental variables             | rev {ev name}
rf   - read files                              | rf {file/path}
sev  - set enviormental variables              | sev {ev name} {ev value}
ver  - version                                 | ver
log  - log commands, errors and warnings       | log (clear/level {1,2,3}/w {text})
```
## Dependicies
### Python - Base
[Installer For Mac](https://www.python.org/ftp/python/3.14.0/python-3.14.0-macos11.pkg)<br>
[Installer For Windows](https://www.python.org/ftp/python/pymanager/python-manager-25.0.msix)<br>
[Installer For Linux/Unix](https://www.python.org/ftp/python/3.14.0/Python-3.14.0.tar.xz)
## Notices
1. IDLE Shell is a gui shell and uses more rescources, please use terminal (python3 command) for more preformance. Typing the cs command in idle shell shows how slow it is.
2. current rf character limit is 5000. In release 1.4, this limit can be changed.
## Errors
1. Full disk access is needed for python if inavlid permission occurs when using md, lf, af or cd.
Any other errors should be reported as [issues](https://github.com/Denie-Dev/pyterminal/issues/new) with good evidence.
