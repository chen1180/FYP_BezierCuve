import sys
import argparse
from PyQt5.QtWidgets import QApplication
from MainWindow import MainWindow

NAME='System for curve and surface GUI (PyQT)'
app=QApplication(sys.argv,applicationName=NAME)



def main():
    window=MainWindow()

    parser=argparse.ArgumentParser(description=NAME)
    parser.add_argument('filename',nargs='?',default=None)

    args=parser.parse_args(app.arguments()[1:])
    print(args)
    if args.filename:
        window.components['editor'].load_from_file(args.filename)
    window.show()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()
