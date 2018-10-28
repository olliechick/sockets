# COSC264 Sockets

To run the program, first run ``channel.py``, ``sender.py``, and ``receiver.py``. For example:
* ``channel.py 15620 15621 15622 15623 15630 15640 0.05``
* ``sender.py 15630 15631 15620 data.txt``
* ``receiver.py 15640 15641 15622 rec.txt``

Then click enter on ``channel.py``, then on ``receiver.py``, then on ``sender.py``.

Note that if rec.txt (or whatever file you have specified for receiver) exists, then the program will close.

Also note that Windows isn't great at closing sockets, so to re-run the program, either change the socket numbers or restart your computer.

## Checking validity

To check that the two files are the same, run ``diff`` on the two files: e.g. ``diff data.txt rec.txt``.
