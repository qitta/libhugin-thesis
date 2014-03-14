while true;
do
  inotifywait -e close_write -r ./rst conf.py *.rst *.bib *.py
  notify-send "Compiling thesis..."
  make latexpdf
  notify-send "finished."
done
