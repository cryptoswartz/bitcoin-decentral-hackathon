import serpent
from pyethereum import transactions, blocks, processblock, utils
from retrieve import *

users, keys = make_population(10)
master_key = keys[0]
genesis = genesis_block(users)
contracts = init_system(genesis, master_key)
root_contract = [i for i,j in zip(contracts.keys(), contracts.values()) if j=='root'][0]
data_contract = [i for i,j in zip(contracts.keys(), contracts.values()) if j=='data'][0]
users_contract = [i for i,j in zip(contracts.keys(), contracts.values()) if j=='users'][0]
tag_contract = [i for i,j in zip(contracts.keys(), contracts.values()) if j=='tags'][0]

c1 = push_content("anthony is a badass", "story", master_key, genesis, root_contract, 5)
register_name('ethan', master_key, root_contract, genesis, 6) 
tag_content(c1, 'balls', master_key, root_contract, genesis, 7)
tag_content(c1, 'dickcheese', master_key, root_contract, genesis, 8)
tag_content(c1, 'genius', master_key, root_contract, genesis, 9)

print get_content_title(c1, data_contract, genesis)
print get_name(users[0], users_contract, genesis)
print get_tags(c1, tag_contract, genesis)

quit()
# tag some content.  recover tag from blockchain.


display_user(genesis, users_contract, addr)
quit()
display_block_chain(genesis, adresses)






