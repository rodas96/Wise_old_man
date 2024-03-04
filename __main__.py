#
# Eu mando-te um objeto assim

# {
#   username: "psikoi",
#   overallRank: 74858
# }
# Não podes fazer mais que 1 pesquisa a cada X segundos
# Configurável
# E, se o casing do nome que encontrares for diferente do que eu te mandei, mandas um pedido de volta para mim
# Depois dou-te os detalhes deste pedido, se não vais fazer merda e spammar-me a API
# Fica para último, faz só print por agora
# Do nome que recebeste e o que encontraste
# queue . recebo 10 players vou mandando o player sempre que esta pront

from utils import make_request, find_player_from_overall
import queue
import threading

player_queue = queue.Queue()

def player_worker():
    while not player_queue.empty():
        player = player_queue.get()
        try:
            url = "https://secure.runescape.com/m=hiscore_oldschool/overall?category_type=0"
            payload = {'rank': player["overallRank"]}
            soup = make_request(url, payload)
            if soup:
                player_name_hiscores = find_player_from_overall(soup, player["overallRank"])
                if player["username"] != player_name_hiscores:
                    print(player_name_hiscores)
                else:
                    print(f"same, player: {player['username']} and hiscores: {player_name_hiscores}")
            else:
                print(f"Failed to fetch data for {player['username']}")
        except Exception as e:
            print(f"Error processing {player['username']}: {e}")
        finally:
            player_queue.task_done()

players = [
    {"username": "wdr pimp", "overallRank": 365988},
    {"username": "psikoi", "overallRank": 82488},
]

for player in players:
    player_queue.put(player)

num_threads = 10

# Create and start threads
threads = []
for i in range(num_threads):
    thread = threading.Thread(target=player_worker)
    thread.start()
    threads.append(thread)
for thread in threads:
    thread.join()

print("All players processed.")



