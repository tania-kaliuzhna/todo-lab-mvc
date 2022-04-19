from view.todo_pyqt import Window, QApplication
from view.alpha import run_alpha
import sys

if __name__ == "__main__":
    if input("console run[empty for `no`]"):
        app = QApplication(sys.argv)
        screen = Window()
        screen.show()
        sys.exit(app.exec_())
    else:
        run_alpha()
