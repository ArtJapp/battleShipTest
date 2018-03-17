from game_engine import Game
import json


def setting_ships_up(data):
    data = json.load(data)
    game_id = data['game_id']
    try:
       # game = Game(game_id, "hey hey")
        ships = data['ships']
        for x in ships:
            print(x['size'])
            print(x['coordinates'])
    except KeyError:
        print("No game with such id")
        #emit('error', {
         #   'message': "No game with such ID"
        #})


data = '''
{
  game_id: 0,
  user_id: 1,
  ships: [
   {
      "size": 3,
      "coordinates": [
         {
            "y": 1,
            "x": 1
         },
         {
            "y": 2,
            "x": 1
         },
         {
            "y": 3,
            "x": 1
         }
      ]
   },
   {
      "size": 4,
      "coordinates": [
         {
            "y": 1,
            "x": 3
         },
         {
            "y": 1,
            "x": 4
         },
         {
            "y": 1,
            "x": 5
         },
         {
            "y": 1,
            "x": 6
         }
      ]
   },
   {
      "size": 2,
      "coordinates": [
         {
            "y": 5,
            "x": 3
         },
         {
            "y": 6,
            "x": 3
         }
      ]
   },
   {
      "size": 3,
      "coordinates": [
         {
            "y": 8,
            "x": 5
         },
         {
            "y": 8,
            "x": 6
         },
         {
            "y": 8,
            "x": 7
         }
      ]
   },
   {
      "size": 1,
      "coordinates": [
         {
            "y": 8,
            "x": 3
         }
      ]
   },
   {
      "size": 1,
      "coordinates": [
         {
            "y": 1,
            "x": 9
         }
      ]
   },
   {
      "size": 2,
      "coordinates": [
         {
            "y": 3,
            "x": 5
         },
         {
            "y": 3,
            "x": 6
         }
      ]
   },
   {
      "size": 2,
      "coordinates": [
         {
            "y": 7,
            "x": 0
         },
         {
            "y": 8,
            "x": 0
         }
      ]
   },
   {
      "size": 1,
      "coordinates": [
         {
            "y": 6,
            "x": 9
         }
      ]
   },
   {
      "size": 1,
      "coordinates": [
         {
            "y": 5,
            "x": 6
         }
      ]
   }
]

}
'''
setting_ships_up(data)