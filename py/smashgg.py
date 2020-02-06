import json
from participant import Participant
from graphqlclient import GraphQLClient

client = GraphQLClient('https://api.smash.gg/gql/alpha')

# SmashGG token taken from ggtoken.dat file
with open('ggtoken.dat') as TokenFile:
    TOKEN = TokenFile.read()

client.inject_token('Bearer ' + TOKEN)

def tournamentPlacements(topcutIn, slugIn):
  '''
  Returns a list of topcut player objects of the participant class
  '''

  # Variables to figure out what is actually being found
  topcut = topcutIn
  slug = slugIn


  # Find top (x) players names, profile pictures, and placements based on event slug
  result = client.execute(
  '''
  query EventStandings($slug: String!, $page: Int!, $perPage: Int!) {
    event(slug: $slug) {
      name
      standings(query: {
        perPage: $perPage,
        page: $page
      }){
        nodes {
          standing
          entrant {
            name,
            participants {
              player {
                gamerTag,
                prefix,
                images {
                  url
                }
              }
            }
          }
        }
      }
    }
  }
  ''',
  {
    "slug": slug,
    "page": 1,
    "perPage": topcut
  })

  dict_result = json.loads(result)

  #print('\nSlug: ' + slug)
  #print('Topcut: ' + str(topcut))
  #print('Dict_result: ' + str(dict_result) + '\n')

  if 'errors' in dict_result:
      print('ERROR: ' + dict_result['errors'][0]['message'])
  else:
      pulledplayers = []

      for x in dict_result['data']['event']['standings']['nodes']: # Loops through all found players
          if len(x['entrant']['participants'][0]['player']['images']) >= 1: # Ensures there are no errors if a player does not have a profile picture
              pfpurl = x['entrant']['participants'][0]['player']['images'][0]['url']
          else: # Adds a bidoof profile picture to players without a pfp
              pfpurl = 'https://cdn.bulbagarden.net/upload/thumb/f/f5/399Bidoof.png/375px-399Bidoof.png'

          pulledplayers.append(Participant(x['entrant']['name'], x['standing'], pfpurl)) # Adds new players to a list of participant objects
  return pulledplayers