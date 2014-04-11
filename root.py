import serpent
from pyethereum import transactions, blocks, processblock, utils
from cryptoswartz import *
from display import *

users, keys = make_population(10)
master_key = keys[0]
master_addy = users[0]
genesis = genesis_block(users)
contracts = init_system(genesis, master_key)
root_contract = [i for i,j in zip(contracts.keys(), contracts.values()) if j=='root'][0]
data_contract = [i for i,j in zip(contracts.keys(), contracts.values()) if j=='data'][0]
users_contract = [i for i,j in zip(contracts.keys(), contracts.values()) if j=='users'][0]
tag_contract = [i for i,j in zip(contracts.keys(), contracts.values()) if j=='tags'][0]

c1 = push_content("anthony is a badass", "story", master_key, genesis, root_contract, master_addy)
print c1.encode('hex')
for addr in users:
    display_user(genesis, users_contract, addr)
    print ''
quit()
c2 = push_content("some bullshit about your mamma", "the deets", keys[1], genesis, root_contract, users[1])
register_name('ethan', master_key, root_contract, genesis, users[0]) 
tag_content(c1, 'balls', master_key, root_contract, genesis, users[0])
tag_content(c1, 'dickcheese', master_key, root_contract, genesis, users[0])
tag_content(c1, 'genius', master_key, root_contract, genesis, users[1])
tag_content(c1, 'spam', keys[1], root_contract, genesis, users[0])
tag_content(c2, 'genius', keys[0], root_contract, genesis, users[1])






print get_content_title(c1, data_contract, genesis)
print get_name(users[0], users_contract, genesis)
print get_tags(c1, tag_contract, genesis)







