

import requests
import mysql.connector

class Database:

    def __init__(self):
        self.mydb = mysql.connector.connect(
            host = 'yourhost',
            user = 'username',
            password = '123456789',
            database = 'NBA'
            )

        self.cursor = self.mydb.cursor()

    def store_player(self, name_f, name_l, stats) -> None:

        self.ppg = stats['league']['standard']['stats']['regularSeason']['season'][0]['total']['ppg']
        self.rpg = stats['league']['standard']['stats']['regularSeason']['season'][0]['total']['rpg']
        self.apg = stats['league']['standard']['stats']['regularSeason']['season'][0]['total']['apg']
        self.mpg = stats['league']['standard']['stats']['regularSeason']['season'][0]['total']['mpg']
        self.spg = stats['league']['standard']['stats']['regularSeason']['season'][0]['total']['spg']
        self.bpg = stats['league']['standard']['stats']['regularSeason']['season'][0]['total']['bpg']
        self.ftp = stats['league']['standard']['stats']['regularSeason']['season'][0]['total']['ftp']
        self.fgp = stats['league']['standard']['stats']['regularSeason']['season'][0]['total']['fgp']

        self.sql = f"""INSERT INTO players (first_name,
                                            last_name,
                                            points_per_game,
                                            rebounds_per_game,
                                            assists_per_game,
                                            minutes_per_game,
                                            steals_per_game,
                                            blocks_per_game,
                                            free_throws,
                                            field_goals)

                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        self.val = (name_f,
                    name_l,
                    self.ppg,
                    self.rpg,
                    self.apg,
                    self.mpg,
                    self.spg,
                    self.bpg,
                    self.ftp,
                    self.fgp)

        self.cursor.execute(self.sql, self.val)
        self.mydb.commit()

class NBA:

    def __init__(self, name, l_name):
        self.name = name
        self.l_name = l_name

    def find_player_id(self) -> str:

        self.response = requests.get("http://data.nba.net/10s/prod/v1/2021/players.json")
        self.data = self.response.json()
        self.all_players = self.data['league']['standard']

        for self.player in self.all_players:
            if self.player['firstName'] == self.name and self.player['lastName'] == self.l_name:
                return self.player['personId']

    def get_player_stats(self, id) -> dict:

        self.response = requests.get(f"http://data.nba.net/10s/prod/v1/2021/players/{id}_profile.json")
        self.player_stats = self.response.json()
        return self.player_stats

    def display_stats(self, stats) -> None:
        print(f"\n{self.name} {self.l_name} had following stats in the 2021 NBA season")
        print(f"Points per game: {stats['league']['standard']['stats']['regularSeason']['season'][0]['total']['ppg']}")
        print(f"Rebounds per game: {stats['league']['standard']['stats']['regularSeason']['season'][0]['total']['rpg']}")
        print(f"Assists per game: {stats['league']['standard']['stats']['regularSeason']['season'][0]['total']['apg']}")
        print(f"Minutes per game: {stats['league']['standard']['stats']['regularSeason']['season'][0]['total']['mpg']}")
        print(f"Steals per game: {stats['league']['standard']['stats']['regularSeason']['season'][0]['total']['spg']}")
        print(f"Blocks per game: {stats['league']['standard']['stats']['regularSeason']['season'][0]['total']['bpg']}")
        print(f"Free throws percentage: {stats['league']['standard']['stats']['regularSeason']['season'][0]['total']['ftp']}%")
        print(f"Field goal percentage: {stats['league']['standard']['stats']['regularSeason']['season'][0]['total']['fgp']}%")

    def continue_searching(self) -> bool:

        self.choice = input("\nDo you want to look for another player[Y/N]?: ").upper()

        if self.choice == 'Y':
            return True
        else:
            return False

def main():

    database = Database()
    while True:

        name = input("\nEnter NBA player's first name: ")
        l_name = input("Enter NBA player's last name: ")
        nba = NBA(name, l_name)
        player_id = nba.find_player_id()

        if player_id == None:
            print("\nNo such player in the league")
            continue

        else:
            stats = nba.get_player_stats(player_id)
            nba.display_stats(stats)

            save_player = input("\nDo you want to save this player to your database[Y/N]?: ")

            if save_player.upper() == 'Y':
                database.store_player(name, l_name, stats)
                if nba.continue_searching():
                    continue
                else:
                    break
            else:
                if nba.continue_searching():
                    continue
                else:
                    break

if __name__ == '__main__':
    main()
