from SDKWrapper import SdkWrapper

sdkWrapper = SdkWrapper.GetInstance()


class WalletManager():
    def __init__(self):
        self.singames = SinGames()
        self.singamesAddr = SinGamesAddress()
        self.furnaceAddr = FurnaceAddress()
        self.furnace = Furnace()
        


def SinGames():
    return sdkWrapper.GetSdk().wallet_manager.get_account(SinGamesAddress(), 'password')

def Furnace():
    return sdkWrapper.GetSdk().wallet_manager.get_account(FurnaceAddress(), 'password')



def SinGamesAddress():
    return 'AM82aCCE1NyE7cmpwpRzbcuvr3ndXHCq8Q'

def FurnaceAddress():
    return 'ASz7Rr7YWMJrNkCk8UDYA5YaFpco6Z5xVF'
