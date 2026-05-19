from model import ZumaTowerDefenceModel
from view import ZumaTowerDefenceView
from controller import ZumaTowerDefenceController

def main():
    model = ZumaTowerDefenceModel()
    view = ZumaTowerDefenceView()
    controller = ZumaTowerDefenceController(model, view)
    
    controller.start_game()

if __name__ == "__main__":
    main()