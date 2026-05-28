from model import ZumaTowerDefenceModel
from view import ZumaTowerDefenceView
from controller import ZumaTowerDefenceController
from random import Random

def main():
    # fetheches gamemode
    model = ZumaTowerDefenceModel(Random())
    view = ZumaTowerDefenceView()
    controller = ZumaTowerDefenceController(model, view)
    
    controller.start_game()

if __name__ == "__main__":
    main()