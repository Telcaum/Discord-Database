import json


class DiscordDB:
  """
  A database inside Discord.
  # How to setup
  1. Create a Discord server.
  2. Create a new channel.
  3. Add a new JSON file on your device. You can name it however you want.
  4. Initiate a DiscordDB object and use the init() function to set it up.

  The database works just like a JSON file.
  """

  def __init__(self):
    self.channel = None
    self.json_path = None

  async def _get_msg(self, name):
    async for i in self.channel.history(limit=None):
      if i.content.startswith(f"ID: {name}\n"):
        return i

  async def init(self, bot, channel_id: int, json_path: str):
    self.channel = await bot.fetch_channel(channel_id)
    self.json_path = json_path
    return self

  async def load(self, name: str, *args, **kwargs):
    with open(self.json_path, "w") as f:
      msg = await self._get_msg(name)
      if not msg:
        return
      f.write(("\n".join(msg.content.split("\n")[2:]))[:-4])
    with open(self.json_path) as f:
      return json.load(f, *args, **kwargs)
    
  async def dump(self, name: str, data, *args, **kwargs):
    try:
      await (await self._get_msg(name)).delete()
    except:
      pass
    with open(self.json_path, "w") as f:
      json.dump(data, f, *args, **kwargs)
    with open(self.json_path) as f:
      string = f"ID: {name}\n```json\n{f.read()}\n```"
    await self.channel.send(string)
