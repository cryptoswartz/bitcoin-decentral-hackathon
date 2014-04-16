import time
import serpent
from pyethereum import transactions, blocks, processblock, utils
from cryptoswartz import *
from display import *
N = 2
addrs, keys = make_population(N)
usrs = zip(keys, addrs)
master_key = usrs[0][0]
genesis = genesis_block(addrs)
contracts = init_system(genesis, master_key)

root_contract = [i for i,j in zip(contracts.keys(), contracts.values()) if j=='root'][0]
data_contract = [i for i,j in zip(contracts.keys(), contracts.values()) if j=='data'][0]
users_contract = [i for i,j in zip(contracts.keys(), contracts.values()) if j=='users'][0]
tag_contract = [i for i,j in zip(contracts.keys(), contracts.values()) if j=='tags'][0]

c1 = push_content("anthony is a badass", "story", genesis, root_contract, usrs[0])
c2 = push_content("here's a bunch of content its nice look at it here but whats going on!  good luck", "story2", genesis, root_contract, usrs[1])

c3 = push_content("anthony is a shithead badass", "silly3",  genesis, root_contract, usrs[0])
c4 = push_content("fuck!!!badass", "sill4y", genesis, root_contract, usrs[0])

register_name('ethan', genesis, root_contract, usrs[0]) 

tag_content(c1, 'genius', genesis, root_contract, usrs[0])
tag_content(c1, 'cooldude', genesis, root_contract, usrs[0])
tag_content(c1, 'shitty', genesis, root_contract, usrs[1])

'''
aa = get_all_content(genesis, root_contract, usrs[0])
b = aa[0] 
a = get_tags(b, tag_contract, genesis)
print a
quit()
'''


#vote_tag(c1, 'spam', 1, root_contract, keys[0], genesis, users[0])




#print get_name(usrs[0][1], users_contract, genesis)

#for i in xrange(N):
#    display_user(genesis, users_contract, addrs[i])
#display_block_chain(genesis, contracts)

#d1 = get_content_title(c1, data_contract, genesis)
#d2 = get_content_title(c2, data_contract, genesis)
#data = get_all_content(genesis, root_contract, usrs[0])







'''
for i in xrange(N):
    display_user(genesis, users_contract, users[i])

print genesis.get_balance(users[0])
print genesis.get_balance(users[1])



print get_content_title(c1, data_contract, genesis)
print get_name(users[0], users_contract, genesis)
print get_tags(c1, tag_contract, genesis)
'''

