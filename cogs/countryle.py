import discord, json, random, time
from discord.ext import commands
from pymongo import MongoClient

country_list = open("./country-list.txt").read().splitlines()

country_data = {
    # Country Name, Hemisphere, Continent, Population, Avg. Temp
    "Afghanistan": "Northern, Asia, 38900000, 12.60",
    "Albania": "Northern, Europe, 2800000, 11.40",
    "Algeria": "Northern, Africa, 43000000, 22.50",
    "Andorra": "Northern, Europe, 55000, 7.60",
    "Angola": "Southern, Africa, 32000000, 21.55",
    "Antigua and Barbuda": "Northern, North America, 98000, 25.85",
    "Argentina": "Southern, South America, 45100000, 14.80",
    "Armenia": "Northern, Asia, 2900000, 7.15", 
    "Australia": "Southern, Oceania, 25500000, 21.65",
    "Austria": "Northern, Europe, 9000000, 6.35",
    "Azerbaijan": "Northern, Asia, 10100000, 11.95",
    "Bahrain": "Northern, Asia, 1700000, 26.80",
    "Bangladesh": "Northern, Asia, 165000000, 25.00",
    "Barbados": "Northern, North America, 280000, 26.00",
    "Belarus": "Northern, Europe, 9500000, 6.15",
    "Belgium": "Northern, Europe, 11000000, 9.55",
    "Belize": "Northern, North America, 400000, 25.35",
    "Benin": "Northern, Africa, 12000000, 27.55",
    "Bhutan": "Northern, Asia, 770000, 7.40"
}

with open("./config.json") as f:
        config = json.load(f)

cluster = MongoClient(config['c01password'])
db_countryle = cluster['pyguesser']['countryle']

class countryle(commands.Cog):
    def __init__(self, client):
        self.client = client

    global is_correct
    is_correct = False

    @commands.command(aliases=['countryle'])
    async def play_countryle(self, ctx):
        user_stats = db_countryle.find_one({"id": ctx.author.id})
        if not ctx.author.bot:
            if user_stats is None:
                insert = {"id": ctx.author.id, "wins": 0, "games_played": 0, "best_game": 0}
                db_countryle.insert_one(insert)

                time.sleep(3)

                user_stats = db_countryle.find_one({"id": ctx.author.id})

                games_played = user_stats['games_played'] + 1
                db_countryle.update_one({"id": ctx.author.id}, {"$set":{"games_played": games_played}})
            else:
                games_played = user_stats['games_played'] + 1
                db_countryle.update_one({"id": ctx.author.id}, {"$set":{"games_played": games_played}})

        puzzle_id = random_puzzle_id()
        embed = generate_puzzle_embed(puzzle_id)
        await ctx.reply(embed = embed)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        ref = message.reference
        if not ref or not isinstance(ref.resolved, discord.Message) or is_correct:
            return
        
        parent = ref.resolved

        if parent.author.id != self.client.user.id:
            return
        
        if not parent.embeds:
            return
        
        embed = parent.embeds[0]
        
        if not is_valid_country(message.content):
            await message.reply("Sorry! This country doesn't exist. 😔", delete_after = 5)
            await message.delete(delay = 5)
            return
        
        embed = update_embed(embed, message.content, message.author)
        await parent.edit(embed = embed)

        try:
            await message.delete()
        except Exception:
            pass

    
def generate_puzzle_embed(puzzle_id: int) -> discord.Embed:
    embed = discord.Embed(title = "Countryle: WAITING FOR USER", colour = 0xBA55D3)
    embed.description = f"**🌐 Hemisphere | <:earth_oceania:1080012117035450408> Continent | 👥 Population | 🌡 Avg. Temp**"

    embed.set_footer(text = f"Game ID: {puzzle_id} | To play, use the command pycountryle!\nTo guess, reply to this message with a valid country.")
    return embed

def is_valid_country(word: str) -> bool:
    if word in country_list:
        return True
    else:
        return False
    
def is_guessed_country_correct(guess, answer) -> bool:
    if guess == answer:
        return True
    else:
        return False

def random_puzzle_id() -> int:
    temp = random.randint(0, len(country_list) - 1)

    global puzzle_id_rand_int
    puzzle_id_rand_int = random.randint(1, 10)

    global puzzle_id_operation
    puzzle_id_operation = random.randint(1, 2)
    if puzzle_id_operation == 1:
        temp *= puzzle_id_rand_int
        return temp
    elif puzzle_id_operation == 2:
        temp += puzzle_id_rand_int
        return temp

def generate_guessed_country(guess, answer, puzzle_id):
    country_data_keys = list(country_data.keys())
    correct_country = country_data_keys[puzzle_id]
    correct_country_values = country_data[correct_country]
    correct_country_values_split = correct_country_values.split(", ")

    global correct_hemisphere, correct_continent, correct_population, correct_avg_temp

    correct_hemisphere = correct_country_values_split[0]
    correct_continent = correct_country_values_split[1]
    correct_population = correct_country_values_split[2]
    correct_avg_temp = correct_country_values_split[3]

    correct_population = int(correct_population)
    correct_avg_temp = float(correct_avg_temp)

    guessed_country_values = country_data[f"{guess}"]
    guessed_country_values_split = guessed_country_values.split(", ")

    global guessed_hemisphere, guessed_continent, guessed_population, guessed_avg_temp

    guessed_hemisphere = guessed_country_values_split[0]
    guessed_continent = guessed_country_values_split[1]
    guessed_population = guessed_country_values_split[2]
    guessed_avg_temp = guessed_country_values_split[3]

    global hemisphere_str, continent_str, population_str, avg_temp_str

    guessed_population = int(guessed_population)
    guessed_population_str = format(guessed_population, ",")
    guessed_avg_temp = float(guessed_avg_temp)

    if guessed_hemisphere == correct_hemisphere:
        hemisphere_str = f"{guessed_hemisphere} ✅"
    else:
        hemisphere_str = f"{guessed_hemisphere} ❌"

    if guessed_continent == correct_continent:
        continent_str = f"{guessed_continent} ✅"
    else:
        continent_str = f"{guessed_continent} ❌"

    # Displays population with commas
    if guessed_population == correct_population:
        population_str = f"{guessed_population_str} ✅"
    elif guessed_population > correct_population:
        population_str = f"{guessed_population_str} ⬇"
    elif guessed_population < correct_population:
        population_str = f"{guessed_population_str} ⬆"

    if guessed_avg_temp == correct_avg_temp:
        avg_temp_str = f"{guessed_avg_temp}°C ✅"
    elif guessed_avg_temp > correct_avg_temp:
        avg_temp_str = f"{guessed_avg_temp}°C ⬇"
    elif guessed_avg_temp < correct_avg_temp:
        avg_temp_str = f"{guessed_avg_temp}°C ⬆"
    
    return f"{hemisphere_str} | {continent_str} | {population_str} | {avg_temp_str}"


def update_embed(embed: discord.Embed, guess: str, user: discord.Member) -> discord.Embed:
    puzzle_id = int(embed.footer.text.split()[2])

    if puzzle_id_operation == 1:
        puzzle_id /= puzzle_id_rand_int
        puzzle_id = int(puzzle_id)
    elif puzzle_id_operation == 2:
        puzzle_id -= puzzle_id_rand_int
        puzzle_id = int(puzzle_id)

    answer = country_list[puzzle_id]
    guessed_result = generate_guessed_country(guess, answer, puzzle_id)
    
    is_correct = is_guessed_country_correct(guess, answer)

    num_of_guesses = len(embed.fields) + 1

    embed.title = f"Countryle: {6 - num_of_guesses} GUESSES LEFT"

    if is_correct == True:
        embed.add_field(name = f"{guess}:", value = f"{guessed_result}\n\n**Correct! ✅**\n\nStats:\nGuesses: {num_of_guesses}", inline=False)
        embed.title = f"Countryle: COMPLETE"

        user_stats = db_countryle.find_one({'id': user.id})
        wins = user_stats['wins'] + 1
        db_countryle.update_one({"id": user.id}, {"$set":{"wins": wins}})

        best_guess = user_stats['best_guess']
        if best_guess > 0:
            if best_guess > num_of_guesses:
                best_guess = num_of_guesses
                db_countryle.update_one({"id": user.id}, {"$set":{"best_guess": best_guess}})
        elif best_guess == 0:
            best_guess = num_of_guesses
            db_countryle.update_one({"id": user.id}, {"$set":{"best_guess": best_guess}})
    elif num_of_guesses >= 6: 
        embed.add_field(name = f"{guess}:", value = f"{guessed_result}\n\n**GAME OVER! 😟**\n\nAnswer:\n{answer}", inline=False)
        embed.title = f"Countryle: COMPLETE"
    else:
        embed.add_field(name = f"{guess}:", value = f"{guessed_result}", inline=False)
    return embed

async def setup(client):
    await client.add_cog(countryle(client))