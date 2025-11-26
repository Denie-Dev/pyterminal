# [Pyterminal](https://github.com/Denie-Dev/pyterminal)
A small, lightweight terminal built on python.
## Commands
Use help to check current commands.

rf - read file                   | rf {file/path}<br>
df - delete file                 | df {file/path}<br>
sev - set enviormental variables  | sev {ev name} {ev value}<br>
rev - read enviormental variables | rev {ev name}<br>
af - append (to) file            | af {file/path} {text}<br>
cs - clear screen                | cs<br>
ot  - output text                 | ot {text}<br>
md  - make directory              | md {dir/path}<br>
cf  - create file                 | cf {file/part}<br>
ver - version                     | ver<br>
ds - device specification        | ds<br>
cwd - current woking directory    | cwd<br>
## Notices
1. IDLE Shell is a gui shell and uses more rescources, please use terminal (python3 command) for more preformance. Typing the cs command in idle shell shows how slow it is.
2. current rf character limit is 5000. In release 1.4, this limit can be changed.
## Errors
1. Full disk access is needed for python if inavlid permission occurs when using md, lf, af or cd.
Any other errors should be reported as [issues](https://github.com/Denie-Dev/pyterminal/issues/new) with good evidence.
