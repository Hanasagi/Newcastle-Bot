from credentials import Creds
import requests
import json

class slashCommandController:
    def __init__(self):
        self.c = Creds()
        self.botId = self.c.get_id(2)
        self.token = self.c.get_token(2)
        self.api_url = "https://discord.com/api/v8"
        self.get_all_endpoint = "/applications/{}/commands"
        self.command_endpoint = self.get_all_endpoint + "/{}"
        self.header= {
                "Authorization": "Bot "+self.token
        }


    async def addCommand(self, ctx, command):
            command = command.replace("'", '"')


    async def delCommand(self,ctx,command):
            r=requests.delete(self.api_url+self.get_all_endpoint.format(self.botId)+"/"+command,headers=self.header)
            print(r.content)