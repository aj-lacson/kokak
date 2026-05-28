from model import ZumaTowerDefenceModel
from view import ZumaTowerDefenceView
from controller import ZumaTowerDefenceController
import json
from random import Random

def main():
    with open('settings.json', 'r') as file:
        data = json.load(file)
    
    # fetheches gamemode
    model = ZumaTowerDefenceModel(Random(), data)
    view = ZumaTowerDefenceView()
    controller = ZumaTowerDefenceController(model, view)
    
    controller.start_game()

if __name__ == "__main__":
    main()