# main.py
from src.model.model import TetrisModel
from src.view.view import TetrisView
from src.presenter.presenter import TetrisPresenter

def main():
    model = TetrisModel()
    view = TetrisView(model)
    presenter = TetrisPresenter(model, view)
    presenter.run()
    view.quit()

if __name__ == "__main__":
    main()
