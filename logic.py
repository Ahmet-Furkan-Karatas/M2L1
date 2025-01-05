import aiohttp
import random

class Pokemon:
    pokemons = {}

    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = random.randint(1, 1000)
        self.img = None
        self.name = None
        self.hp = random.randint(50, 150)
        self.power = random.randint(20, 100)
        self.weight = None  # Kilo bilgisi için alan
        self.height = None  # Boy bilgisi için alan

    async def get_pokemon_data(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    self.name = data['forms'][0]['name']
                    self.weight = data['weight']
                    self.height = data['height']
                    self.img = data['sprites']['front_default']
                else:
                    self.name = "Pikachu"
                    self.weight = "Bilinmiyor"
                    self.height = "Bilinmiyor"

    async def info(self):
        if not self.name or self.weight is None or self.height is None:
            await self.get_pokemon_data()
        return (
            f"Pokémon Adı: {self.name.capitalize()}\n"
            f"Sağlık: {self.hp}\n"
            f"Güç: {self.power}\n"
            f"Kilo: {self.weight / 10} kg\n"
            f"Boy: {self.height / 10} m\n"
            f"Eğitici: {self.pokemon_trainer}"
        )

    async def show_img(self):
        if not self.img:
            await self.get_pokemon_data()
        return self.img

    async def attack(self, enemy):
        if isinstance(enemy, Wizard):  # Eğer düşman bir Wizard ise
            şans = random.randint(1, 5)
            if şans == 1:
                return "Sihirbaz Pokémon, savaşta bir kalkan kullanıldı!"
        if enemy.hp > self.power:
            enemy.hp -= self.power
            return (
                f"Pokémon eğitmeni @{self.pokemon_trainer}, @{enemy.pokemon_trainer}'ne saldırdı.\n"
                f"@{enemy.pokemon_trainer}'nin sağlık durumu: {enemy.hp}"
            )
        else:
            enemy.hp = 0
            return f"Pokémon eğitmeni @{self.pokemon_trainer}, @{enemy.pokemon_trainer}'ni yendi!"

class Wizard(Pokemon):
    async def attack(self, enemy):
        return await super().attack(enemy)

class Fighter(Pokemon):
    async def attack(self, enemy):
        süper_güç = random.randint(5, 15)
        self.power += süper_güç
        sonuç = await super().attack(enemy)
        self.power -= süper_güç
        return sonuç + f"\nDövüşçü Pokémon süper saldırı kullandı. Eklenen güç: {süper_güç}"
