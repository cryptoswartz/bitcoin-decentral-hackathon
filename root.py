import serpent
from pyethereum import transactions, blocks, processblock, utils


key = utils.sha3('this is a great brain wallet')
addr = utils.privtoaddr(key)
genesis = blocks.Block.genesis({ addr: 10**18 })

code = serpent.compile(open('root.cll').read())
tx_make_root = transactions.Transaction.contract(0,0,10**12, 10000, code).sign(key)
code = serpent.compile(open('data.se').read())
tx_make_data = transactions.Transaction.contract(1,0,10**12, 10000, code).sign(key)
code = serpent.compile(open('tag.se').read())
tx_make_tag = transactions.Transaction.contract(2,0,10**12, 10000, code).sign(key)
code = serpent.compile(open('users.se').read())
tx_make_users = transactions.Transaction.contract(3,0,10**12, 10000, code).sign(key)

root_contract = processblock.apply_tx(genesis, tx_make_root)
data_contract = processblock.apply_tx(genesis, tx_make_data)
tag_contract = processblock.apply_tx(genesis, tx_make_tag)
users_contract = processblock.apply_tx(genesis, tx_make_users)

d_contract = data_contract.encode('hex')
t_contract = tag_contract.encode('hex')
v_contract = 0
u_contract = users_contract.encode('hex')

print 'root:', root_contract.encode('hex')
print 'me:', addr
print 'data:', d_contract
print 'tag:', t_contract
print 'users:', u_contract

#init root
tx_init_root = transactions.Transaction(4, 0, 10**12, 10000, root_contract, serpent.encode_datalist([d_contract, t_contract, v_contract, u_contract])).sign(key)
ans = processblock.apply_tx(genesis, tx_init_root)
print 'data_contract address: ', ans.encode('hex')

content = "anthony is a badass"
content_hash = utils.sha3(content)
title = "story"

tag = "a true statement"
tag_hash = utils.sha3(tag)

vote = 1


# push a transaction with a title.  recover title from blockchain
tx_push = transactions.Transaction(5, 0, 10**12, 10000, root_contract, serpent.encode_datalist([1, content_hash, title])).sign(key)
ans = processblock.apply_tx(genesis, tx_push)
a = int(content_hash.encode('hex'),16) + 1 # index of title
jj = genesis.get_storage_data(data_contract, a)
print hex(jj)[2:-1].decode('hex')

# register eth-address to a name.  recover name from blockchain.  names are not unique. but names + first 4 digits of address probably are....
tx_register_name = transactions.Transaction(6, 0, 10**12, 10000, root_contract, serpent.encode_datalist([5, 'ethan'])).sign(key)
ans = processblock.apply_tx(genesis, tx_register_name)
jj = genesis.get_storage_data(users_contract, addr)
print hex(jj)[2:-1].decode('hex')

# tag some content.  recover tag from blockchain.
tx_tag = transactions.Transaction(7, 0, 10**12, 10000, root_contract, serpent.encode_datalist([2, content_hash, tag_hash])).sign(key)
ans = processblock.apply_tx(genesis, tx_tag)
print 'tag results: ', ans.encode('hex')

quit()

tx_vote = transactions.Transaction(7, 0, 10**12, 10000, root_contract, serpent.encode_datalist([3, content_hash, tag_hash, vote])).sign(key)
ans = processblock.apply_tx(genesis, tx_vote)
print ans.encode('hex')


tx_name_me = transactions.Transaction(8, 0, 10**12, 10000, root_contract, serpent.encode_datalist([5, 'fagson'])).sign(key)
ans = processblock.apply_tx(genesis, tx_name_me)
print ans.encode('hex')

print genesis.get_storage_data(u_contract, addr)
print genesis.to_dict()








def display_block_chain(genesis):
    di = genesis.to_dict()
    state = di['state']
    print 'keys!'
    print state.keys()
    print 'loop!'
    for k in state.keys():
        print k
        for s in state[k]:
            if type(s) == long:
                print s
            elif type(s) == dict:
                for j in s.keys():
                    if type(s[j]) == long: print s[j]
                    else:
                        print s[j].encode(encoding='UTF-8')
                
            else:
                print s.encode('hex')
        print ''
    quit()

