import graphene as gr


players = [
    {'id': 1, 'name': 'Czech'},
    {'id': 9, 'name': 'Lukaku'},
    {'id': 10, 'name': 'Hazard'},
    {'id': 99, 'name': 'Werner'},
    {'id': 8, 'name': 'Lampard'}
    # '1', '2', '3', '4', '5'
]


class Player(gr.ObjectType):
    ''' Type definition for User '''
    id = gr.Int()
    name = gr.String()


class Query(gr.ObjectType):
    hello = gr.String(name=gr.String(default_value='Madi'))
    players = gr.List(
        Player,
        start=gr.Int(default_value=0),
        end=gr.Int(default_value=-1)
    )

    def resolve_hello(self, _, name):
        return 'Hello ' + name

    def resolve_players(self, _, start, end):
        try:
            return players[start:end]
        except:
            return 'Invalid start and end arguments'

    def resolve_user_agent(self, info):
        ''' Return the User-Agent of the incoming request '''
        request = info.context["request"]
        user_agent = request.headers.get('User-Agent', '<unknown>')
        background = info.context['background']
        background.add_task(log_user_agent, user_agent=user_agent)
        return user_agent


async def log_user_agent(user_agent):
    print('Logging user agent:', user_agent)


''' 
Sample queries

{
    players(start: 2) {
        id
        name
    }
}

{
    hello(name: "Alex")
}

'''
