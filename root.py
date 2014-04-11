import serpent
from pyethereum import transactions, blocks, processblock, utils
from cryptoswartz import *
from display import *
N = 2
users, keys = make_population(N)
master_key = keys[0]
master_addy = users[0]
second_key = keys[1]
second_addy = users[1]
genesis = genesis_block(users)
contracts = init_system(genesis, master_key)

root_contract = [i for i,j in zip(contracts.keys(), contracts.values()) if j=='root'][0]
data_contract = [i for i,j in zip(contracts.keys(), contracts.values()) if j=='data'][0]
users_contract = [i for i,j in zip(contracts.keys(), contracts.values()) if j=='users'][0]
tag_contract = [i for i,j in zip(contracts.keys(), contracts.values()) if j=='tags'][0]

c1 = push_content("anthony is a badass", "story", master_key, genesis, root_contract, users[0])
quit()
c2 = push_content("anthony isss", "story", master_key, genesis, root_contract, users[0])

for i in xrange(N):
    display_user(genesis, users_contract, users[i])
quit()
display_block_chain(genesis, contracts)

print 'yeh yeh yeh', c1.encode('hex')
print 'are you kidding me?'



quit()
a = genesis.get_storage_data(root_contract,c1)
print a
quit()

print c1.encode('hex')
display_user(genesis, users_contract, users[0])
quit()
print genesis.to_dict()
quit()
'''
c2 = push_content("anthony is a shithead badass", "silly", master_key, genesis, root_contract, users[0])
c3 = push_content("fuck!!!badass", "silly", master_key, genesis, root_contract, users[0])
#register_name('ethan', master_key, root_contract, genesis, users[0]) 
'''

print "wtf"
d = get_content_title(c1, data_contract, genesis)
print d
data = get_all_content(root_contract, keys[0], genesis, users[0])
print data.encode('hex')
quit()





tag_content(c1, 'genius', master_key, root_contract, genesis, users[0])
vote_tag(c1, 'spam', 1, root_contract, keys[0], genesis, users[0])


'''
for i in xrange(N):
    display_user(genesis, users_contract, users[i])

print genesis.get_balance(users[0])
print genesis.get_balance(users[1])




print get_content_title(c1, data_contract, genesis)
print get_name(users[0], users_contract, genesis)
print get_tags(c1, tag_contract, genesis)
'''





