from src.model import Model
from src.data import *
from torch.utils.data import DataLoader


@hydra.main(config_path="../config", config_name="train",)
def train():
    model = Model()

    # add rest of your training code here
    # # Save the final trained model
    # torch.save(
    #     model.state_dict(), f"models/{model_save_path}/resnet18_rice_final.pth"
    # )

if __name__ == "__main__":
    train()
