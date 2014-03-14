while true;
do
  inotifywait -e close_write -r ./rst conf.py *.rst *.bib *.py
  catlight rgb 255 50 0
  make latexpdf
  catlight rgb 0 255 0
done
